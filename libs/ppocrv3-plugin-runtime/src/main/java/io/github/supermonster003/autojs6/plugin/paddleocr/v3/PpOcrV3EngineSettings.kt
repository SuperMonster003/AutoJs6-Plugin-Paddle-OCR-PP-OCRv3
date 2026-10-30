package io.github.supermonster003.autojs6.plugin.paddleocr.v3

import org.autojs.plugin.paddle.ocr.api.PaddleOcrOptionExtraKeys

/**
 * Engine settings resolved from the host's `OcrOptions` (roadmap D25). Equal settings reuse the
 * cached engine; the resolution itself takes plain values so it can be unit tested on the JVM.
 */
data class PpOcrV3EngineSettings(
    val threads: Int,
    val useSlim: Boolean,
    val useNnapi: Boolean,
    val useCls: Boolean,
    val detLimitSideLen: Int,
    val detLimitType: String,
    val detMaxSideLimit: Int,
    val detThresh: Float,
    val detBoxThresh: Float,
    val detUnclipRatio: Float,
    val recScoreThresh: Float,
    val recBatchSize: Int,
) {
    val detAssetPath: String get() = if (useSlim) SLIM_DET_ASSET else DET_ASSET
    val recAssetPath: String get() = if (useSlim) SLIM_REC_ASSET else REC_ASSET
    val recConfigAssetPath: String get() = REC_CONFIG_ASSET

    /** The orientation model is not quantized, so both model sets share it. */
    val clsAssetPath: String? get() = CLS_ASSET.takeIf { useCls }

    companion object {
        const val DET_ASSET = "models/ppocrv3/det/inference.onnx"
        const val REC_ASSET = "models/ppocrv3/rec/inference.onnx"
        const val REC_CONFIG_ASSET = "models/ppocrv3/rec/inference.yml"
        const val CLS_ASSET = "models/ppocrv3/cls/inference.onnx"
        const val SLIM_DET_ASSET = "models/ppocrv3-slim/det/inference.onnx"
        const val SLIM_REC_ASSET = "models/ppocrv3-slim/rec/inference.onnx"

        // Defaults of the Paddle Lite engine in plugin 1.0.6, kept so scripts see the same behavior.
        const val DEFAULT_THREADS = 4
        const val DEFAULT_DET_LIMIT_SIDE_LEN = 960
        const val DEFAULT_REC_SCORE_THRESH = 0.1f

        // Plugin 1.0.6 never ran the orientation classifier; scripts opt in with extras useCls (appendix D Q11).
        const val DEFAULT_USE_CLS = false

        const val DEFAULT_DET_LIMIT_TYPE = "max"
        const val DEFAULT_DET_MAX_SIDE_LIMIT = 4000
        const val DEFAULT_DET_THRESH = 0.3f
        const val DEFAULT_DET_BOX_THRESH = 0.5f
        const val DEFAULT_DET_UNCLIP_RATIO = 1.6f

        const val EXTRA_DET_LIMIT_TYPE = "detLimitType"
        const val EXTRA_DET_MAX_SIDE_LIMIT = "detMaxSideLimit"
        const val EXTRA_DET_THRESH = "detThresh"
        const val EXTRA_DET_BOX_THRESH = "detBoxThresh"
        const val EXTRA_DET_UNCLIP_RATIO = "detUnclipRatio"
        const val EXTRA_REC_BATCH_SIZE = "recBatchSize"

        /**
         * Maps the host options. [extras] holds the values of the options' extras bundle; a value of
         * the wrong type counts as absent, as with `Bundle` getters. `useOpenCL` has no ONNX Runtime
         * counterpart and requests the NNAPI execution provider instead (appendix D Q6).
         */
        fun resolve(
            cpuThreadNum: Int,
            useSlim: Boolean,
            useOpenCL: Boolean,
            detLongSize: Int,
            scoreThreshold: Float,
            extras: Map<String, Any?>,
        ): PpOcrV3EngineSettings {
            val explicitSideLen = extras.int(PaddleOcrOptionExtraKeys.DET_LIMIT_SIDE_LEN, 0)
            return PpOcrV3EngineSettings(
                threads = if (cpuThreadNum > 0) cpuThreadNum else DEFAULT_THREADS,
                useSlim = useSlim,
                useNnapi = useOpenCL,
                useCls = extras.boolean(PaddleOcrOptionExtraKeys.USE_CLS, DEFAULT_USE_CLS),
                detLimitSideLen = when {
                    explicitSideLen > 0 -> explicitSideLen
                    detLongSize > 0 -> detLongSize
                    else -> DEFAULT_DET_LIMIT_SIDE_LEN
                },
                detLimitType = extras.string(EXTRA_DET_LIMIT_TYPE) ?: DEFAULT_DET_LIMIT_TYPE,
                detMaxSideLimit = extras.int(EXTRA_DET_MAX_SIDE_LIMIT, 0).takeIf { it > 0 } ?: DEFAULT_DET_MAX_SIDE_LIMIT,
                detThresh = extras.float(EXTRA_DET_THRESH, DEFAULT_DET_THRESH),
                detBoxThresh = extras.float(EXTRA_DET_BOX_THRESH, DEFAULT_DET_BOX_THRESH),
                detUnclipRatio = extras.float(EXTRA_DET_UNCLIP_RATIO, DEFAULT_DET_UNCLIP_RATIO),
                // The host sends -1 when the script leaves scoreThreshold unset.
                recScoreThresh = if (scoreThreshold >= 0f) scoreThreshold else DEFAULT_REC_SCORE_THRESH,
                recBatchSize = extras.int(EXTRA_REC_BATCH_SIZE, 1).coerceAtLeast(1),
            )
        }

        private fun Map<String, Any?>.int(key: String, fallback: Int) = this[key] as? Int ?: fallback

        private fun Map<String, Any?>.float(key: String, fallback: Float) = this[key] as? Float ?: fallback

        private fun Map<String, Any?>.boolean(key: String, fallback: Boolean) = this[key] as? Boolean ?: fallback

        private fun Map<String, Any?>.string(key: String) = this[key] as? String
    }
}
