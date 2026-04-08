import boto3

s3 = boto3.client('s3')

bucket_name = "universal-file-reader-keerthana"

def download_file(file_key, local_file_name):
    try:
        s3.download_file(bucket_name, file_key, local_file_name)
        print(f"✅ Downloaded {file_key} from S3 as {local_file_name}")
    except Exception as e:
        print("❌ Error:", e)


# Example usage
download_file("raw/data.txt", "data.txt")
