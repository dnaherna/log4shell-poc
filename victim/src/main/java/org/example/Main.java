package org.example;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Main {

    private static final Logger logger = LogManager.getLogger(Main.class);

    public static void main(String[] args) {
        System.setProperty("com.sun.jndi.rmi.object.trustURLCodebase", "true");

        String username = args[0];
        logger.error("Hello: " + username);
    }
}
