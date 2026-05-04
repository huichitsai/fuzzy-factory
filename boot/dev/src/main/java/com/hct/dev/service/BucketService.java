package com.hct.dev.service;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.esotericsoftware.minlog.Log;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.internal.resource.S3Resource;
import software.amazon.awssdk.services.s3.model.CompletedMultipartUpload;
import software.amazon.awssdk.services.s3.model.CompletedPart;
import software.amazon.awssdk.services.s3.model.CreateMultipartUploadResponse;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;
import software.amazon.awssdk.services.s3.model.ListObjectsRequest;
import software.amazon.awssdk.services.s3.model.UploadPartRequest;

@Service
@RequiredArgsConstructor
@Slf4j
public class BucketService {

    public static final String DATA_BUCKET_NAME = "data";
    public static final String REPORT_BUCKET_NAME = "reporting";
    private final S3Client s3Client;

    public boolean fileExistsInSourceBucket(String fileName) {
        ListObjectsRequest listObjectsRequest = ListObjectsRequest.builder()
                .bucket(DATA_BUCKET_NAME)
                .prefix(fileName)
                .build();
        return s3Client.listObjects(listObjectsRequest).contents().stream()
                .anyMatch(s3Object -> s3Object.key().equals(fileName));
    }

    public boolean updateDataResource(String fileName, InputStream inputStream)  {
        try {
            // Use multipart upload for large streams to avoid temp files
            CreateMultipartUploadResponse createResponse = s3Client.createMultipartUpload(b -> b.bucket(DATA_BUCKET_NAME).key(fileName));
            String uploadId = createResponse.uploadId();
            List<CompletedPart> completedParts = new ArrayList<>();

            byte[] buffer = new byte[5 * 1024 * 1024]; // 5MB minimum part size
            int bytesRead, partNumber = 1;

            while ((bytesRead = readInputStream(buffer, inputStream)) != -1) {
                UploadPartRequest partRequest = UploadPartRequest.builder()
                        .bucket(DATA_BUCKET_NAME).key(fileName).uploadId(uploadId)
                        .partNumber(partNumber).build();

                String etag = s3Client.uploadPart(partRequest, RequestBody.fromBytes(Arrays.copyOf(buffer, bytesRead))).eTag();
                completedParts.add(CompletedPart.builder().partNumber(partNumber).eTag(etag).build());
                partNumber++;
            }

            // Complete the multipart upload
            CompletedMultipartUpload completedUpload = CompletedMultipartUpload.builder().parts(completedParts).build();
            s3Client.completeMultipartUpload(b -> b.bucket(DATA_BUCKET_NAME).key(fileName).uploadId(uploadId).multipartUpload(completedUpload));
            
            return true;
        } catch (Exception e) {
            log.error("Error occurred while updating data resource", e);
            return false;
        }
    }

    private int readInputStream(byte[] buffer, InputStream inputStream) {
        try {
            return inputStream.read(buffer);
        } catch (IOException e) {
            log.error("Failed to read from input stream", e);
            throw new RuntimeException("Failed to read from input stream", e);
        }
    }

    public List<String> listDataResources(String bucketName) {
        return s3Client.listObjects(ListObjectsRequest.builder().bucket(bucketName).build())
            .contents()
            .stream()
            .map(s3Object -> s3Object.key())
            .collect(Collectors.toList());
    }

    public ResponseInputStream<GetObjectResponse> getDataResource(String bucketName, String fileName) {
        GetObjectRequest getObjectRequest = GetObjectRequest.builder()
            .bucket(bucketName)
            .key(fileName)
            .build();
        return s3Client.getObject(getObjectRequest);
    }
}
