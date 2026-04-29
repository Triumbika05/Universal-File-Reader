import os
import yaml
from dotenv import load_dotenv


# 🔷 Load environment variables from .env
load_dotenv(dotenv_path=".env")


class Config:

    # 🔷 Load YAML config
    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    INPUT = cfg.get("input", {})
    OUTPUT = cfg.get("output", {})
    PROCESSING = cfg.get("processing", {})
    PARSERS = cfg.get("parsers", {})
    LOGGING = cfg.get("logging", {})
    ERROR = cfg.get("error_handling", {})
    TEMP_DIR = cfg.get("temp_dir", "temp/")

    # 🔥 Replace ENV placeholders with actual values
    # ---------------- INPUT AZURE ----------------
    if INPUT.get("azure"):
        if INPUT["azure"].get("connection_string") == "ENV":
            INPUT["azure"]["connection_string"] = os.getenv("AZURE_CONNECTION_STRING")

    # ---------------- OUTPUT AZURE ----------------
    if OUTPUT.get("azure"):
        if OUTPUT["azure"].get("connection_string") == "ENV":
            OUTPUT["azure"]["connection_string"] = os.getenv("AZURE_CONNECTION_STRING")

    # 🔥 Optional: Validation (VERY IMPORTANT)
    # Fail fast if env missing
    if INPUT.get("azure") and INPUT["azure"].get("connection_string") is None:
        raise Exception("AZURE_CONNECTION_STRING not set in .env for INPUT")

    if OUTPUT.get("azure") and OUTPUT["azure"].get("connection_string") is None:
        raise Exception("AZURE_CONNECTION_STRING not set in .env for OUTPUT")