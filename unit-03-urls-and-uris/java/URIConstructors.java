import java.net.*;

// 3.3 Constructing a URI.
public class URIConstructors {
    public static void main(String[] args) {
        try {
            // from one string
            System.out.println(new URI("http://www.example.com/docs/index.html?lang=en#top"));

            // scheme, scheme-specific part, fragment
            System.out.println(new URI("tel", "+977-1-4331000", null));

            // scheme, host, path, fragment: illegal characters are escaped for you
            System.out.println(new URI("http", "www.example.com", "/a b/c.html", "top"));

            // scheme, authority, path, query, fragment
            System.out.println(new URI("http", "www.example.com:8080", "/docs", "lang=en", "top"));

            // scheme, userInfo, host, port, path, query, fragment
            System.out.println(new URI("https", "admin", "www.example.com", 8443,
                                       "/docs", "lang=en", "top"));

            // URI.create() throws an unchecked exception instead
            System.out.println(URI.create("urn:isbn:9781449357672"));

            // a URI need not be absolute, and the scheme need not be known to Java
            System.out.println(new URI("docs/index.html"));
            System.out.println(new URI("myscheme://anything/at/all"));

            // the one-string constructor does not escape: a space is illegal
            System.out.println(new URI("http://www.example.com/a b"));
        } catch (URISyntaxException e) {
            System.out.println("Bad URI: " + e.getMessage());
        }
    }
}
