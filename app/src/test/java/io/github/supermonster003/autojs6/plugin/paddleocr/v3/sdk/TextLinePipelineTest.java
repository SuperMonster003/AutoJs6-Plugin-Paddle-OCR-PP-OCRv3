package io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk;

import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.engine.ExecutionProviders;
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.postprocess.ClsDecision;
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.postprocess.ClsPostprocessor;
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.preprocess.TextLineResize;
import kotlin.Pair;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/** Pure parts of the det -> cls -> rec pipeline, checked against PaddleOCR 2.7 behavior. */
public class TextLinePipelineTest {
    private static final TextLineResize RESIZE = TextLineResize.INSTANCE;
    private static final ClsPostprocessor CLS = ClsPostprocessor.INSTANCE;

    @Test public void recBatchWidthStartsAt320AndFollowsTheWidestCrop() {
        assertEquals(320, RESIZE.recBatchWidth(Collections.singletonList(new Pair<>(100, 48))));
        assertEquals(960, RESIZE.recBatchWidth(Arrays.asList(new Pair<>(100, 48), new Pair<>(960, 48))));
        assertEquals(480, RESIZE.recBatchWidth(Collections.singletonList(new Pair<>(100, 10))));
        assertEquals(3200, RESIZE.recBatchWidth(Collections.singletonList(new Pair<>(10000, 10))));
    }
    @Test public void resizedWidthRoundsUpAndStopsAtTheTensorWidth() {
        assertEquals(100, RESIZE.resizedWidth(100, 48, 320));
        assertEquals(97, RESIZE.resizedWidth(101, 50, 320));
        assertEquals(320, RESIZE.resizedWidth(1000, 48, 320));
        assertEquals(192, RESIZE.resizedWidth(1000, 48, TextLineResize.CLS_WIDTH));
    }
    @Test public void emptyCropsAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> RESIZE.resizedWidth(0, 48, 320));
        List<Pair<Integer, Integer>> sizes = Collections.singletonList(new Pair<>(10, 0));
        assertThrows(IllegalArgumentException.class, () -> RESIZE.recBatchWidth(sizes));
    }
    @Test public void onlyConfident180LabelsRotate() {
        float[] output = {0.95f, 0.05f, 0.02f, 0.98f, 0.15f, 0.85f, 0.5f, 0.5f};
        List<ClsDecision> decisions = CLS.decode(output, new long[] {4, 2}, 0.9f);
        assertEquals(4, decisions.size());
        assertEquals(0, decisions.get(0).getAngle());
        assertFalse(decisions.get(0).getRotate());
        assertEquals(180, decisions.get(1).getAngle());
        assertTrue(decisions.get(1).getRotate());
        assertEquals(180, decisions.get(2).getAngle());
        assertFalse(decisions.get(2).getRotate());
        assertEquals(0, decisions.get(3).getAngle());
        assertFalse(decisions.get(3).getRotate());
    }
    @Test public void unexpectedClassifierOutputIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> CLS.decode(new float[6], new long[] {2, 3}, 0.9f));
        assertThrows(IllegalArgumentException.class, () -> CLS.decode(new float[2], new long[] {2, 2}, 0.9f));
    }
    // Appendix D Q6: useOpenCL maps to NNAPI, which ONNX Runtime supports from Android 8.1 (API 27).
    @Test public void nnapiIsRequestedOnlyFromApi27() {
        assertTrue(ExecutionProviders.INSTANCE.shouldRequestNnapi(true, 27));
        assertTrue(ExecutionProviders.INSTANCE.shouldRequestNnapi(true, 35));
        assertFalse(ExecutionProviders.INSTANCE.shouldRequestNnapi(true, 26));
        assertFalse(ExecutionProviders.INSTANCE.shouldRequestNnapi(false, 35));
        assertEquals("cpu", ExecutionProviders.CPU);
        assertEquals("nnapi", ExecutionProviders.NNAPI);
    }
}
