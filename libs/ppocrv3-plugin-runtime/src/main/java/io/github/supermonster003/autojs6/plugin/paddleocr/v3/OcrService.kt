package io.github.supermonster003.autojs6.plugin.paddleocr.v3

import android.app.Service
import android.content.Intent
import android.graphics.Rect
import android.os.Bundle
import android.os.IBinder
import android.os.ParcelFileDescriptor
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.model.OCRRunResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import org.autojs.plugin.common.api.PluginCapabilityKeys
import org.autojs.plugin.common.api.PluginInfo
import org.autojs.plugin.paddle.ocr.api.IOcrPlugin
import org.autojs.plugin.paddle.ocr.api.OcrOptions
import org.autojs.plugin.paddle.ocr.api.OcrResult
import org.autojs.plugin.paddle.ocr.api.PaddleOcrPluginCapabilityKeys
import org.autojs.plugin.runtime.InstalledPackageIdentity
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.model.OCRResult as PaddleResult

class OcrService : Service() {

    private val ocrLock = Any()
    private lateinit var engineHolder: PpOcrV3EngineHolder

    override fun onCreate() {
        super.onCreate()
        engineHolder = PpOcrV3EngineHolder(this)
    }

    override fun onDestroy() {
        engineHolder.release()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder = binder

    private val binder = object : IOcrPlugin.Stub() {
        override fun getInfo(): PluginInfo {
            val runtimeConfig = PpOcrV3RuntimeConfig.from(this@OcrService)
            val profile = PpOcrV3Profile.fromValue(runtimeConfig.modelProfile)
            return PluginInfo().apply {
                name = InstalledPackageIdentity.stringResource(this@OcrService, "app_name")
                description = InstalledPackageIdentity.stringResource(this@OcrService, "plugin_description")
                author = runtimeConfig.pluginAuthor
                id = runtimeConfig.pluginId
                engine = runtimeConfig.pluginEngine
                variant = runtimeConfig.pluginVariant
                versionName = runtimeConfig.versionName
                versionCode = runtimeConfig.versionCode
                versionDate = runtimeConfig.versionDate
                InstalledPackageIdentity.apply(this@OcrService, this)
                capabilities = Bundle().apply {
                    putInt(PluginCapabilityKeys.REQUIRES_HOST_VERSION, REQUIRES_HOST_VERSION)
                    putBoolean(PaddleOcrPluginCapabilityKeys.SUPPORTS_RAW_IMAGE, true)
                    putBoolean(PaddleOcrPluginCapabilityKeys.SUPPORTS_TEXT_DETECTION, true)
                    putBoolean(PaddleOcrPluginCapabilityKeys.SUPPORTS_TEXT_RECOGNITION, true)
                    putBoolean(PaddleOcrPluginCapabilityKeys.SUPPORTS_TEXTLINE_ORIENTATION_CLASSIFICATION, true)
                    putString(CAPABILITY_MODEL_FAMILY, runtimeConfig.modelFamily)
                    putString(PaddleOcrPluginCapabilityKeys.MODEL_PROFILE, profile.value)
                    putString(CAPABILITY_LANGUAGE, profile.language)
                    putBoolean(PaddleOcrPluginCapabilityKeys.RECOMMENDED_FOR_MOBILE_DEFAULT, profile.recommendedForMobileDefault)
                }
            }
        }

        override fun recognizeText(
            imageFd: ParcelFileDescriptor,
            options: OcrOptions,
        ): MutableList<String> {
            return detect(imageFd, options)
                .map { it.text.orEmpty() }
                .toMutableList()
        }

        override fun detect(
            imageFd: ParcelFileDescriptor,
            options: OcrOptions,
        ): MutableList<OcrResult> {
            synchronized(ocrLock) {
                val bitmap = ImageFdDecoder.decode(imageFd, options.extras)
                try {
                    val engine = engineHolder.get(options)
                    val runResult = runBlocking(Dispatchers.IO) {
                        engine.recognize(bitmap)
                    }
                    val runtimeConfig = PpOcrV3RuntimeConfig.from(this@OcrService)
                    return runResult.results
                        .map { it.toAutoJsResult(runResult, runtimeConfig) }
                        .toMutableList()
                } finally {
                    if (!bitmap.isRecycled) {
                        bitmap.recycle()
                    }
                }
            }
        }
    }

    private fun PaddleResult.toAutoJsResult(runResult: OCRRunResult, runtimeConfig: PpOcrV3RuntimeConfig): OcrResult {
        val xs = box.points.map { it.x }
        val ys = box.points.map { it.y }
        return OcrResult().apply {
            text = this@toAutoJsResult.text
            confidence = this@toAutoJsResult.confidence
            bounds = Rect(
                xs.minOrNull()?.toInt() ?: 0,
                ys.minOrNull()?.toInt() ?: 0,
                xs.maxOrNull()?.toInt() ?: 0,
                ys.maxOrNull()?.toInt() ?: 0,
            )
            extras = Bundle().apply {
                putString(CAPABILITY_MODEL_FAMILY, runtimeConfig.modelFamily)
                putString(PaddleOcrPluginCapabilityKeys.MODEL_PROFILE, runtimeConfig.modelProfile)
                putFloatArray(
                    "quad",
                    this@toAutoJsResult.box.points.flatMap { point ->
                        listOf(point.x, point.y)
                    }.toFloatArray(),
                )
                putLong("detectionTimeMs", runResult.detectionTimeMs)
                putLong("classificationTimeMs", runResult.classificationTimeMs)
                putLong("recognitionTimeMs", runResult.recognitionTimeMs)
                putLong("totalTimeMs", runResult.totalTimeMs)
                putLong("coldLoadTimeMs", runResult.coldLoadTimeMs)
                putString("executionProvider", runResult.executionProvider)
            }
        }
    }

    internal companion object {
        // First host build that matches by profile and forwards useCls (roadmap D24).
        const val REQUIRES_HOST_VERSION = 5935
        const val CAPABILITY_MODEL_FAMILY = "modelFamily"
        const val CAPABILITY_LANGUAGE = "language"
    }
}
