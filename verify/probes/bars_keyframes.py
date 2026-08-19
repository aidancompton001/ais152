# -*- coding: utf-8 -*-
"""Каждый ролик перематывается покадрово.

Отданный генератором файл имел один опорный кадр на весь ролик: браузер
не умеет мгновенно показать кадр, до которого надо досчитать от далёкого
опорного, и перемотка прокруткой дёргается. Порог 0,9 — с запасом ниже
достигнутых 96 из 97 и заведомо выше исходного 0.
"""
import glob
import os
import subprocess
import sys

THRESHOLD = 0.9


def ratio(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "frame=key_frame", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    vals = [x.strip() for x in r.stdout.splitlines() if x.strip()]
    if not vals:
        return 0.0, 0
    return vals.count("1") / float(len(vals)), len(vals)


def main():
    files = sorted(glob.glob("assets/video/bars/*.mp4"))
    if len(files) != 4:
        print("роликов не четыре, а %d" % len(files))
        print("min_keyframe_ratio_ok=0;")
        return 1
    ok = True
    for f in files:
        r, n = ratio(f)
        print("%-34s опорных %.3f из %d кадров" % (os.path.basename(f), r, n))
        if r < THRESHOLD:
            ok = False
    print("min_keyframe_ratio_ok=%d;" % (1 if ok else 0))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
