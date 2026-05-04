package com.hct.dev.controller;

import java.io.IOException;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.hct.dev.service.BucketService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import static com.hct.dev.service.BucketService.DATA_BUCKET_NAME;

@RestController
@RequiredArgsConstructor
@RequestMapping("/data")
@Slf4j
public class DataManageController {

    private final BucketService bucketService;

    @GetMapping("")
    public List<String> list() {
        return bucketService.listDataResources(DATA_BUCKET_NAME);
    }

    @PutMapping("/upload/{fileName}")
    public boolean uploadData(@PathVariable String fileName, @RequestParam("file") MultipartFile content) throws IOException {
        return bucketService.updateDataResource(fileName, content.getInputStream());
    }

}
