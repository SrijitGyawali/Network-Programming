package main

import (
	"fmt"
	"log"
	"net"
	"os"
)

// 2.1 Getting information about an address (Java: InetAddress getter methods).
func main() {
	host := "www.facebook.com"
	if len(os.Args) > 1 {
		host = os.Args[1]
	}

	ips, err := net.LookupIP(host)
	if err != nil {
		log.Fatal(err)
	}
	ip := ips[0]

	cname, _ := net.LookupCNAME(host) // Java: getCanonicalHostName
	fmt.Println("Host name      :", host)
	fmt.Println("Canonical name :", cname)
	fmt.Println("IP address     :", ip.String()) // Java: getHostAddress

	if v4 := ip.To4(); v4 != nil { // Java: getAddress().length == 4
		fmt.Println("Raw bytes      :", []byte(v4)) // Go bytes are unsigned (0..255)
		fmt.Println("IP version     : IPv4")
	} else {
		fmt.Println("Raw bytes      :", []byte(ip))
		fmt.Println("IP version     : IPv6")
	}

	// reverse lookup: IP address -> host names (Java: getHostName)
	names, err := net.LookupAddr("8.8.8.8")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("8.8.8.8 is     :", names)
}
