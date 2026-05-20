#!/usr/bin/env python3
"""
verify.py — прогоняет acceptance.json и математически считает результат.
Скрипт читает реальное состояние проекта. Его вывод подделать нельзя.

Использование:
    python verify/verify.py [path/to/acceptance.json]

Exit code: 0 если 100% проверок прошли, иначе 1.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

manifest_path = sys.argv[1] if len(sys.argv) > 1 else 'verify/acceptance.json'
manifest = json.load(open(manifest_path, encoding='utf-8'))

print(f"VERIFY: {manifest['task']}")
print(f"Время прогона (UTC): {datetime.now(timezone.utc).isoformat()}")
print("=" * 72)

passed = 0
total = len(manifest['checks'])
failed_ids = []

for c in manifest['checks']:
    r = subprocess.run(c['cmd'], shell=True, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()

    ok = True
    reason = ""
    if 'expect_exit' in c:
        ok &= (r.returncode == c['expect_exit'])
        reason = f"exit={r.returncode}"
    if 'expect_equal' in c:
        ok &= (out == str(c['expect_equal']))
        reason = f"got '{out}' want '{c['expect_equal']}'"
    if 'expect_min' in c:
        try:
            val = int(out or 0)
        except ValueError:
            val = 0
        ok &= (val >= c['expect_min'])
        reason = f"got {val} need >={c['expect_min']}"
    if 'expect_contain' in c:
        ok &= (c['expect_contain'] in out)
        reason = f"want substr '{c['expect_contain']}'"

    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed_ids.append(c['id'])

    out_short = out.replace('\n', ' ')[:50]
    print(f"{c['id']:5} {status}  {c['desc']:48} | {reason} | raw[{out_short}]")

print("=" * 72)
pct = passed / total * 100 if total else 0
print(f"RESULT: {passed}/{total} PASSED  ({pct:.1f}%)")
if failed_ids:
    print(f"FAILED: {', '.join(failed_ids)}")
    print("VERDICT: TASK NOT COMPLETE")
else:
    print("VERDICT: TASK VERIFIED")

sys.exit(0 if passed == total else 1)
