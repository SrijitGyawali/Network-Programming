package main

import (
	"fmt"
	"net"
	"net/netip"
	"os"
)

// 2.3 IPv4 vs IPv6 (Java: Inet4Address and Inet6Address).
func main() {
	hosts := []string{"127.0.0.1", "::1", "2001:4860:4860::8888", "::ffff:192.168.1.1", "www.google.com"}
	if len(os.Args) > 1 {
		hosts = os.Args[1:]
	}
	for _, h := range hosts {
		ip := net.ParseIP(h)
		if ip == nil { // not a literal address: look up the name
			ips, err := net.LookupIP(h)
			if err != nil {
				fmt.Println(h, "-> unknown host")
				continue
			}
			ip = ips[0]
		}

		// method 1: net.IP.To4() returns nil for a real IPv6 address
		if ip.To4() != nil {
			fmt.Println(h, "-> IPv4", ip)
		} else {
			fmt.Println(h, "-> IPv6", ip)
		}

		// method 2: netip.Addr remembers exactly how the address was written
		if addr, err := netip.ParseAddr(h); err == nil {
			fmt.Printf("    netip: Is4=%v Is6=%v Is4In6=%v\n", addr.Is4(), addr.Is6(), addr.Is4In6())
		}
	}
}
