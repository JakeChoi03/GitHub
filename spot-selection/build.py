import json,math
u=json.load(open('unique.json'))
K=(35.71108,139.79635)
def hav(a,b,c,d):
    R=6371000;p=math.radians
    x=math.sin(p(c-a)/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(p(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))
# approximate Sumida River centreline (lat,lng), south->north
RIVER=[(35.6945,139.7905),(35.7015,139.7955),(35.7055,139.7965),(35.7083,139.7978),(35.7102,139.7990),(35.7150,139.8020),(35.7175,139.8040),(35.7250,139.8100)]
def river_lng(lat):
    for (a,b),(c,d) in zip(RIVER,RIVER[1:]):
        if a<=lat<=c: return b+(d-b)*(lat-a)/(c-a)
    return RIVER[0][1] if lat<RIVER[0][0] else RIVER[-1][1]
# public, non-commercial spots (manual curation). value = (app category, type)
PUBLIC={
 'Sensō-ji':('Sightseeing','Temple'),'Kaminarimon Gate':('Sightseeing','Landmark'),'Nakamise Shopping Street':('Shopping','Shopping street'),
 'Kappabashi Kitchen Supply Town':('Shopping','Shopping street'),'Asakusa Shrine':('Sightseeing','Shrine'),
 'Asakusa Culture Tourist Information Center':('Sightseeing','Public observation terrace'),'Imado Shrine':('Sightseeing','Shrine'),
 'Ōtori Shrine':('Sightseeing','Shrine'),'Senso-ji Hozomon Gate':('Sightseeing','Landmark'),'Matsuchiyama Shoden':('Sightseeing','Temple'),
 'Shitaya Shrine':('Sightseeing','Shrine'),'Torikoe Shrine':('Sightseeing','Shrine'),'Yoshiwara Shrine':('Sightseeing','Shrine'),
 'Kuramae Shrine':('Sightseeing','Shrine'),'Higashi Hongan-ji':('Sightseeing','Temple'),'Asakusa Underground Street':('Shopping','Shopping street'),
 'Sensō-ji Five-Storied Pagoda':('Sightseeing','Landmark'),'Iriya South Park':('Sightseeing','Park'),'Yasaki Inari Shrine':('Sightseeing','Shrine'),
 'Asakusa Shin-Nakamise Shopping Street':('Shopping','Shopping street'),'Akiba Shrine':('Sightseeing','Shrine'),
 'Edo Taitō Traditional Crafts Museum':('Experience','Museum (free)'),'Asakusa Fuji Sengen-jinja Shrine':('Sightseeing','Shrine'),
 'Hikan Inari-jinja Shrine':('Sightseeing','Shrine'),'Azuma Bridge':('Sightseeing','Bridge'),'Senzoku Park':('Sightseeing','Park'),
 'Asakusa Nishi-sandō Shopping Street':('Shopping','Shopping street'),'The Yogodo Hall':('Sightseeing','Temple'),
 'Seika Park':('Sightseeing','Park'),'Sumida River Ryokudō Park':('Sightseeing','Park'),'Komagata Bridge':('Sightseeing','Bridge'),
 'Kappabashi Hondōri Shopping Street':('Shopping','Shopping street'),'Komagatado':('Sightseeing','Temple'),'Sogenji Temple':('Sightseeing','Temple'),
 'Benten-dō':('Sightseeing','Temple'),'Higirijizoson':('Sightseeing','Temple'),'Orange Street':('Shopping','Shopping street'),
 'Bentenyama Children\'s Park':('Sightseeing','Park'),'Kan\'non-dōri':('Shopping','Shopping street'),'Seisuiji':('Sightseeing','Temple'),
 'Hoppy Street ホッピー通り':('Gourmet','Food street'),'Mitsumine-jinja Shrine':('Sightseeing','Shrine'),'Honkakuji':('Sightseeing','Temple'),
 'Sensōji Chingodō':('Sightseeing','Temple'),'Kuramae Park':('Sightseeing','Park'),'Asakusakomagatasuwa Shrine':('Sightseeing','Shrine'),
 'Tawara Park':('Sightseeing','Park'),'Tanuki Street':('Shopping','Shopping street'),'Nishi-Asakusa Hachiman Shrine':('Sightseeing','Shrine'),
 'Denboin Street':('Shopping','Shopping street'),'Manryuji Temple':('Sightseeing','Temple'),'Matsuba Park':('Sightseeing','Park'),
 'Miyamoto-Unosuke Drum Museum':('Experience','Museum'),'Asakusa Hisago-dori Shopping Street':('Shopping','Shopping street'),
 'World Bags & Luggage Museum':('Experience','Museum (free)'),'Dairokuten Sakaki Shrine':('Sightseeing','Shrine'),
}
# same-place duplicates merged into parent
MERGE={'Matsuchiyamashoten Park':'Matsuchiyama Shoden','Asakusa Culture Tourist Center Observation Terrace':'Asakusa Culture Tourist Information Center'}
best={}
for x in u:
    t=x['title']
    if t not in PUBLIC or x.get('permanentlyClosed') or x.get('temporarilyClosed'): continue
    if t in best and (best[t].get('reviewsCount') or 0)>=(x.get('reviewsCount') or 0): continue
    best[t]=x
rows=[]
for t,x in best.items():
    lat,lng=x['lat'],x['lng']; r=x.get('reviewsCount') or 0
    d=hav(K[0],K[1],lat,lng)
    west = lng < river_lng(lat)
    if d>1500 or not west or r<50: continue
    rows.append(dict(name=t,app_category=PUBLIC[t][0],type=PUBLIC[t][1],reviews=r,rating=x.get('totalScore'),lat=lat,lng=lng,dist_kaminarimon_m=round(d)))
rows.sort(key=lambda r:-r['reviews'])
# Jenks natural breaks (2 classes) on log10(reviews)
v=sorted(math.log10(r['reviews']) for r in rows)
def ssd(a): m=sum(a)/len(a); return sum((y-m)**2 for y in a)
best_k=min(range(1,len(v)),key=lambda k:ssd(v[:k])+ssd(v[k:]))
thr=10**v[best_k]
# also 3-class jenks for reference
n=len(v); b3=min(((i,j) for i in range(1,n-1) for j in range(i+1,n)),key=lambda ij:ssd(v[:ij[0]])+ssd(v[ij[0]:ij[1]])+ssd(v[ij[1]:]))
print('n',n,'2-class threshold',round(thr),' 3-class thresholds',round(10**v[b3[0]]),round(10**v[b3[1]]))
q75=sorted(r['reviews'] for r in rows)[int(0.75*n)]
print('top-quartile threshold',q75)
json.dump(dict(rows=rows,thr2=thr,thr3=[10**v[b3[0]],10**v[b3[1]]],q75=q75),open('rows.json','w'),ensure_ascii=False)
for r in rows: print(r['reviews'],r['dist_kaminarimon_m'],r['type'],'|',r['name'])
