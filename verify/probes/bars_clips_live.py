# -*- coding: utf-8 -*-
"""Четыре ролика сцены отдаются сайтом и не битые.

Проверяется отданное сервером, а не то, что лежит на диске: до 19.08 на
этом сайте уже был случай, когда правка существовала локально и не
существовала для посетителя.
"""
import sys
import urllib.request

BASE = "https://ais152.com/assets/video/bars/"
NAMES = ["scene1-stand-to-treadmill", "scene2-run-loop", "scene3-point", "scene4-wave"]
MIN_BYTES = 200 * 1024


def head(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        return resp.status, resp.headers.get("Content-Type", ""), resp.read(MIN_BYTES + 1)


def main():
    broken = []
    for n in NAMES:
        url = BASE + n + ".mp4"
        try:
            code, ctype, blob = head(url)
        except Exception as e:
            broken.append("%s: %s" % (n, e))
            continue
        if code != 200:
            broken.append("%s: код %s" % (n, code))
        elif "video" not in ctype and "octet-stream" not in ctype:
            broken.append("%s: тип %s" % (n, ctype))
        elif len(blob) <= MIN_BYTES:
            broken.append("%s: меньше %d КБ" % (n, MIN_BYTES // 1024))
        elif blob[4:8] != b"ftyp":
            broken.append("%s: не mp4" % n)
    for b in broken:
        print("БИТЫЙ %s" % b)
    print("clips=%d;broken=%d;" % (len(NAMES), len(broken)))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
