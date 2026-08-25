import json
import sqlite3
import re


DB_FILE = "tudien.db"


def import_file(filename, ngon_ngu_nguon, ngon_ngu_dich):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tu_vung (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tu_goc TEXT NOT NULL,
            nghia TEXT NOT NULL,
            ngon_ngu_nguon TEXT,
            ngon_ngu_dich TEXT
        )
    """)

    count = 0

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)

                tu_goc = data.get("word", "").strip()

                # File Anh-Việt có thể có phiên âm ở cuối từ
                if ngon_ngu_nguon == "en":
                    tu_goc = re.sub(
                        r"\s*/[^/]*\/\s*$",
                        "",
                        tu_goc
                    ).strip()

                nghia_list = []

                for sense in data.get("senses", []):
                    for gloss in sense.get("glosses", []):
                        gloss = gloss.strip()

                        if gloss:
                            nghia_list.append(gloss)

                nghia = "; ".join(nghia_list)

                if not tu_goc or not nghia:
                    continue

                cursor.execute("""
                    INSERT INTO tu_vung
                    (
                        tu_goc,
                        nghia,
                        ngon_ngu_nguon,
                        ngon_ngu_dich
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    tu_goc,
                    nghia,
                    ngon_ngu_nguon,
                    ngon_ngu_dich
                ))

                count += 1

            except Exception as e:
                print("Lỗi:", e)

    conn.commit()
    conn.close()

    print(
        f"Đã import {count} từ "
        f"{ngon_ngu_nguon} -> {ngon_ngu_dich}"
    )


# Anh -> Việt
import_file(
    "anhviet109K.dict.jsonl",
    "en",
    "vi"
)

# Việt -> Anh
import_file(
    "vietanh.dict.jsonl",
    "vi",
    "en"
)

print("===== HOÀN TẤT =====")