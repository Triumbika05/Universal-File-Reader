import shutil 
import streamlit as st
import boto3
import json
import pandas as pd
from processor import process_pdf
from sftp_ingestor import fetch_from_sftp
from processor import detect_file_type, process_csv, process_txt, process_xml, create_output
from config import BUCKET_NAME, REGION



st.title("🚀 Universal File Reader")


# def fetch_from_sftp(source_path):
#     try:
#         local_file = source_path.split("/")[-1]
#         shutil.copy(source_path, local_file)
#         st.success("✅ File fetched from SFTP (simulated)")
#         return local_file
#     except Exception as e:
#         st.error(f"❌ SFTP Error: {e}")
#         return None
# ---------------- S3 SECTION ---------------- #
st.subheader("📥 Fetch File from S3")
if "file_name" not in st.session_state:
    st.session_state.file_name = None
s3_key = st.text_input("Enter S3 file path (e.g., raw/data.txt)")

def download_from_s3(file_key):
    s3 = boto3.client('s3', region_name=REGION)
    bucket_name = BUCKET_NAME

    local_file = file_key.split("/")[-1]

    try:
        s3.download_file(bucket_name, file_key, local_file)
        st.success(f"✅ File fetched from S3: {file_key}")
        return local_file
    except Exception as e:
        st.error(f"❌ S3 Error: {e}")
        return None

# Initialize file_name
file_name = None

# Fetch from S3
if st.button("Fetch from S3", key="s3_button" ):
    st.session_state.file_name = download_from_s3(s3_key)
    if st.session_state.file_name:
        st.info(f"📂 Source: S3 → {s3_key}")

st.subheader("🔌 Fetch File from SFTP")

# sftp_path = st.text_input("Enter SFTP path (e.g., sftp_folder/data.txt)")


if st.button("Fetch from SFTP", key="sftp_button"):
    fetch_from_sftp()
    st.success("Files fetched from SFTP and uploaded to S3!")
    st.info("📂 Files uploaded to S3 → Please fetch using S3 section to process")

# if st.button("Fetch from SFTP", key="sftp_button"):
#     st.session_state.file_name = fetch_from_sftp(sftp_path)
#     if st.session_state.file_name:
#         st.info(f"📂 Source: SFTP → {sftp_path}")
# ---------------- LOCAL UPLOAD ---------------- #
st.subheader("📤 Upload Local File")

# uploaded_file = st.file_uploader("Upload your file", type=["csv", "txt", "xml"])
uploaded_file = st.file_uploader("Upload your file", type=["csv", "txt", "xml", "pdf"])
if uploaded_file is not None:
    file_name = uploaded_file.name
    st.session_state.file_name = file_name

    with open(file_name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded: {file_name}")
    st.info("📂 Source: Local Upload")

# ---------------- PROCESSING ---------------- #
file_name = st.session_state.file_name
if st.session_state.file_name and st.button("Process File", key="process_btn"):

    file_type = detect_file_type(file_name)

    if file_type == "csv":
        data = process_csv(file_name)

    elif file_type == "txt":
        data = process_txt(file_name)

    elif file_type == "xml":
        data = process_xml(file_name)
    elif file_type == "pdf":
        data = process_pdf(file_name)
    else:
        st.error("Unsupported file type ❌")
        st.stop()

    create_output(file_name, data)

    st.success("✅ File processed successfully!")

    # Load result
    with open(f"{file_name.split('.')[0]}_output.json") as f:
        result = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(result["data"])

    # ---------------- INSIGHTS ---------------- #
    st.subheader("📈 Quick Insights")
    # st.write("Total Records:", len(df))
    # st.write("Average Age:", df["age"].astype(int).mean())
    # st.write("Cities:", df["city"].unique())
    st.write("Total Records:", len(df))

    if "age" in df.columns:
        st.write("Average Age:", pd.to_numeric(df["age"], errors="coerce").mean())

    if "city" in df.columns:
        st.write("Cities:", df["city"].unique())

    # ---------------- TABLE ---------------- #
    st.subheader("📊 Data in Table Format")
    st.dataframe(df)

    # ---------------- DOWNLOAD ---------------- #
    json_data = json.dumps(result, indent=4)

    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name="output.json",
        mime="application/json"
    )

