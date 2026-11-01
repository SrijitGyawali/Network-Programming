import java.io.*;
import java.net.*;

// Concurrent, connection-oriented (TCP) server: one thread per client.
public class MultiThreadedServer {
    public static void main(String[] args) {
        int port = 5001;
        try (ServerSocket server = new ServerSocket(port)) {
            System.out.println("Multithreaded server started on port " + port);
            while (true) {
                Socket client = server.accept();
                System.out.println("New client: " + client.getInetAddress());
                new Thread(new ClientHandler(client)).start();  // serve in a new thread
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}

class ClientHandler implements Runnable {
    private Socket client;

    ClientHandler(Socket client) {
        this.client = client;
    }

    public void run() {
        try {
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(client.getInputStream()));
            PrintWriter out = new PrintWriter(client.getOutputStream(), true);

            String line;
            while ((line = in.readLine()) != null) {
                System.out.println(Thread.currentThread().getName() + " got: " + line);
                out.println("Echo: " + line);
                if (line.equalsIgnoreCase("bye")) break;
            }
            client.close();
        } catch (IOException e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}
