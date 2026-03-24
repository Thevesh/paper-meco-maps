"""Helper module for file operations, data processing, and S3 interactions."""

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import List

import boto3
from boto3.s3.transfer import TransferConfig
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


def upload_s3(bucket_name=None, source_file_name=None, cloud_file_name=None):
    """Upload a file to S3 bucket.

    Args:
        bucket_name (str): Name of the S3 bucket
        source_file_name (str): Path to the source file
        cloud_file_name (str): Name to use in the cloud

    Returns:
        str: Status message indicating success or failure
    """
    if not cloud_file_name:
        cloud_file_name = source_file_name
    try:
        time_start = time.time()
        s3 = boto3.client(
            "s3",
            aws_access_key_id=TOKEN_API_S3[0],
            aws_secret_access_key=TOKEN_API_S3[1],
        )
        s3.upload_file(source_file_name, bucket_name, cloud_file_name)
        duration = f"{time.time() - time_start:.1f} seconds"
        return f"SUCCESS ({duration}): {bucket_name}/{cloud_file_name}"
    except boto3.exceptions.S3UploadFailedError as e:
        return f"FAILURE: {source_file_name}\n\n{e}"


@lru_cache(maxsize=1)
def get_s3_client():
    """Create and cache a single S3 client instance."""
    return boto3.client(
        "s3",
        aws_access_key_id=TOKEN_API_S3[0],
        aws_secret_access_key=TOKEN_API_S3[1],
    )


def get_transfer_config():
    """Get optimized transfer configuration."""
    return TransferConfig(
        multipart_threshold=1024 * 25,  # 25 MB
        max_concurrency=10,
        multipart_chunksize=1024 * 25,  # 25 MB
        use_threads=True,
    )


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
        s3 = get_s3_client()
        config = get_transfer_config()

        s3.upload_file(source_file_name, bucket_name, cloud_file_name, Config=config)

        duration = f"{time.time() - time_start:.1f} seconds"
        message = f"SUCCESS ({duration}): {bucket_name}/{cloud_file_name}"
        return source_file_name, True, message
    except Exception as e:  # Catch all S3-related exceptions
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
            executor.submit(upload_s3_single, bucket_name, source_file, cloud_file): source_file
            for source_file, cloud_file in files_to_upload
        }

        for future in as_completed(future_to_file):
            source_file = future_to_file[future]
            source_file_name, success, message = future.result()
            results[source_file_name] = (success, message)
            print(message)

    # More efficient failed uploads extraction
    failed_uploads = [
        (source_file, message) for source_file, (success, message) in results.items() if not success
    ]
    return failed_uploads


def get_states(my: int = 0, codes: int = 0) -> List[str]:
    """Get list of Malaysian states.

    Args:
        my (int): Whether to include Malaysia (country)
        code (int): Whether to return full name (0), text code (1), or integer code (2)
    Returns:
        List[str]: List of states as full name, text codes, or integer codes
    """
    data = {
        "Malaysia": ["MYS", 0],
        "Perlis": ["PLS", 1],
        "Kedah": ["KDH", 2],
        "Kelantan": ["KTN", 3],
        "Terengganu": ["TRG", 4],
        "Pulau Pinang": ["PNG", 5],
        "Perak": ["PRK", 6],
        "Pahang": ["PHG", 7],
        "Selangor": ["SGR", 8],
        "W.P. Kuala Lumpur": ["KUL", 9],
        "W.P. Putrajaya": ["PJY", 10],
        "Negeri Sembilan": ["NSN", 11],
        "Melaka": ["MLK", 12],
        "Johor": ["JHR", 13],
        "W.P. Labuan": ["LBN", 14],
        "Sabah": ["SBH", 15],
        "Sarawak": ["SWK", 16],
    }
    state_names = list(data.keys())
    state_codes = [data[x][0] for x in state_names]
    state_order = [data[x][1] for x in state_names]
    if codes == 0:
        return state_names[1 - my :]
    if codes == 1:
        return state_codes[1 - my :]
    if codes == 2:
        return state_order[1 - my :]
    raise ValueError("Invalid code type")
