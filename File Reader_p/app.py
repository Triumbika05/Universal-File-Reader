"""
app.py  —  Streamlit UI for Universal File Reader

Run:
    streamlit run app.py
"""

import json
import os

import boto3
import pandas as pd
import streamlit as st

from adapters.sftp_ingestor import fetch_from_sftp
from adapters.storage_factory import get_storage
from config import BUCKET_NAME, REGION, INPUT_DIR, OUTPUT_DIR, RAW_PREFIX, PROCESSED_PREFIX
from processors.processor import detect_file_type, PROCESSOR_MAP, create_output

# ── Storage backend ──────────────────────────────────────────────────────────
upload_file, download_file = get_storage()

# ── Page setup ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Universal File Reader", page_icon="🚀")
st.title("🚀 Universal File Reader")

# ── Session state ─────────────────────────────────────────────────────────────
if "file_name"   not in st.session_state: st.session_state.file_name   = None
if "input_path"  not in st.session_state: st.session_state.input_path  = None
if "raw_stored"  not in st.session_state: st.session_state.raw_stored  = None


# ═════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ═════════════════════════════════════════════════════════════════════════════

# ── 1. S3 ─────────────────────────────────────────────────────────────────────
with st.expander("📥  Fetch from S3", expanded=False):
    s3_key = st.text_input("S3 key (e.g. raw/employee_data.csv)", key="s3_key_input")

    if st.button("Fetch from S3"):
        try:
            os.makedirs(INPUT_DIR, exist_ok=True)
            local_file = os.path.join(INPUT_DIR, os.path.basename(s3_key))
            s3_client  = boto3.client("s3", region_name=REGION)
            s3_client.download_file(BUCKET_NAME, s3_key, local_file)

            st.session_state.file_name  = os.path.basename(s3_key)
            st.session_state.input_path = os.path.abspath(local_file)
            st.session_state.raw_stored = f"s3://{BUCKET_NAME}/{s3_key}"

            st.success(f"✅ Fetched from S3")
            st.info(f"📂 Saved to  →  `{st.session_state.input_path}`")
        except Exception as e:
            st.error(f"❌ S3 Error: {e}")


# ── 2. SFTP ───────────────────────────────────────────────────────────────────
with st.expander("🔌  Fetch from SFTP", expanded=False):
    if st.button("Fetch all files from SFTP"):
        try:
            keys = fetch_from_sftp()
            st.success(f"✅ {len(keys)} file(s) uploaded to S3 under `{RAW_PREFIX}`")
            st.info("Use the S3 section to pull a file down for processing.")
        except Exception as e:
            st.error(f"❌ SFTP Error: {e}")


# ── 3. Local upload ───────────────────────────────────────────────────────────
with st.expander("📤  Upload local file", expanded=True):
    uploaded = st.file_uploader("Choose a file", type=["csv", "txt", "xml", "pdf"])

    if uploaded:
        os.makedirs(INPUT_DIR, exist_ok=True)
        save_path = os.path.join(INPUT_DIR, uploaded.name)

        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())

        # Also store a copy in raw/ via the configured storage backend
        raw_dest = upload_file(save_path, f"{RAW_PREFIX}{uploaded.name}")

        st.session_state.file_name  = uploaded.name
        st.session_state.input_path = os.path.abspath(save_path)
        st.session_state.raw_stored = str(raw_dest)

        st.success(f"✅ File received")
        st.info(f"📂 Input saved to  →  `{st.session_state.input_path}`")
        st.info(f"📦 Raw stored at   →  `{st.session_state.raw_stored}`")


# ═════════════════════════════════════════════════════════════════════════════
# PROCESSING SECTION
# ═════════════════════════════════════════════════════════════════════════════
st.divider()

if st.session_state.file_name:
    st.markdown(f"**Ready to process:** `{st.session_state.file_name}`")

    if st.button("⚙️  Process File"):
        file_path = st.session_state.input_path or st.session_state.file_name
        file_type = detect_file_type(file_path)

        if file_type not in PROCESSOR_MAP:
            st.error(f"❌ Unsupported file type: `{file_type}`")
            st.stop()

        with st.spinner("Processing …"):
            data        = PROCESSOR_MAP[file_type](file_path)
            output_path = create_output(file_path, data)

        # Store processed JSON via configured backend
        output_name    = os.path.basename(output_path)
        processed_dest = upload_file(output_path, f"{PROCESSED_PREFIX}{output_name}")

        # ── Path summary ──────────────────────────────────────────────────────
        st.success("✅ Processing complete!")

        with st.container(border=True):
            st.markdown("### 📍 Path Summary")
            st.markdown(f"| Step | Path |")
            st.markdown(f"|------|------|")
            st.markdown(f"| 📥 Source file   | `{os.path.abspath(file_path)}` |")
            st.markdown(f"| 📂 Input dir     | `{os.path.abspath(INPUT_DIR)}` |")
            st.markdown(f"| 📦 Raw stored at | `{st.session_state.raw_stored}` |")
            st.markdown(f"| 📁 Output dir    | `{os.path.abspath(OUTPUT_DIR)}` |")
            st.markdown(f"| 💾 Output file   | `{os.path.abspath(output_path)}` |")
            st.markdown(f"| ✅ Processed at  | `{processed_dest}` |")

        # ── Load and display results ──────────────────────────────────────────
        with open(output_path, encoding="utf-8") as f:
            result = json.load(f)

        df = pd.DataFrame(result["data"])

        st.subheader("📈 Quick Insights")
        st.write("Total Records:", len(df))
        if "age" in df.columns:
            st.write("Average Age:", pd.to_numeric(df["age"], errors="coerce").mean())
        if "city" in df.columns:
            st.write("Cities:", df["city"].unique())

        st.subheader("📊 Data Table")
        st.dataframe(df, use_container_width=True)

        st.download_button(
            label="📥 Download Output JSON",
            data=json.dumps(result, indent=4),
            file_name=output_name,
            mime="application/json",
        )

else:
    st.info("👆 Provide a file using one of the input sections above, then click **Process File**.")
