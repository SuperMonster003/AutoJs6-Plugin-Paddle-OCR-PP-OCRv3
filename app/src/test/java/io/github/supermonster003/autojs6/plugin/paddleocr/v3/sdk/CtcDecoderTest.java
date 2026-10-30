package io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk;

import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.model.ModelConfig;
import io.github.supermonster003.autojs6.plugin.paddleocr.v3.sdk.postprocess.CTCDecoder;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import java.util.Arrays;

/** Text order of the arabic recognizer, checked against PaddleOCR 2.7 BaseRecLabelDecode.pred_reverse. */
public class CtcDecoderTest {
    private static final CTCDecoder CTC = CTCDecoder.INSTANCE;
    private static final char ALEF = 0x0627;
    private static final char BEH = 0x0628;
    private static final char TEH = 0x062A;

    @Test public void lettersAreMirroredAndLatinRunsStayReadable() {
        assertEquals("" + TEH + BEH + ALEF, CTC.toLogicalOrder("" + ALEF + BEH + TEH));
        assertEquals("AutoJs6", CTC.toLogicalOrder("AutoJs6"));
        assertEquals(" 12:30" + BEH + ALEF, CTC.toLogicalOrder("" + ALEF + BEH + " 12:30"));
        assertEquals("" + BEH + "v3 " + ALEF, CTC.toLogicalOrder(ALEF + "v3 " + BEH));
        assertEquals("", CTC.toLogicalOrder(""));
    }
    @Test public void decodeOnlyReversesWhenTheModelAsksForIt() {
        // Three time steps of three classes (blank, ALEF, BEH): ALEF, blank, BEH.
        float[] output = {0.1f, 0.8f, 0.1f, 0.8f, 0.1f, 0.1f, 0.1f, 0.1f, 0.8f};
        long[] shape = {1, 3, 3};
        assertEquals("" + ALEF + BEH, CTC.decode(output, shape, Arrays.asList("" + ALEF, "" + BEH), false).get(0).getFirst());
        assertEquals("" + BEH + ALEF, CTC.decode(output, shape, Arrays.asList("" + ALEF, "" + BEH), true).get(0).getFirst());
    }
    @Test public void onlyTheKeyAboveTheDictionaryTurnsReversingOn() {
        assertTrue(ModelConfig.Companion.readReverse("PostProcess:\n  name: CTCLabelDecode\n  reverse: true\n  character_dict:\n    - 'a'\n"));
        assertTrue(ModelConfig.Companion.readReverse("PostProcess:\r\n  reverse: true\r\n  character_dict:\r\n"));
        assertFalse(ModelConfig.Companion.readReverse("PostProcess:\n  name: CTCLabelDecode\n  character_dict:\n    - 'a'\n"));
        assertFalse(ModelConfig.Companion.readReverse("PostProcess:\n  character_dict:\n    - 'reverse: true'\n  reverse: true\n"));
    }
}
