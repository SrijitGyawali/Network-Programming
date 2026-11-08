package main

import (
	"fmt"
	"net/url"
)

// 3.2 Equality, comparison and conversion (Java: URLEquality).
func main() {
	a, _ := url.Parse("http://localhost/index.html")
	b, _ := url.Parse("http://127.0.0.1/index.html")
	c, _ := url.Parse("http://www.example.com/page.html#first")
	d, _ := url.Parse("http://www.example.com/page.html#second")

	// Go compares text and never touches DNS (Java's equals does a lookup)
	fmt.Println("localhost == 127.0.0.1 :", a.String() == b.String())

	fmt.Println("c == d                 :", c.String() == d.String())
	fmt.Println("sameFile(c, d)         :", sameFile(c, d))

	// conversion
	fmt.Println("String()               :", c.String())
	fmt.Println("RequestURI()           :", c.RequestURI())
}

// sameFile compares two URLs ignoring the fragment, like Java's URL.sameFile.
func sameFile(x, y *url.URL) bool {
	p, q := *x, *y // copy the structs so the originals are not changed
	p.Fragment, q.Fragment = "", ""
	return p.String() == q.String()
}
