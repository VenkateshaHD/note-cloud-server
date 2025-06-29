import boto3
from fastapi import UploadFile
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Replace this with your actual S3 bucket name
BUCKET_NAME = "your-bucket-name"

# Create a boto3 S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(file: UploadFile, key: str):
    """
    Uploads a file to AWS S3 and returns the public file URL.
    :param file: FastAPI UploadFile object
    :param key: S3 object key (e.g. 'user-id/filename.ext')
    :return: Public URL of uploaded file
    """
    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, key, ExtraArgs={"ACL": "public-read"})
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
    except Exception as e:
        raise RuntimeError(f"Upload failed: {str(e)}")
