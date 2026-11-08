# Unit 3: URLs and URIs (5 hrs)

Start with the study guide: [Unit3_URLs_and_URIs_Java_and_Go.pdf](Unit3_URLs_and_URIs_Java_and_Go.pdf).
Read Part A (theory) first, then Part B (Java) and Part C (Go) side by side: section B2 matches C2, B3 matches C3, and so on.

## Syllabus topics

| Topic | Theory | Java | Go |
|---|---|---|---|
| 3.1 URIs: URLs and relative URLs | A1, A2 | - | - |
| 3.2 The URL class: creating, retrieving, splitting, equality, conversion | A1 | B1-B5 | C1-C5 |
| 3.3 The URI class: constructing, parts, resolving, equality, strings | A1, A2 | B6-B9 | C6-C9 |
| 3.4 x-www-form-urlencoded: URLEncoder and URLDecoder | A3 | B10 | C10 |
| 3.5 Proxies: system properties, Proxy and ProxySelector | A4 | B11, B12 | C11, C12 |
| 3.6 Communicating with server-side programs through GET | A5 | B13 | C13 |
| 3.7 Password-protected sites: Authenticator, PasswordAuthentication, JPasswordField | A6 | B14, B15 | C14, C15 |

## Programs

| # | Topic | Java | Go |
|---|---|---|---|
| 1 | URL constructors | [URLConstructors](java/URLConstructors.java) | [url_build](go/url_build/main.go) |
| 2 | Supported protocols | [ProtocolTester](java/ProtocolTester.java) | [protocol_tester](go/protocol_tester/main.go) |
| 3 | Reading a page | [SourceViewer](java/SourceViewer.java) | [source_viewer](go/source_viewer/main.go) |
| 4 | Content type | [ContentGetter](java/ContentGetter.java) | [content_getter](go/content_getter/main.go) |
| 5 | Splitting a URL | [URLSplitter](java/URLSplitter.java) | [url_split](go/url_split/main.go) |
| 6 | URL equality | [URLEquality](java/URLEquality.java) | [url_compare](go/url_compare/main.go) |
| 7 | URI constructors | [URIConstructors](java/URIConstructors.java) | [uri_build](go/uri_build/main.go) |
| 8 | Parts of a URI | [URISplitter](java/URISplitter.java) | [uri_parts](go/uri_parts/main.go) |
| 9 | Resolving URIs | [URIResolver](java/URIResolver.java) | [uri_resolve](go/uri_resolve/main.go) |
| 10 | URI equality | [URIEquality](java/URIEquality.java) | [uri_compare](go/uri_compare/main.go) |
| 11 | Encode and decode | [EncoderDecoder](java/EncoderDecoder.java) | [encoder](go/encoder/main.go) |
| 12 | Query strings | [QueryString](java/QueryString.java) | [query_string](go/query_string/main.go) |
| 13 | Proxies | [ProxyDemo](java/ProxyDemo.java) | [proxy_client](go/proxy_client/main.go) |
| 14 | Proxy selection | [LocalProxySelector](java/LocalProxySelector.java) | [proxy_selector](go/proxy_selector/main.go) |
| 15 | GET with a query | [FormGet](java/FormGet.java) | [form_get](go/form_get/main.go) |
| 16 | Password-protected site | [SecureViewer](java/SecureViewer.java) | [basic_auth](go/basic_auth/main.go) |
| 17 | Password dialog | [DialogAuthenticator](java/DialogAuthenticator.java) | none (no GUI in Go's standard library) |
| - | Test server (port 8000) | [LocalTestServer](java/LocalTestServer.java) | [testserver](go/testserver/main.go) |

Run instructions: [java/README.md](java/README.md) and [go/README.md](go/README.md).

## Must-know for the exam

- URI vs URL vs URN, and the parts of a URL.
- URL is final and immutable, and `new URL` throws `MalformedURLException`.
- `getFile()` includes the query, `getPath()` does not, and `getPort()` returns -1 when absent.
- `URL.equals()` does a DNS lookup. `sameFile()` ignores the fragment. `URI.equals()` never uses the network.
- URL can fetch; URI can only identify and manipulate.
- `URLEncoder` turns a space into `+`. Encode names and values, never the whole URL.
- The three proxy system properties, the `Proxy` class, and `ProxySelector.select` / `connectFailed`.
- `Authenticator.setDefault`, `getPasswordAuthentication`, and why passwords are `char[]`.
