package main

import (
	"fmt"
	"log"
	"net"
)

// 2.4 Network interfaces (Java: NetworkInterface).
func main() {
	// all interfaces (Java: getNetworkInterfaces)
	ifaces, err := net.Interfaces()
	if err != nil {
		log.Fatal(err)
	}
	for _, ifc := range ifaces {
		if ifc.Flags&net.FlagUp == 0 { // skip disabled interfaces
			continue
		}
		fmt.Printf("Name: %s  Index: %d\n", ifc.Name, ifc.Index)
		fmt.Printf("    loopback=%v  MTU=%d  MAC=%v\n",
			ifc.Flags&net.FlagLoopback != 0, ifc.MTU, ifc.HardwareAddr)
		addrs, _ := ifc.Addrs() // Java: getInetAddresses
		for _, a := range addrs {
			fmt.Println("    address:", a) // includes the prefix, e.g. 192.168.1.74/24
		}
	}

	// by name (Java: getByName)
	if lo, err := net.InterfaceByName("lo"); err == nil {
		fmt.Println(`InterfaceByName("lo") ->`, lo.Name)
	} else {
		fmt.Println(`InterfaceByName("lo") ->`, err)
	}

	// by address (Java: getByInetAddress): Go has no direct function, so search
	fmt.Println("interface for 127.0.0.1 ->", byIP(ifaces, net.ParseIP("127.0.0.1")))
}

func byIP(ifaces []net.Interface, ip net.IP) string {
	for _, ifc := range ifaces {
		addrs, _ := ifc.Addrs()
		for _, a := range addrs {
			if ipnet, ok := a.(*net.IPNet); ok && ipnet.IP.Equal(ip) {
				return ifc.Name
			}
		}
	}
	return "none"
}
