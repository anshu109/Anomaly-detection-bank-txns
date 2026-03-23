import re
import pandas as pd

def parse_log(log):
    log = log.strip()

    if log in ["", '""', "MALFORMED_LOG", "raw_log"]:
        return None

    try:
        if "::" in log:
            parts = log.split("::")
            return {
                "timestamp": pd.to_datetime(parts[0], errors="coerce"),
                "user_id": int(parts[1].replace("user", "")),
                "txn_text": parts[2],
                "amount": float(parts[3]),
                "location": parts[4],
                "device": parts[5],
            }

        if ">>" in log:
            timestamp = re.search(r"^(.*?)\s*>>", log)
            user = re.search(r"\[(user\d+)\]", log)
            amount = re.search(r"amt=€?([\d\.]+)", log)
            device = re.search(r"dev:(.*)", log)

            return {
                "timestamp": pd.to_datetime(timestamp.group(1), errors="coerce") if timestamp else None,
                "user_id": int(user.group(1).replace("user", "")) if user else None,
                "txn_text": log,
                "amount": float(amount.group(1)) if amount else None,
                "location": None,
                "device": device.group(1).strip() if device else None,
            }

        if "user=" in log:
            timestamp = re.search(r"^(.*?)\s*-", log)
            user = re.search(r"user=(user\d+)", log)
            amount = re.search(r"([\d\.]+)", log)
            device = re.search(r"device=(.*)", log)

            return {
                "timestamp": pd.to_datetime(timestamp.group(1), errors="coerce") if timestamp else None,
                "user_id": int(user.group(1).replace("user", "")) if user else None,
                "txn_text": log,
                "amount": float(amount.group(1)) if amount else None,
                "location": None,
                "device": device.group(1).strip() if device else None,
            }

        if "usr:" in log:
            parts = log.split("|")

            user = re.search(r"user(\d+)", parts[0])
            amount = re.search(r"([\d\.]+)", parts[2])

            return {
                "timestamp": pd.to_datetime(parts[4], errors="coerce"),
                "user_id": int(user.group(1)) if user else None,
                "txn_text": parts[1],
                "amount": float(amount.group(1)) if amount else None,
                "location": parts[3],
                "device": parts[5],
            }

        return None

    except Exception:
        return None