package cz.upce.nnpda.boot.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "app")
public class AppProperties {

    /** Welcome message returned by /api/hello. */
    private String welcomeMessage = "Hello from Lab 09";

    /** Maximum allowed tasks (demo of a custom limit). */
    private int maxTasks = 1000;

    public String getWelcomeMessage() {
        return welcomeMessage;
    }

    public void setWelcomeMessage(String welcomeMessage) {
        this.welcomeMessage = welcomeMessage;
    }

    public int getMaxTasks() {
        return maxTasks;
    }

    public void setMaxTasks(int maxTasks) {
        this.maxTasks = maxTasks;
    }
}
