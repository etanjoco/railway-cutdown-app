import io
import csv
import sqlite3
from typing import Any, Dict, List

import db


def import_players_from_bytes(content_bytes: bytes) -> Dict[str, Any]:
    """Parse CSV bytes and upsert players matching on `name`+`grade`.

    Expects a header row with at least `name` and `grade` columns. Returns a
    summary dict: inserted/updated/skipped counts and a list of row errors.
    """
    try:
        text = content_bytes.decode("utf-8-sig")
    except Exception:
        text = content_bytes.decode("utf-8", errors="replace")

    stream = io.StringIO(text)
    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        raise ValueError("CSV must include a header row with 'name' and 'grade'.")

    normalized_fieldnames = [f.strip().lower() for f in reader.fieldnames]
    if "name" not in normalized_fieldnames or "grade" not in normalized_fieldnames:
        raise ValueError("CSV header must include 'name' and 'grade' columns.")

    inserted = 0
    updated = 0
    skipped = 0
    errors: List[Dict[str, Any]] = []

    conn = db.get_connection()
    cur = conn.cursor()
    line_number = 1
    try:
        for row in reader:
            line_number += 1
            try:
                # Normalize keys to lowercase stripped names
                normalized_row = {k.strip().lower(): (v or "").strip() for k, v in row.items() if k}

                name = normalized_row.get("name", "")
                grade_val = normalized_row.get("grade", "")

                if not name:
                    errors.append({"row": line_number, "error": "missing name"})
                    skipped += 1
                    continue

                if grade_val == "":
                    grade = None
                else:
                    try:
                        grade = int(grade_val)
                    except ValueError:
                        errors.append({"row": line_number, "error": f"invalid grade: {grade_val}"})
                        skipped += 1
                        continue

                # Find existing by name + grade
                if grade is None:
                    cur.execute("SELECT id FROM players WHERE name = ? AND grade IS NULL", (name,))
                else:
                    cur.execute("SELECT id FROM players WHERE name = ? AND grade = ?", (name, grade))

                existing = cur.fetchone()
                if existing:
                    existing_id = existing[0]
                    try:
                        cur.execute("UPDATE players SET name = ?, grade = ? WHERE id = ?", (name, grade, existing_id))
                        conn.commit()
                        updated += 1
                    except sqlite3.IntegrityError as e:
                        errors.append({"row": line_number, "error": str(e)})
                        skipped += 1
                        continue
                else:
                    try:
                        cur.execute("INSERT INTO players (name, grade) VALUES (?, ?)", (name, grade))
                        conn.commit()
                        inserted += 1
                    except sqlite3.IntegrityError as e:
                        errors.append({"row": line_number, "error": str(e)})
                        skipped += 1
                        continue

            except Exception as e:
                errors.append({"row": line_number, "error": str(e)})
                skipped += 1
                continue
    finally:
        cur.close()
        conn.close()

    processed = inserted + updated + skipped
    return {"processed": processed, "inserted": inserted, "updated": updated, "skipped": skipped, "errors": errors}
