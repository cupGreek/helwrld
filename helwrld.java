import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class helwrld {
    
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        server.createContext("/", new MyHandler());
        //Thread control is given to executor service.
        server.setExecutor(java.util.concurrent.Executors.newCachedThreadPool());
        server.start();
        System.out.println("Server started.....awaiting requests");
    }
    
    // Testing Harness Trigger

    // HTTP Handler
    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange t) throws IOException {
            String response = "<HTML>";
            response += "<h1>" + "Hello World!" + "</h1>";
            long threadId = Thread.currentThread().getId();
            System.out.println("I am thread " + threadId );
            response = response + "<h2>" + " This is the thread: Thread Id = "+threadId + "</h2>";
            response += "</HTML>";
            t.sendResponseHeaders(200, response.length());
            OutputStream os = t.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
