/**
 * Paddle OCR (https://github.com/PaddlePaddle/PaddleOCR) build script (Kotlin DSL).
 *
 * Created by TonyJiangWJ (https://github.com/TonyJiangWJ) on Aug 7, 2023.
 * Modified by TonyJiangWJ (https://github.com/TonyJiangWJ) as of Aug 11, 2023.
 * Modified by SuperMonster003 as of Sep 4, 2023.
 * Transformed by SuperMonster003 on Sep 30, 2025.
 */

import groovy.json.JsonSlurper
import java.net.URI
import java.security.MessageDigest

plugins {
    id("org.autojs.build.utils")
    id("org.autojs.build.properties")
    id("org.autojs.build.jvm-convention")
    id("com.android.library")
}

ext {
    set("projectName", "Paddle OCR")
}

val versionMap = mapOf(
    "MIN_SDK" to props["MIN_SDK"].toInt(),
    "COMPILE_SDK" to props["COMPILE_SDK"].toInt(),
    "TARGET_SDK" to props["TARGET_SDK"].toInt(),
    "NDK" to props["PADDLE_OCR/NDK"],
    "CMAKE" to props["PADDLE_OCR/CMAKE"],
    "OPENCV" to props["PADDLE_OCR/OPENCV"],
)

val nameMap = mapOf(
    "PROJECT" to extensions.extraProperties.get("projectName") as String,
    "OPENCV" to "OpenCV",
    "NDK" to "NDK",
    "CMAKE" to "Cmake",
)

val paddleOcrAbis = listOf("arm64-v8a", "armeabi-v7a")

fun File.sha256String(): String {
    val digest = MessageDigest.getInstance("SHA-256")
    inputStream().use { input ->
        val buffer = ByteArray(1 shl 16)
        while (true) {
            val read = input.read(buffer)
            if (read < 0) break
            digest.update(buffer, 0, read)
        }
    }
    return digest.digest().joinToString("") { "%02x".format(it.toInt() and 0xff) }
}

// Private OpenCV: libNative.so statically links the core, imgproc and imgcodecs libraries of the
// official OpenCV Android SDK and exports only its JNI methods, so it never shares OpenCV with the
// host or another plugin. The record pins the release archive and every static library per ABI;
// tools/opencv/opencv_sdk_provenance.py regenerates it for an upgrade.
// zh-CN: 私有 OpenCV: libNative.so 静态链接官方 OpenCV Android SDK 的 core, imgproc 与 imgcodecs,
// 只导出 JNI 方法, 不与宿主或其他插件共享 OpenCV. 来源记录固定发布包及各 ABI 的静态库哈希.
val openCvVersion = versionMap["OPENCV"] as String
val openCvSdkProvenanceFile = rootProject.file("libs/opencv-android-sdk-$openCvVersion.provenance.json")

@Suppress("UNCHECKED_CAST")
val openCvSdkProvenance = JsonSlurper().parse(openCvSdkProvenanceFile) as Map<String, Any?>

@Suppress("UNCHECKED_CAST")
val openCvSdkUpstream = openCvSdkProvenance["upstream"] as Map<String, Any?>

@Suppress("UNCHECKED_CAST")
val openCvSdkStaticLibraries = openCvSdkProvenance["staticLibraries"] as Map<String, Map<String, String>>
require(openCvSdkProvenance["opencvVersion"] == openCvVersion) {
    "${openCvSdkProvenanceFile.name} does not describe OpenCV $openCvVersion"
}
require(paddleOcrAbis.all(openCvSdkStaticLibraries::containsKey)) {
    "${openCvSdkProvenanceFile.name} must record the static libraries of every ABI: $paddleOcrAbis"
}
val openCvSdkArchive = layout.projectDirectory.file("cache/opencv-$openCvVersion-android-sdk.zip").asFile
val openCvSdkDirectory = layout.buildDirectory.dir("opencv-android-sdk-$openCvVersion")

val downloadOpenCvSdk by tasks.registering {
    group = "paddleocr"
    description = "Downloads and verifies the official OpenCV $openCvVersion Android SDK."
    inputs.file(openCvSdkProvenanceFile)
    outputs.file(openCvSdkArchive)
    doLast {
        val expected = openCvSdkUpstream["archiveSha256"] as String
        if (!openCvSdkArchive.isFile || !openCvSdkArchive.sha256String().equals(expected, ignoreCase = true)) {
            val url = openCvSdkUpstream["archive"] as String
            val partial = File(openCvSdkArchive.path + ".part")
            openCvSdkArchive.parentFile.mkdirs()
            logger.lifecycle("Downloading OpenCV $openCvVersion Android SDK: $url")
            URI(url).toURL().openStream().use { input -> partial.outputStream().use { output -> input.copyTo(output) } }
            val actual = partial.sha256String()
            if (!actual.equals(expected, ignoreCase = true)) {
                partial.delete()
                throw GradleException("SHA-256 mismatch for $url: expected=$expected actual=$actual")
            }
            openCvSdkArchive.delete()
            check(partial.renameTo(openCvSdkArchive)) { "Unable to move ${partial.path} to ${openCvSdkArchive.path}" }
        }
    }
}

val extractOpenCvSdk by tasks.registering(Sync::class) {
    group = "paddleocr"
    description = "Extracts and verifies the static OpenCV $openCvVersion libraries for libNative.so."
    dependsOn(downloadOpenCvSdk)
    inputs.file(openCvSdkProvenanceFile)
    from({ zipTree(openCvSdkArchive) }) {
        include(
            "OpenCV-android-sdk/sdk/native/jni/**",
            "OpenCV-android-sdk/sdk/native/staticlibs/**",
            "OpenCV-android-sdk/sdk/native/3rdparty/**",
            // Only for the SDK's CMake export check; libNative.so never links or ships it.
            "OpenCV-android-sdk/sdk/native/libs/**",
        )
        // Keep sdk/native: the SDK's CMake exports locate libraries relative to that layout.
        eachFile { relativePath = RelativePath(true, *relativePath.segments.drop(1).toTypedArray()) }
        includeEmptyDirs = false
    }
    into(openCvSdkDirectory)
    doLast {
        val nativeDir = openCvSdkDirectory.get().dir("sdk/native").asFile
        paddleOcrAbis.forEach { abi ->
            openCvSdkStaticLibraries.getValue(abi).forEach { (relative, expected) ->
                val actual = nativeDir.resolve(relative).takeIf(File::isFile)?.sha256String()
                if (!expected.equals(actual, ignoreCase = true)) {
                    throw GradleException("OpenCV static library mismatch for $abi/$relative: expected=$expected actual=$actual")
                }
            }
        }
    }
}

tasks.configureEach {
    if (name == "preBuild" || name.startsWith("configureCMake") || name.startsWith("buildCMake")) {
        dependsOn(extractOpenCvSdk)
    }
}

val argsMap = mapOf(
    // @Hint by LZX284 (https://github.com/LZX284) on Sep 30, 2023.
    //  ! "ANDROID_PLATFORM" 默认为 "android-23", 这里修改为与 AutoJs6 最低 SDK 版本一致的 `versionMap.MIN_SDK`.
    //  ! en-US (translated by SuperMonster003 on Oct 22, 2024):
    //  ! "ANDROID_PLATFORM" with default value "android-23" was changed to `versionMap.MIN_SDK`
    //  ! to align with the min SDK version of AutoJs6.
    "ANDROID_PLATFORM" to "android-${versionMap["MIN_SDK"]}",
    "ANDROID_STL" to "c++_shared",
    "ANDROID_ARM_NEON" to "TRUE",
    "OPENCV_SDK_NATIVE_DIR" to openCvSdkDirectory.get().dir("sdk/native").asFile.invariantSeparatorsPath,
)

// @Hint by SuperMonster003 on Nov 12, 2023.
//  ! Do not add a space (nbsp) after "-D".
//  ! Reference: https://stackoverflow.com/questions/14887438/spacing-in-d-option-in-cmake
//  ! zh-CN:
//  ! 在 "-D" 后不要添加空格 (不间断空格).
//  ! 参阅: https://stackoverflow.com/questions/14887438/spacing-in-d-option-in-cmake
val args = argsMap.entries.map { (k, v) -> "-D$k=$v" }

utils.configureLibraryLifecycleHooks(
    project,
    nameMap["PROJECT"] as String,
    listOf("OPENCV", "NDK", "CMAKE").map { "${nameMap[it]}: ${versionMap[it]}" },
    emptyList(),
    "isCleanupPaddleOcr",
    listOf(".cxx")
)

android {
    namespace = "io.github.supermonster003.autojs6.plugin.paddleocr.v3.nativecore"

    ndkVersion = versionMap["NDK"] as String
    compileSdk = versionMap["COMPILE_SDK"] as Int

    defaultConfig {
        minSdk = versionMap["MIN_SDK"] as Int

        externalNativeBuild {
            cmake {
                val cppFlagsMap = mapOf(
                    "-std" to "c++11"
                )
                val cppListFlags = mapOf(
                    "-f" to listOf("rtti", "exceptions"),
                    "-W" to "no-format"
                )

                // 组装等价于 Groovy 脚本中的拼接逻辑
                val cppFlagsJoined = buildString {
                    append(
                        cppFlagsMap.entries.joinToString(" ") { (k, v) -> "$k=$v" }
                    )
                    append(" ")
                    append(
                        cppListFlags.entries.joinToString(" ") { (k, v) ->
                            when (v) {
                                is List<*> -> v.joinToString(" ") { opt -> k + opt }
                                else -> "$k$v"
                            }
                        }
                    )
                }.trim()

                cppFlags += cppFlagsJoined
                arguments += args
            }
        }

        ndk {
            // @Hint by SuperMonster003 on Jan 2, 2024.
            //  ! Supported architectures: arm-v7, arm-v8.
            //  ! References:
            //  ! https://github.com/PaddlePaddle/Paddle-Lite/blob/develop/lite/tools/build_android.sh#L7
            //  ! https://github.com/PaddlePaddle/Paddle-Lite/issues/80
            //  ! zh-CN:
            //  ! 支持的架构: arm-v7, arm-v8.
            //  ! 参阅:
            //  ! https://github.com/PaddlePaddle/Paddle-Lite/blob/develop/lite/tools/build_android.sh#L7
            //  ! https://github.com/PaddlePaddle/Paddle-Lite/issues/80
            // noinspection ChromeOsAbiSupport
            abiFilters += paddleOcrAbis
            @Suppress("DEPRECATION")
            ldLibs?.add("jnigraphics")
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
        debug {
            isMinifyEnabled = false
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = versionMap["CMAKE"] as String
        }
    }

    lint {
        targetSdk = versionMap["TARGET_SDK"] as Int
    }
}

dependencies {
    implementation(fileTree(mapOf("include" to listOf("*.jar"), "dir" to "libs")))
    implementation(libs.core.ktx)
    implementation(libs.preference.ktx)
}
