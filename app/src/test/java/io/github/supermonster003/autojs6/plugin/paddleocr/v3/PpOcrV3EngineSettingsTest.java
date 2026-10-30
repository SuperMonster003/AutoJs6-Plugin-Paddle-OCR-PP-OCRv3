package io.github.supermonster003.autojs6.plugin.paddleocr.v3;

import org.autojs.plugin.paddle.ocr.api.PaddleOcrOptionExtraKeys;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class PpOcrV3EngineSettingsTest {
    private static final Map<String, Object> NONE = Collections.emptyMap();

    private static PpOcrV3EngineSettings resolve(int threads, boolean slim, boolean openCl, int detLongSize, float score, Map<String, Object> extras) {
        return PpOcrV3EngineSettings.Companion.resolve(threads, slim, openCl, detLongSize, score, extras);
    }

    // Host defaults: cpuThreadNum 0, detLongSize 0, scoreThreshold -1 and no extras.
    @Test public void hostDefaultsKeepThePaddleLiteDefaults() {
        PpOcrV3EngineSettings settings = resolve(0, false, false, 0, -1f, NONE);
        assertEquals(4, settings.getThreads());
        assertEquals(960, settings.getDetLimitSideLen());
        assertEquals("max", settings.getDetLimitType());
        assertEquals(4000, settings.getDetMaxSideLimit());
        assertEquals(0.3f, settings.getDetThresh(), 0f);
        assertEquals(0.5f, settings.getDetBoxThresh(), 0f);
        assertEquals(1.6f, settings.getDetUnclipRatio(), 0f);
        assertEquals(0.1f, settings.getRecScoreThresh(), 0f);
        assertEquals(1, settings.getRecBatchSize());
        assertFalse(settings.getUseCls());
        assertFalse(settings.getUseNnapi());
        assertEquals("models/ppocrv3/det/inference.onnx", settings.getDetAssetPath());
        assertEquals("models/ppocrv3/rec/inference.onnx", settings.getRecAssetPath());
        assertEquals("models/ppocrv3/rec/inference.yml", settings.getRecConfigAssetPath());
        assertNull(settings.getClsAssetPath());
    }
    @Test public void positiveThreadCountIsUsedAndOthersFallBack() {
        assertEquals(2, resolve(2, false, false, 0, -1f, NONE).getThreads());
        assertEquals(4, resolve(-3, false, false, 0, -1f, NONE).getThreads());
    }
    @Test public void detLimitSideLenPrefersTheExtraThenDetLongSize() {
        assertEquals(1280, resolve(0, false, false, 1280, -1f, NONE).getDetLimitSideLen());
        assertEquals(640, resolve(0, false, false, 1280, -1f, extras(PaddleOcrOptionExtraKeys.DET_LIMIT_SIDE_LEN, 640)).getDetLimitSideLen());
        assertEquals(1280, resolve(0, false, false, 1280, -1f, extras(PaddleOcrOptionExtraKeys.DET_LIMIT_SIDE_LEN, 0)).getDetLimitSideLen());
    }
    @Test public void explicitScoreThresholdIncludingZeroIsKept() {
        assertEquals(0f, resolve(0, false, false, 0, 0f, NONE).getRecScoreThresh(), 0f);
        assertEquals(0.5f, resolve(0, false, false, 0, 0.5f, NONE).getRecScoreThresh(), 0f);
    }
    @Test public void useSlimSwitchesDetAndRecOnly() {
        PpOcrV3EngineSettings settings = resolve(0, true, false, 0, -1f, extras(PaddleOcrOptionExtraKeys.USE_CLS, true));
        assertEquals("models/ppocrv3-slim/det/inference.onnx", settings.getDetAssetPath());
        assertEquals("models/ppocrv3-slim/rec/inference.onnx", settings.getRecAssetPath());
        assertEquals("models/ppocrv3/rec/inference.yml", settings.getRecConfigAssetPath());
        assertEquals("models/ppocrv3/cls/inference.onnx", settings.getClsAssetPath());
    }
    // Appendix D Q6: useOpenCL requests NNAPI; the session manager falls back to CPU below API 27.
    @Test public void useOpenClRequestsNnapi() {
        assertTrue(resolve(0, false, true, 0, -1f, NONE).getUseNnapi());
        assertFalse(resolve(0, false, false, 0, -1f, NONE).getUseNnapi());
    }
    // Appendix D Q11: the classifier is off unless the script sets useCls, as plugin 1.0.6 never ran it.
    @Test public void useClsExtraEnablesTheClassifier() {
        PpOcrV3EngineSettings settings = resolve(0, false, false, 0, -1f, extras(PaddleOcrOptionExtraKeys.USE_CLS, true));
        assertTrue(settings.getUseCls());
        assertEquals("models/ppocrv3/cls/inference.onnx", settings.getClsAssetPath());
        assertFalse(resolve(0, false, false, 0, -1f, extras(PaddleOcrOptionExtraKeys.USE_CLS, false)).getUseCls());
    }
    @Test public void extrasOfTheWrongTypeAreIgnored() {
        Map<String, Object> extras = extras(PaddleOcrOptionExtraKeys.USE_CLS, "true");
        extras.put(PaddleOcrOptionExtraKeys.DET_LIMIT_SIDE_LEN, 640L);
        extras.put("detThresh", 0.4);
        PpOcrV3EngineSettings settings = resolve(0, false, false, 0, -1f, extras);
        assertFalse(settings.getUseCls());
        assertEquals(960, settings.getDetLimitSideLen());
        assertEquals(0.3f, settings.getDetThresh(), 0f);
    }
    @Test public void detectorExtrasOverrideTheDefaults() {
        Map<String, Object> extras = extras("detLimitType", "min");
        extras.put("detMaxSideLimit", 2000);
        extras.put("detThresh", 0.2f);
        extras.put("detBoxThresh", 0.6f);
        extras.put("detUnclipRatio", 2.0f);
        extras.put("recBatchSize", 0);
        PpOcrV3EngineSettings settings = resolve(0, false, false, 0, -1f, extras);
        assertEquals("min", settings.getDetLimitType());
        assertEquals(2000, settings.getDetMaxSideLimit());
        assertEquals(0.2f, settings.getDetThresh(), 0f);
        assertEquals(0.6f, settings.getDetBoxThresh(), 0f);
        assertEquals(2.0f, settings.getDetUnclipRatio(), 0f);
        assertEquals(1, settings.getRecBatchSize());
    }
    @Test public void equalOptionsShareTheCachedEngine() {
        assertEquals(resolve(0, true, true, 0, -1f, NONE), resolve(4, true, true, 960, 0.1f, NONE));
        assertFalse(resolve(0, true, false, 0, -1f, NONE).equals(resolve(0, false, false, 0, -1f, NONE)));
    }
    @Test public void hostExtraKeysMatchTheContract() {
        assertEquals("detLimitSideLen", PaddleOcrOptionExtraKeys.DET_LIMIT_SIDE_LEN);
        assertEquals("useCls", PaddleOcrOptionExtraKeys.USE_CLS);
    }

    private static Map<String, Object> extras(String key, Object value) {
        Map<String, Object> map = new HashMap<>();
        map.put(key, value);
        return map;
    }
}
