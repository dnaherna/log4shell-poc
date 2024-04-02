package org.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

// Added --------------

import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

// --------------------

//added for accessing servlet
@WebServlet(name = "simpleServlet", value = "/simpleServlet")
public class Main extends HttpServlet{

    private static final Logger logger = LogManager.getLogger(Main.class);

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException{
        String username = req.getParameter("username");
        
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();

        logger.error("Hello" + username);
        // frontend html webpage
        out.println("<html>");
            out.println("<body>");
                out.println("<head><title>Servlet Webpage</title></head>");
                    out.println("<h1>Hello " + username + "</h1>");
            out.println("</body>");
        out.println("</html>");
    }

    public static void main(String[] args) throws ServletException, IOException {
        System.setProperty("com.sun.jndi.rmi.object.trustURLCodebase", "true");

        // doPost();
        // String username = args[0];
        // logger.error("Hello: " + username);

    }

}
