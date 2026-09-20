# Programming 03 — Floodlight Java Development (Custom Module)

**Objective:** Import Floodlight into Eclipse, write a Java module hooking the core packet-in pipeline.

## 1. Setup

```bash
git clone https://github.com/floodlight/floodlight.git && cd floodlight
git submodule init && git submodule update
# Java 11 (Floodlight 1.2). Java 17+ breaks ant build.
sudo apt install -y ant openjdk-11-jdk eclipse
ant
java -jar target/floodlight.jar   # sanity: REST on :8080
```

Eclipse: File → Import → Existing Java Project → select `floodlight/` → wait for build (fix `lib/` jars if red X).

## 2. Module (`CustomSecurityModule.java`)

Implements `IFloodlightModule, IOFMessageListener`:

- `getModuleServices / getServiceImpls` — none (leaf module).
- `getDependencies` — needs `IFloodlightProviderService`.
- `startUp` — `addOFMessageListener(OPENFLOW, this)`.
- `receive` — same logic as RYU Prog 02 but in Java:
  - Parse `Ethernet` → if `srcMac` in blocklist → `Command.STOP` (drop, optionally install drop flow).
  - Else `Command.CONTINUE` (let Forwarding/LearningSwitch handle it).

Register in `src/main/resources/META-INF/services/net.floodlightcontroller.core.module.IFloodlightModule`
or `floodlightdefault.properties`:

```properties
floodlight.modules = ...,net.floodlightcontroller.custom.CustomSecurityModule
```

## 3. Build & Run

```bash
ant
java -jar target/floodlight.jar -cf src/main/resources/floodlightdefault.properties
# Test with Mininet remote to :6653, ping blocked host -> 100% loss, check log:
# WARN CustomSecurity - BLOCKED src-mac 00:00:00:00:00:03
```

## Exercises

1. Install a permanent drop flow via `IOFSwitch.write(flowMod)` instead of just `STOP`. Compare counter behavior.
2. Expose blocklist over Floodlight REST (`IRestApiService`) — `GET /wm/custom/block/json`, `POST` to add.
3. Write a JUnit test feeding a crafted `OFPacketIn` and asserting `STOP` vs `CONTINUE`.
