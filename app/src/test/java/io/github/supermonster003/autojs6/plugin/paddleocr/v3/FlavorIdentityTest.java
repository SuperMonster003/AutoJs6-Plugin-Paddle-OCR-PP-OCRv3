package io.github.supermonster003.autojs6.plugin.paddleocr.v3;

import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/** Identity of each language package (roadmap 5.4); runs once per flavor's unit test task. */
public class FlavorIdentityTest {
    private static final String PACKAGE = "io.github.supermonster003.autojs6.plugin.paddleocr.v3";
    private static final Map<String, String[]> EXPECTED = new HashMap<>();

    static {
        // flavor -> applicationId, plugin_id, app_name, modelProfile, recommendedForMobileDefault
        EXPECTED.put("zh", new String[] {PACKAGE, "paddle-ocr-pp-ocrv3", "Paddle OCR (PP-OCRv3)", "zh", "true"});
        EXPECTED.put("en", new String[] {PACKAGE + ".en", "paddle-ocr-pp-ocrv3-en", "Paddle OCR (PP-OCRv3 EN)", "en", "false"});
        EXPECTED.put("zhHant", new String[] {PACKAGE + ".zhhant", "paddle-ocr-pp-ocrv3-zh-hant", "Paddle OCR (PP-OCRv3 ZH-Hant)", "zh-hant", "false"});
        EXPECTED.put("ja", new String[] {PACKAGE + ".ja", "paddle-ocr-pp-ocrv3-ja", "Paddle OCR (PP-OCRv3 JA)", "ja", "false"});
        EXPECTED.put("ko", new String[] {PACKAGE + ".ko", "paddle-ocr-pp-ocrv3-ko", "Paddle OCR (PP-OCRv3 KO)", "ko", "false"});
    }

    @Test public void buildConfigMatchesTheIdentityTable() {
        String[] row = EXPECTED.get(BuildConfig.FLAVOR);
        assertNotNull("Unknown flavor " + BuildConfig.FLAVOR, row);
        assertEquals(row[0], BuildConfig.APPLICATION_ID);
        assertEquals(row[1], BuildConfig.PLUGIN_ID);
        assertEquals(row[2], BuildConfig.APP_NAME);
        assertEquals(row[3], BuildConfig.MODEL_PROFILE);
        assertEquals("paddle-ocr", BuildConfig.PLUGIN_ENGINE);
        assertEquals("v3", BuildConfig.PLUGIN_VARIANT);
        assertEquals("PP-OCRv3", BuildConfig.MODEL_FAMILY);
    }
    @Test public void profileCapabilitiesFollowTheFlavor() {
        String[] row = EXPECTED.get(BuildConfig.FLAVOR);
        PpOcrV3Profile profile = PpOcrV3Profile.Companion.fromValue(BuildConfig.MODEL_PROFILE);
        assertEquals(row[3], profile.getValue());
        assertEquals(Boolean.parseBoolean(row[4]), profile.getRecommendedForMobileDefault());
    }
    @Test public void everyProfileHasItsOwnValueAndOnlyChineseIsTheMobileDefault() {
        Set<String> values = new HashSet<>();
        int recommended = 0;
        for (PpOcrV3Profile profile : PpOcrV3Profile.values()) {
            values.add(profile.getValue());
            assertEquals(profile, PpOcrV3Profile.Companion.fromValue(profile.getValue()));
            if (profile.getRecommendedForMobileDefault()) recommended++;
        }
        assertEquals(EXPECTED.size(), values.size());
        for (String[] row : EXPECTED.values()) values.remove(row[3]);
        assertEquals(0, values.size());
        assertEquals(1, recommended);
        assertEquals(PpOcrV3Profile.ZH, PpOcrV3Profile.Companion.fromValue("unknown"));
    }
}
