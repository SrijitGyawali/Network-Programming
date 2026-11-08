import java.net.*;

// 3.2 Splitting a URL into pieces with the getter methods.
public class URLSplitter {
    public static void main(String[] args) {
        String address = args.length > 0 ? args[0]
                : "https://admin@www.example.com:8443/docs/guide.html?lang=en&v=2#intro";
        try {
            URL u = new URL(address);
            System.out.println("URL          : " + u);
            System.out.println("Protocol     : " + u.getProtocol());
            System.out.println("User info    : " + u.getUserInfo());
            System.out.println("Host         : " + u.getHost());
            System.out.println("Port         : " + u.getPort());          // -1 if not in the URL
            System.out.println("Default port : " + u.getDefaultPort());
            System.out.println("Authority    : " + u.getAuthority());
            System.out.println("File         : " + u.getFile());          // path + query
            System.out.println("Path         : " + u.getPath());
            System.out.println("Query        : " + u.getQuery());
            System.out.println("Ref          : " + u.getRef());           // the #fragment
        } catch (MalformedURLException e) {
            System.out.println(address + " is not a valid URL");
        }
    }
}
