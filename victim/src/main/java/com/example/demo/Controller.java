package com.example.demo;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Controller {

    private static final Logger logger = LogManager.getLogger(Controller.class);

    // retrieve from the local directory
    @GetMapping("/")
    public String index() {
        return "<h1>Greetings from Spring Boot!</h1>" +
                "<form action='/' method='post'>" +
                "<textarea name='message' rows='4' cols='50'></textarea><br><br>" +
                "<input type='submit' value='Submit'>" +
                "</form>";
    }

    // add this to read the posting from the form
    @PostMapping("/")
    @ResponseBody
    public String handleMessage(@RequestBody String body) throws Exception {
        String encodedMessage = body.substring(8);
        String message = URLDecoder.decode(encodedMessage, StandardCharsets.UTF_8.name());
        logger.info("Message: " + message);

        return "Message received from POST: " + message + "<br>" +
                "<form action='/' method='get'>" +
                "<input type='submit' value='Go back'>" +
                "</form>";
    }
}
