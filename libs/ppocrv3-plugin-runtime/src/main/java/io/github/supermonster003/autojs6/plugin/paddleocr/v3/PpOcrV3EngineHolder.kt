package io.github.supermonster003.autojs6.plugin.paddleocr.v3

import android.content.Context
import android.os.Bundle
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.EngineConfig
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.PaddleOCR
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.PaddleOCRConfig
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.util.OpenCVUtils
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import org.autojs.plugin.paddle.ocr.api.OcrOptions

class PpOcrV3EngineHolder(context: Context) {

    private val appContext = context.applicationContext
    private val lock = Any()

    @Volatile
    private var cachedSettings: PpOcrV3EngineSettings? = null

    @Volatile
    private var cachedEngine: PaddleOCR? = null

    fun get(options: OcrOptions): PaddleOCR {
        val settings = PpOcrV3EngineSettings.resolve(
            cpuThreadNum = options.cpuThreadNum,
            useSlim = options.useSlim,
            useOpenCL = options.useOpenCL,
            detLongSize = options.detLongSize,
            scoreThreshold = options.scoreThreshold,
            extras = options.extras.toMap(),
        )

        cachedEngine?.let { engine ->
            if (cachedSettings == settings) return engine
        }

        synchronized(lock) {
            cachedEngine?.let { engine ->
                if (cachedSettings == settings) return engine
            }

            val old = cachedEngine
            cachedSettings = null
            cachedEngine = null
            val created = runBlocking(Dispatchers.IO) {
                old?.release()
                check(OpenCVUtils.init(appContext)) {
                    "Failed to initialize OpenCV for Paddle OCR PP-OCRv3: ${OpenCVUtils.lastError.orEmpty()}"
                }
                PaddleOCR.create(
                    context = appContext,
                    config = PaddleOCRConfig(
                        detLimitSideLen = settings.detLimitSideLen,
                        detLimitType = settings.detLimitType,
                        detMaxSideLimit = settings.detMaxSideLimit,
                        detThresh = settings.detThresh,
                        detBoxThresh = settings.detBoxThresh,
                        detUnclipRatio = settings.detUnclipRatio,
                        recScoreThresh = settings.recScoreThresh,
                        recBatchSize = settings.recBatchSize,
                        useCls = settings.useCls,
                    ),
                    engineConfig = EngineConfig(numThreads = settings.threads, useNnapi = settings.useNnapi),
                    detModelAssetPath = settings.detAssetPath,
                    recModelAssetPath = settings.recAssetPath,
                    recConfigAssetPath = settings.recConfigAssetPath,
                    clsModelAssetPath = settings.clsAssetPath,
                )
            }

            cachedSettings = settings
            cachedEngine = created
            return created
        }
    }

    fun release() {
        synchronized(lock) {
            val engine = cachedEngine
            cachedSettings = null
            cachedEngine = null
            if (engine != null) {
                runBlocking(Dispatchers.IO) {
                    engine.release()
                }
            }
        }
    }

    private fun Bundle?.toMap(): Map<String, Any?> {
        if (this == null) return emptyMap()
        @Suppress("DEPRECATION")
        return keySet().associateWith { get(it) }
    }
}
