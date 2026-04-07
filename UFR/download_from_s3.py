import boto3

# Create S3 client
s3 = boto3.client('s3')

bucket_name = "universal-file-reader-keerthana"

def download_file():
    s3_key = "raw/standard_spt_datasheet.pdf"   # change this
    local_file = "downloaded.pdf"

    try:
        s3.download_file(bucket_name, s3_key, local_file)
        print("✅ File downloaded successfully!")
    except Exception as e:
        print("❌ Error:", e)

download_file()
