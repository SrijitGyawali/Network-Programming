package main

import (
	"bytes"
	"fmt"
	"net"
	"net/netip"
)

// 2.2 Object methods: comparing and printing addresses (Java: equals, hashCode, toString).
func main() {
	a := net.ParseIP("127.0.0.1") // stored in 16-byte form
	b := net.IP{127, 0, 0, 1}     // stored in 4-byte form
	c := net.ParseIP("127.0.0.2")

	// String() is Go's toString()
	fmt.Println("a =", a.String(), " b =", b.String(), " c =", c.String())

	// net.IP is a byte slice: == does not compile, and comparing bytes is wrong
	fmt.Println("bytes.Equal(a, b):", bytes.Equal(a, b)) // false: 16 bytes vs 4 bytes
	fmt.Println("a.Equal(b)       :", a.Equal(b))        // true: same address
	fmt.Println("a.Equal(c)       :", a.Equal(c))

	// netip.Addr (Go 1.18+) is a value type: == works and it can be a map key
	x := netip.MustParseAddr("127.0.0.1")
	y := netip.AddrFrom4([4]byte{127, 0, 0, 1})
	fmt.Println("x == y           :", x == y)

	seen := map[netip.Addr]int{} // like using InetAddress in a HashMap (needs hashCode)
	seen[x]++
	seen[y]++
	fmt.Println("map count for x  :", seen[x])
}
