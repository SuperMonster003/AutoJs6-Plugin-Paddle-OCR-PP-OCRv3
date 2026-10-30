package org.autojs.plugin.runtime;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.ResolveInfo;
import android.content.pm.ServiceInfo;
import android.os.Bundle;
import android.os.IBinder;
import android.os.ParcelFileDescriptor;
import android.util.Log;
import androidx.test.platform.app.InstrumentationRegistry;
import org.autojs.plugin.paddle.ocr.api.IOcrPlugin;
import org.autojs.plugin.paddle.ocr.api.OcrOptions;
import org.autojs.plugin.paddle.ocr.api.OcrResult;
import org.autojs.plugin.paddle.ocr.api.PaddleOcrOptionExtraKeys;
import org.autojs.plugin.paddle.ocr.api.PaddleOcrPluginCapabilityKeys;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.TimeUnit;
import static org.junit.Assert.*;
import static org.junit.Assume.assumeTrue;

/** Recognizes the language sample of the installed flavor (assets/samples, see scripts/generate_ocr_samples.py). */
public class OcrEndToEndTest {
    private static final String TAG = "OcrEndToEndTest";
    private static final double MIN_SIMILARITY = 0.8;

    private Context context;
    private ServiceConnection connection;
    private IOcrPlugin plugin;
    private String profile;
    private JSONObject samples;

    @Before public void bind() throws Exception {
        context = InstrumentationRegistry.getInstrumentation().getTargetContext();
        Intent discovery = new Intent("org.autojs.plugin.PADDLE_OCR").addCategory("paddle-ocr").setPackage(context.getPackageName());
        List<ResolveInfo> services = context.getPackageManager().queryIntentServices(discovery, 0);
        assertEquals(1, services.size());
        ServiceInfo service = services.get(0).serviceInfo;
        ArrayBlockingQueue<IBinder> connectionResult = new ArrayBlockingQueue<>(1);
        connection = new ServiceConnection() {
            @Override public void onServiceConnected(ComponentName name, IBinder binder) { connectionResult.add(binder); }
            @Override public void onServiceDisconnected(ComponentName name) {}
        };
        assertTrue(context.bindService(new Intent().setComponent(new ComponentName(service.packageName, service.name)), connection, Context.BIND_AUTO_CREATE));
        IBinder binder = connectionResult.poll(30, TimeUnit.SECONDS);
        assertNotNull(binder);
        plugin = IOcrPlugin.Stub.asInterface(binder);
        profile = plugin.getInfo().getCapabilities().getString(PaddleOcrPluginCapabilityKeys.MODEL_PROFILE);
        assertNotNull(profile);
        samples = new JSONObject(new String(readAsset("samples/samples.json"), StandardCharsets.UTF_8));
    }

    @After public void unbind() {
        if (connection != null) context.unbindService(connection);
    }

    @Test(timeout = 600000) public void recognizesTheFlavorSampleWithEveryModelSetAndProvider() throws Exception {
        String sample = "zh-hant".equals(profile) ? "zhHant" : profile;
        assertTrue("No sample for profile " + profile, samples.has(sample));
        recognize(sample, false, false, false, true);
        recognize(sample, true, false, false, true);
        recognize(sample, false, true, false, true);
    }

    @Test(timeout = 600000) public void orientationClassifierReadsUpsideDownText() throws Exception {
        assumeTrue("The rotated sample is Simplified Chinese", "zh".equals(profile));
        // Logged only: without the classifier the recognizer reads the upside-down crops as other characters.
        recognize("zh-rotated", false, false, false, false);
        recognize("zh-rotated", false, false, true, true);
    }

    /** Returns the lowest best-match similarity over the expected lines; fails below the threshold when matchRequired. */
    private double recognize(String sample, boolean useSlim, boolean useOpenCL, boolean useCls, boolean matchRequired) throws Exception {
        JSONObject entry = samples.getJSONObject(sample);
        OcrOptions options = new OcrOptions();
        options.useSlim = useSlim;
        options.useOpenCL = useOpenCL;
        options.extras = new Bundle();
        options.extras.putBoolean(PaddleOcrOptionExtraKeys.USE_CLS, useCls);
        File image = File.createTempFile("ocr-sample-", ".png", context.getCacheDir());
        try {
            try (FileOutputStream stream = new FileOutputStream(image)) { stream.write(readAsset("samples/" + entry.getString("file"))); }
            List<OcrResult> results;
            try (ParcelFileDescriptor fd = ParcelFileDescriptor.open(image, ParcelFileDescriptor.MODE_READ_ONLY)) {
                results = plugin.detect(fd, options);
            }
            String run = sample + (useSlim ? " slim" : " fp32") + (useOpenCL ? "/nnapi" : "/cpu") + (useCls ? " cls" : "");
            assertFalse(run + ": nothing recognized", results.isEmpty());
            List<String> lines = lines(results);
            JSONArray expected = entry.getJSONArray("lines");
            double lowest = 1;
            for (int index = 0; index < expected.length(); index++) {
                String target = expected.getString(index).replace(" ", "");
                double best = 0;
                for (String line : lines) best = Math.max(best, similarity(target, line));
                assertTrue(run + ": line " + (index + 1) + " similarity " + best + " in " + lines, best >= MIN_SIMILARITY || !matchRequired);
                lowest = Math.min(lowest, best);
            }
            Bundle extras = results.get(0).extras;
            String provider = extras.getString("executionProvider");
            assertTrue(run + ": provider " + provider, "cpu".equals(provider) || useOpenCL && "nnapi".equals(provider));
            Log.i(TAG, String.format(Locale.ROOT, "%s: %d lines, lowest similarity %.2f, provider %s, total %d ms, cls %d ms, cold load %d ms",
                    run, lines.size(), lowest, provider, extras.getLong("totalTimeMs"), extras.getLong("classificationTimeMs"), extras.getLong("coldLoadTimeMs")));
            return lowest;
        } finally {
            assertTrue(image.delete() || !image.exists());
        }
    }

    /** Joins boxes that share a row, so word-level detection (ko) still yields whole lines. */
    private static List<String> lines(List<OcrResult> results) {
        List<OcrResult> sorted = new ArrayList<>(results);
        sorted.sort(Comparator.comparingInt(result -> result.bounds.centerY()));
        List<List<OcrResult>> rows = new ArrayList<>();
        for (OcrResult result : sorted) {
            List<OcrResult> row = rows.isEmpty() ? null : rows.get(rows.size() - 1);
            if (row != null && Math.abs(row.get(0).bounds.centerY() - result.bounds.centerY()) * 2 < row.get(0).bounds.height()) {
                row.add(result);
            } else {
                row = new ArrayList<>();
                row.add(result);
                rows.add(row);
            }
        }
        List<String> lines = new ArrayList<>();
        for (List<OcrResult> row : rows) {
            row.sort(Comparator.comparingInt(result -> result.bounds.left));
            StringBuilder text = new StringBuilder();
            for (OcrResult result : row) text.append(result.text == null ? "" : result.text);
            lines.add(text.toString().replace(" ", ""));
        }
        return lines;
    }

    /** 1 - Levenshtein distance / longer length, over UTF-16 units (the samples have no surrogate pairs). */
    private static double similarity(String a, String b) {
        if (a.isEmpty() && b.isEmpty()) return 1;
        int[] previous = new int[b.length() + 1];
        int[] current = new int[b.length() + 1];
        for (int j = 0; j <= b.length(); j++) previous[j] = j;
        for (int i = 1; i <= a.length(); i++) {
            current[0] = i;
            for (int j = 1; j <= b.length(); j++) {
                int substitution = previous[j - 1] + (a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1);
                current[j] = Math.min(substitution, Math.min(previous[j], current[j - 1]) + 1);
            }
            int[] swap = previous;
            previous = current;
            current = swap;
        }
        return 1 - (double) previous[b.length()] / Math.max(a.length(), b.length());
    }

    private static byte[] readAsset(String path) throws Exception {
        try (InputStream input = InstrumentationRegistry.getInstrumentation().getContext().getAssets().open(path)) {
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            byte[] buffer = new byte[8192];
            int count;
            while ((count = input.read(buffer)) != -1) output.write(buffer, 0, count);
            return output.toByteArray();
        }
    }
}
