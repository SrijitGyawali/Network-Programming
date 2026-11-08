import java.net.*;

// 3.3 Equality, comparison and string representation of URIs.
public class URIEquality {
    public static void main(String[] args) {
        try {
            URI a = new URI("HTTP://WWW.Example.COM/index.html");
            URI b = new URI("http://www.example.com/index.html");
            URI c = new URI("http://www.example.com/INDEX.html");

            // scheme and host ignore case, the path does not; no DNS lookup happens
            System.out.println("a.equals(b) : " + a.equals(b));
            System.out.println("b.equals(c) : " + b.equals(c));
            System.out.println("a.hashCode() == b.hashCode() : " + (a.hashCode() == b.hashCode()));

            // compareTo() gives an ordering, so URIs can be sorted
            System.out.println("b.compareTo(c) > 0 : " + (b.compareTo(c) > 0));

            // toString() may hold non-ASCII text, toASCIIString() never does
            URI cafe = new URI("http", "www.example.com", "/caf\u00e9", null);
            System.out.println("toASCIIString() : " + cafe.toASCIIString());
        } catch (URISyntaxException e) {
            System.out.println("Bad URI: " + e.getMessage());
        }
    }
}
