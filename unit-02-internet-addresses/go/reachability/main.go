package main

import (
	"errors"
	"fmt"
	"net"
	"os"
	"time"
)

// 2.2 Testing reachability. Go has no isReachable(): ICMP ping needs raw sockets
// (admin rights), so we try a TCP connection with a timeout instead.
func main() {
	hosts := []string{"localhost", "www.google.com", "10.255.255.1"}
	if len(os.Args) > 1 {
		hosts = os.Args[1:]
	}
	for _, h := range hosts {
		fmt.Println(h, "->", check(h, "443", 3*time.Second))
	}
}

func check(host, port string, timeout time.Duration) string {
	conn, err := net.DialTimeout("tcp", net.JoinHostPort(host, port), timeout)
	if err == nil {
		conn.Close()
		return "reachable (port " + port + " open)"
	}
	var netErr net.Error
	if errors.As(err, &netErr) && netErr.Timeout() {
		return "NOT reachable (timed out)"
	}
	// "connection refused" means the host answered, but nothing listens on that port
	return "no service on port " + port + ": " + err.Error()
}
