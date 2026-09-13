import com.android.build.api.variant.FilterConfiguration
import org.gradle.api.provider.Property

plugins {
    id("org.autojs.build.utils")
    id("org.autojs.build.versions")
    id("org.autojs.build.signs")
    id("org.autojs.build.jvm-convention")
    id("com.android.application")
    id("io.github.supermonster003.autojs6-native-alignment")
}

val globalApplicationId = "io.github.supermonster003.autojs6.plugin.paddleocr.v3"

val buildTypeDebug = "debug"
val buildTypeRelease = "release"

android {

    namespace = globalApplicationId
    compileSdk = versions.sdkVersionCompile

    defaultConfig {
        applicationId = globalApplicationId

        minSdk = versions.sdkVersionMin
        targetSdk = versions.sdkVersionTarget

        versionCode = versions.appVersionCode
        versionName = versions.appVersionName

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        multiDexEnabled = true
        multiDexKeepProguard = file("multidex-keep.pro")

        buildConfigField("String", "VERSION_DATE", "\"${utils.getDateString("MMM d, yyyy", "GMT+08:00")}\"")
        resValue("string", "app_name", "Paddle OCR (PP-OCRv3)")
        resValue("string", "plugin_author", "TonyJiangWJ")
        resValue("string", "plugin_id", "paddle-ocr-pp-ocrv3")
        resValue("string", "plugin_engine", "paddle-ocr")
        resValue("string", "plugin_variant", "v3")
        resValue("string", "plugin_version_date", utils.getDateString("MMM d, yyyy", "GMT+08:00"))

        ndk {
            // noinspection ChromeOsAbiSupport
            abiFilters += listOf("arm64-v8a", "armeabi-v7a")
        }
    }

    lint {
        abortOnError = false
    }

    signingConfigs {
        if (signs.isValid) {
            create(buildTypeRelease) {
                storeFile = signs.properties["storeFile"]?.let { file(it as String) }
                keyPassword = signs.properties["keyPassword"] as String
                keyAlias = signs.properties["keyAlias"] as String
                storePassword = signs.properties["storePassword"] as String
            }
        }
    }

    buildTypes {
        val proguardFiles = arrayOf<Any>(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro",
        )
        val niceSigningConfig = takeIf { signs.isValid }?.let {
            signingConfigs.getByName(buildTypeRelease)
        }
        debug {
            isMinifyEnabled = false
            proguardFiles(*proguardFiles)
            niceSigningConfig?.let { signingConfig = it }
        }
        release {
            isMinifyEnabled = true
            proguardFiles(*proguardFiles)
            niceSigningConfig?.let { signingConfig = it }
        }
    }

    buildFeatures {
        aidl = true
        buildConfig = true
        resValues = true
    }

    // @Hint by SuperMonster003 on Sep 25, 2024.
    //  ! To maintain compatibility with lower versions of Gradle (such as 7.4.2).
    //  ! zh-CN: 为了兼容低版本 Gradle (如 7.4.2).
    //  # packaging { ... }
    @Suppress("DEPRECATION")
    packagingOptions {
        jniLibs.useLegacyPackaging = false

        listOf(
            "META-INF/DEPENDENCIES",
            "META-INF/LICENSE",
            "META-INF/LICENSE.*",
            "META-INF/LICENSE-notice.*",
            "META-INF/license.*",
            "META-INF/NOTICE",
            "META-INF/NOTICE.*",
            "META-INF/notice.*",
            "META-INF/ASL2.0",
            "META-INF/*.kotlin_module",
        ).let { resources.pickFirsts.addAll(it) }

        listOf(
            "com/**/*",
            "frameworks/**/*",
            "junit/**/*",
            "LICENSE-junit.txt",
            "spec.txt",
            "EmojiReference.txt",
        ).let { resources.excludes.addAll(it) }
    }

    splits {
        // Configures multiple APKs based on ABI.
        abi {
            // Enables building multiple APKs per ABI.
            isEnable = true
            // By default, all ABIs are included, so use reset() and include to specify that we only
            // want APKs for x86 and x86_64.
            // Resets the list of ABIs that Gradle should create APKs for to none.
            reset()
            // Specifies a list of ABIs that Gradle should create APKs for.
            include("arm64-v8a", "armeabi-v7a")
            // Specifies that we do not want to also generate a universal APK that includes all ABIs.
            isUniversalApk = true
        }
    }
}

androidComponents {
    onVariants { variant ->
        variant.outputs.forEach { output ->
            val architecture = output.filters.find {
                it.filterType == FilterConfiguration.FilterType.ABI
            }?.identifier ?: "universal"
            val outputFileNameProperty = output.javaClass.methods.firstOrNull {
                it.name == "getOutputFileName" && it.parameterTypes.isEmpty()
            }?.invoke(output) as? Property<*>

            @Suppress("UNCHECKED_CAST")
            (outputFileNameProperty as? Property<String>)?.set(
                output.versionName.map { versionName ->
                    val version = versionName.replace("\\s".toRegex(), "-")
                    val extension = utils.FILE_EXTENSION_APK
                    "${rootProject.name}-v$version-$architecture.$extension".lowercase()
                }
            )
        }
    }
}

dependencies {
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.3.0")
    androidTestImplementation("androidx.test:runner:1.7.0")

    // Kotlin Runtime
    implementation("org.jetbrains.kotlin:kotlin-stdlib:2.2.21")

    // JetBrains Annotations
    implementation("org.jetbrains:annotations:26.0.2")

    // Plugin API: Common API
    implementation(files("$rootDir/libs/common-plugin-api.aar"))

    // Plugin API: OCR API
    implementation(files("$rootDir/libs/paddle-ocr-api.aar"))

    // Plugin API: OCR Engine
    implementation(files("$rootDir/libs/paddle-ocr-engine.aar"))

    // PaddleOCR
    implementation(project(":libs:paddleocr"))

    // AndroidX Annotations
    implementation(libs.annotation.jvm)
}

tasks {
    withType(JavaCompile::class.java) {
        options.encoding = "UTF-8"
    }


}

extra {
    versions.handleIfNeeded(project, listOf(buildTypeDebug, buildTypeRelease))
}

apply(from = rootProject.file("gradle/release-archive.gradle"))
