import boto3

# Create S3 client
s3 = boto3.client('s3')

bucket_name = "universal-file-reader-keerthana"

def upload_file():
    file_path = "downloaded.pdf"   # local file
    s3_key = "raw/downloaded.pdf"  # where it goes in S3

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print("✅ File uploaded successfully to S3!")
    except Exception as e:
        print("❌ Error:", e)

upload_file()
