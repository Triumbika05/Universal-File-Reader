import shutil

def fetch_from_sftp(source_path, destination):
    try:
        shutil.copy(source_path, destination)
        print("✅ File fetched from SFTP (simulated)")
    except Exception as e:
        print("❌ Error:", e)


# Example usage
fetch_from_sftp("sftp_folder/data.txt", "data.txt")

