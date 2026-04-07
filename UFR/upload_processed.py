import boto3

s3 = boto3.client('s3')

bucket_name = "universal-file-reader-keerthana"

def upload_processed():
    file_path = "output.json"   # file from your friend
    s3_key = "processed/output.json"

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(" Processed file uploaded successfully!")
    except Exception as e:
        print("❌ Error:", e)

upload_processed()
