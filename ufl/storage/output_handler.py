import os
import json
import boto3
from config.config import Config
from azure.storage.blob import BlobServiceClient

def save_output(result):

    # ✅ safety checks
    if not isinstance(result, dict):
        print("Invalid result format")
        return

    if "file" not in result or "schema" not in result:
        print("Skipping invalid result")
        return

    file_name = os.path.basename(result["file"]) + ".json"

    if Config.OUTPUT["target"] == "local":

        # ✅ FIXED HERE
        output_dir = Config.OUTPUT["local"]["dir"]

        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, file_name)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"Saved: {output_path}")

    elif Config.OUTPUT["target"] == "s3":

        s3_cfg = Config.OUTPUT["s3"]

        s3 = boto3.client("s3", region_name=s3_cfg["region"])

        key = s3_cfg["prefix"] + file_name

        s3.put_object(
            Bucket=s3_cfg["bucket"],
            Key=key,
            Body=json.dumps(result)
        )

        print(f"Uploaded to S3: {key}")
    
    elif Config.OUTPUT["target"] == "azure":

        azure_cfg = Config.OUTPUT["azure"]

        blob_service = BlobServiceClient.from_connection_string(
        azure_cfg["connection_string"]
        )

        container_client = blob_service.get_container_client(
        azure_cfg["container"]
        )

        blob_name = os.path.basename(result["file"]) + ".json"

        container_client.upload_blob(
           name=blob_name,
           data=json.dumps(result),
           overwrite=True
        )

        print(f"Uploaded to Azure Blob: {blob_name}")

    else:
        raise Exception("Invalid OUTPUT target")