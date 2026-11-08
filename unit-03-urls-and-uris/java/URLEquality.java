import java.net.*;

// 3.2 Equality, comparison and conversion of URLs.
public class URLEquality {
    public static void main(String[] args) {
        try {
            URL a = new URL("http://localhost/index.html");
            URL b = new URL("http://127.0.0.1/index.html");
            URL c = new URL("http://www.example.com/page.html#first");
            URL d = new URL("http://www.example.com/page.html#second");

            // equals() resolves host names, so this is a blocking DNS operation
            System.out.println("localhost equals 127.0.0.1 : " + a.equals(b));

            // the fragment counts for equals() but not for sameFile()
            System.out.println("c.equals(d)                : " + c.equals(d));
            System.out.println("c.sameFile(d)              : " + c.sameFile(d));

            // conversion
            System.out.println("toString()                 : " + c.toString());
            System.out.println("toExternalForm()           : " + c.toExternalForm());
            URI uri = c.toURI();
            System.out.println("toURI()                    : " + uri);
        } catch (MalformedURLException e) {
            System.out.println("Malformed URL: " + e.getMessage());
        } catch (URISyntaxException e) {
            System.out.println("Cannot convert to URI: " + e.getMessage());
        }
    }
}
