package cz.upce.nnpda.server.controller;

import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.time.Instant;
import java.util.Map;
import java.util.TreeMap;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/info")
public class InfoController {

    @Value("${server.port:8080}")
    private String port;

    @GetMapping
    public Map<String, Object> info() {
        RuntimeMXBean runtime = ManagementFactory.getRuntimeMXBean();
        Map<String, Object> out = new TreeMap<>();
        out.put("app", "lab-10-appservers");
        out.put("timestamp", Instant.now().toString());
        out.put("javaVersion", System.getProperty("java.version"));
        out.put("javaVendor", System.getProperty("java.vendor"));
        out.put("serverPort", port);
        out.put("contextPath", "/ (embedded) or /lab10-app (WAR)");
        out.put("uptimeMs", runtime.getUptime());
        out.put("availableProcessors", Runtime.getRuntime().availableProcessors());
        out.put("heapMaxMB", Runtime.getRuntime().maxMemory() / 1024 / 1024);
        out.put("servletContainer",
                getClass().getPackage().getImplementationTitle() != null
                        ? getClass().getPackage().getImplementationTitle() : "embedded-tomcat (Spring Boot)");
        return out;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }
}
