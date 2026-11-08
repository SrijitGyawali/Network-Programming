import java.io.*;
import java.net.*;

// 3.5 Proxies: system properties and the Proxy class.
// Start LocalTestServer first: it also behaves as an HTTP proxy on port 8000.
public class ProxyDemo {
    public static void main(String[] args) {
        try {
            URL u = new URL("http://www.example.com/page.html");

            // 1. system properties: apply to every connection in this JVM
            System.setProperty("http.proxyHost", "localhost");
            System.setProperty("http.proxyPort", "8000");
            System.setProperty("http.nonProxyHosts", "*.intranet.example.com");
            System.out.println("System properties: " + firstLine(u.openConnection()));
            System.clearProperty("http.proxyHost");
            System.clearProperty("http.proxyPort");
            System.clearProperty("http.nonProxyHosts");

            // 2. the Proxy class: applies to this one connection only
            SocketAddress address = new InetSocketAddress("localhost", 8000);
            Proxy proxy = new Proxy(Proxy.Type.HTTP, address);
            System.out.println("Proxy object: " + proxy);
            System.out.println("Proxy class: " + firstLine(u.openConnection(proxy)));

            // 3. Proxy.NO_PROXY: go directly, ignoring any proxy settings
            System.out.println("Proxy type of NO_PROXY: " + Proxy.NO_PROXY.type());
        } catch (IOException e) {
            System.out.println("Error (is LocalTestServer running?): " + e);
        }
    }

    private static String firstLine(URLConnection connection) throws IOException {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(connection.getInputStream()))) {
            return in.readLine();
        }
    }
}
