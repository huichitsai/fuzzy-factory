package com.hct.dev.controller;

import java.io.IOException;

import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import lombok.extern.slf4j.Slf4j;

@RestController
@RequestMapping("/job")
@Slf4j
public class SparkJobController {

    @Value("${spark.master:spark://localhost:7077}")
    private String sparkMasterUrl;

    @Value("${spark.docker.enabled:true}")
    private boolean dockerEnabled;

    public String submitJob() throws IOException, InterruptedException { 
        log.info("Submitting Spark job to remote Docker cluster at: {}", sparkMasterUrl);
        
        SparkSession.Builder builder = SparkSession.builder()
            .appName("My Spark Job")
            .master(sparkMasterUrl);
        
        // Configure for remote Docker deployment
        if (dockerEnabled) {
            builder.config("spark.submit.deployMode", "client")
                   .config("spark.driver.host", getDriverHost())
                   .config("spark.eventLog.enabled", "true")
                   .config("spark.eventLog.dir", "/tmp/spark-events");
        }
        
        SparkSession spark = builder.getOrCreate();

        try {
            // Example Spark job: count lines in a file
            long lineCount = spark.read().textFile("s3://data/my-input-file.txt").count();
            log.info("Line count: {}", lineCount);
            
            return "Remote job completed with line count: " + lineCount;
        } finally {
            spark.stop();
        }
    }

    private String getDriverHost() {
        try {
            return java.net.InetAddress.getLocalHost().getHostAddress();
        } catch (Exception e) {
            log.warn("Failed to determine driver host, using localhost");
            return "localhost";
        }
    }
}
