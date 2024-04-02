package com.example.demo;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {

    private static final Logger logger = LogManager.getLogger(Controller.class);

    @GetMapping("/")
    public String index() {
        logger.error("get: index");
        return "Greetings from Spring Boot!";
    }
}
