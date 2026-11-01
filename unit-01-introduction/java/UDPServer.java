import java.net.*;

// Iterative, connectionless (UDP) server: replies to each datagram.
public class UDPServer {
    public static void main(String[] args) {
        int port = 5002;
        try (DatagramSocket socket = new DatagramSocket(port)) {
            System.out.println("UDP server started on port " + port);
            byte[] buffer = new byte[1024];
            while (true) {
                DatagramPacket request = new DatagramPacket(buffer, buffer.length);
                socket.receive(request);                  // blocks until a datagram arrives
                String msg = new String(request.getData(), 0, request.getLength());
                System.out.println("Received: " + msg);

                byte[] reply = ("Echo: " + msg).getBytes();
                DatagramPacket response = new DatagramPacket(reply, reply.length,
                        request.getAddress(), request.getPort());  // send back to sender
                socket.send(response);
            }
        } catch (Exception e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}
