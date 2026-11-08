package main

import (
	"fmt"
	"log"
	"net/url"
)

// 3.4 x-www-form-urlencoded (Java: EncoderDecoder).
func main() {
	samples := []string{"This has spaces", "a+b=c", "50%", "x&y", "/path", "*.~-_", "caf" + string(rune(233))}
	for _, s := range samples {
		encoded := url.QueryEscape(s)              // Java: URLEncoder.encode
		decoded, err := url.QueryUnescape(encoded) // Java: URLDecoder.decode
		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s   decodes back: %v\n", encoded, decoded == s)
	}

	// a space is + in a query but %20 in a path
	fmt.Println("QueryEscape:", url.QueryEscape("a b"))
	fmt.Println("PathEscape :", url.PathEscape("a b"))

	// encode only the values, never the whole URL
	fmt.Println("Wrong:", url.QueryEscape("http://www.example.com/s?q=a b"))
	fmt.Println("Right:", "http://www.example.com/s?q="+url.QueryEscape("a b"))
}
