import java.io.*;
import java.net.*;

// TCP client: sends lines typed by the user, prints the server's reply.
public class EchoClient {
    public static void main(String[] args) {
        String host = "localhost";
        int port = 5000;
        try (Socket socket = new Socket(host, port)) {
            System.out.println("Connected to " + host + ":" + port);

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader keyboard = new BufferedReader(
                    new InputStreamReader(System.in));

            String msg;
            while ((msg = keyboard.readLine()) != null) {
                out.println(msg);                         // send to server
                System.out.println("Server: " + in.readLine());  // wait for reply
                if (msg.equalsIgnoreCase("bye")) break;
            }
        } catch (UnknownHostException e) {
            System.out.println("Unknown host: " + host);
        } catch (IOException e) {
            System.out.println("I/O error: " + e.getMessage());
        }
    }
}
