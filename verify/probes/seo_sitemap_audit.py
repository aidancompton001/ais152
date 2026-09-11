import re, urllib.request, html
def get(u):
    r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (compatible; Googlebot/2.1)"}),timeout=20)
    return r.status, r.geturl(), r.read().decode("utf-8","replace")
sm=get("https://ais152.com/sitemap.xml")[2]
urls=re.findall(r"<loc>([^<]+)</loc>",sm)
print("адресов в sitemap.xml:",len(urls))
print("код | конечный адрес = исходный | canonical = свой | meta robots | слов в <body> без JS")
bad=0
for u in urls:
    st,final,h=get(u)
    can=(re.search(r'<link rel="canonical" href="([^"]+)"',h) or [None,None])[1]
    rob=(re.search(r'<meta name="robots" content="([^"]+)"',h,re.I) or [None,"—"])[1]
    body=re.search(r"<body[^>]*>(.*)</body>",h,re.S|re.I).group(1)
    body=re.sub(r"<(script|style|svg|noscript)\b.*?</\1>"," ",body,flags=re.S|re.I)
    words=len(re.findall(r"\w{2,}",html.unescape(re.sub(r"<[^>]+>"," ",body))))
    ok= st==200 and final==u and can==u and "noindex" not in rob.lower()
    bad+= not ok
    print("%s %s | %s | %s | %s | %d" % ("OK " if ok else "BAD",st,final==u,can==u,rob,words), u)
print("проблемных:",bad)
