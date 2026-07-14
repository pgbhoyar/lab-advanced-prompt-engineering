package com.workshop.runner;

import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

@Tag("offline")
class OfflineTests {

    private static Map<String, String> goodEnv() {
        Map<String, String> env = new HashMap<>();
        env.put("AZURE_OPENAI_BASE_URL", "https://example.openai.azure.com/openai/v1/");
        env.put("AZURE_OPENAI_API_KEY", "abcd1234abcd1234abcd1234abcd1234");
        env.put("AZURE_OPENAI_DEPLOYMENT", "workshop-gpt-54");
        return env;
    }

    private static final String VALID_TRIAGE =
        "{\"request_id\":\"SR-1\",\"summary\":\"x\",\"category\":\"network\",\"urgency\":\"high\"," +
        "\"recommended_action\":\"do x\",\"missing_information\":[],\"evidence\":[]," +
        "\"confidence\":\"medium\",\"needs_human_review\":false}";

    @Test
    void configLoadsAndRedacts() {
        Config cfg = Config.load(goodEnv());
        assertEquals("workshop-gpt-54", cfg.deployment);
        assertTrue(cfg.redacted().contains("***redacted***"));
    }

    @Test
    void configRejectsMissing() {
        Map<String, String> env = goodEnv();
        env.put("AZURE_OPENAI_API_KEY", "");
        Config.ConfigException ex = assertThrows(Config.ConfigException.class, () -> Config.load(env));
        assertTrue(ex.getMessage().toLowerCase().contains("missing required"));
    }

    @Test
    void configRejectsNonHttps() {
        Map<String, String> env = goodEnv();
        env.put("AZURE_OPENAI_BASE_URL", "http://x/openai/v1/");
        Config.ConfigException ex = assertThrows(Config.ConfigException.class, () -> Config.load(env));
        assertFalse(ex.getMessage().contains("abcd1234"));
    }

    @Test
    void validateSuccess() {
        Validate.Result r = Validate.structured(VALID_TRIAGE);
        assertTrue(r.passed);
        assertTrue(r.errors.isEmpty());
    }

    @Test
    void validateInvalidJson() {
        Validate.Result r = Validate.structured("category is network");
        assertFalse(r.passed);
        assertTrue(r.errors.stream().anyMatch(e -> e.contains("not valid JSON")));
    }

    @Test
    void validateSchemaViolation() {
        String bad = "{\"request_id\":\"SR-1\",\"summary\":\"x\",\"category\":\"network\",\"urgency\":\"urgent\"," +
            "\"recommended_action\":\"a\",\"missing_information\":[],\"evidence\":[],\"confidence\":\"low\"," +
            "\"needs_human_review\":false,\"extra\":1}";
        Validate.Result r = Validate.structured(bad);
        assertFalse(r.passed);
        assertTrue(r.errors.stream().anyMatch(e -> e.contains("urgency")));
        assertTrue(r.errors.stream().anyMatch(e -> e.contains("extra")));
    }

    @Test
    void retryThenSuccess() {
        final int[] calls = {0};
        ModelClient.Transport transport = request -> {
            calls[0]++;
            if (calls[0] <= 2) throw new ModelClient.HttpStatusException(429);
            return new ModelClient.Response(VALID_TRIAGE);
        };
        ModelClient client = new ModelClient(Config.load(goodEnv()), transport);
        ModelClient.Response resp = client.respond(null, "hi", null);
        assertEquals(3, calls[0]);
        assertTrue(resp.text.contains("network"));
    }

    @Test
    void authFailureNotRetried() {
        ModelClient.Transport transport = request -> { throw new ModelClient.HttpStatusException(401); };
        ModelClient client = new ModelClient(Config.load(goodEnv()), transport);
        ModelClient.ModelException ex = assertThrows(ModelClient.ModelException.class,
            () -> client.respond(null, "hi", null));
        assertEquals(Integer.valueOf(401), ex.status);
        assertFalse(ex.retryable);
    }

    @Test
    void requestIsStatelessAndOmitsUnsupportedParams() {
        final Map<String, Object>[] captured = new Map[1];
        ModelClient.Transport transport = request -> { captured[0] = request; return new ModelClient.Response(VALID_TRIAGE); };
        new ModelClient(Config.load(goodEnv()), transport).respond("sys", "usr", null);
        assertEquals(Boolean.FALSE, captured[0].get("store"));
        for (String banned : new String[]{"temperature", "top_p", "presence_penalty", "frequency_penalty"})
            assertFalse(captured[0].containsKey(banned));
    }

    @Test
    void retryClassification() {
        assertTrue(ModelClient.isRetryable(503));
        assertFalse(ModelClient.isRetryable(400));
        assertTrue(ModelClient.isRetryable(null));
    }
}
