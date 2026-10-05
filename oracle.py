# Generates sitemap-like documents, validates with libxml2 (lxml) against the real sitemap.xsd / siteindex.xsd, writes JSONL.
import random, json, sys
from lxml import etree
seed=int(sys.argv[1]); N=int(sys.argv[2]); random.seed(seed)
XS=etree.XMLSchema(etree.parse('/tmp/smw/sitemap.xsd')); XI=etree.XMLSchema(etree.parse('/tmp/smw/siteindex.xsd'))
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
def pick(l): return random.choice(l)
LOCS=['http://www.example.com/','https://example.com/a/b?x=1&amp;y=2','http://example.com/catalog?item=12&amp;desc=vacation_hawaii','http://a.co/','http://a.com','http://a.com/a b','http://a.com/%zz','http://a.com/%41','http://a.com/[x]','http://[::1]/x/yy','http://a.com:80/x','http://a.com:8x/x','http://a.com/ü/ü','http://a.com/#frag','http://a.com/#a#b','ftp://a.com/xxxx','a/b/c/d/e/f/g/h','  http://a.com/x  ','http://a.com/'+'a'*2040,'http://a.com/'+'a'*2036,'xx','','http://a.com/\\x','http://a.com/{}|^`','ht!tp://a.com/xx','://a.com/xxxxxx','http://us@er:pw@a.com/x','mailto:someone@example.com','http://a.com/x"y',"http://a.com/x'y",'http://a.com/&lt;x&gt;','http://a.com/%','http://a.com/?q=%20%e2%82%ac']
LMS=['2005-01-01','2005-01-01T10:00:00Z','2005-01-01T10:00:00','2005-02-30','2004-02-29','1900-02-29','2000-02-29','2005-13-01','2005-01-01T24:00:00Z','2005-01-01T24:00:01Z','2005-01-01T10:00Z','2005-01-01T10:00:00.5+02:00','2005-01-01Z','2005-01-01+14:00','2005-01-01+14:01','20050101','0000-01-01','-0001-01-01','-0004-02-29','-0001-02-29','12005-01-01','2005-1-1',' 2005-01-01 ','2005-01-01T10:00:00+0200','2005-01-01T10:00:60Z','2005-01-01T25:00:00Z','2005-01-01t10:00:00Z','2005-01-31','2005-04-31','2005-06-31','2005-11-30','2005-12-32','2005-00-10','2005-01-00','2005-01-01T00:00:00-05:30','2005-01-01T10:00:00.123456Z','2005-01-01T10:00:00.Z','2005-01-01T23:59:59+14:00','2005-01-01T23:59:59-14:01','today','2005/01/01','']
CFS=['always','hourly','daily','weekly','monthly','yearly','never','Daily',' daily','daily ','sometimes','','DAILY']
PRS=['0.5','1','1.0','0','0.0','1.1','-0.1','.5','5.','+0.5',' 0.5 ','1e0','abc','','0.','1.00000','1.0000001','00.5','0.99999999','+1','-0','+.0']
def el(n,v): return '<%s>%s</%s>'%(n,v,n)
def url(idx):
    parts=[('loc',pick(LOCS)) if random.random()<.5 else ('loc','http://example.com/p%d'%random.randrange(999))]
    if random.random()<.5: parts.append(('lastmod',pick(LMS) if random.random()<.6 else '2005-01-01'))
    if random.random()<.4: parts.append(('changefreq',pick(CFS) if random.random()<.6 else 'daily'))
    if random.random()<.4: parts.append(('priority',pick(PRS) if random.random()<.6 else '0.5'))
    r=random.random()
    if r<.06 and len(parts)>1: random.shuffle(parts)
    elif r<.09: parts=parts[1:]
    elif r<.12: parts.append(pick(parts))
    elif r<.14: parts.append(('extra','x'))
    elif r<.16: parts.append(('x:ext','x'))
    body=''.join(el(n,v) for n,v in parts)
    if random.random()<.03: body='text'+body
    if random.random()<.03: body=el('loc','<b>http://a.com/xyzzy</b>')+body
    if random.random()<.03: return '<url foo="1">%s</url>'%body
    return '<url>%s</url>'%body
def doc():
    idx=random.random()<.2
    root='sitemapindex' if idx else 'urlset'; kid='sitemap' if idx else 'url'
    n=pick([0,1,1,1,2,3,5])
    if idx:
        body=''.join('<sitemap>'+''.join(el(a,b) for a,b in ([('loc',pick(LOCS))]+([('lastmod',pick(LMS))] if random.random()<.5 else [])))+'</sitemap>' for _ in range(n))
    else: body=''.join(url(i) for i in range(n))
    ns=' xmlns="%s"'%NS
    r=random.random()
    if r<.03: ns=''
    elif r<.05: ns=' xmlns="http://www.sitemaps.org/schemas/sitemap/0.9/"'
    elif r<.06: ns=' xmlns="https://www.sitemaps.org/schemas/sitemap/0.9"'
    elif r<.08: ns+=' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="%s http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"'%NS
    elif r<.09: ns+=' version="1"'
    elif r<.10: ns+=' xmlns:x="urn:x"'
    if random.random()<.03: root=pick(['URLSET','sitemap','urlset2','feed'])
    pre=pick(['<?xml version="1.0" encoding="UTF-8"?>\n','<?xml version="1.0"?>','','\n<?xml version="1.0"?>','<!-- c -->\n','<?xml version="1.0" encoding="UTF-8"?>\n<!-- c -->\n','text'])
    post=pick(['','\n','<!-- end -->','junk','<x/>'])
    d=pre+'<%s%s>%s</%s>'%(root,ns,body,root)+post
    r=random.random()
    if r<.04: d=d.replace('</'+root+'>','')
    elif r<.07: d=d.replace('<loc>','<loc>&',1)
    elif r<.09: d=d.replace('<loc>','<loc>&nbsp;',1)
    elif r<.10: d=d.replace('<loc>','<loc><![CDATA[',1).replace('</loc>',']]></loc>',1)
    elif r<.11: d=d.replace('<loc>','<loc>&#x26;',1)
    elif r<.12: d=d.replace('<loc>','<loc>&#0;',1)
    elif r<.13: d=d.replace('<loc>','<LOC>',1)
    elif r<.14: d=d.replace('</loc>','</loc >',1)
    elif r<.15: d=d.replace('<url>','<url >',1)
    elif r<.16 and len(d)>5: i=random.randrange(len(d)); d=d[:i]+d[i+1:]
    elif r<.17 and len(d)>5: i=random.randrange(len(d)); d=d[:i]+pick(['<','>','&','"',"'",'\x01','\u00a0'])+d[i:]
    return d,idx
out=open(sys.argv[3],'w')
for _ in range(N):
    d,idx=doc()
    b=d.encode('utf-8')
    try: t=etree.fromstring(b); wf=True
    except Exception as e: wf=False; t=None
    v=None
    if wf:
        v=(XI if idx else XS).validate(t)
        # libxml2 validates against whichever schema; the engine picks by root name
        if t.tag=='{%s}sitemapindex'%NS and not idx: v=XI.validate(t)
        elif t.tag=='{%s}urlset'%NS and idx: v=XS.validate(t)
        elif t.tag not in ('{%s}sitemapindex'%NS,'{%s}urlset'%NS): v=False
    out.write(json.dumps({'doc':d,'wf':wf,'valid':v})+'\n')
