# MITM-ATTACK
A great tool for DNS and traffic sniffing over LAN

A Python-based tool for ARP spoofing and DNS sniffing, designed for ethical hacking and internal network testing.

![Banner](https://img.shields.io/badge/purpose-ethical--hacking-green)

## 🔍 Features
- ARP-based MITM attack
- Real-time DNS sniffing
- Device scanning with MAC vendor lookup
- Colorized terminal output using `colorama`
- ASCII banner using `pyfiglet`

## 🚀 Usage

```bash
sudo python3 dns_sniffer.py \
  --targetip <target IP> \
  --routerip <router IP> \
  --iface <network interface>
or

python dns_sniffer.py --network 0.x.x.0/00 --iface eth0 --routerip 0.x.x.0
