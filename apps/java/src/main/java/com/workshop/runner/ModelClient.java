package com.workshop.runner;

import java.util.Map;

/** Model client for the v1 Responses API. Stateless requests; retry with backoff. */
public final class ModelClient {
    private static final int[] RETRYABLE = {408, 429, 500, 502, 503, 504};
    private static final int MAX_ATTEMPTS = 3;

    private final Config config;
    private final Transport transport;

    /** Transport abstraction so offline tests can inject fake responses. */
    public interface Transport {
        Response send(Map<String, Object> request) throws Exception;
    }

    public static final class Response {
        public final String text;
        public Response(String text) { this.text = text; }
    }

    public static final class ModelException extends RuntimeException {
        public final boolean retryable;
        public final Integer status;
        public ModelException(String message, boolean retryable, Integer status) {
            super(message); this.retryable = retryable; this.status = status;
        }
    }

    /** Exception carrying an HTTP status, used to classify retryability. */
    public static final class HttpStatusException extends RuntimeException {
        public final int status;
        public HttpStatusException(int status) { super("HTTP " + status); this.status = status; }
    }

    public ModelClient(Config config, Transport transport) {
        this.config = config;
        this.transport = transport != null ? transport : new HttpTransport(config);
    }

    public static boolean isRetryable(Integer status) {
        if (status != null) {
            for (int s : RETRYABLE) if (s == status) return true;
            if (status == 400 || status == 401 || status == 403 || status == 404 || status == 422) return false;
        }
        return status == null; // transient network error
    }

    public Response respond(String system, String user, Object outputSchema) {
        java.util.List<Map<String, String>> input = new java.util.ArrayList<>();
        if (system != null) input.add(Map.of("role", "system", "content", system));
        input.add(Map.of("role", "user", "content", user));

        Map<String, Object> request = new java.util.LinkedHashMap<>();
        request.put("model", config.deployment);
        request.put("input", input);
        request.put("store", false);                 // stateless (AD-004)
        request.put("max_output_tokens", config.maxOutputTokens);
        request.put("reasoning", Map.of("effort", config.reasoningEffort));
        if (outputSchema != null) {
            request.put("text", Map.of("format", Map.of(
                "type", "json_schema", "name", "triage_output", "strict", true, "schema", outputSchema)));
        }

        Exception last = null;
        for (int attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
            try {
                return transport.send(request);
            } catch (ModelException me) {
                throw me;
            } catch (Exception ex) {
                last = ex;
                Integer status = (ex instanceof HttpStatusException) ? ((HttpStatusException) ex).status : null;
                if (isRetryable(status) && attempt < MAX_ATTEMPTS) {
                    try { Thread.sleep((long) (500 * Math.pow(2, attempt - 1)) + (long) (Math.random() * 250)); }
                    catch (InterruptedException ignored) { Thread.currentThread().interrupt(); }
                    continue;
                }
                throw new ModelException(friendly(status, ex), isRetryable(status), status);
            }
        }
        throw new ModelException(last == null ? "unknown error" : last.getMessage(), false, null);
    }

    private static String friendly(Integer status, Exception ex) {
        if (status == null) return "Model request failed: " + ex.getClass().getSimpleName() + ".";
        switch (status) {
            case 401: case 403: return "Authentication failed. Check AZURE_OPENAI_API_KEY and that your workshop key is active.";
            case 404: return "Deployment not found. Check AZURE_OPENAI_DEPLOYMENT matches the workshop deployment name.";
            case 429: return "Rate limited by the service. The runner retried; try again shortly.";
            case 400: case 422: return "The request was rejected as invalid. Check the prompt and output schema.";
            default: return "Model request failed with status " + status + ".";
        }
    }

    /** Default transport using the v1 Responses API over HTTPS (REST reference path). */
    static final class HttpTransport implements Transport {
        private final Config config;
        private final java.net.http.HttpClient http;

        HttpTransport(Config config) {
            this.config = config;
            this.http = java.net.http.HttpClient.newBuilder()
                .connectTimeout(java.time.Duration.ofSeconds(config.requestTimeoutSeconds)).build();
        }

        @Override
        public Response send(Map<String, Object> request) throws Exception {
            String url = (config.baseUrl.endsWith("/") ? config.baseUrl.substring(0, config.baseUrl.length() - 1) : config.baseUrl) + "/responses";
            java.net.http.HttpRequest req = java.net.http.HttpRequest.newBuilder()
                .uri(java.net.URI.create(url))
                .timeout(java.time.Duration.ofSeconds(config.requestTimeoutSeconds))
                .header("api-key", config.apiKey)
                .header("content-type", "application/json")
                .POST(java.net.http.HttpRequest.BodyPublishers.ofString(JsonWriter.write(request)))
                .build();
            java.net.http.HttpResponse<String> resp = http.send(req, java.net.http.HttpResponse.BodyHandlers.ofString());
            if (resp.statusCode() >= 400) throw new HttpStatusException(resp.statusCode());
            Object parsed = Json.parse(resp.body());
            Object text = (parsed instanceof Map) ? ((Map<?, ?>) parsed).get("output_text") : null;
            return new Response(text == null ? "" : String.valueOf(text));
        }
    }
}
