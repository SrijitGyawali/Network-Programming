package main

import (
	"fmt"
	"net/url"
	"strings"
)

// 3.3 Equality, comparison and string form (Java: URIEquality).
func main() {
	a, _ := url.Parse("HTTP://WWW.Example.COM/index.html")
	b, _ := url.Parse("http://www.example.com/index.html")
	c, _ := url.Parse("http://www.example.com/INDEX.html")

	// Parse lowercases the scheme but keeps the host's case, so write the rule yourself
	fmt.Println("a.String()   :", a.String())
	fmt.Println("equal(a, b)  :", equal(a, b))
	fmt.Println("equal(b, c)  :", equal(b, c))

	// strings.Compare gives an ordering (Java: compareTo)
	fmt.Println("b after c    :", strings.Compare(b.String(), c.String()) > 0)

	// String() percent-encodes non-ASCII text (Java: toASCIIString)
	cafe := &url.URL{Scheme: "http", Host: "www.example.com", Path: "/caf" + string(rune(233))}
	fmt.Println("String()     :", cafe.String())
}

// equal follows Java's URI.equals: scheme and host ignore case, the rest does not.
func equal(x, y *url.URL) bool {
	return strings.EqualFold(x.Scheme, y.Scheme) &&
		strings.EqualFold(x.Host, y.Host) &&
		x.EscapedPath() == y.EscapedPath() &&
		x.RawQuery == y.RawQuery &&
		x.Fragment == y.Fragment
}
