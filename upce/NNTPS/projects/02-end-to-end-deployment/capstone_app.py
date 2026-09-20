"""Capstone RYU app: L2 learning + static diamond routing + blocklist + link-failover flush.

Simplified teaching version: reactive forwarding with per-flow install;
on link down, delete all flows to force re-learning over surviving path.
Production version would use topology discovery + Dijkstra (see README stretch).

Run: ryu-manager capstone_app.py
"""
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, tcp
from ryu.topology import event as topo_event

BLOCKED_IPS = {"10.0.0.5"}      # h5 quarantined (demo security policy)
ADMIN_HOST = "10.0.0.1"         # only h1 may use TCP/22
BLOCKED_TCP_PORT = 22


class CapstoneApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapaths = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features(self, ev):
        dp = ev.msg.datapath
        self.datapaths[dp.id] = dp
        ofp, parser = dp.ofproto, dp.ofproto_parser
        inst = [parser.OFPInstructionActions(
            ofp.OFPIT_APPLY_ACTIONS,
            [parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)])]
        dp.send_msg(parser.OFPFlowMod(datapath=dp, priority=0, match=parser.OFPMatch(),
                                      instructions=inst))

    def _flood(self, dp, msg, in_port):
        parser = dp.ofproto_parser
        dp.send_msg(parser.OFPPacketOut(
            datapath=dp, buffer_id=msg.buffer_id, in_port=in_port,
            actions=[parser.OFPActionOutput(dp.ofproto.OFPP_FLOOD)], data=msg.data))

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in(self, ev):
        msg = ev.msg
        dp, ofp, parser = msg.datapath, msg.datapath.ofproto, msg.datapath.ofproto_parser
        in_port = msg.match["in_port"]
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth is None:
            return
        ip = pkt.get_protocol(ipv4.ipv4)
        tcph = pkt.get_protocol(tcp.tcp)

        # --- Security policies ---
        if ip is not None:
            if ip.src in BLOCKED_IPS or ip.dst in BLOCKED_IPS:
                self.logger.warning("DENY quarantined ip %s -> %s", ip.src, ip.dst)
                return  # drop: no PacketOut, no flow
            if tcph is not None and tcph.dst_port == BLOCKED_TCP_PORT and ip.src != ADMIN_HOST:
                self.logger.warning("DENY tcp/22 from %s", ip.src)
                return

        # --- Reactive routing (learn + forward) ---
        self.mac_to_port.setdefault(dp.id, {})[eth.src] = in_port
        out = self.mac_to_port[dp.id].get(eth.dst, ofp.OFPP_FLOOD)
        actions = [parser.OFPActionOutput(out)]
        if out != ofp.OFPP_FLOOD:
            inst = [parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]
            dp.send_msg(parser.OFPFlowMod(
                datapath=dp, priority=10,
                match=parser.OFPMatch(in_port=in_port, eth_dst=eth.dst),
                instructions=inst, idle_timeout=15))
        dp.send_msg(parser.OFPPacketOut(datapath=dp, buffer_id=msg.buffer_id,
                                        in_port=in_port, actions=actions, data=msg.data))

    # --- Failover: on any link down, flush flows so traffic re-learns via backup ---
    @set_ev_cls(topo_event.EventLinkDelete, MAIN_DISPATCHER)
    def link_down(self, ev):
        self.logger.warning("LINK DOWN %s; flushing flows for reconvergence", ev.link)
        for dp in self.datapaths.values():
            dp.send_msg(dp.ofproto_parser.OFPFlowMod(
                datapath=dp, command=dp.ofproto.OFPFC_DELETE,
                out_port=dp.ofproto.OFPP_ANY, out_group=dp.ofproto.OFPG_ANY,
                match=dp.ofproto_parser.OFPMatch()))
        self.mac_to_port.clear()
