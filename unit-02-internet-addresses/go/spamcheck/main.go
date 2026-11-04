package main

import (
	"fmt"
	"net"
	"os"
)

// 2.5 SpamCheck: ask a DNS blackhole list (DNSBL) whether an IP is a known spammer.
const blackhole = "sbl.spamhaus.org"

func main() {
	ips := []string{"127.0.0.2", "8.8.8.8"}
	if len(os.Args) > 1 {
		ips = os.Args[1:]
	}
	for _, ip := range ips {
		if isSpammer(ip) {
			fmt.Println(ip, "is a known spammer.")
		} else {
			fmt.Println(ip, "appears legitimate.")
		}
	}
}

func isSpammer(s string) bool {
	ip := net.ParseIP(s).To4()
	if ip == nil {
		return false // this simple check handles IPv4 only
	}
	// reverse the octets: 1.2.3.4 -> 4.3.2.1.sbl.spamhaus.org
	query := fmt.Sprintf("%d.%d.%d.%d.%s", ip[3], ip[2], ip[1], ip[0], blackhole)
	_, err := net.LookupHost(query)
	return err == nil // resolves -> listed
}
