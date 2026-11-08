package main

import (
	"fmt"
	"net/url"
	"path"
	"strings"
)

// 3.3 Resolving relative URIs (Java: URIResolver).
func main() {
	base, _ := url.Parse("http://www.example.com/docs/intro/index.html")

	// relative -> absolute (Java: resolve)
	for _, r := range []string{"chapter2.html", "../images/logo.png", "/about.html", "https://other.example.org/x"} {
		ref, _ := url.Parse(r)
		fmt.Println(base.ResolveReference(ref))
	}

	// absolute -> relative (Java: relativize; Go has no built-in, so write it)
	top, _ := url.Parse("http://www.example.com/docs/")
	page, _ := url.Parse("http://www.example.com/docs/intro/chapter1.html")
	fmt.Println(relativize(top, page))

	// remove . and .. from the path (Java: normalize)
	messy, _ := url.Parse("http://www.example.com/a/./b/../c.html")
	messy.Path = path.Clean(messy.Path)
	fmt.Println(messy)
}

func relativize(base, target *url.URL) string {
	if base.Scheme == target.Scheme && base.Host == target.Host &&
		strings.HasPrefix(target.Path, base.Path) {
		return strings.TrimPrefix(target.Path, base.Path)
	}
	return target.String() // cannot be relativized: return it unchanged, as Java does
}
