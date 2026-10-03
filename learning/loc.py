import os, sys, json, collections, re
root = sys.argv[1]
def classify(path):
    code=com=doc=blank=0; in_block=False
    for line in open(path, encoding='utf-8', errors='replace'):
        s=line.strip()
        if in_block:
            com+=1
            if '*/' in s: in_block=False
            continue
        if not s: blank+=1
        elif s.startswith('///') or s.startswith('//!'): doc+=1
        elif s.startswith('//'): com+=1
        elif s.startswith('/*'):
            com+=1
            if '*/' not in s: in_block=True
        else: code+=1
    return code,com,doc,blank
rows=[]
for dp,dn,fn in os.walk(root):
    dn[:] = [d for d in dn if d not in ('.git','target')]
    for f in fn:
        p=os.path.join(dp,f); rel=os.path.relpath(p,root)
        ext=os.path.splitext(f)[1] or f
        if ext=='.rs':
            c,cm,d,b=classify(p)
        else:
            try: n=sum(1 for _ in open(p,encoding='utf-8',errors='replace'))
            except: n=0
            c,cm,d,b=n,0,0,0
        rows.append(dict(path=rel,ext=ext,code=c,comment=cm,doc=d,blank=b))
json.dump(rows,open(sys.argv[2],'w'))
