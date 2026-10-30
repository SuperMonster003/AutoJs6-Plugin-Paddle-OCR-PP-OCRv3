// Copyright (c) 2026 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk

import android.content.Context
import android.graphics.Bitmap
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.engine.OCREngine
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.engine.OCREngineResult
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.model.OCRRunResult
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.model.OCRError
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class PaddleOCR private constructor(
    private val engine: OCREngine,
) {
    /** Time spent loading ONNX models (milliseconds). */
    val coldLoadTimeMs: Long get() = engine.coldLoadTimeMs

    /** Execution provider the sessions run on: `cpu` or `nnapi`. */
    val executionProvider: String get() = engine.executionProvider

    companion object {

        suspend fun create(context: Context): PaddleOCR {
            val appContext = context.applicationContext
            return withContext(Dispatchers.IO) {
                val engine = OCREngine(appContext, PaddleOCRConfig(), EngineConfig())
                PaddleOCR(engine)
            }
        }

        suspend fun create(
            context: Context,
            config: PaddleOCRConfig,
            engineConfig: EngineConfig = EngineConfig(),
        ): PaddleOCR {
            val appContext = context.applicationContext
            return withContext(Dispatchers.IO) {
                val engine = OCREngine(appContext, config, engineConfig)
                PaddleOCR(engine)
            }
        }

        suspend fun create(
            context: Context,
            config: PaddleOCRConfig,
            engineConfig: EngineConfig,
            detModelAssetPath: String,
            recModelAssetPath: String,
            recConfigAssetPath: String,
            clsModelAssetPath: String? = null,
        ): PaddleOCR {
            val appContext = context.applicationContext
            return withContext(Dispatchers.IO) {
                val engine = OCREngine(
                    appContext, config, engineConfig,
                    detModelAsset = detModelAssetPath,
                    recModelAsset = recModelAssetPath,
                    recConfigAsset = recConfigAssetPath,
                    clsModelAsset = clsModelAssetPath,
                )
                PaddleOCR(engine)
            }
        }
    }

    suspend fun recognize(bitmap: Bitmap): OCRRunResult {
        if (bitmap.width == 0 || bitmap.height == 0) {
            throw OCRError.InvalidImage()
        }
        return recognizeResult { engine.run(bitmap) }
    }

    suspend fun recognize(imageBytes: ByteArray): OCRRunResult {
        if (imageBytes.isEmpty()) {
            throw OCRError.InvalidImage()
        }
        return recognizeResult { engine.run(imageBytes) }
    }

    private suspend fun recognizeResult(runEngine: () -> OCREngineResult): OCRRunResult {
        return withContext(Dispatchers.IO) {
            val result = runEngine()
            OCRRunResult(
                results = result.results,
                detectionTimeMs = result.detectionTimeMs,
                classificationTimeMs = result.classificationTimeMs,
                recognitionTimeMs = result.recognitionTimeMs,
                totalTimeMs = result.totalTimeMs,
                lineCount = result.lineCount,
                detPreprocessMs = result.detPreprocessMs,
                detInferenceMs = result.detInferenceMs,
                detPostprocessMs = result.detPostprocessMs,
                recPreprocessMs = result.recPreprocessMs,
                recInferenceMs = result.recInferenceMs,
                recPostprocessMs = result.recPostprocessMs,
                pipelineOverheadMs = result.pipelineOverheadMs,
                coldLoadTimeMs = result.coldLoadTimeMs,
                executionProvider = result.executionProvider,
                detInputShape = result.detInputShape,
                recInputShapes = result.recInputShapes,
                perLineRecMs = result.perLineRecMs,
            )
        }
    }

    suspend fun release() {
        withContext(Dispatchers.IO) {
            engine.release()
        }
    }
}
