import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

// 2.5 Faster log processing: DNS lookups run in a thread pool, output keeps file order.
public class PooledWeblog {
    public static void main(String[] args) {
        String file = args.length > 0 ? args[0] : "access.log";
        ExecutorService pool = Executors.newFixedThreadPool(4);
        List<Future<String>> results = new ArrayList<>();

        try (BufferedReader in = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = in.readLine()) != null) {
                results.add(pool.submit(new LookupTask(line)));   // lookups run in parallel
            }
        } catch (IOException e) {
            System.out.println("Could not read " + file + ": " + e.getMessage());
        }

        for (Future<String> result : results) {                // print in original order
            try {
                System.out.println(result.get());              // waits for that lookup
            } catch (InterruptedException | ExecutionException e) {
                System.out.println("Lookup failed: " + e.getMessage());
            }
        }
        pool.shutdown();
    }
}

class LookupTask implements Callable<String> {
    private String line;

    LookupTask(String line) {
        this.line = line;
    }

    public String call() {
        int index = line.indexOf(' ');
        String ip = line.substring(0, index);
        try {
            return InetAddress.getByName(ip).getHostName() + line.substring(index);
        } catch (UnknownHostException e) {
            return line;
        }
    }
}
