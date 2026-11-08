import java.net.*;

// 3.3 Resolving relative URIs: resolve(), relativize() and normalize().
public class URIResolver {
    public static void main(String[] args) {
        try {
            URI base = new URI("http://www.example.com/docs/intro/index.html");

            // relative -> absolute
            System.out.println(base.resolve("chapter2.html"));
            System.out.println(base.resolve("../images/logo.png"));
            System.out.println(base.resolve("/about.html"));
            System.out.println(base.resolve(new URI("https://other.example.org/x")));

            // absolute -> relative
            URI top = new URI("http://www.example.com/docs/");
            URI page = new URI("http://www.example.com/docs/intro/chapter1.html");
            System.out.println(top.relativize(page));

            // remove . and .. from the path
            URI messy = new URI("http://www.example.com/a/./b/../c.html");
            System.out.println(messy.normalize());
        } catch (URISyntaxException e) {
            System.out.println("Bad URI: " + e.getMessage());
        }
    }
}
