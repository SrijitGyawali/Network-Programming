package main

import (
	"fmt"
	"net/http"
	"strings"
	"time"
)

// 3.2 Which schemes can Go's HTTP client fetch? (Java: ProtocolTester)
func main() {
	client := &http.Client{Timeout: 3 * time.Second}
	for _, scheme := range []string{"http", "https", "ftp", "file", "mailto", "telnet", "gopher"} {
		// nothing listens on port 1, so a supported scheme fails only when connecting
		_, err := client.Get(scheme + "://localhost:1/")
		if err != nil && strings.Contains(err.Error(), "unsupported protocol scheme") {
			fmt.Println(scheme, "is NOT supported")
		} else {
			fmt.Println(scheme, "is supported")
		}
	}
}
