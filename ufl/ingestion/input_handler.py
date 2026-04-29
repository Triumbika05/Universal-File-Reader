import os
import boto3
import paramiko
from config.config import Config
from azure.storage.blob import BlobServiceClient

def fetch_input(input_value):

    source = Config.INPUT["source"]

    if source == "local":
        return input_value   # ✅ STRING ONLY

    elif source == "s3":
        return fetch_s3(input_value)

    elif source == "sftp":
        return fetch_sftp(input_value)
    
    elif source == "azure":
        return fetch_azure(input_value)
    else:
        raise Exception("Unsupported input")


# ---------------- S3 ----------------
def fetch_s3(key):

    s3_cfg = Config.INPUT["s3"]

    s3 = boto3.client("s3", region_name=s3_cfg["region"])

    os.makedirs(Config.TEMP_DIR, exist_ok=True)

    local_path = os.path.join(Config.TEMP_DIR, os.path.basename(key))

    s3.download_file(s3_cfg["bucket"], key, local_path)

    return local_path


# ---------------- SFTP ----------------
def fetch_sftp(remote_path):

    sftp_cfg = Config.INPUT["sftp"]

    transport = paramiko.Transport((sftp_cfg["host"], sftp_cfg["port"]))
    transport.connect(
        username=sftp_cfg["user"],
        password=sftp_cfg["pass"]
    )

    sftp = paramiko.SFTPClient.from_transport(transport)

    os.makedirs(Config.TEMP_DIR, exist_ok=True)

    local_path = os.path.join(Config.TEMP_DIR, os.path.basename(remote_path))

    sftp.get(remote_path, local_path)

    sftp.close()
    transport.close()

    return local_path

def fetch_azure(blob_name):

    azure_cfg = Config.INPUT["azure"]

    blob_service = BlobServiceClient.from_connection_string(
        azure_cfg["connection_string"]
    )

    container_client = blob_service.get_container_client(
        azure_cfg["container"]
    )

    os.makedirs(Config.TEMP_DIR, exist_ok=True)

    local_path = os.path.join(Config.TEMP_DIR, os.path.basename(blob_name))

    with open(local_path, "wb") as f:
        data = container_client.download_blob(blob_name)
        f.write(data.readall())

    return local_path