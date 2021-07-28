import socket
import enum
import psutil
from pprint import pprint

class IPV4_ADDR(enum.Enum):
    netmask = '255.255.255.0'
    family = socket.AddressFamily.AF_INET


def get_wifi_ip(address_family="ipv4"):
    if psutil.net_if_stats().get("Wi-Fi").isup:
        wifi_addrs = psutil.net_if_addrs().get("Wi-Fi")
        if  address_family == "ipv4":
            for addr in wifi_addrs:
                if addr.netmask == IPV4_ADDR.netmask.value and addr.family == IPV4_ADDR.family.value :
                    return addr.address
    return "127.0.0.1"

if __name__ == '__main__':
    print(get_wifi_ip())
