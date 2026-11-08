package main

import (
	"fmt"
	"log"
	"net/url"
)

// 3.4 Building and parsing a query string (Java: the QueryString class).
func main() {
	v := url.Values{} // a map[string][]string with helper methods
	v.Add("name", "Hari Bahadur")
	v.Add("course", "Network Programming")
	v.Add("marks", "60+20")

	encoded := v.Encode() // keys come out sorted
	fmt.Println(encoded)

	parsed, err := url.ParseQuery(encoded)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("marks =", parsed.Get("marks"))
}
