package main

import (
	"fmt"
	"net/url"
	"os"
)

// 3.3 The parts of the URI (Java: URISplitter).
func main() {
	addresses := []string{
		"https://admin@www.example.com:8443/a%20b/c.html?lang=en#top",
		"tel:+977-1-4331000",
		"docs/index.html",
	}
	if len(os.Args) > 1 {
		addresses = os.Args[1:]
	}

	for _, address := range addresses {
		u, err := url.Parse(address)
		if err != nil {
			fmt.Println(address, "is not a valid URI:", err)
			continue
		}
		fmt.Println("URI:", u)
		fmt.Println("  IsAbs()       ", u.IsAbs())
		fmt.Println("  Scheme        ", u.Scheme)
		if u.Opaque != "" { // Java: isOpaque()
			fmt.Println("  Opaque        ", u.Opaque)
		} else {
			fmt.Println("  User          ", u.User)
			fmt.Println("  Hostname()    ", u.Hostname())
			fmt.Println("  Port()        ", u.Port())
			fmt.Println("  Path          ", u.Path)          // decoded
			fmt.Println("  EscapedPath() ", u.EscapedPath()) // still encoded
			fmt.Println("  RawQuery      ", u.RawQuery)
		}
		fmt.Println("  Fragment      ", u.Fragment)
	}
}
