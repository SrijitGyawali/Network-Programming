package main

import (
	"fmt"
	"net/url"
)

// 3.3 Constructing a URI (Java: URIConstructors). Go has one type for URLs and URIs.
func main() {
	// from one string (Java: new URI(string))
	u, _ := url.Parse("http://www.example.com/docs/index.html?lang=en#top")
	fmt.Println(u)

	// opaque: scheme + scheme-specific part (Java: new URI(scheme, ssp, fragment))
	fmt.Println(&url.URL{Scheme: "tel", Opaque: "+977-1-4331000"})

	// illegal characters in Path are escaped for you
	fmt.Println(&url.URL{Scheme: "http", Host: "www.example.com", Path: "/a b/c.html", Fragment: "top"})

	// port and query
	fmt.Println(&url.URL{Scheme: "http", Host: "www.example.com:8080", Path: "/docs", RawQuery: "lang=en", Fragment: "top"})

	// user info (Java: the seven-argument constructor)
	fmt.Println(&url.URL{Scheme: "https", User: url.User("admin"), Host: "www.example.com:8443", Path: "/docs", RawQuery: "lang=en", Fragment: "top"})

	// a URN and a relative reference are fine too
	urn, _ := url.Parse("urn:isbn:9781449357672")
	fmt.Println(urn)
	fmt.Println(&url.URL{Path: "docs/index.html"})

	// errors: Parse is more forgiving than Java (a space in the path is accepted)
	_, err := url.Parse("http://www.example.com/a b")
	fmt.Println("space in path, error:", err)
	_, err = url.Parse(":no-scheme")
	fmt.Println("bad URI, error:", err)
}
