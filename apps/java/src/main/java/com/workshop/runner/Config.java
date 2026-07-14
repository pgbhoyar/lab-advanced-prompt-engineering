package com.workshop.runner;

import java.util.Map;

/** Configuration from environment variables. Never exposes the API key. */
public final class Config {
    public final String baseUrl;
    public final String apiKey;
    public final String deployment;
    public final String reasoningEffort;
    public final int maxOutputTokens;
    public final int requestTimeoutSeconds;
    public final boolean saveResults;
    public final String resultsDirectory;

    public Config(String baseUrl, String apiKey, String deployment, String reasoningEffort,
                  int maxOutputTokens, int requestTimeoutSeconds, boolean saveResults, String resultsDirectory) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
        this.deployment = deployment;
        this.reasoningEffort = reasoningEffort;
        this.maxOutputTokens = maxOutputTokens;
        this.requestTimeoutSeconds = requestTimeoutSeconds;
        this.saveResults = saveResults;
        this.resultsDirectory = resultsDirectory;
    }

    public static final class ConfigException extends RuntimeException {
        public ConfigException(String message) { super(message); }
    }

    public static Config load(Map<String, String> env) {
        java.util.function.Function<String, String> get =
            k -> env != null ? env.get(k) : System.getenv(k);

        String[] required = {"AZURE_OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT"};
        StringBuilder missing = new StringBuilder();
        for (String k : required) {
            String v = get.apply(k);
            if (v == null || v.isBlank()) {
                if (missing.length() > 0) missing.append(", ");
                missing.append(k);
            }
        }
        if (missing.length() > 0) {
            throw new ConfigException("Missing required environment variable(s): " + missing
                + ". Copy .env.example to .env and fill in the workshop values.");
        }

        String baseUrl = get.apply("AZURE_OPENAI_BASE_URL").trim();
        String apiKey = get.apply("AZURE_OPENAI_API_KEY").trim();
        String deployment = get.apply("AZURE_OPENAI_DEPLOYMENT").trim();

        if (apiKey.contains("<") && apiKey.contains(">"))
            throw new ConfigException("AZURE_OPENAI_API_KEY still contains a placeholder. Paste the real workshop key.");
        if (!baseUrl.startsWith("https://"))
            throw new ConfigException("AZURE_OPENAI_BASE_URL must use https://.");
        String trimmed = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
        if (!trimmed.endsWith("/openai/v1"))
            throw new ConfigException("AZURE_OPENAI_BASE_URL must end in /openai/v1/ (the v1 Responses API base).");
        if (deployment.isBlank())
            throw new ConfigException("AZURE_OPENAI_DEPLOYMENT must not be blank.");

        return new Config(baseUrl, apiKey, deployment,
            orDefault(get.apply("WORKSHOP_REASONING_EFFORT"), "low"),
            parseInt(get.apply("WORKSHOP_MAX_OUTPUT_TOKENS"), 800, "WORKSHOP_MAX_OUTPUT_TOKENS"),
            parseInt(get.apply("WORKSHOP_REQUEST_TIMEOUT_SECONDS"), 90, "WORKSHOP_REQUEST_TIMEOUT_SECONDS"),
            "true".equalsIgnoreCase(orDefault(get.apply("WORKSHOP_SAVE_RESULTS"), "false")),
            orDefault(get.apply("WORKSHOP_RESULTS_DIRECTORY"), "generated-results"));
    }

    private static String orDefault(String v, String d) { return (v == null || v.isBlank()) ? d : v.trim(); }

    private static int parseInt(String v, int dflt, String name) {
        if (v == null || v.isBlank()) return dflt;
        try {
            int parsed = Integer.parseInt(v.trim());
            if (parsed <= 0) throw new ConfigException(name + " must be a positive integer.");
            return parsed;
        } catch (NumberFormatException e) {
            throw new ConfigException(name + " must be a positive integer.");
        }
    }

    public String redacted() {
        return "base_url=" + baseUrl + ", api_key=***redacted***, deployment=" + deployment
            + ", reasoning_effort=" + reasoningEffort + ", max_output_tokens=" + maxOutputTokens;
    }
}
