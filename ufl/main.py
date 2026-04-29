import os
import boto3
import paramiko

from config.config import Config
from pipeline.processor import process
from azure.storage.blob import BlobServiceClient

# 🔷 FILTER LOGIC
def should_process(file):

    filter_cfg = Config.PROCESSING["filter"]

    if filter_cfg["type"] == "all":
        return True

    elif filter_cfg["type"] == "single":
        return file == filter_cfg["value"]

    elif filter_cfg["type"] == "extension":
        return file.endswith(filter_cfg["value"])

    return False


def run_local():

    input_dir = Config.INPUT["local"]["dir"]

    files = os.listdir(input_dir)

    for file in files:

        if not should_process(file):
            continue

        full_path = os.path.join(input_dir, file)

        try:
            print(f"Processing local file: {file}")

            outputs = process(full_path)   # ✅ SINGLE FILE

            for output in outputs:
                if "status" in output and output["status"] == "failed":
                    print(f"Failed: {output['file']}")
                

        except Exception as e:
            print(f"Error processing {file}: {e}")


# 🔷 S3 PROCESSING
def run_s3():

    s3_cfg = Config.INPUT["s3"]

    s3 = boto3.client("s3", region_name=s3_cfg["region"])

    response = s3.list_objects_v2(
        Bucket=s3_cfg["bucket"],
        Prefix=s3_cfg["prefix"]
    )

    if "Contents" not in response:
        print("No files found in S3")
        return

    for obj in response["Contents"]:

        key = obj["Key"]

        if key.endswith("/"):
            continue

        filename = os.path.basename(key)

        if not should_process(filename):
            continue

        try:
            print(f"Processing S3 file: {key}")
            outputs = process(key)

            for output in outputs:
                if "status" in output and output["status"] == "failed":
                    print(f"Failed: {output['file']}")
                

        except Exception as e:
            print(f"Error processing {key}: {e}")


# 🔷 SFTP PROCESSING
def run_sftp():

    sftp_cfg = Config.INPUT["sftp"]

    transport = paramiko.Transport((sftp_cfg["host"], sftp_cfg["port"]))
    transport.connect(
        username=sftp_cfg["user"],
        password=sftp_cfg["pass"]
    )

    sftp = paramiko.SFTPClient.from_transport(transport)

    remote_dir = sftp_cfg["remote_dir"]

    files = sftp.listdir(remote_dir)

    for file in files:

        if not should_process(file):
            continue

        remote_path = remote_dir + file

        try:
            print(f"Processing SFTP file: {remote_path}")

            outputs = process(remote_path)   # ✅ CORRECT

            for output in outputs:
                if "status" in output and output["status"] == "failed":
                    print(f"Failed: {output['file']}")
                

        except Exception as e:
            print(f"Error processing {file}: {e}")

    sftp.close()
    transport.close()

def run_azure():

    azure_cfg = Config.INPUT["azure"]

    blob_service = BlobServiceClient.from_connection_string(
        azure_cfg["connection_string"]
    )

    container_client = blob_service.get_container_client(
        azure_cfg["container"]
    )

    blobs = container_client.list_blobs()

    for blob in blobs:

        filename = os.path.basename(blob.name)

        if not should_process(filename):
            continue

        try:
            print(f"Processing Azure blob: {blob.name}")

            outputs = process(blob.name)

            for output in outputs:
                if "status" in output and output["status"] == "failed":
                    print(f"Failed: {output['file']}")

        except Exception as e:
            print(f"Error processing {blob.name}: {e}")

# 🔷 MAIN RUNNER
def run():

    source = Config.INPUT["source"]

    print(f"Running pipeline with INPUT_SOURCE={source}")

    if source == "local":
        run_local()

    elif source == "s3":
        run_s3()

    elif source == "sftp":
        run_sftp()
        
    elif source == "azure":
        run_azure()

    else:
        print("Unsupported INPUT_SOURCE")


if __name__ == "__main__":
    run()





