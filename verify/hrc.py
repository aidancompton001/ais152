#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hrc.py v2 — Hallucination Rate Counter (Закон 23).

Считает долю галлюцинаций P = H/N по РЕЕСТРУ claim'ов и гейтит по порогу.
Едет на существующей рельсе: вызывается из verify/acceptance.json как обычная
проверка (expect_exit: 0), а глобальный Stop-хук (Закон 21) не выпустит сессию,
пока проверка не зелёная.

────────────────────────────────────────────────────────────────────────────
ЧТО ИЗМЕНИЛОСЬ В v2 (после инцидента 2026-07-31)
────────────────────────────────────────────────────────────────────────────
v1 верил агенту на слово: тот сам писал status="PROVEN" и строку evidence.
Реестр {"status":"PROVEN","evidence":"проверено"} с текстом «Луна из сыра»
давал P=0% и PASS. Детектором это не было — только калькулятором.

v2: СТАТУС НЕ ОБЪЯВЛЯЕТСЯ, А ВЫЧИСЛЯЕТСЯ. Доказательство — исполнимая команда,
которую скрипт ПЕРЕЗАПУСКАЕТ прямо сейчас и сверяет вывод с ожиданием.
Не воспроизвелось → claim не verified → растит H. «проверено», «см. логи»,
«я проверял» больше не являются доказательствами: там нечего запускать.

────────────────────────────────────────────────────────────────────────────
ФОРМАТ РЕЕСТРА (verify/hrc_ledger.json)
────────────────────────────────────────────────────────────────────────────
{
  "task": "краткое имя задачи",
  "threshold": 1e-8,                    # опционально; дефолт 1e-8
  "require_landa": false,               # опционально; см. ниже
  "claims": [
    {"id":"01", "text":"утверждение, поданное как факт",
     "asserted": true,
     "proof": {"cmd":"grep -c HRC verify/acceptance.json", "expect_equal":"1"}},

    {"id":"02", "text":"догадка о смысле — НЕ факт",
     "asserted": false,
     "note":"почему это гипотеза, а не факт"}
  ]
}

Виды ожиданий в proof (можно комбинировать):
  expect_exit    — команда вернула этот код возврата
  expect_equal   — stdout+stderr (trimmed) РОВНО равен значению
  expect_contain — вывод содержит подстроку
  expect_min     — вывод как число >= значения

────────────────────────────────────────────────────────────────────────────
ПРАВИЛА ПОДСЧЁТА
────────────────────────────────────────────────────────────────────────────
  N = число claim'ов с asserted=true (поданы КАК ФАКТ).
  VERIFIED = у claim'а есть proof.cmd, команда выполнилась и ожидание совпало.
  H = asserted, но НЕ verified (нет proof / команда упала / вывод не совпал).
  P = H / N.  PASS если P <= threshold, иначе FAIL (exit 1).

  Историческое состояние («до задачи файла не было») по умолчанию идёт с
  asserted=false. НО если для него есть воспроизводимое доказательство в
  настоящем (git status --porcelain → '?? file', git log --diff-filter=A),
  claim обязан идти asserted=true с этим proof: прятать проверяемое в гипотезы
  — занижение знаменателя N, такое же жульничество, как липовый пруф.

АНТИ-ОБХОД БЕЗДЕЙСТВИЕМ:
  claims == []            → exit 2, если не указан "no_claims_reason".
  task — плейсхолдер      → exit 2 (реестр не адаптирован под задачу).
  claims есть, все asserted=false → PASS: реестр вёлся, статус-факт снят.

СЛОЙ ЛАНДЫ ("require_landa": true):
  Требует verify/landa_review.json — вердикт #14 Hans Landa, покрывающий все id
  реестра и отдельно перечисляющий claim'ы, которые агент в реестр НЕ внёс.
  Закрывает дыру, которую машина закрыть не может: умолчание.

────────────────────────────────────────────────────────────────────────────
ЧЕСТНОЕ ОГРАНИЧЕНИЕ (не удалять)
────────────────────────────────────────────────────────────────────────────
v2 сильнее v1, но всемогущим не стал. Остаются два обхода:
  1. НЕ ВНЕСТИ claim в реестр — соврал в тексте, в список не записал. Машине
     нечего считать. Лечится только внешним ревью (слой Ланды).
  2. ПОДОБРАТЬ ручную команду (`echo OK` + expect_contain OK) — формально
     исполнимо, содержательно пусто. Лечится тем же ревью.
Заявлять, что hrc.py «ловит галлюцинации автоматически», по-прежнему нельзя.
Он делает ложь дорогой и заметной, а не невозможной.

Запуск:  python core/verify/hrc.py [verify/hrc_ledger.json]
Exit: 0 = PASS, 1 = FAIL (P>порога), 2 = реестр отсутствует/битый/незаполненный.
"""
import json
import os
import shutil
import subprocess
import sys

DEFAULT_THRESHOLD = 1e-8  # 0.000001 %
PLACEHOLDER_MARK = "заполняется агентом"  # маркер незаполненного шаблона
PROOF_TIMEOUT_SEC = 60
EXPECT_KEYS = ("expect_exit", "expect_equal", "expect_contain", "expect_min")


def die(code, msg):
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def run_proof(proof):
    """Выполнить доказательство. Возврат: (verified: bool, why: str)."""
    cmd = str(proof.get("cmd", "")).strip()
    if not cmd:
        return False, "в proof нет команды"
    if not any(k in proof for k in EXPECT_KEYS):
        return False, "в proof нет ожидания (expect_*) — нечего сверять"

    # На Windows shell=True — это cmd.exe, который не понимает одинарные кавычки,
    # 2>/dev/null и пайпы вида wc -l. Доказательства пишутся на POSIX sh, поэтому
    # исполняем через bash, если он есть (Git Bash на Windows, /bin/bash на Linux).
    bash = shutil.which("bash")
    try:
        if bash:
            r = subprocess.run([bash, "-lc", cmd], capture_output=True, text=True,
                               timeout=PROOF_TIMEOUT_SEC)
        else:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                               timeout=PROOF_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        return False, f"команда не уложилась в {PROOF_TIMEOUT_SEC}s"
    except Exception as e:                                   # noqa: BLE001
        return False, f"команда не запустилась ({e})"

    out = (r.stdout + r.stderr).strip()

    if "expect_exit" in proof and r.returncode != proof["expect_exit"]:
        return False, f"exit={r.returncode}, ждали {proof['expect_exit']}"
    if "expect_equal" in proof and out != str(proof["expect_equal"]):
        return False, f"вывод '{out[:40]}' != '{proof['expect_equal']}'"
    if "expect_contain" in proof and str(proof["expect_contain"]) not in out:
        return False, f"в выводе нет '{proof['expect_contain']}'"
    if "expect_min" in proof:
        try:
            val = int(out or 0)
        except ValueError:
            return False, f"вывод '{out[:30]}' не число"
        if val < proof["expect_min"]:
            return False, f"{val} < {proof['expect_min']}"

    return True, "воспроизведено"


def check_landa(ledger_path, claim_ids):
    """Слой внешнего ревью. Возврат: (ok: bool, msg: str)."""
    review = os.path.join(os.path.dirname(ledger_path) or ".", "landa_review.json")
    if not os.path.isfile(review):
        return False, ("требуется ревью #14 Hans Landa: файла verify/landa_review.json нет. "
                       "Вызови субагента hans-landa и сохрани его вердикт.")
    try:
        with open(review, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"landa_review.json не парсится ({e})"

    reviewed = {str(c.get("id")) for c in data.get("reviewed_claims", [])}
    missing = [i for i in claim_ids if i not in reviewed]
    if missing:
        return False, f"Ланда не покрыл claim(ы): {', '.join(missing)}"
    if "unlisted_claims" not in data:
        return False, ("в landa_review.json нет поля 'unlisted_claims' — Ланда обязан "
                       "перечислить утверждения из ответа, которых НЕТ в реестре "
                       "(пустой список = таких не найдено)")
    rejected = [str(c.get("id")) for c in data.get("reviewed_claims", [])
                if c.get("verdict") == "REJECTED"]
    if rejected:
        return False, f"Ланда отклонил claim(ы): {', '.join(rejected)}"
    unlisted = data.get("unlisted_claims") or []
    if unlisted:
        return False, (f"Ланда нашёл {len(unlisted)} утверждени(я/й) вне реестра — "
                       f"внеси их и переприми: {'; '.join(str(u)[:60] for u in unlisted[:3])}")
    return True, "ревью Ланды пройдено"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "verify/hrc_ledger.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        die(2, f"HRC: реестр не найден: {path}. Составь его перед завершением задачи (Закон 23).")
    except json.JSONDecodeError as e:
        die(2, f"HRC: реестр не парсится ({e}).")

    claims = data.get("claims")
    if not isinstance(claims, list):
        die(2, "HRC: в реестре нет списка 'claims'.")

    threshold = float(data.get("threshold", DEFAULT_THRESHOLD))
    task = data.get("task", "(без имени)")
    no_claims_reason = str(data.get("no_claims_reason", "")).strip()

    # Анти-обход бездействием: незаполненный реестр — не PASS, а «составь реестр».
    if PLACEHOLDER_MARK in task:
        die(2, "HRC: поле 'task' осталось шаблонным плейсхолдером — реестр не адаптирован "
               "под текущую задачу. Впиши имя задачи и claim'ы (Закон 23).")
    if not claims and not no_claims_reason:
        die(2, "HRC: реестр пуст. Пустой реестр НЕ засчитывается как PASS — иначе гейт "
               "обходится бездействием. Внеси claim'ы задачи; если фактических утверждений "
               "действительно нет, укажи явно поле \"no_claims_reason\": \"почему\".")

    asserted = [c for c in claims if c.get("asserted") is True]
    N = len(asserted)

    print("=" * 72)
    print(f"HRC v2 — доказательства ПЕРЕЗАПУСКАЮТСЯ | задача: {task}")
    print("=" * 72)

    halluc = []
    if asserted:
        print("ПРОВЕРКА ДОКАЗАТЕЛЬСТВ (каждое исполняется прямо сейчас):")
    for c in asserted:
        proof = c.get("proof")
        if not isinstance(proof, dict):
            ok, why = False, "нет исполнимого proof — слово агента доказательством не является"
        else:
            ok, why = run_proof(proof)
        mark = "OK  " if ok else "ЛОЖЬ"
        print(f"  [{mark}] {str(c.get('id','?')):<4} {str(c.get('text',''))[:52]:<52} | {why}")
        if not ok:
            halluc.append((c, why))

    H = len(halluc)
    P = (H / N) if N else 0.0

    print("-" * 72)
    print(f"N (заявлено как факт): {N}")
    print(f"H (доказательство не воспроизвелось): {H}")
    print(f"P = H/N = {P:.8f} = {P*100:.6f} %   |   порог = {threshold:.1e}")
    print("-" * 72)

    if N == 0:
        why = no_claims_reason or "все claim'ы помечены asserted=false"
        print(f"VERDICT: PASS (нет утверждений, поданных как факт — {why})")
        sys.exit(0)

    if P > threshold:
        print("VERDICT: FAIL — P выше порога. Либо доведи доказательство до воспроизводимого,")
        print("либо сними статус-факт (asserted=false). Слово агента фактом не является.")
        sys.exit(1)

    if data.get("require_landa") is True:
        ok, msg = check_landa(path, [str(c.get("id")) for c in claims])
        print(f"СЛОЙ ЛАНДЫ: {msg}")
        if not ok:
            print("VERDICT: FAIL — внешнее ревью не пройдено.")
            sys.exit(1)

    print("VERDICT: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
