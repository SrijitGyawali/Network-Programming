# Unit 3: Java programs (exam track)

| Program | Syllabus | What it shows |
|---|---|---|
| `URLConstructors.java` | 3.2 | The four URL constructors, `MalformedURLException` |
| `ProtocolTester.java` | 3.2 | Which protocols this JVM has handlers for |
| `SourceViewer.java` | 3.2 | Retrieving data with `openStream()` |
| `ContentGetter.java` | 3.2 | Retrieving data with `getContent()` |
| `URLSplitter.java` | 3.2 | Every URL getter method |
| `URLEquality.java` | 3.2 | `equals`, `sameFile`, `toExternalForm`, `toURI` |
| `URIConstructors.java` | 3.3 | All URI constructors and `URI.create` |
| `URISplitter.java` | 3.3 | The parts of hierarchical, opaque and relative URIs |
| `URIResolver.java` | 3.3 | `resolve`, `relativize`, `normalize` |
| `URIEquality.java` | 3.3 | `equals`, `compareTo`, `toASCIIString` |
| `EncoderDecoder.java` | 3.4 | `URLEncoder` and `URLDecoder` |
| `QueryString.java` | 3.4 | Building an x-www-form-urlencoded query |
| `ProxyDemo.java` | 3.5 | System properties and the `Proxy` class |
| `LocalProxySelector.java` | 3.5 | A custom `ProxySelector` |
| `FormGet.java` | 3.6 | Talking to a server-side program through GET |
| `SecureViewer.java` | 3.7 | `Authenticator` and `PasswordAuthentication` |
| `DialogAuthenticator.java` | 3.7 | Asking for a password with `JPasswordField` |
| `LocalTestServer.java` | helper | Test server for sections 3.5 to 3.7 (not exam material) |

## Compile

Needs JDK 8 or newer.

```bash
cd unit-03-urls-and-uris/java
javac *.java
```

## Run

The first group works on its own. `SourceViewer` and `ContentGetter` need Internet access.

```bash
java URLSplitter https://www.tu.edu.np/about?x=1#top
java URIResolver
java EncoderDecoder
java SourceViewer http://example.com/
```

For `ProxyDemo`, `LocalProxySelector`, `FormGet`, `SecureViewer` and `DialogAuthenticator`, start the test server
in another terminal first. It listens on port 8000 and needs no Internet access.

```bash
java LocalTestServer
```

```bash
java ProxyDemo
java FormGet
java SecureViewer
java DialogAuthenticator   # login: student / network123
```
