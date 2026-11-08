import java.io.*;
import java.net.*;
import java.util.*;

// 3.5 The ProxySelector class: choose a proxy for each URI.
// Start LocalTestServer first: it also behaves as an HTTP proxy on port 8000.
public class LocalProxySelector extends ProxySelector {
    private List<URI> failed = new ArrayList<>();
    private Proxy proxy = new Proxy(Proxy.Type.HTTP, new InetSocketAddress("localhost", 8000));

    public List<Proxy> select(URI uri) {
        List<Proxy> result = new ArrayList<>();
        if (failed.contains(uri) || !"http".equalsIgnoreCase(uri.getScheme())
                || uri.getHost().endsWith(".intranet.example.com")) {
            result.add(Proxy.NO_PROXY);       // go direct
        } else {
            result.add(proxy);
        }
        return result;
    }

    public void connectFailed(URI uri, SocketAddress address, IOException e) {
        failed.add(uri);                      // do not use the proxy for this URI again
    }

    public static void main(String[] args) throws IOException {
        LocalProxySelector selector = new LocalProxySelector();
        ProxySelector.setDefault(selector);   // every URL in this JVM now asks the selector

        String[] tests = {"http://www.example.com/", "https://www.example.com/",
                          "http://wiki.intranet.example.com/"};
        for (String test : tests) {
            System.out.println(test + " -> " + selector.select(URI.create(test)));
        }

        URL u = new URL("http://www.example.com/page.html");
        try (BufferedReader in = new BufferedReader(new InputStreamReader(u.openStream()))) {
            System.out.println(in.readLine());
        }
    }
}
