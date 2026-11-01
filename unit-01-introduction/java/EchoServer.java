import java.io.*;
import java.net.*;

// Iterative, connection-oriented (TCP) server: handles ONE client at a time.
public class EchoServer {
    public static void main(String[] args) {
        int port = 5000;
        try (ServerSocket server = new ServerSocket(port)) {
            System.out.println("Server started on port " + port);
            while (true) {
                Socket client = server.accept();          // blocks until a client connects
                System.out.println("Client connected: " + client.getInetAddress());

                BufferedReader in = new BufferedReader(
                        new InputStreamReader(client.getInputStream()));
                PrintWriter out = new PrintWriter(client.getOutputStream(), true);

                String line;
                while ((line = in.readLine()) != null) {  // null = client closed connection
                    System.out.println("Received: " + line);
                    out.println("Echo: " + line);
                    if (line.equalsIgnoreCase("bye")) break;
                }
                client.close();
                System.out.println("Client disconnected");
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}
