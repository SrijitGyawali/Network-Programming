package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

// 3.7 Accessing a password-protected site (Java: SecureViewer + Authenticator).
// Start testserver first (login: student / network123).
func main() {
	user, password := "student", "network123"
	if len(os.Args) > 2 {
		user, password = os.Args[1], os.Args[2]
	}
	const address = "http://localhost:8000/secret"

	// without credentials the server answers 401 and says which login it wants
	resp, err := http.Get(address)
	if err != nil {
		log.Fatal(err)
	}
	resp.Body.Close()
	fmt.Println("No login        :", resp.Status)
	fmt.Println("WWW-Authenticate:", resp.Header.Get("WWW-Authenticate"))

	// Go has no Authenticator callback: attach the login to the request yourself
	req, err := http.NewRequest("GET", address, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.SetBasicAuth(user, password)

	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	fmt.Println("With login      :", resp.Status)
	io.Copy(os.Stdout, resp.Body)
}
