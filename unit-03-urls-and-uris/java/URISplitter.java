import java.net.*;

// 3.3 The parts of the URI.
public class URISplitter {
    public static void main(String[] args) {
        String[] addresses = args.length > 0 ? args : new String[] {
            "https://admin@www.example.com:8443/a%20b/c.html?lang=en#top",
            "tel:+977-1-4331000",
            "docs/index.html"
        };
        for (String address : addresses) {
            try {
                URI u = new URI(address);
                System.out.println("URI: " + u);
                System.out.println("  absolute?   " + u.isAbsolute());
                System.out.println("  opaque?     " + u.isOpaque());
                System.out.println("  scheme      " + u.getScheme());
                if (u.isOpaque()) {
                    System.out.println("  specific    " + u.getSchemeSpecificPart());
                } else {
                    System.out.println("  authority   " + u.getAuthority());
                    System.out.println("  user info   " + u.getUserInfo());
                    System.out.println("  host        " + u.getHost());
                    System.out.println("  port        " + u.getPort());
                    System.out.println("  path        " + u.getPath());       // decoded
                    System.out.println("  raw path    " + u.getRawPath());    // still encoded
                    System.out.println("  query       " + u.getQuery());
                }
                System.out.println("  fragment    " + u.getFragment());
            } catch (URISyntaxException e) {
                System.out.println(address + " is not a valid URI");
            }
        }
    }
}
