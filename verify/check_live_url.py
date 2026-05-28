#!/usr/bin/env python3
"""HTTP GET check с retry (5x, 2s delay). Печатает HTTP status или 'ERR'."""
import sys, time, urllib.request, urllib.error

url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
for _ in range(5):
    try:
        req = urllib.request.Request(url, method='GET', headers={'User-Agent': 'verify/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(resp.status)
            sys.exit(0)
    except urllib.error.HTTPError as e:
        print(e.code)
        sys.exit(0)
    except Exception:
        time.sleep(2)
print('ERR')
sys.exit(1)
