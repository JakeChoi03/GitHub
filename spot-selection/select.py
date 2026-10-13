import json,math
D=json.load(open('rows.json')); rows=D['rows']; t_hi,t_mid=round(D['thr3'][1]),round(D['thr3'][0])
def hav(a,b,c,d):
    R=6371000;p=math.radians
    x=math.sin(p(c-a)/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(p(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))
dist=lambda r,s: hav(r['lat'],r['lng'],s['lat'],s['lng'])
for r in rows:
    r['jenks_class']='High' if r['reviews']>=t_hi else ('Medium' if r['reviews']>=t_mid else 'Low')
    r['label']='Popular' if r['jenks_class']=='High' else 'Less popular'
pop=[r for r in rows if r['label']=='Popular']
for r in rows:
    r['dist_nearest_popular_m']=0 if r['label']=='Popular' else round(min(dist(r,p) for p in pop))
# select checkpoints: popular first (by reviews), then less popular; min spacing 300 m
sel=[]
def ok(r): return all(dist(r,s)>=300 for s in sel)
for r in [p for p in rows if p['label']=='Popular']:
    if ok(r): sel.append(r); r['note']='Selected (popular checkpoint)'
    else: r['note']='Within 300 m of '+min(sel,key=lambda s:dist(r,s))['name']+' - merged into that checkpoint'
for r in [p for p in rows if p['label']!='Popular']:
    if not (300<=r['dist_nearest_popular_m']<=1500): r['note']='Excluded: <300 m from a popular spot'; continue
    if ok(r): sel.append(r); r['note']='Selected (less popular checkpoint)'
    else: r['note']='Excluded: <300 m from selected '+min(sel,key=lambda s:dist(r,s))['name']
for r in rows: r['selected']= r['note'].startswith('Selected')
S=[r for r in rows if r['selected']]
print(len(rows),'candidates;',len(S),'selected')
for r in S: print(f"{r['label']:13} {r['jenks_class']:6} {r['reviews']:>6} {r['dist_nearest_popular_m']:>5}m {r['type']:22} {r['name']}")
mind=min(dist(a,b) for i,a in enumerate(S) for b in S[i+1:]); print('min pairwise',round(mind))
json.dump(dict(rows=rows,t_hi=t_hi,t_mid=t_mid),open('final.json','w'),ensure_ascii=False)
