package com.hct.dev.controller;

import java.util.List;

import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.hct.dev.service.BucketService;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;

import static com.hct.dev.service.BucketService.REPORT_BUCKET_NAME;;

@RestController
@RequiredArgsConstructor
@RequestMapping("/report")
@Slf4j
public class ReportManageController {
    private final BucketService bucketService;

    @GetMapping("")
    public List<String> list() {
        return bucketService.listDataResources(REPORT_BUCKET_NAME);
    }

    @GetMapping("/download/{fileName}")
    public ResponseEntity<InputStreamResource> download(@PathVariable String fileName) {
        ResponseInputStream<GetObjectResponse> s3is = bucketService.getDataResource(REPORT_BUCKET_NAME, fileName);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + fileName + "\"")
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(new InputStreamResource(s3is));
    }

}
