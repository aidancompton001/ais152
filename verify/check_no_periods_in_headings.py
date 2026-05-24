#!/usr/bin/env python3
"""Считает заголовки h1-h4 (включая lang-spans), оканчивающиеся точкой.
Печатает число. Используется в verify/acceptance.json."""
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
heads = re.findall(r'<h[1-4][^>]*>([\s\S]*?)</h[1-4]>', html)
v = 0
for h in heads:
    spans = re.findall(r'<span\s+data-lang-[a-z]+[^>]*>([^<]*)</span>', h)
    if spans:
        for s in spans:
            if re.sub(r'<[^>]+>', '', s).strip().endswith('.'):
                v += 1
    else:
        if re.sub(r'<[^>]+>', '', h).strip().endswith('.'):
            v += 1
print(v)
