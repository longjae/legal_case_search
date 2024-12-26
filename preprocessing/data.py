import os
import json
from kiwipiepy import Kiwi

kiwi = Kiwi()


def make_metadata(DATA_DIR):
    documents = []
    for dir in os.listdir(DATA_DIR):
        file_dir = os.path.join(DATA_DIR, dir)
        if dir in [".DS_Store"]:
            continue
        for filename in os.listdir(file_dir):
            file_path = os.path.join(file_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                text = json.dumps(data, ensure_ascii=False)
                documents.append(
                    {
                        "content": text,
                        "metadata": {
                            "file_path": file_path,
                            "info": {
                                "caseField": data.get("info", {}).get("caseFleid", ""),
                                "detailField": data.get("info", {}).get(
                                    "detailField", ""
                                ),
                                "trailField": data.get("info", {}).get(
                                    "trailField", ""
                                ),
                                "caseNm": data.get("info", {}).get("caseNm", ""),
                                "courtNm": data.get("info", {}).get("courtNm", ""),
                                "judmnAdjuDe": data.get("info", {}).get(
                                    "judmnAdjuDe", ""
                                ),
                                "caseNo": data.get("info", {}).get("caseNo", ""),
                                "relateLaword": data.get("info", {}).get(
                                    "relateLaword", ""
                                ),
                            },
                        },
                    }
                )

    return documents
