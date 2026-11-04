package main

import (
	"fmt"
	"net"
	"os"
)

// 2.2 Address types: classify an address with the IsXXX() methods.
func main() {
	hosts := []string{
		"0.0.0.0", "127.0.0.1", "169.254.10.1", "192.168.1.10", "8.8.8.8",
		"224.0.0.1", "239.255.255.250", "::1", "fe80::1", "ff0e::1",
	}
	if len(os.Args) > 1 {
		hosts = os.Args[1:]
	}
	for _, h := range hosts {
		ip := net.ParseIP(h)
		if ip == nil {
			fmt.Println(h, "-> not an IP address")
			continue
		}
		fmt.Println(h, "->", kind(ip))
	}
}

func kind(ip net.IP) string {
	switch {
	case ip.IsUnspecified():
		return "wildcard (unspecified) address"
	case ip.IsLoopback():
		return "loopback address"
	case ip.IsLinkLocalUnicast():
		return "link-local address"
	case ip.IsPrivate():
		return "private (site-local) address"
	case ip.IsInterfaceLocalMulticast():
		return "interface-local multicast address"
	case ip.IsLinkLocalMulticast():
		return "link-local multicast address"
	case ip.IsMulticast():
		return "multicast address (wider scope)"
	case ip.IsGlobalUnicast():
		return "global (public) unicast address"
	}
	return "unknown type"
}
