import java.net.*;

// UDP client: sends one datagram and waits for the reply.
public class UDPClient {
    public static void main(String[] args) {
        try (DatagramSocket socket = new DatagramSocket()) {
            InetAddress server = InetAddress.getByName("localhost");
            int port = 5002;

            byte[] data = "Hello UDP".getBytes();
            DatagramPacket request = new DatagramPacket(data, data.length, server, port);
            socket.send(request);

            byte[] buffer = new byte[1024];
            DatagramPacket response = new DatagramPacket(buffer, buffer.length);
            socket.setSoTimeout(3000);                    // UDP may lose packets: don't wait forever
            socket.receive(response);
            System.out.println("Server: " + new String(response.getData(), 0, response.getLength()));
        } catch (SocketTimeoutException e) {
            System.out.println("No reply (packet lost?)");
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
