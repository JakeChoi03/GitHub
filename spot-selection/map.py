import json,math
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows=json.load(open('final.json'))['rows']
# same approximate Sumida River centreline used for the west-bank filter in build.py
RIVER=[(35.6945,139.7905),(35.7015,139.7955),(35.7055,139.7965),(35.7083,139.7978),(35.7102,139.7990),(35.7150,139.8020),(35.7175,139.8040),(35.7250,139.8100)]
fig,ax=plt.subplots(figsize=(9,9))
ax.plot([p[1] for p in RIVER],[p[0] for p in RIVER],color='#7fb3d5',lw=2.5,alpha=.8,label='Sumida River centreline (approx.)')
K=(35.71108,139.79635); t=[i/100*2*math.pi for i in range(101)]
ring=lambda la,lo,m:([lo+m/(111320*math.cos(math.radians(la)))*math.cos(a) for a in t],[la+m/110574*math.sin(a) for a in t])
ax.plot(*ring(*K,1500),'--',color='grey',lw=1,label='1.5 km study area')
for r in rows:
    if not r['selected']: ax.scatter(r['lng'],r['lat'],s=12,color='#bbbbbb',zorder=2)
off={'Imado Shrine':(6,-10),'Asakusa Fuji Sengen-jinja Shrine':(-60,8),'Kappabashi Kitchen Supply Town':(-40,-14),'Dairokuten Sakaki Shrine':(6,-10)}
for r in rows:
    if not r['selected']: continue
    pop=r['label']=='Popular'; c='#d62728' if pop else '#1f77b4'
    ax.scatter(r['lng'],r['lat'],s=40+math.log10(r['reviews'])*40,color=c,edgecolor='white',zorder=3)
    ax.plot(*ring(r['lat'],r['lng'],300),color=c,lw=.5,alpha=.4)
    ax.annotate(f"{r['name']} ({r['reviews']:,})",(r['lng'],r['lat']),xytext=off.get(r['name'],(6,4)),textcoords='offset points',fontsize=7.5)
ax.scatter([],[],color='#d62728',label='Popular checkpoint'); ax.scatter([],[],color='#1f77b4',label='Less popular checkpoint'); ax.scatter([],[],color='#bbbbbb',s=12,label='Other candidate (not selected)')
ax.set_aspect(1/math.cos(math.radians(K[0]))); ax.legend(loc='lower left',fontsize=8)
ax.set_title('Asakusa study area: selected checkpoints\n(Google Maps review count in brackets; rings = 300 m)',fontsize=11)
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude'); ax.grid(alpha=.2)
plt.tight_layout(); plt.savefig('asakusa_spots_map.png',dpi=160)
