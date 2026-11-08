package main

import (
	"fmt"
	"log"
	"net/http"
	"sort"
)

// A small server on port 8000 for trying out the programs in sections 3.5 - 3.7.
//
//	/search?q=...  echoes the decoded query parameters
//	/secret        needs HTTP Basic login: student / network123
//	any absolute-URI request is answered as if this server were an HTTP proxy
func main() {
	http.HandleFunc("/", root)
	http.HandleFunc("/search", search)
	http.HandleFunc("/secret", secret)
	fmt.Println("testserver running on http://localhost:8000/")
	log.Fatal(http.ListenAndServe(":8000", nil))
}

func root(w http.ResponseWriter, r *http.Request) {
	if r.URL.IsAbs() {
		fmt.Fprintln(w, "Answered by the proxy for", r.URL)
		return
	}
	fmt.Fprintln(w, "Hello from testserver, you asked for", r.URL)
}

func search(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Search received:")
	values := r.URL.Query()
	keys := make([]string, 0, len(values))
	for k := range values {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	for _, k := range keys {
		fmt.Fprintf(w, "  %s = %s\n", k, values.Get(k))
	}
}

func secret(w http.ResponseWriter, r *http.Request) {
	user, password, ok := r.BasicAuth()
	if ok && user == "student" && password == "network123" {
		fmt.Fprintln(w, "Welcome! This page is password protected.")
		return
	}
	w.Header().Set("WWW-Authenticate", `Basic realm="Network Programming"`)
	http.Error(w, "Login required", http.StatusUnauthorized)
}
