#! /usr/bin/env python

# The following line will import all Scapy modules
from scapy.all import *

# Set each layer
ip_layer = IP(dst="INSERT DESTINATION IP HERE")
icmp_layer = ICMP(seq=9999)

# Stack all layers with /
packet = ip_layer / icmp_layer

# Send the packet
send(packet)
