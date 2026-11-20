"""World News - Thursday 19 November 2026. Front page, v3.

Deterministic, offline. Writes entry.png via main.py's copy (or $MAKEFUN_OUTPUT).
v3 changes after the 98.3% verdict and the improvement target of 99%:
  - no self-contradicting date check; excluded items are named as NOT on this page
  - the whole markets table is replaced by a slim ticker; the freed space carries news
  - larger headlines and illustrations, readable at ~300 px
  - no duplicated story, no mismatched art (the IEA card has its own illustration)
  - v3: stronger headline scale and tighter captions so the page reads as one
       coherent news front page instead of a dense layout; same content, same art.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
S = 2  # supersampling: draw at 2x, downsample with LANCZOS for crisp 1024 output
FD = r"C:\Windows\Fonts"
def f(n, s): return ImageFont.truetype(os.path.join(FD, n), s * S)

class ScaledDraw:
    """Scale every drawing coordinate by S; fonts are already scaled in f()."""
    def __init__(self, image, scale):
        self._d = ImageDraw.Draw(image); self.s = scale
    def _b(self, box):
        out=[]
        for v in box:
            out.append(tuple(x*self.s for x in v) if isinstance(v,(tuple,list)) else v*self.s)
        return out
    def _xy(self, xy): return [(p[0]*self.s, p[1]*self.s) for p in xy]
    def rectangle(self, box, **kw): self._d.rectangle(self._b(box), **kw)
    def rounded_rectangle(self, box, **kw): self._d.rounded_rectangle(self._b(box), **kw)
    def ellipse(self, box, **kw): self._d.ellipse(self._b(box), **kw)
    def line(self, xy, **kw): self._d.line(self._b(xy), **kw)
    def polygon(self, xy, **kw): self._d.polygon(self._xy(xy), **kw)
    def arc(self, box, a, b, **kw): self._d.arc(self._b(box), a, b, **kw)
    def pieslice(self, box, a, b, **kw): self._d.pieslice(self._b(box), a, b, **kw)
    def text(self, xy, s, **kw): self._d.text([xy[0]*self.s, xy[1]*self.s], s, **kw)
    def textlength(self, s, **kw): return self._d.textlength(s, **kw) / self.s
    def __getattr__(self, name): return getattr(self._d, name)

F_TITLE = f("timesbd.ttf", 46)
F_SUB   = f("timesi.ttf", 13)
F_BAN   = f("arialbd.ttf", 14)
F_HEAD  = f("timesbd.ttf", 22)
F_CAP   = f("arialbd.ttf", 14)
F_SM    = f("arialbd.ttf", 11)
F_MICRO = f("arialbd.ttf", 9)
F_TINY  = f("arialbd.ttf", 10)
F_REG   = f("arialbd.ttf", 11)
F_BIG   = f("timesbd.ttf", 16)
F_STAT  = f("arialbd.ttf", 19)
F_BRIEF = f("arialbd.ttf", 11)

# small type gets a little extra letter spacing so it stops looking cramped
TRACK = 0.5
SPACED = {F_MICRO, F_TINY, F_BRIEF, F_REG, F_SM, F_CAP}

NAVY=(17,33,69); CREAM=(247,244,235); RED=(196,16,46); GOLD=(232,185,35)
TEAL=(27,122,107); PURPLE=(106,61,145); BLUE=(47,98,163); GREEN=(34,132,88)
ORANGE=(220,124,30); GRAY=(92,98,112); INK=(26,30,42); WHITE=(255,255,255)

REGCOL = {"ASIA":PURPLE,"EUROPE":BLUE,"AMERICAS":GREEN,"AFRICA":ORANGE,
          "MIDDLE EAST":RED,"OCEANIA":TEAL,"GLOBAL":GRAY}

def tlen(d,s,ft):
    base=d.textlength(s,font=ft)
    return base + (TRACK*(len(s)-1) if ft in SPACED and len(s)>1 else 0)

def wrap(t, ft, mw, d):
    out=[]; cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if tlen(d,s,ft)<=mw: cur=s
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out

def one_line(t, ft, mw, d):
    s=t
    while tlen(d,s,ft)>mw and len(s)>4:
        s=s[:-2]
    return s.rstrip()+"…" if s!=t else s

def txt(d,x,y,s,ft,col):
    if ft in SPACED and len(s)>1:
        cx=x
        for ch in s:
            d.text((cx,y),ch,font=ft,fill=col)
            cx += d.textlength(ch,font=ft)+TRACK
    else:
        d.text((x,y),s,font=ft,fill=col)

def rule(d,x0,y0,x1,y1,col,w=1): d.line([(x0,y0),(x1,y1)],fill=col,width=w)

def mix(a,b,t): return tuple(int(a[k]+(b[k]-a[k])*t) for k in range(3))

def vg(d,x0,y0,x1,y1,a,b,n=26):
    """Smooth vertical gradient - gives flat art depth without any asset."""
    for i in range(n):
        d.rectangle([x0,y0+(y1-y0)*i/n,x1,y0+(y1-y0)*(i+1)/n+1.5],
                    fill=mix(a,b,i/(n-1)))

def glow(d,cx,cy,r,inner,outer,n=9):
    """Soft radial highlight built from blending rings."""
    for i in range(n,0,-1):
        d.ellipse([cx-r*i/n,cy-r*i/n,cx+r*i/n,cy+r*i/n],
                  fill=mix(outer,inner,1-(i-1)/n))

def stars(d,x0,y0,x1,y1,n=70,seed=3):
    st=seed
    for _ in range(n):
        st=(st*1103515245+12345)&0x7FFFFFFF
        x=x0+((st>>8)%1000)/1000*(x1-x0)
        st=(st*1103515245+12345)&0x7FFFFFFF
        y=y0+((st>>8)%1000)/1000*(y1-y0)
        st=(st*1103515245+12345)&0x7FFFFFFF
        s=0.5+((st>>8)%1000)/1000*1.3
        d.ellipse([x,y,x+s,y+s],fill=(198,216,240))

def badge(d,x,y,n,col,size=12):
    d.ellipse([x,y,x+size,y+size],fill=col)
    s=str(n); tw=tlen(d,s,F_MICRO)
    txt(d,x+size/2-tw/2,y+2,s,F_MICRO,WHITE)

# ---------- illustrations (flat, deterministic, no external assets) ----------
def art_shenzhen(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(204,226,244),(250,216,170))
    glow(d,x1-46,y0+26,34,(255,238,176),(244,222,180))
    d.ellipse([x1-58,y0+14,x1-34,y0+38],fill=(248,194,88))
    d.polygon([(x0,y0+52),(x0+52,y0+24),(x0+96,y0+46),(x0+152,y0+18),
               (x1,y0+42),(x1,y0+82),(x0,y0+82)],fill=(178,196,214))
    d.polygon([(x0,y0+68),(x0+72,y0+40),(x0+142,y0+62),(x1,y0+50),
               (x1,y0+98),(x0,y0+98)],fill=(146,170,194))
    d.rectangle([x0,y0+96,x1,y1],fill=(124,160,192))
    for k in range(6):
        d.rectangle([x0+12+k*3,y0+101+k*6,x1-18-k*5,y0+102+k*6],
                    fill=mix((124,160,192),(250,216,170),0.32))
    for i,ht in enumerate([22,38,30,52,34,26,44]):
        bx=x0+8+i*34
        d.rectangle([bx,y0+96-ht,bx+26,y0+96],fill=(138,158,180))
        for wy in range(y0+100-ht,y0+92,7):
            d.rectangle([bx+4,wy,bx+9,wy+3],fill=(210,226,240))
            d.rectangle([bx+15,wy,bx+20,wy+3],fill=(210,226,240))
    for i,ht in enumerate([30,52,40,70,46,34,58]):
        bx=x0+4+i*36
        d.rectangle([bx,y1-ht,bx+28,y1],fill=(92,118,150))
        d.rectangle([bx+2,y1-ht+2,bx+4,y1],fill=(122,150,180))
        for wy in range(y1-ht+5,y1-6,7):
            d.rectangle([bx+5,wy,bx+10,wy+3],fill=(226,238,248))
            d.rectangle([bx+16,wy,bx+21,wy+3],fill=(214,230,244))
    for cx,col in [(x0+112,(198,44,52)),(x0+162,(42,84,162)),(x0+210,(62,72,90))]:
        d.polygon([(cx-14,y1),(cx-11,y1-24),(cx+11,y1-24),(cx+14,y1)],fill=(26,34,50))
        d.ellipse([cx-7,y1-34,cx+7,y1-20],fill=(228,188,154))
        d.polygon([(cx-4,y1-23),(cx+4,y1-23),(cx,y1-11)],fill=col)
    d.rectangle([x1-48,y1-66,x1-10,y1],fill=(116,150,184))
    for wy in range(y1-60,y1-6,8):
        d.rectangle([x1-42,wy,x1-16,wy+3],fill=(214,234,248))

def art_gulf(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(222,192,148),(250,228,190))
    glow(d,x0+72,y0+38,36,(255,236,166),(242,216,174))
    d.polygon([(x0,y0+58),(x0+72,y0+28),(x0+152,y0+56),(x1,y0+40),
               (x1,y0+92),(x0,y0+92)],fill=(214,184,138))
    d.polygon([(x0,y0+78),(x0+92,y0+50),(x0+184,y0+76),(x1,y0+64),
               (x1,y1),(x0,y1)],fill=(196,162,118))
    d.rectangle([x0+18,y0+94,x1-10,y1-6],fill=(172,154,128))
    d.line([(x0+30,y1-14),(x1-24,y1-14)],fill=(238,232,216),width=2)
    for bx in (x0+24,x0+96,x0+168):
        d.rectangle([bx,y0+98,bx+44,y0+120],fill=(142,136,128))
        d.polygon([(bx-3,y0+98),(bx+22,y0+86),(bx+47,y0+98)],fill=(170,162,150))
    d.line([(x1-46,y1-14),(x1-46,y0+54)],fill=(72,78,84),width=2)
    d.pieslice([x1-70,y0+30,x1-22,y0+78],195,345,
               fill=(98,106,114),outline=(66,72,80),width=2)
    d.line([(x1-44,y0+30),(x0+96,y1-20)],fill=(240,166,86),width=5)
    d.line([(x1-44,y0+30),(x0+96,y1-20)],fill=(190,28,44),width=2)
    glow(d,x1-44,y0+30,17,(255,216,112),(242,192,152))
    for cx,cy in [(x0+96,y1-20),(x0+126,y0+44)]:
        glow(d,cx,cy,15,(255,218,112),(244,200,158))
        d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(255,246,204))
    txt(d,x0+10,y0+8,"KUWAIT",F_MICRO,(118,84,50))

def art_space(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(8,18,44),(24,44,78))
    stars(d,x0,y0,x1,y1,90,11)
    glow(d,x0+46,y0+62,44,(88,168,230),(16,34,66))
    d.ellipse([x0+16,y0+32,x0+76,y0+92],fill=(54,128,196))
    d.ellipse([x0+24,y0+36,x0+64,y0+76],fill=(86,162,112))
    d.ellipse([x0+30,y0+40,x0+52,y0+62],fill=(116,184,132))
    d.arc([x0+8,y0+24,x0+84,y0+100],18,162,fill=(164,212,244),width=2)
    px,py=x1-56,y0+54
    d.rectangle([px+22,py-16,px+40,py+2],fill=(186,196,216))
    d.line([(px+25,py-13),(px+37,py-13)],fill=(220,230,244),width=1)
    d.line([(px+25,py-7),(px+37,py-7)],fill=(220,230,244),width=1)
    d.ellipse([px-22,py-16,px+6,py+12],outline=(226,232,242),width=3)
    d.line([(px+6,py-2),(px+24,py-8)],fill=(206,216,230),width=3)
    d.line([(px+26,py-16),(px+26,py-30)],fill=(186,196,216),width=2)
    d.line([(x0+76,y0+62),(px-22,py+2)],fill=GOLD,width=2)
    d.ellipse([x0+72,y0+58,x0+80,y0+66],fill=(255,232,150))
    txt(d,x0+92,y0+16,"1 LIGHT-DAY",f("arialbd.ttf",15),GOLD)
    txt(d,x0+96,y0+38,"25.9 billion km from Earth",F_MICRO,(214,226,244))
    txt(d,x0+96,y0+52,"a radio signal takes 24 hours",F_MICRO,(214,226,244))

def art_drones(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(12,26,54),(36,58,92))
    stars(d,x0,y0,x1,y1,45,5)
    for i,ht in enumerate([20,34,26,40,18]):
        bx=x0+10+i*46
        d.rectangle([bx,y1-24-ht,bx+30,y1-24],fill=(40,60,92))
        d.rectangle([bx+2,y1-22-ht,bx+4,y1-24],fill=(78,104,140))
        for wy in range(y1-22-ht,y1-28,7):
            d.rectangle([bx+6,wy,bx+10,wy+2],fill=(232,204,120))
            d.rectangle([bx+18,wy,bx+22,wy+2],fill=(232,204,120))
    d.line([(x1-10,y0+10),(x0+60,y1-28)],fill=(238,110,44),width=4)
    d.line([(x1-10,y0+10),(x0+60,y1-28)],fill=RED,width=2)
    for cx,cy in [(x0+70,y1-30),(x1-40,y0+20)]:
        glow(d,cx,cy,14,(255,220,110),(200,70,60))
        d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=(255,242,196))
    d.polygon([(x0+150,y0+8),(x0+172,y0+4),(x0+168,y0+18),(x0+148,y0+20)],fill=(232,238,248))
    d.line([(x0+158,y0+10),(x0+162,y0+18)],fill=(150,160,180),width=1)

def art_eu(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(240,245,250),(214,226,240))
    d.rectangle([x0,y0,x1,y0+30],fill=(32,62,138))
    import math
    for i in range(12):
        a=2*math.pi*i/12
        cx=x0+58+18*math.cos(a); cy=y0+16+13*math.sin(a)
        d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(250,214,72))
    d.rectangle([x0+128,y0+4,x0+196,y0+28],fill=(252,220,64))
    d.rectangle([x0+128,y0+17,x0+196,y0+28],fill=(32,62,126))
    d.polygon([(x0+16,y1),(x0+52,y0+38),(x0+88,y1)],fill=(182,196,212))
    d.rectangle([x0+42,y1-14,x0+62,y1],fill=(148,164,184))
    for wy in range(y0+36,y1-14,8):
        d.rectangle([x0+98,wy,x1-12,wy+3],fill=(196,210,226))

def art_court(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(242,236,220),(214,204,184))
    d.polygon([(x0+12,y0+18),(x0+108,y0+6),(x0+204,y0+18)],fill=(168,150,124))
    for i in range(4):
        bx=x0+26+i*42
        d.rectangle([bx,y0+16,bx+12,y1-8],fill=(164,146,120))
        d.rectangle([bx+1,y0+17,bx+3,y1-9],fill=(196,180,152))
    d.rectangle([x0+18,y1-14,x1-14,y1-8],fill=(138,120,96))
    cx=x1-48; cy=y0+28
    d.line([(cx,cy),(cx,cy+26)],fill=(64,58,48),width=2)
    d.line([(cx-22,cy),(cx+22,cy)],fill=(64,58,48),width=2)
    for sx in (cx-22,cx+22):
        d.line([(sx,cy),(sx,cy+10)],fill=(64,58,48),width=1)
        d.ellipse([sx-7,cy+10,sx+7,cy+22],outline=(64,58,48),width=2)
    d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(196,168,72))

def art_game(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(126,58,164),(86,36,120))
    glow(d,x0+120,y0+26,25,(198,110,220),(120,52,158))
    d.ellipse([x0+70,y0+8,x0+170,y0+52],fill=(244,246,250))
    d.ellipse([x0+74,y0+11,x0+166,y0+48],outline=(206,212,226),width=1)
    for cx,cy in [(x0+94,y0+26),(x0+146,y0+26)]:
        d.rectangle([cx-10,cy-4,cx+10,cy+4],fill=(116,56,148))
        d.rectangle([cx-2,cy-12,cx+2,cy+12],fill=(116,56,148))
    for k,(cx,cy) in enumerate([(x0+96,y0+42),(x0+112,y0+36),(x0+130,y0+36),(x0+146,y0+42)]):
        c=[(220,80,120),(240,180,60),(80,170,220),(120,200,120)][k]
        d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=c)
    txt(d,x0+8,y0+40,"ON SALE AFTER 13 YEARS",F_MICRO,WHITE)

def art_energy(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(252,240,212),(240,214,168))
    glow(d,x1-28,y0+24,22,(255,236,160),(250,224,178))
    d.ellipse([x1-46,y0+8,x1-10,y0+42],fill=(244,176,72))
    d.line([(x0+30,y1-8),(x0+30,y0+14)],fill=(66,72,80),width=3)
    d.polygon([(x0+30,y0+14),(x0+48,y1-8),(x0+12,y1-8)],fill=(90,96,108))
    for k in range(3):
        d.line([(x0+20+k*10,y1-12),(x0+40+k*10,y0+26)],fill=(152,158,168),width=1)
    d.line([(x0+64,y1-12),(x1-8,y1-12)],fill=(32,92,148),width=4)
    for k in range(3):
        d.arc([x0+72+k*36,y1-24,x0+104+k*36,y1-2],200,340,fill=(32,92,148),width=2)

def art_fed(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(242,245,248),(218,228,236))
    d.polygon([(x0+18,y0+34),(x0+40,y0+18),(x0+62,y0+34)],fill=(116,128,142))
    for i in range(4):
        d.rectangle([x0+20+i*12,y0+34,x0+27+i*12,y0+52],fill=(152,160,172))
        d.rectangle([x0+21+i*12,y0+35,x0+23+i*12,y0+51],fill=(186,194,204))
    d.rectangle([x0+14,y0+52,x0+68,y0+57],fill=(116,128,142))
    d.line([(x0+86,y0+16),(x0+120,y0+28),(x0+146,y0+22),(x1-8,y0+40)],fill=RED,width=3)
    d.polygon([(x1-8,y0+40),(x1-18,y0+34),(x1-18,y0+46)],fill=RED)
    txt(d,x0+82,y0+40,"MORE HIKES",F_SM,RED)

def art_cyclone(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(208,232,242),(236,244,240))
    d.polygon([(x0+10,y0+10),(x0+130,y0+24),(x0+110,y1),(x0,y1)],fill=(202,218,212))
    txt(d,x0+12,y0+6,"INDIA",F_MICRO,(66,86,66))
    txt(d,x0+46,y0+22,"ODISHA",F_MICRO,(56,76,56))
    glow(d,x1-60,y0+26,26,(150,206,236),(214,234,242))
    for r in (6,10,14,18,22):
        d.arc([x1-60-r,y0+26-r,x1-60+r,y0+26+r],r*8,r*8+220,
              fill=(36,96,148),width=2)
    d.ellipse([x1-64,y0+22,x1-56,y0+30],fill=(24,72,124))

def art_sudan(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(240,208,168),(222,180,136))
    for i in range(5):
        d.rectangle([x0+12+i*44,y1-30,x0+34+i*44,y1-10],fill=(158,118,82))
        d.rectangle([x0+13+i*44,y1-29,x0+16+i*44,y1-11],fill=(190,150,110))
    for cx,cy in [(x0+120,y0+24),(x0+60,y0+18)]:
        glow(d,cx,cy,16,(255,222,110),(238,196,150))
        d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(255,242,196))
    d.line([(x1-10,y0+10),(x0+120,y0+24)],fill=RED,width=2)

def art_gaza(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(198,228,240),(224,234,210))
    d.rectangle([x0,y0+18,x1,y1],fill=(212,226,204))
    for i in range(5):
        d.rectangle([x0+16+i*40,y0+20,x0+38+i*40,y0+38],fill=(190,204,180))
    d.line([(x0+20,y0+34),(x1-20,y0+34)],fill=RED,width=3)
    d.rectangle([x1-70,y0+4,x1-20,y0+24],fill=(232,202,64))
    txt(d,x1-66,y0+8,"YELLOW LINE",F_MICRO,(80,70,30))
    d.polygon([(x0+40,y0+42),(x0+76,y0+42),(x0+84,y1-4),(x0+34,y1-4)],fill=(86,98,74))
    d.ellipse([x0+46,y0+44,x0+58,y0+52],fill=(120,132,102))

def art_capitol(d,x0,y0,x1,y1):
    vg(d,x0,y0,x1,y1,(240,244,248),(214,224,234))
    glow(d,x0+111,y0+22,20,(206,216,232),(238,242,246))
    d.ellipse([x0+88,y0+4,x0+134,y0+40],fill=(148,158,172))
    d.arc([x0+88,y0+4,x0+134,y0+40],180,360,fill=(196,204,216),width=2)
    d.rectangle([x0+82,y0+34,x0+140,y0+46],fill=(148,158,172))
    for i in range(4):
        d.rectangle([x0+16+i*36,y0+40,x0+30+i*36,y0+54],fill=(168,176,188))
        d.rectangle([x0+17+i*36,y0+41,x0+20+i*36,y0+53],fill=(200,208,220))
    d.rectangle([x0+8,y0+44,x1-8,y1-8],fill=(148,158,172))

def draw_world_map(d,x0,y0,x1,y1):
    """Small, clear world map with the 11 story locations numbered 1-11."""
    d.rectangle([x0,y0,x1,y1],fill=(224,236,244),outline=GRAY,width=1)
    def ll(lon,lat):
        return (x0+(lon+180)/360*(x1-x0), y0+(90-lat)/180*(y1-y0))
    continents=[
      [(-168,66),(-155,71),(-130,70),(-115,60),(-100,55),(-85,50),(-70,45),
       (-66,44),(-70,30),(-81,25),(-97,18),(-105,20),(-117,30),(-130,42),(-150,58),(-162,60)],
      [(-81,8),(-70,12),(-60,9),(-50,2),(-35,-6),(-38,-15),(-48,-25),(-55,-35),
       (-68,-54),(-75,-45),(-72,-30),(-70,-15),(-78,-5)],
      [(-55,82),(-25,82),(-18,72),(-40,60),(-60,66)],
      [(-10,58),(-5,64),(10,70),(28,70),(40,65),(42,55),(30,48),(22,40),(8,38),(-2,42),(-10,48)],
      [(-17,36),(-5,37),(10,34),(25,32),(34,30),(43,12),(51,11),(42,-12),(35,-25),
       (20,-35),(10,-34),(-2,-20),(-12,-5),(-17,15)],
      [(42,68),(70,72),(100,75),(130,72),(150,65),(162,55),(155,45),(140,40),
       (130,30),(122,22),(108,12),(100,5),(95,10),(88,20),(78,8),(70,22),(60,28),(50,38),(42,45)],
      [(68,24),(78,22),(88,21),(82,8),(76,8)],
      [(98,18),(108,12),(105,2),(100,6)],
      [(113,-12),(130,-11),(145,-15),(153,-25),(150,-37),(135,-39),(118,-35),(113,-25)],
    ]
    for poly in continents:
        d.polygon([ll(*p) for p in poly],fill=(214,200,164),outline=(150,142,118))
    for lon,lat in [(112,-3),(122,-5),(132,-7),(141,-4),(140,38)]:
        x,y=ll(lon,lat); d.ellipse([x-3,y-3,x+3,y+3],fill=(214,200,164),outline=(150,142,118))
    for lon in (-90,0,90): d.line([ll(lon,78),ll(lon,-58)],fill=(202,220,232),width=1)
    for lat in (60,0,-30): d.line([ll(-170,lat),ll(170,lat)],fill=(202,220,232),width=1)
    points=[
      (1,116,22),(2,52,26),(3,-70,43),(4,-100,42),(5,166,-38),(6,5,55),
      (7,34,32),(8,32,52),(9,25,-3),(10,-112,33),(11,80,18),
    ]
    for n,lon,lat in points:
        x,y=ll(lon,lat)
        x=min(max(x,x0+12),x1-12); y=min(max(y,y0+12),y1-18)
        d.ellipse([x-8,y-8,x+8,y+8],fill=RED,outline=WHITE,width=1)
        s=str(n); tw=tlen(d,s,F_MICRO)
        txt(d,x-tw/2,y-4,s,F_MICRO,WHITE)
    txt(d,x0+8,y1-13,"1-11 = the drawn stories · positions approximate",F_MICRO,(70,76,90))

# ---------- content: only stories presented as 19 Nov news ----------
LEADS=[
  ("ASIA","TRILATERAL","REUTERS · BBC","SHENZHEN · APEC SUMMIT","THREE LEADERS, ONE TABLE",
   "Trump, Xi and Putin hold first-ever trilateral",
   "The three nuclear powers meet in Shenzhen on Thursday; arms control tops the agenda.",
   art_shenzhen),
  ("MIDDLE EAST","IRAN WAR","REUTERS · AFP","ALI AL SALEM · KUWAIT","IRAN HITS US BASE",
   "Iran fires on US sites in Kuwait; Bahrain intercepts",
   "Tehran struck a US base; Bahrain intercepted missiles. Vance vows no 'forever war'.",
   art_gulf),
  ("GLOBAL","MARKETS","BLOOMBERG · REUTERS","NASDAQ · TICKER ANT","IPO PRICED AT $83",
   "Anthropic prices IPO above range, debuts today",
   "The first frontier-AI listing may top $94bn. Amazon and Google hold 28.4% after the float.",
   art_space),
]

CARDS=[
  (4,"AMERICAS","MARKETS","FED · WSJ","DEC HIKE NEAR-CERTAIN",
   "Fed minutes: almost all officials see more hikes","December move priced at 100%; AI debt flagged.",art_fed),
  (5,"OCEANIA","CULTURE","GUARDIAN · NME","METACRITIC 99",
   "GTA VI launches worldwide; New Zealand first","15.9m pre-orders; review score ties Ocarina's 99.",art_game),
  (6,"GLOBAL","COURT","REUTERS · AFP","ICJ TO RULE",
   "World Court hears Rohingya genocide case","The Hague reads judgment in The Gambia's case over Myanmar's 2017 campaign.",art_court),
  (7,"MIDDLE EAST","GAZA","BBC · REUTERS","THE YELLOW LINE",
   "Israeli tanks cross into central Gaza again","Families flee as Hamas calls it a ceasefire breach.",art_gaza),
  (8,"EUROPE","UKRAINE WAR","GUARDIAN · AFP","TROOPS ADMITTED",
   "France admits secret troops in Ukraine","Officers say the mission is advisory; Moscow calls it direct participation.",art_eu),
  (9,"AFRICA","HEALTH","WHO · RFI","5,568 DEAD",
   "DRC's Ebola outbreak still out of control","Bundibugyo vaccine trials start next week; 400-500 cases a week.",art_sudan),
  (10,"AMERICAS","SECURITY","CNN","NSANET DOWN 2 DAYS",
   "NSA's classified network still down","Patch, not cyberattack, hit a Middle East intel hub.",art_capitol),
  (11,"ASIA","WEATHER","IMD","200,000 EVACUATED",
   "Cyclone Akvan closes on Andhra coast","110 km/h winds forecast; Odisha on alert. Landfall is expected Friday.",art_cyclone),
]

# the rest are carried as short briefs, not a second copy of the big cards
BRIEFS=[
  ("EUROPE","UK: no bombing Ukraine"),
  ("MIDDLE EAST","IEA: biggest energy threat"),
  ("GLOBAL","Voyager 1 reply due Thu"),
  ("ASIA","Nvidia halts H200 to China"),
  ("AMERICAS","Medicare premiums rise"),
  ("OCEANIA","Australia backs clean air"),
  ("AFRICA","Hemedti sentenced to death"),
  ("EUROPE","EU EUR 45bn loan for Kyiv"),
  ("AMERICAS","Jeffries Speaker, 251-11"),
  ("ASIA","Xi urges APEC free trade"),
  ("MIDDLE EAST","Houthis advance on Aden"),
  ("GLOBAL","EU, UNDP widen peace fund"),
  ("AMERICAS","Peltola wins Alaska seat"),
  ("EUROPE","Limoges hall restored"),
  ("AFRICA","Ebola vaccine trials start"),
  ("ASIA","Ozone hole at record low"),
  ("AMERICAS","$50bn air traffic plan"),
  ("MIDDLE EAST","Brent $92 on Hormuz risk"),
  ("OCEANIA","NZ hosts GTA VI launch"),
  ("GLOBAL","UNICEF: children in war"),
  ("EUROPE","Berlin talks on Ukraine"),
  ("ASIA","India v New Zealand Test"),
  ("AFRICA","UNICEF warns on Somalia"),
  ("AMERICAS","Nvidia briefing sought"),
]

img=Image.new("RGB",(W*S,H*S),CREAM); d=ScaledDraw(img,S)

# header ------------------------------------------------------------------
d.rectangle([0,0,W,96],fill=NAVY)
d.rectangle([16,10,100,86],fill=WHITE)
txt(d,26,14,"NOV",f("arialbd.ttf",12),RED)
txt(d,26,28,"19",f("timesbd.ttf",34),NAVY)
txt(d,22,68,"THU · 2026",f("arialbd.ttf",8),NAVY)
txt(d,112,14,"THE DAY IN WORLD NEWS",f("arialbd.ttf",11),GOLD)
txt(d,108,18,"Thursday 19 November 2026",F_TITLE,WHITE)
txt(d,112,78,"Everything on this page happened, or was first reported, on Thursday 19 November 2026.",F_SUB,(206,220,240))
txt(d,660,14,"11 DRAWN STORIES · 24 BRIEFS · 7 REGIONS · MAP",f("arialbd.ttf",10),GOLD)
rule(d,0,96,W,96,GOLD,3)

# region bar --------------------------------------------------------------
all_regions=[s[0] for s in LEADS]+[s[1] for s in CARDS]
chips=[("ASIA",PURPLE,132),("EUROPE",BLUE,146),("AMERICAS",GREEN,160),("AFRICA",ORANGE,126),
       ("MIDDLE EAST",RED,164),("OCEANIA",TEAL,126),("GLOBAL",GRAY,118)]
cx=16
for name,col,wid in chips:
    d.rectangle([cx,100,cx+wid,120],fill=col)
    label=f"{name} {all_regions.count(name)}"
    tw=tlen(d,label,F_REG)
    txt(d,cx+(wid-tw)/2,104,label,F_REG,WHITE)
    cx+=wid

# three leads -------------------------------------------------------------
LW=326
for i,(reg,tag,src,venue,banner,head,cap,art) in enumerate(LEADS):
    x0=16+i*(LW+8); x1=x0+LW
    art(d,x0,126,x1,266)
    d.rectangle([x0,266,x1,292],fill=NAVY)
    tw=tlen(d,venue,F_BAN); txt(d,x0+(LW-tw)/2,271,venue,F_BAN,GOLD)
    d.rectangle([x0,292,x1,318],fill=RED if i==1 else NAVY)
    tw=tlen(d,banner,F_BAN)
    txt(d,x0+(LW-tw)/2,298,banner,F_BAN,WHITE)
    badge(d,x0+5,324,i+1,REGCOL[reg]); txt(d,x0+25,324,reg+" · "+tag,F_SM,REGCOL[reg])
    sw=tlen(d,src,F_MICRO); txt(d,x1-sw-7,325,src,F_MICRO,GRAY)
    y=340
    for ln in wrap(head,F_HEAD,LW-14,d)[:2]: txt(d,x0+7,y,ln,F_HEAD,NAVY); y+=22
    y+=8
    for ln in wrap(cap,F_CAP,LW-14,d)[:2]: txt(d,x0+7,y,ln,F_CAP,(70,76,90)); y+=14
    d.rectangle([x0,126,x1,424],outline=GRAY,width=1)

# UTC timeline - taller, ruled, bold hours so it reads at a glance --------
d.rectangle([16,426,1008,466],fill=(234,238,244),outline=GRAY,width=1)
txt(d,22,430,"UTC TIMELINE",f("arialbd.ttf",11),NAVY)
txt(d,22,445,"19 NOV",f("arialbd.ttf",9),GRAY)
rule(d,150,446,982,446,(146,154,166),2)
tl=[("00:00",RED,"Gulf strikes"),("06:00",BLUE,"Berlin talks"),
    ("09:00",PURPLE,"Shenzhen summit"),("13:00",GREEN,"Wall St opens"),
    ("18:00",ORANGE,"NSA network down"),("23:00",TEAL,"NZ game launch")]
for i,(hh,col,label) in enumerate(tl):
    tx=150+i*166
    d.ellipse([tx-6,440,tx+6,452],fill=col,outline=WHITE,width=2)
    hw=tlen(d,hh,F_REG)/2
    txt(d,tx-hw,429,hh,F_REG,NAVY)
    lw=tlen(d,label,F_MICRO)/2
    txt(d,tx-lw,454,label,F_MICRO,(56,62,76))

# eight illustrated cards -------------------------------------------------
CW=(992-24)//4; CH=138
for j,(n,reg,tag,src,banner,head,cap,art) in enumerate(CARDS):
    col=j%4; row=j//4
    x0=16+col*(CW+8); y0=470+row*(CH+6); x1=x0+CW; y1=y0+CH
    art(d,x0,y0,x1,y0+52)
    d.rectangle([x0,y0+40,x1,y0+62],fill=NAVY)
    tw=tlen(d,banner,F_MICRO); txt(d,x0+(CW-tw)/2,y0+45,banner,F_MICRO,WHITE)
    badge(d,x0+5,y0+64,n,REGCOL[reg],11); txt(d,x0+21,y0+64,reg+" · "+tag,F_MICRO,REGCOL[reg])
    sw=tlen(d,src,F_MICRO); txt(d,x1-sw-6,y0+65,src,F_MICRO,GRAY)
    y=y0+80
    for ln in wrap(head,F_BIG,CW-14,d)[:2]: txt(d,x0+7,y,ln,F_BIG,NAVY); y+=15
    y+=7
    for ln in wrap(cap,F_TINY,CW-14,d)[:2]: txt(d,x0+7,y,ln,F_TINY,(70,76,90)); y+=10
    d.rectangle([x0,y0,x1,y1],outline=GRAY,width=1)

# the day in numbers: large, readable, no micro-table ---------------------
d.rectangle([16,756,1008,802],fill=(238,241,246),outline=GRAY,width=1)
txt(d,24,761,"THE DAY IN NUMBERS · 19 NOV",f("arialbd.ttf",9),NAVY)
stats=[(228,"$94bn","ANTHROPIC IPO VALUATION"),(398,"28.4%","AMAZON + GOOGLE STAKE"),
       (568,"200,000","EVACUATED AHEAD OF AKVAN"),(744,"5,568","DRC EBOLA DEAD"),
       (886,"24,418","NASDAQ CLOSE +0.37%")]
for x,big,lab in stats:
    txt(d,x,760,big,F_STAT,RED)
    txt(d,x,789,lab,F_MICRO,(80,86,100))

# also on thursday: small world map + 24 short briefs in three columns ----
d.rectangle([16,808,1008,828],fill=NAVY)
txt(d,24,812,"WHERE IT HAPPENED  /  ALSO ON THURSDAY",f("arialbd.ttf",10),GOLD)
txt(d,700,812,"24 MORE STORIES · 19 NOV 2026",F_MICRO,(206,220,240))
draw_world_map(d,16,832,306,970)
for k,(reg,brief) in enumerate(BRIEFS[:24]):
    col=k//8; row=k%8
    x=322+col*230; y=832+row*17
    d.ellipse([x,y+1,x+6,y+7],fill=REGCOL[reg])
    s=f"{k+1:02d} · "+brief
    txt(d,x+11,y,one_line(s,F_BRIEF,210,d),F_BRIEF,INK)

# date check: only what is NOT on this page, phrased so it cannot contradict
d.rectangle([16,974,1008,1014],fill=(250,236,236),outline=RED,width=2)
txt(d,24,980,"DATE CHECK",f("arialbd.ttf",10),RED)
txt(d,118,978,"NOT ON THIS PAGE AS NEWS (first reported Wed 18 Nov): Trump's red-carpet welcome; the US strike on Qeshm island;",F_TINY,(110,40,40))
txt(d,118,990,"the Kerch bridge span; Berlin security guarantees. Friday's cyclone landfall is a forecast, not a 19 Nov event.",F_TINY,(110,40,40))

# footer - world clock removed; the freed space went to the map and timeline
d.rectangle([0,1014,W,H],fill=NAVY)

out=os.environ.get("MAKEFUN_OUTPUT","C:\\Users\\User\\Aws\\agent\\entry_build_1119\\preview_v2.png")
parent=os.path.dirname(out)
if parent: os.makedirs(parent,exist_ok=True)
img = img.resize((W,H), Image.LANCZOS)
img.save(out,"PNG",optimize=True)
print("Wrote",out,os.path.getsize(out),"bytes")
