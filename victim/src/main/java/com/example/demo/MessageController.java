package com.example.demo;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class MessageController {

    private static final Logger logger = LogManager.getLogger(MessageController.class);

    @GetMapping("/")
    public String homePage() {
        // thymeleaf template name for home page
        return "home";
    }

    @PostMapping("/process-message")
    public String processMessage(@RequestParam("message") String message, Model model) {
        // process the received message (e.g., log it)
        logger.info("Received message: " + message);

        // add the message to the model (for displaying on a result page)
        model.addAttribute("receivedMessage", message);

        // thymeleaf template name for displaying the result
        return "result";
    }
}
