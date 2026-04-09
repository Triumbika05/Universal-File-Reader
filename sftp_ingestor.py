import paramiko
import boto3
from config import BUCKET_NAME, RAW_PREFIX, REGION

s3 = boto3.client('s3', region_name=REGION)

def fetch_from_sftp():
    host = "localhost"
    port = 22
    username = "triumbika"   # change if needed
    password = "1105"

    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    # IMPORTANT: use forward slashes
    sftp.chdir("C:\sftp-files")

    files = sftp.listdir()

    for file in files:
        local_path = f"./temp_{file}"

        print(f"Downloading {file}...")
        sftp.get(file, local_path)

        print(f"Uploading {file} to S3...")
        s3.upload_file(local_path, BUCKET_NAME, f"{RAW_PREFIX}{file}")

    sftp.close()
    print("SFTP ingestion complete!")

if __name__ == "__main__":
    fetch_from_sftp()