import com.sun.net.httpserver.*;
import java.io.*;
import java.net.*;
import java.util.*;

// A small server on port 8000 for trying out the programs in sections 3.5 - 3.7.
//   /search?q=...  echoes the decoded query parameters
//   /secret        needs HTTP Basic login: student / network123
//   any absolute-URI request is answered as if this server were an HTTP proxy
public class LocalTestServer {
    private static final String LOGIN = "student:network123";

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", LocalTestServer::root);
        server.createContext("/search", LocalTestServer::search);
        server.createContext("/secret", LocalTestServer::secret);
        server.start();
        System.out.println("LocalTestServer running on http://localhost:8000/");
    }

    private static void root(HttpExchange ex) throws IOException {
        URI uri = ex.getRequestURI();
        if (uri.isAbsolute()) {
            send(ex, 200, "Answered by the proxy for " + uri + "\n");
        } else {
            send(ex, 200, "Hello from LocalTestServer, you asked for " + uri + "\n");
        }
    }

    private static void search(HttpExchange ex) throws IOException {
        StringBuilder reply = new StringBuilder("Search received:\n");
        String query = ex.getRequestURI().getRawQuery();
        if (query != null) {
            for (String pair : query.split("&")) {
                String[] parts = pair.split("=", 2);
                reply.append("  ").append(URLDecoder.decode(parts[0], "UTF-8")).append(" = ")
                     .append(parts.length > 1 ? URLDecoder.decode(parts[1], "UTF-8") : "")
                     .append("\n");
            }
        }
        send(ex, 200, reply.toString());
    }

    private static void secret(HttpExchange ex) throws IOException {
        String expected = "Basic " + Base64.getEncoder().encodeToString(LOGIN.getBytes("UTF-8"));
        if (expected.equals(ex.getRequestHeaders().getFirst("Authorization"))) {
            send(ex, 200, "Welcome! This page is password protected.\n");
        } else {
            ex.getResponseHeaders().set("WWW-Authenticate", "Basic realm=\"Network Programming\"");
            send(ex, 401, "Login required\n");
        }
    }

    private static void send(HttpExchange ex, int status, String body) throws IOException {
        byte[] bytes = body.getBytes("UTF-8");
        ex.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        ex.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = ex.getResponseBody()) {
            out.write(bytes);
        }
    }
}
