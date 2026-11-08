# Unit 3: Go programs (job track)

The same programs as the Java folder. Go has one type, `url.URL`, for both URLs and URIs,
and fetching is done separately by `net/http`.

| Program | Java equivalent | Key Go APIs |
|---|---|---|
| `url_build` | `URLConstructors` | `url.Parse`, `url.URL{...}`, `base.Parse` |
| `protocol_tester` | `ProtocolTester` | `http.Client`, "unsupported protocol scheme" error |
| `source_viewer` | `SourceViewer` | `http.Get`, `io.Copy` |
| `content_getter` | `ContentGetter` | `Content-Type` header, `http.DetectContentType` |
| `url_split` | `URLSplitter` | `u.Hostname()`, `u.Port()`, `u.RawQuery`, `u.Query()` |
| `url_compare` | `URLEquality` | `u.String()`, a `sameFile` helper |
| `uri_build` | `URIConstructors` | `url.URL` fields, `Opaque`, `url.User` |
| `uri_parts` | `URISplitter` | `u.IsAbs()`, `u.Opaque`, `u.EscapedPath()` |
| `uri_resolve` | `URIResolver` | `ResolveReference`, `path.Clean`, a `relativize` helper |
| `uri_compare` | `URIEquality` | an `equal` helper, `strings.EqualFold` |
| `encoder` | `EncoderDecoder` | `url.QueryEscape`, `url.PathEscape`, `url.QueryUnescape` |
| `query_string` | `QueryString` | `url.Values`, `Encode`, `url.ParseQuery` |
| `proxy_client` | `ProxyDemo` | `http.ProxyFromEnvironment`, `http.ProxyURL` |
| `proxy_selector` | `LocalProxySelector` | a function assigned to `Transport.Proxy` |
| `form_get` | `FormGet` | `url.Values`, `http.Get` |
| `basic_auth` | `SecureViewer` | `req.SetBasicAuth` |
| `testserver` | `LocalTestServer` | `net/http`, `r.BasicAuth`, `r.URL.IsAbs` |

## Run

Needs Go 1.22 or newer.

```bash
cd unit-03-urls-and-uris/go
go run ./url_split https://www.tu.edu.np/about?x=1#top
go run ./uri_resolve
go run ./encoder
```

For `proxy_client`, `proxy_selector`, `form_get` and `basic_auth`, start the test server in another terminal first.
It listens on port 8000, and the Java and Go test servers can be used interchangeably.

```bash
go run ./testserver
```

```bash
go run ./proxy_client
go run ./form_get
go run ./basic_auth
```

## Things that differ from Java

- `url.Parse` only checks syntax, so an unknown scheme is accepted. Java's `new URL` rejects it.
- URL comparison is plain text with no DNS lookup. Java's `URL.equals` resolves host names.
- A 404 is not an `error` in Go, so check `resp.StatusCode`. Java's `openStream` throws an exception.
- Always `defer resp.Body.Close()`, and set a `Timeout` on the client in real code.
- `url.Values.Encode()` sorts by key, and `*` and `~` are encoded the opposite way to Java.
- There is no Authenticator callback: set the login on the request with `SetBasicAuth`.
