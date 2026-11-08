package main

import (
	"fmt"
	"log"
	"net"
	"net/url"
)

// 3.2 Creating new URLs (Java: the URL constructors).
func main() {
	// 1. from one complete string (Java: new URL(spec))
	u1, err := url.Parse("http://www.example.com:8080/docs/index.html?lang=en#top")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("url.Parse           :", u1)

	// 2. from parts (Java: new URL(protocol, host, file))
	u2 := &url.URL{Scheme: "http", Host: "www.example.com", Path: "/docs/index.html"}
	fmt.Println("url.URL{...}        :", u2)

	// 3. with a port (Java: new URL(protocol, host, port, file))
	u3 := &url.URL{
		Scheme: "https",
		Host:   net.JoinHostPort("www.example.com", "8443"),
		Path:   "/docs/index.html",
	}
	fmt.Println("url.URL{... port}   :", u3)

	// 4. relative to a base URL (Java: new URL(base, relative))
	base, _ := url.Parse("http://www.example.com/docs/intro/index.html")
	for _, relative := range []string{"chapter1.html", "../img/logo.png", "/about.html"} {
		u, err := base.Parse(relative)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("base.Parse(%-16q): %s\n", relative, u)
	}

	// url.Parse only checks syntax: an unknown scheme is fine, a bad host is not
	unknown, err := url.Parse("htp://www.example.com/")
	fmt.Println("unknown scheme      :", unknown, "error:", err)
	_, err = url.Parse("http://bad host/")
	fmt.Println("bad host            :", err)
}
