package net.floodlightcontroller.custom;

import java.util.*;
import org.projectfloodlight.openflow.protocol.*;
import org.projectfloodlight.openflow.types.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import net.floodlightcontroller.core.*;
import net.floodlightcontroller.core.module.*;
import net.floodlightcontroller.packet.Ethernet;

/**
 * Prog 03: Custom Floodlight security module.
 * Drops packets from blocked MACs; lets everything else CONTINUE
 * to the normal Forwarding module.
 *
 * Register in floodlightdefault.properties:
 *   floodlight.modules=...,net.floodlightcontroller.custom.CustomSecurityModule
 */
public class CustomSecurityModule implements IFloodlightModule, IOFMessageListener {

    protected IFloodlightProviderService floodlightProvider;
    protected static final Logger log = LoggerFactory.getLogger(CustomSecurityModule.class);

    // Customize: in production load from config / REST API
    private final Set<MacAddress> blockedMacs = new HashSet<>(Arrays.asList(
            MacAddress.of("00:00:00:00:00:03")));

    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleServices() {
        return null;
    }

    @Override
    public Map<Class<? extends IFloodlightService>, IFloodlightService> getServiceImpls() {
        return null;
    }

    @Override
    public Collection<Class<? extends IFloodlightService>> getDependencies() {
        return Collections.singletonList(IFloodlightProviderService.class);
    }

    @Override
    public void init(FloodlightModuleContext context) throws FloodlightModuleException {
        floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
    }

    @Override
    public void startUp(FloodlightModuleContext context) {
        floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
        log.info("CustomSecurityModule started; blocked={}", blockedMacs);
    }

    @Override
    public String getName() {
        return CustomSecurityModule.class.getSimpleName();
    }

    @Override
    public boolean isCallbackOrderingPrereq(OFType type, String name) {
        return false; // run before Forwarding: return true if name.equals("forwarding")
    }

    @Override
    public boolean isCallbackOrderingPostreq(OFType type, String name) {
        return false;
    }

    @Override
    public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
        if (msg.getType() != OFType.PACKET_IN) return Command.CONTINUE;
        Ethernet eth = IFloodlightProviderService.bcStore.get(cntx,
                IFloodlightProviderService.CONTEXT_PI_PAYLOAD);
        if (eth == null) return Command.CONTINUE;

        MacAddress src = eth.getSourceMACAddress();
        if (blockedMacs.contains(src)) {
            log.warn("BLOCKED src-mac {} on {}", src, sw.getId());
            return Command.STOP; // drop: do not forward to other listeners/switch
        }
        return Command.CONTINUE;
    }
}
