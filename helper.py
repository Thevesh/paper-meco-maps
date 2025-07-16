"""Helper module for file operations, data processing, and S3 interactions."""

import os
import re
import time
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# S3 configuration
s3_bucket = os.getenv("S3_BUCKET")
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

TOKEN_API_S3 = (os.getenv("S3_KEY"), os.getenv("S3_SECRET"))


def generate_slug(x):
    """Generate URL-friendly slug from string.
    
    Args:
        x (str): Input string
        
    Returns:
        str: URL-friendly slug
    """
    slug = re.sub(r"[^a-zA-Z0-9\s]", "", x)
    slug = slug.replace(" ", "-").lower()
    return slug


def upload_s3_single(bucket_name, source_file_name, cloud_file_name):
    """Upload a single file to S3.
    
    Args:
        bucket_name (str): Name of the S3 bucket
        source_file_name (str): Path to the source file
        cloud_file_name (str): Name to use in the cloud
        
    Returns:
        tuple: (source_file_name, success, message)
    """
    try:
        time_start = time.time()
        s3 = boto3.client(
            "s3",
            aws_access_key_id=TOKEN_API_S3[0],
            aws_secret_access_key=TOKEN_API_S3[1],
        )
        s3.upload_file(source_file_name, bucket_name, cloud_file_name)
        duration = f"{time.time() - time_start:.1f} seconds"
        message = f"SUCCESS ({duration}): {bucket_name}/{cloud_file_name}"
        return source_file_name, True, message
    except boto3.exceptions.S3UploadFailedError as e:
        message = f"FAILURE: {bucket_name}/{source_file_name}\n\n{e}"
        return source_file_name, False, message


def upload_s3_bulk(bucket_name, files_to_upload, max_workers=50):
    """Upload multiple files to S3 in parallel.
    
    Args:
        bucket_name (str): S3 bucket name
        files_to_upload (list): List of tuples (source_file_name, cloud_file_name)
        max_workers (int): Number of concurrent uploads
        
    Returns:
        list: List of tuples containing failed uploads (source_file, error_message)
    """
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(upload_s3_single, bucket_name, source_file, cloud_file): (
                source_file,
                cloud_file,
            )
            for source_file, cloud_file in files_to_upload
        }

        for future in as_completed(future_to_file):
            source_file, cloud_file = future_to_file[future]
            source_file_name, success, message = future.result()
            results[source_file_name] = (success, message)
            print(message)

    failed_uploads = [
        (source_file, message.split(": ", 1)[1][9:])
        for source_file, (success, message) in results.items()
        if not success
    ]
    return failed_uploads
