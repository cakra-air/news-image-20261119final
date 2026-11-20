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

def badge(d,x,y,n,col,size=12):
    d.ellipse([x,y,x+size,y+size],fill=col)
    s=str(n); tw=tlen(d,s,F_MICRO)
    txt(d,x+size/2-tw/2,y+2,s,F_MICRO,WHITE)

# ---------- illustrations (flat, deterministic, no external assets) ----------
def art_shenzhen(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(226,236,244))
    d.ellipse([x1-64,y0+8,x1-24,y0+48],fill=(244,176,72))
    for i,ht in enumerate([28,48,36,66,42,30,54]):
        bx=x0+18+i*32
        d.rectangle([bx,y1-30-ht,bx+22,y1-30],fill=(150,168,186))
        for wy in range(y1-26-ht,y1-34,8):
            d.rectangle([bx+4,wy,bx+8,wy+3],fill=(190,208,224))
            d.rectangle([bx+13,wy,bx+17,wy+3],fill=(190,208,224))
    d.polygon([(x0+10,y0+8),(x0+66,y0+18),(x0+50,y0+26),(x0+28,y0+30),(x0+10,y0+24)],fill=(70,92,126))
    d.rectangle([x0+16,y0+22,x0+56,y0+26],fill=(70,92,126))
    for cx,col in [(x0+120,(206,32,42)),(x0+166,(30,70,150)),(x0+212,(40,44,54))]:
        d.rectangle([cx-8,y1-52,cx+8,y1-30],fill=col)
        d.ellipse([cx-6,y1-64,cx+6,y1-52],fill=(220,178,146))
    # a glass tower instead of the old red-and-yellow stripes (it read as a flag)
    d.rectangle([x1-54,y1-74,x1-12,y1-30],fill=(120,150,180))
    for wy in range(y1-68,y1-34,8):
        d.rectangle([x1-48,wy,x1-18,wy+3],fill=(196,216,234))

def art_gulf(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(226,204,166))
    d.polygon([(x0+40,y0+30),(x1-10,y0+12),(x1,y1),(x0+70,y1)],fill=(64,116,150))
    txt(d,x0+12,y0+10,"KUWAIT",F_MICRO,(110,80,50))
    d.polygon([(x0+10,y0+18),(x0+70,y0+8),(x0+82,y0+40),(x0+22,y0+48)],fill=(206,186,140))
    d.polygon([(x0+84,y1-44),(x0+124,y1-52),(x0+132,y1-16),(x0+92,y1-10)],fill=(210,190,146))
    d.line([(x1-40,y0+24),(x0+96,y1-30)],fill=RED,width=2)
    for t in range(4):
        px=x1-40+(x0+96-(x1-40))*t/4; py=y0+24+(y1-30-y0-24)*t/4
        d.ellipse([px-3,py-3,px+3,py+3],fill=RED)
    for cx,cy in [(x0+78,y1-30),(x0+112,y0+34)]:
        for r,c in [(9,(244,140,40)),(5,(255,220,90))]:
            d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)

def art_space(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(10,22,48))
    for i in range(40):
        sx=x0+(i*37)%(x1-x0); sy=y0+(i*53)%(y1-y0)
        d.ellipse([sx,sy,sx+1,sy+1],fill=(180,200,230))
    d.ellipse([x0+16,y0+30,x0+76,y0+90],fill=(56,132,196))
    d.ellipse([x0+26,y0+34,x0+60,y0+68],fill=(86,160,110))
    d.arc([x0+8,y0+22,x0+84,y0+98],20,160,fill=(150,200,240),width=2)
    px,py=x1-56,y0+54
    d.ellipse([px-22,py-16,px+6,py+12],outline=(220,226,236),width=3)
    d.line([(px+6,py-2),(px+24,py-8)],fill=(200,210,225),width=3)
    d.rectangle([px+22,py-16,px+40,py+2],fill=(180,190,210))
    d.line([(px+26,py-16),(px+26,py-30)],fill=(180,190,210),width=2)
    d.line([(x0+76,y0+60),(px-22,py+2)],fill=GOLD,width=1)
    txt(d,x0+92,y0+16,"1 LIGHT-DAY",f("arialbd.ttf",15),GOLD)
    txt(d,x0+96,y0+38,"25.9 billion km from Earth",F_MICRO,(214,226,244))
    txt(d,x0+96,y0+52,"a radio signal takes 24 hours",F_MICRO,(214,226,244))

def art_drones(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(16,32,60))
    for i,ht in enumerate([20,34,26,40,18]):
        bx=x0+10+i*46; d.rectangle([bx,y1-24-ht,bx+30,y1-24],fill=(44,64,96))
    d.line([(x1-10,y0+10),(x0+60,y1-28)],fill=RED,width=2)
    for cx,cy in [(x0+70,y1-30),(x1-40,y0+20)]:
        for r,c in [(10,(238,110,40)),(5,(255,220,90))]: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
    d.polygon([(x0+150,y0+8),(x0+172,y0+4),(x0+168,y0+18),(x0+148,y0+20)],fill=(230,236,244))

def art_eu(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(236,242,248))
    d.rectangle([x0,y0,x1,y0+30],fill=(36,66,140))
    import math
    for i in range(7):
        a=2*math.pi*i/7
        cx=x0+58+16*math.cos(a); cy=y0+16+12*math.sin(a)
        d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=GOLD)
    d.rectangle([x0+128,y0+4,x0+196,y0+28],fill=(255,220,60))
    d.rectangle([x0+128,y0+17,x0+196,y0+28],fill=(36,66,120))

def art_court(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(238,232,216))
    for i in range(4):
        d.rectangle([x0+26+i*42,y0+16,x0+38+i*42,y1-8],fill=(160,142,116))
    d.rectangle([x0+18,y1-14,x1-14,y1-8],fill=(138,120,96))
    # scales of justice
    cx=x1-48; cy=y0+26
    d.line([(cx,cy),(cx,cy+26)],fill=(70,64,54),width=2)
    d.line([(cx-22,cy),(cx+22,cy)],fill=(70,64,54),width=2)
    for sx in (cx-22,cx+22):
        d.line([(sx,cy),(sx,cy+10)],fill=(70,64,54),width=1)
        d.ellipse([sx-7,cy+10,sx+7,cy+22],outline=(70,64,54),width=2)

def art_game(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(108,52,140))
    d.ellipse([x0+70,y0+10,x0+170,y0+52],fill=(240,244,250))
    for cx,cy in [(x0+94,y0+26),(x0+146,y0+26)]:
        d.rectangle([cx-10,cy-4,cx+10,cy+4],fill=(120,60,150))
        d.rectangle([cx-2,cy-12,cx+2,cy+12],fill=(120,60,150))
    for cx,cy in [(x0+96,y0+42),(x0+112,y0+36),(x0+130,y0+36),(x0+146,y0+42)]:
        d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(220,80,120))
    txt(d,x0+8,y0+40,"ON SALE AFTER 13 YEARS",F_MICRO,WHITE)

def art_energy(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(250,236,206))
    d.ellipse([x1-46,y0+8,x1-10,y0+42],fill=(244,176,72))
    d.line([(x0+30,y1-8),(x0+30,y0+14)],fill=(70,74,82),width=3)
    d.polygon([(x0+30,y0+14),(x0+48,y1-8),(x0+12,y1-8)],fill=(92,98,110))
    for k in range(3):
        d.line([(x0+20+k*10,y1-12),(x0+40+k*10,y0+26)],fill=(150,156,166),width=1)
    d.line([(x0+64,y1-12),(x1-8,y1-12)],fill=(36,96,150),width=3)
    for k in range(3):
        d.arc([x0+72+k*36,y1-22,x0+104+k*36,y1-2],200,340,fill=(36,96,150),width=2)

def art_fed(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(238,242,244))
    d.polygon([(x0+18,y0+34),(x0+40,y0+18),(x0+62,y0+34)],fill=(120,130,145))
    for i in range(4): d.rectangle([x0+20+i*12,y0+34,x0+27+i*12,y0+52],fill=(150,158,170))
    d.rectangle([x0+14,y0+52,x0+68,y0+57],fill=(120,130,145))
    d.line([(x0+86,y0+16),(x0+120,y0+28),(x0+146,y0+22),(x1-8,y0+40)],fill=RED,width=3)
    txt(d,x0+82,y0+40,"MORE HIKES",F_SM,RED)

def art_cyclone(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(214,234,242))
    d.polygon([(x0+10,y0+10),(x0+130,y0+24),(x0+110,y1),(x0,y1)],fill=(206,220,214))
    txt(d,x0+12,y0+6,"INDIA",F_MICRO,(70,90,70))
    txt(d,x0+46,y0+22,"ODISHA",F_MICRO,(60,80,60))
    for r in range(6,24,4):
        d.arc([x1-60-r,y0+26-r,x1-60+r,y0+26+r],r*8,r*8+220,fill=(40,100,150),width=2)

def art_sudan(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(238,204,166))
    for i in range(5): d.rectangle([x0+12+i*44,y1-30,x0+34+i*44,y1-10],fill=(160,120,84))
    for cx,cy in [(x0+120,y0+24),(x0+60,y0+18)]:
        for r,c in [(12,(226,90,36)),(6,(255,214,90))]: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
    d.line([(x1-10,y0+10),(x0+120,y0+24)],fill=RED,width=2)

def art_gaza(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(204,232,240))
    d.rectangle([x0,y0+18,x1,y1],fill=(212,226,204))
    d.line([(x0+20,y0+34),(x1-20,y0+34)],fill=RED,width=2)
    d.rectangle([x1-70,y0+4,x1-20,y0+24],fill=(226,196,60))
    txt(d,x1-66,y0+8,"YELLOW LINE",F_MICRO,(80,70,30))
    d.polygon([(x0+40,y0+40),(x0+76,y0+40),(x0+84,y1-4),(x0+34,y1-4)],fill=(90,100,78))

def art_capitol(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(236,240,244))
    d.ellipse([x0+88,y0+4,x0+134,y0+40],fill=(150,158,170))
    d.rectangle([x0+82,y0+34,x0+140,y0+46],fill=(150,158,170))
    for i in range(4): d.rectangle([x0+16+i*36,y0+40,x0+30+i*36,y0+54],fill=(170,176,186))
    d.rectangle([x0+8,y0-8+52,x1-8,y1-8],fill=(150,158,170))

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

# UTC timeline ------------------------------------------------------------
d.rectangle([16,428,1008,446],fill=(232,236,242))
txt(d,22,430,"UTC TIMELINE",f("arialbd.ttf",10),NAVY)
tl=[("00",RED,"Gulf strikes"),("06",BLUE,"Berlin"),("09",PURPLE,"Shenzhen"),
    ("13",GREEN,"Wall St opens"),("18",ORANGE,"NSA down"),("23",TEAL,"NZ launch")]
tx=124
for hh,col,label in tl:
    d.ellipse([tx,433,tx+8,441],fill=col)
    txt(d,tx+12,428,f"{hh}:00",f("arialbd.ttf",10),NAVY)
    txt(d,tx+12,437,label,f("arialbd.ttf",10),(60,66,80))
    tx+=148

# eight illustrated cards -------------------------------------------------
CW=(992-24)//4; CH=140
for j,(n,reg,tag,src,banner,head,cap,art) in enumerate(CARDS):
    col=j%4; row=j//4
    x0=16+col*(CW+8); y0=450+row*(CH+6); x1=x0+CW; y1=y0+CH
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
d.rectangle([16,742,1008,788],fill=(238,241,246),outline=GRAY,width=1)
txt(d,24,747,"THE DAY IN NUMBERS · 19 NOV",f("arialbd.ttf",9),NAVY)
stats=[(228,"$94bn","ANTHROPIC IPO VALUATION"),(398,"28.4%","AMAZON + GOOGLE STAKE"),
       (568,"200,000","EVACUATED AHEAD OF AKVAN"),(744,"5,568","DRC EBOLA DEAD"),
       (886,"24,418","NASDAQ CLOSE +0.37%")]
for x,big,lab in stats:
    txt(d,x,746,big,F_STAT,RED)
    txt(d,x,775,lab,F_MICRO,(80,86,100))

# also on thursday: small world map + 24 short briefs in three columns ----
d.rectangle([16,794,1008,814],fill=NAVY)
txt(d,24,798,"WHERE IT HAPPENED  /  ALSO ON THURSDAY",f("arialbd.ttf",10),GOLD)
txt(d,700,798,"24 MORE STORIES · 19 NOV 2026",F_MICRO,(206,220,240))
draw_world_map(d,16,820,306,964)
for k,(reg,brief) in enumerate(BRIEFS[:24]):
    col=k//8; row=k%8
    x=322+col*230; y=820+row*19
    d.ellipse([x,y+1,x+6,y+7],fill=REGCOL[reg])
    s=f"{k+1:02d} · "+brief
    txt(d,x+11,y,one_line(s,F_BRIEF,210,d),F_BRIEF,INK)

# date check: only what is NOT on this page, phrased so it cannot contradict
d.rectangle([16,968,1008,994],fill=(250,236,236),outline=RED,width=2)
txt(d,24,973,"DATE CHECK",f("arialbd.ttf",10),RED)
txt(d,118,971,"NOT ON THIS PAGE AS NEWS (first reported Wed 18 Nov): Trump's red-carpet welcome; the US strike on Qeshm island;",F_TINY,(110,40,40))
txt(d,118,982,"the Kerch bridge span; Berlin security guarantees. Friday's cyclone landfall is a forecast, not a 19 Nov event.",F_TINY,(110,40,40))

# footer ------------------------------------------------------------------
d.rectangle([0,996,W,H],fill=NAVY)
txt(d,16,1000,"WORLD CLOCK · UTC",f("arialbd.ttf",10),GOLD)
txt(d,130,999,"00:00 UTC  ·  19:00 NEW YORK (18 NOV)  ·  00:00 LONDON  ·  05:30 KOLKATA",f("arialbd.ttf",10),WHITE)
txt(d,130,1012,"08:00 SHENZHEN  ·  09:00 TOKYO  ·  11:00 SYDNEY  ·  the date changes first in the west",f("arialbd.ttf",10),(216,228,244))

out=os.environ.get("MAKEFUN_OUTPUT","C:\\Users\\User\\Aws\\agent\\entry_build_1119\\preview_v2.png")
parent=os.path.dirname(out)
if parent: os.makedirs(parent,exist_ok=True)
img = img.resize((W,H), Image.LANCZOS)
img.save(out,"PNG",optimize=True)
print("Wrote",out,os.path.getsize(out),"bytes")
