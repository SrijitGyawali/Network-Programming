import java.net.*;

// 3.2 Creating new URLs: the URL constructors.
public class URLConstructors {
    public static void main(String[] args) {
        try {
            // 1. from one complete string
            URL u1 = new URL("http://www.example.com:8080/docs/index.html?lang=en#top");
            System.out.println("URL(spec)                    : " + u1);

            // 2. from protocol, host and file
            URL u2 = new URL("http", "www.example.com", "/docs/index.html");
            System.out.println("URL(protocol, host, file)    : " + u2);

            // 3. from protocol, host, port and file
            URL u3 = new URL("https", "www.example.com", 8443, "/docs/index.html");
            System.out.println("URL(protocol,host,port,file) : " + u3);

            // 4. relative to a base URL
            URL base = new URL("http://www.example.com/docs/intro/index.html");
            System.out.println("URL(base, chapter1.html)     : " + new URL(base, "chapter1.html"));
            System.out.println("URL(base, ../img/logo.png)   : " + new URL(base, "../img/logo.png"));
            System.out.println("URL(base, /about.html)       : " + new URL(base, "/about.html"));

            // an unknown protocol throws MalformedURLException
            URL bad = new URL("htp://www.example.com/");
            System.out.println("Never printed: " + bad);
        } catch (MalformedURLException e) {
            System.out.println("Malformed URL: " + e.getMessage());
        }
    }
}
