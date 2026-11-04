package main

import (
	"fmt"
	"log"
	"net"
	"os"
)

// 2.1 Creating IP addresses: DNS lookups and parsing (Java: InetAddress factory methods).
func main() {
	host := "www.google.com"
	if len(os.Args) > 1 {
		host = os.Args[1]
	}

	// 1. first address of a host (Java: getByName)
	addr, err := net.ResolveIPAddr("ip", host)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("ResolveIPAddr :", addr)

	// 2. every address of the host (Java: getAllByName)
	ips, err := net.LookupIP(host)
	if err != nil {
		log.Fatal(err)
	}
	for _, ip := range ips {
		fmt.Println("LookupIP      :", ip)
	}

	// 3. this machine (Java: getLocalHost)
	name, _ := os.Hostname()
	local, _ := net.LookupIP(name)
	fmt.Println("Hostname      :", name, local)

	// 4. loopback (Java: getLoopbackAddress)
	fmt.Println("Loopback      :", net.IPv4(127, 0, 0, 1), net.IPv6loopback)

	// 5. from text or raw bytes: no DNS lookup (Java: getByAddress)
	fmt.Println("ParseIP       :", net.ParseIP("192.168.1.1"))
	fmt.Println("From bytes    :", net.IP{192, 168, 1, 1})
}
