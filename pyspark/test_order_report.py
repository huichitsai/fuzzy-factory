import unittest
from unittest.mock import patch, MagicMock
from order_report import read_s3_file


class TestOrderReport(unittest.TestCase):
    
    @patch.dict('os.environ', {
        'AWS_ACCESS_KEY_ID': 'test-access-key',
        'AWS_SECRET_ACCESS_KEY': 'test-secret-key',
        'AWS_DEFAULT_REGION': 'us-east-1',
        'AWS_S3_ENDPOINT_URL': 'http://localhost:9000'
    })
    @patch('order_report.boto3')
    def test_read_s3_file_orders_csv(self, mock_boto3):
        """Test reading orders.csv from s3://data/orders.csv"""
        # Arrange
        bucket_name = "data"
        file_key = "orders.csv"
        expected_content = "order_id,customer,amount\n1,John,100\n2,Jane,200"
        
        # Mock the S3 client
        mock_s3_client = MagicMock()
        mock_boto3.client.return_value = mock_s3_client
        mock_s3_client.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=expected_content.encode('utf-8')))
        }
        
        # Act
        result = read_s3_file(bucket_name, file_key)
        
        # Assert
        self.assertEqual(result, expected_content)
        mock_boto3.client.assert_called_once_with(
            's3',
            aws_access_key_id='test-access-key',
            aws_secret_access_key='test-secret-key',
            region_name='us-east-1',
            endpoint_url='http://localhost:9000'
        )
        mock_s3_client.get_object.assert_called_once_with(Bucket=bucket_name, Key=file_key)
    
    @patch.dict('os.environ', {
        'AWS_ACCESS_KEY_ID': 'test-access-key',
        'AWS_SECRET_ACCESS_KEY': 'test-secret-key',
        'AWS_DEFAULT_REGION': 'us-west-2'
    })
    @patch('order_report.boto3')
    def test_read_s3_file_with_special_characters(self, mock_boto3):
        """Test reading S3 file with special characters"""
        # Arrange
        bucket_name = "data"
        file_key = "orders.csv"
        expected_content = "order_id,customer,amount\n1,José García,100.50\n2,李名,200.75"
        
        # Mock the S3 client
        mock_s3_client = MagicMock()
        mock_boto3.client.return_value = mock_s3_client
        mock_s3_client.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=expected_content.encode('utf-8')))
        }
        
        # Act
        result = read_s3_file(bucket_name, file_key)
        
        # Assert
        self.assertEqual(result, expected_content)


if __name__ == '__main__':
    unittest.main()
