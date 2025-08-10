import mimetypes
import os
import boto3
from fastapi import UploadFile
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, CLOUDFRONT_URL

# Replace this with your actual S3 bucket name

# CLOUDFRONT_URL = "https://dhfeh4cz70vvz.cloudfront.net"
# BUCKET_NAME = "notes-files-cc"

# Create a boto3 S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def get_content_type(filename: str) -> str:
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"

def upload_to_s3(file: UploadFile, key: str):
    # content_type = file.content_type or "application/octet-stream"
    content_type = get_content_type(file.filename)

    print(content_type)

#     """
#     Uploads a file to AWS S3 and returns the public file URL.
#     :param file: FastAPI UploadFile object
#     :param key: S3 object key (e.g. 'user-id/filename.ext')
#     :return: Public URL of uploaded file
#     """
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, key, ExtraArgs={
                "ContentType": content_type,
                "ContentDisposition": "inline"  # show in browser
            })
        return f"{CLOUDFRONT_URL}/{key}"
    except Exception as e:
        raise RuntimeError(f"Upload failed: {str(e)}")


# def upload_to_s3(file: UploadFile, key: str):
#     s3.upload_fileobj(file.file, BUCKET_NAME, key, ExtraArgs={"ACL": "public-read"})
#     return f"{CLOUDFRONT_URL}/{key}"