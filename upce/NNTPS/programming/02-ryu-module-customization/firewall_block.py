"""Prog 02: RYU L2 switch + blocklist security (MAC + IPv4).

Customize BLOCKED_MACS / BLOCKED_IPS, then:
    ryu-manager firewall_block.py
"""
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

# --- Customize here (exercise: make runtime-configurable) ---
BLOCKED_MACS = {"00:00:00:00:00:03"}  # h3 in `mn --mac` topo
BLOCKED_IPS = {"10.0.0.3"}


class FirewallBlock(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        dp = ev.msg.datapath
        ofp, parser = dp.ofproto, dp.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
        dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=0, match=match, instructions=inst))

    def _install_drop(self, dp, parser, match, reason):
        # Empty instruction set => drop. Permanent (no timeout) so future
        # packets are dropped in hardware without Packet-In overhead.
        inst = []  # no APPLY_ACTIONS = drop
        dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=100, match=match,
                                      instructions=inst, idle_timeout=0, hard_timeout=0))
        self.logger.warning("BLOCKED (%s) on s%s", reason, dp.id)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp, ofp, parser = msg.datapath, msg.datapath.ofproto, msg.datapath.ofproto_parser
        in_port = msg.match["in_port"]
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth is None:
            return

        # --- Security: MAC blocklist ---
        if eth.src in BLOCKED_MACS:
            self._install_drop(dp, parser, parser.OFPMatch(eth_src=eth.src),
                               reason=f"src-mac {eth.src}")
            return  # do not forward, do not learn

        # --- Security: IP blocklist ---
        ip = pkt.get_protocol(ipv4.ipv4)
        if ip is not None and ip.src in BLOCKED_IPS:
            self._install_drop(dp, parser, parser.OFPMatch(eth_type=0x0800, ipv4_src=ip.src),
                               reason=f"src-ip {ip.src}")
            return

        # --- Normal L2 learning (same as Prog 01) ---
        dpid = dp.id
        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid][eth.src] = in_port
        out_port = self.mac_to_port[dpid].get(eth.dst, ofp.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out_port)]
        if out_port != ofp.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=eth.dst)
            inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=1, match=match,
                                          instructions=inst, idle_timeout=10))
        dp.send_msg(parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                        in_port=in_port, actions=actions, data=msg.data))
