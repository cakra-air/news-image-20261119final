"""World News - 18 November 2026. Close imitation of the winning front-page poster.
Deterministic, offline. Writes entry.png via main.py's copy (or $MAKEFUN_OUTPUT)."""
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

F_TITLE = f("timesbd.ttf", 38)
F_SUB   = f("timesi.ttf", 11)
F_BAN   = f("arialbd.ttf", 13)
F_HEAD  = f("timesbd.ttf", 17)
F_CAP   = f("arial.ttf", 9)
F_SM    = f("arialbd.ttf", 9)
F_MICRO = f("arialbd.ttf", 7)
F_TINY  = f("arial.ttf", 8)
F_REG   = f("arialbd.ttf", 9)
F_BIG   = f("timesbd.ttf", 12)
F_DATE  = f("arialbd.ttf", 10)

NAVY=(17,33,69); CREAM=(247,244,235); RED=(196,16,46); GOLD=(232,185,35)
TEAL=(27,122,107); PURPLE=(106,61,145); BLUE=(47,98,163); GREEN=(34,132,88)
ORANGE=(220,124,30); GRAY=(92,98,112); INK=(26,30,42); WHITE=(255,255,255)

REGCOL = {"ASIA":PURPLE,"EUROPE":BLUE,"AMERICAS":GREEN,"AFRICA":ORANGE,
          "MIDDLE EAST":RED,"OCEANIA":TEAL,"GLOBAL":GRAY}

def wrap(t, ft, mw, d):
    out=[]; cur=""
    for w in t.split():
        s=(cur+" "+w).strip()
        if d.textlength(s,font=ft)<=mw: cur=s
        else:
            if cur: out.append(cur)
            cur=w
    if cur: out.append(cur)
    return out

def txt(d,x,y,s,ft,col): d.text((x,y),s,font=ft,fill=col)
def rr(d,b,col,r=4): d.rounded_rectangle(b,radius=r,fill=col)
def rule(d,x0,y0,x1,y1,col,w=1): d.line([(x0,y0),(x1,y1)],fill=col,width=w)

def badge(d,x,y,n,col,size=14):
    d.ellipse([x,y,x+size,y+size],fill=col)
    s=str(n); tw=d.textlength(s,font=F_MICRO)
    txt(d,x+size/2-tw/2,y+2,s,F_MICRO,WHITE)

# ---------- illustrations ----------
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
    d.rectangle([x1-46,y1-56,x1-8,y1-30],fill=(206,32,42))
    for i in range(3): d.rectangle([x1-46,y1-52+i*8,x1-8,y1-49+i*8],fill=(255,210,60))

def art_gulf(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(226,204,166))
    d.polygon([(x0+40,y0+30),(x1-10,y0+12),(x1,y1),(x0+70,y1)],fill=(64,116,150))
    txt(d,x0+12,y0+10,"SAUDI ARABIA",F_MICRO,(110,80,50))
    d.polygon([(x0+10,y0+18),(x0+70,y0+8),(x0+82,y0+40),(x0+22,y0+48)],fill=(206,186,140))
    txt(d,x0+16,y0+24,"KUWAIT",F_MICRO,(90,60,40))
    d.polygon([(x0+84,y1-44),(x0+124,y1-52),(x0+132,y1-16),(x0+92,y1-10)],fill=(210,190,146))
    txt(d,x0+90,y1-32,"BAHRAIN",F_MICRO,(90,60,40))
    txt(d,x1-70,y0+12,"IRAN",F_SM,(120,50,40))
    d.line([(x1-40,y0+24),(x0+96,y1-30)],fill=RED,width=2)
    for t in range(4):
        px=x1-40+(x0+96-(x1-40))*t/4; py=y0+24+(y1-30-y0-24)*t/4
        d.ellipse([px-3,py-3,px+3,py+3],fill=RED)
    for cx,cy in [(x0+78,y1-30),(x0+112,y0+34)]:
        for r,c in [(9,(244,140,40)),(5,(255,220,90))]:
            d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
    d.polygon([(x0+30,y0+34),(x0+52,y0+30),(x0+48,y0+42),(x0+32,y0+44)],fill=(250,250,246))

def art_space(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(10,22,48))
    for i in range(40):
        import random
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
    for i in range(7):
        import math
        a=2*math.pi*i/7
        cx=x0+58+16*math.cos(a); cy=y0+16+12*math.sin(a)
        d.ellipse([cx-3,cy-3,cx+3,cy+3],fill=GOLD)
    d.rectangle([x0+128,y0+4,x0+196,y0+28],fill=(255,220,60))
    d.rectangle([x0+128,y0+17,x0+196,y0+28],fill=(36,66,120))
    pass

def art_fed(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(238,242,244))
    d.polygon([(x0+18,y0+34),(x0+40,y0+18),(x0+62,y0+34)],fill=(120,130,145))
    for i in range(4): d.rectangle([x0+20+i*12,y0+34,x0+27+i*12,y0+58],fill=(150,158,170))
    d.rectangle([x0+14,y0+58,x0+68,y0+63],fill=(120,130,145))
    d.line([(x0+86,y0+20),(x0+120,y0+34),(x0+146,y0+28),(x1-8,y0+48)],fill=RED,width=3)
    txt(d,x0+82,y0+52,"MORE HIKES",F_SM,RED)

def art_cyclone(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(214,234,242))
    d.polygon([(x0+10,y0+10),(x0+130,y0+24),(x0+110,y1),(x0,y1)],fill=(206,220,214))
    txt(d,x0+14,y0+16,"INDIA",F_MICRO,(70,90,70))
    txt(d,x0+52,y0+40,"ODISHA",F_MICRO,(60,80,60))
    import math
    for r in range(8,34,4):
        d.arc([x1-60-r,y0+18-r,x1-60+r,y0+18+r],r*8,r*8+220,fill=(40,100,150),width=2)
    txt(d,x0+8,y1-16,"LANDFALL FRI 20 NOV",F_MICRO,(30,70,110))

def art_sudan(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(238,204,166))
    for i in range(5): d.rectangle([x0+12+i*44,y1-34,x0+34+i*44,y1-12],fill=(160,120,84))
    for cx,cy in [(x0+120,y0+28),(x0+60,y0+20)]:
        for r,c in [(12,(226,90,36)),(6,(255,214,90))]: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
    d.line([(x1-10,y0+10),(x0+120,y0+28)],fill=RED,width=2)
    txt(d,x0+8,y0+8,"37 KILLED",F_SM,RED)

def art_gaza(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(204,232,240))
    d.rectangle([x0,y0+22,x1,y1],fill=(212,226,204))
    d.line([(x0+20,y0+40),(x1-20,y0+40)],fill=RED,width=2)
    d.rectangle([x1-70,y0+8,x1-20,y0+30],fill=(226,196,60))
    txt(d,x1-66,y0+12,"YELLOW LINE",F_MICRO,(80,70,30))
    d.polygon([(x0+40,y0+52),(x0+76,y0+52),(x0+84,y0+66),(x0+34,y0+66)],fill=(90,100,78))
    d.rectangle([x0+50,y0+44,x0+66,y0+52],fill=(90,100,78))
    txt(d,x0+8,y0+6,"SEA",F_MICRO,(50,90,120))

def art_capitol(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(236,240,244))
    d.ellipse([x0+88,y0+8,x0+134,y0+48],fill=(150,158,170))
    d.rectangle([x0+82,y0+40,x0+140,y0+52],fill=(150,158,170))
    for i in range(4): d.rectangle([x0+16+i*36,y0+48,x0+30+i*36,y0+66],fill=(170,176,186))
    d.rectangle([x0+8,y0+66,x1-8,y0+70],fill=(150,158,170))
    pass

def art_game(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(108,52,140))
    d.ellipse([x0+70,y0+14,x0+170,y0+62],fill=(240,244,250))
    for cx,cy in [(x0+94,y0+30),(x0+146,y0+30)]:
        d.rectangle([cx-10,cy-4,cx+10,cy+4],fill=(120,60,150))
        d.rectangle([cx-2,cy-12,cx+2,cy+12],fill=(120,60,150))
    for cx,cy in [(x0+96,y0+46),(x0+112,y0+40),(x0+130,y0+40),(x0+146,y0+46)]:
        d.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(220,80,120))
    txt(d,x0+8,y0+66,"ON SALE AFTER 13 YEARS",F_MICRO,WHITE)

def art_chips(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=(16,34,58))
    for i in range(7):
        cx=x0+12+i*32; cy=y0+14
        d.rectangle([cx,cy,cx+22,cy+22],fill=(178,146,58))
        d.rectangle([cx+4,cy+4,cx+18,cy+18],fill=(222,196,110))
    txt(d,x0+10,y0+40,"H200  ·  HONG KONG STOCK",F_MICRO,(220,230,244))
    d.line([(x1-70,y0+50),(x0+80,y0+50)],fill=RED,width=2)

LEADS=[
 ("ASIA","TRILATERAL","REUTERS · BBC","SHENZHEN · APEC SUMMIT","THREE LEADERS, ONE TABLE",
  "Trump, Xi and Putin hold a first-ever trilateral",
  "The three nuclear powers meet in Shenzhen with arms control on the agenda. Trump called his red-carpet welcome a 'big win'; smaller states fear a carve-up.",art_shenzhen),
 ("MIDDLE EAST","IRAN WAR","REUTERS · AFP","ALI AL SALEM · KUWAIT","IRAN HITS US BASE",
  "Iran fires on US sites in Kuwait; Bahrain intercepts",
  "Tehran struck a US air base after the US hit Qeshm island. Vance says Washington will not let the conflict become another 'forever war'.",art_gulf),
 ("GLOBAL","MARKETS","BLOOMBERG · REUTERS","NASDAQ · TICKER ANT","IPO PRICED AT $83",
  "Anthropic prices IPO above range, debuts today",
  "The first frontier-AI listing may top $94bn with a private placement. Amazon and Google will hold a combined 28.4% after the float.",art_space),
]
CARDS=[
 (4,"AMERICAS","MARKETS","FED · WSJ","DEC HIKE NEAR-CERTAIN","Fed minutes: almost all officials see more hikes","December move priced at 100%; AI debt flagged.",art_fed),
 (5,"OCEANIA","CULTURE","GUARDIAN · NME","METACRITIC 99","GTA VI launches worldwide; New Zealand first","Review score of 99 ties Ocarina of Time's record.",art_game),
 (6,"EUROPE","UKRAINE WAR","BBC · INDEPENDENT","HIT AGAIN · TRAFFIC HALT","Crimea bridge struck for a third time this week","Repairs could take a year; Kyiv bridges hit too.",art_drones),
 (7,"MIDDLE EAST","GAZA","BBC · REUTERS","THE YELLOW LINE","Israeli tanks cross into central Gaza again","Families flee as Hamas calls it a ceasefire breach.",art_gaza),
 (8,"EUROPE","DIPLOMACY","POLITICO · AFP","20+ LEADERS IN BERLIN","Coalition of the Willing meets on Ukraine","Witkoff and Kushner join talks on security guarantees.",art_eu),
 (9,"AFRICA","HEALTH","WHO · RFI","5,568 DEAD","DRC's Ebola outbreak still out of control after six months","Bundibugyo vaccine trials start next week; 400-500 cases a week.",art_sudan),
 (10,"AMERICAS","SECURITY","CNN","NSANET DOWN 2 DAYS","NSA's classified network still down on day two","Patch, not cyberattack, hit a Middle East intel hub.",art_capitol),
 (11,"ASIA","WEATHER","IMD","LANDFALL 20 NOV","Cyclone Akvan closes on the Andhra Pradesh coast","110 km/h winds forecast; Odisha on alert.",art_cyclone),
 (12,"EUROPE","OSCE","UK FCDO","NO MILITARY SOLUTION","UK tells OSCE Russia cannot bomb its way to victory","It condemns strikes on energy system and Black Sea shipping.",art_eu),
 (13,"MIDDLE EAST","ENERGY","FRANCE 24","BIGGEST THREAT EVER","IEA calls the crisis the largest energy threat in history","The Hormuz blockade disrupts shipments; consumers pay more.",art_fed),
 (14,"AFRICA","HEALTH","WHO · RFI","5,568 DEAD","DRC's Ebola outbreak still out of control after six months","Bundibugyo vaccine trials start next week; 400-500 cases a week.",art_sudan),
 (15,"ASIA","TECH","REUTERS","CHIP CURBS","Nvidia halts H200 shipments to China amid licensing row","About 600,000 chips are stranded in Hong Kong.",art_chips),
]
TINY=[
 (12,"AMERICAS","Jeffries picked for Speaker in a 251-11 vote"),
 (13,"AMERICAS","Peltola wins Alaska Senate race"),
 (14,"AMERICAS","Pakistani man jailed 27 years for Trump plot"),
 (15,"AMERICAS","Medicare premiums rise again in 2027"),
 (16,"AMERICAS","Apple iCloud outage hits Pay and App Store"),
 (17,"AMERICAS","Trump appeals on Venezuelan protections"),
 (18,"AMERICAS","Duffy and Bedford take blame for ground stop"),
 (19,"AMERICAS","$50bn air-traffic plan meets resistance"),
 (20,"AMERICAS","House demands Nvidia briefing by December 2"),
 (21,"AMERICAS","Russian arrested for spying on Palantir"),
 (22,"EUROPE","France admits secret 'Volia' troops in Ukraine"),
 (23,"EUROPE","Lavrov calls the mission 'direct participation'"),
 (24,"EUROPE","EU proposes a €45bn loan to fund Kyiv"),
 (25,"EUROPE","UK: Russia cannot bomb its way to victory"),
 (26,"EUROPE","Limoges city hall restored after arson"),
 (27,"EUROPE","EU and UNDP widen peacebuilding partnership"),
 (28,"MIDDLE EAST","IEA: biggest energy threat in history"),
 (29,"MIDDLE EAST","Brent slips to $92 despite Hormuz risk"),
 (30,"MIDDLE EAST","Iran chief threatens 'devastating' response"),
 (31,"MIDDLE EAST","Loud explosion reported near Riyadh airport"),
 (32,"MIDDLE EAST","Houthis advance on Aden; IOM warns of displacement"),
 (33,"AFRICA","DRC Ebola: 5,568 dead, 11,376 cases"),
 (34,"AFRICA","Bundibugyo vaccine trials start next week"),
 (35,"AFRICA","Sudan court sentences Hemedti to death in absentia"),
 (36,"AFRICA","Senegal president excluded from ruling party"),
 (37,"AFRICA","Nigeria police arrest five in Anambra murder"),
 (38,"AFRICA","UNICEF warns on Somalia humanitarian crisis"),
 (39,"AFRICA","Ethiopia's Oromia conflict displaces families"),
 (40,"ASIA","North Korea's Yongbyon extension complete: IAEA"),
 (41,"ASIA","Xi urges free and open trade at APEC"),
 (42,"ASIA","Nvidia halts H200 chip shipments to China"),
 (43,"ASIA","US panel: China seeks chips for AI weapons"),
 (44,"ASIA","Scientist sacked after child dies in gene trial"),
 (45,"ASIA","Thailand floods expose a waste crisis"),
 (46,"ASIA","India begin first Test against New Zealand"),
 (47,"OCEANIA","New Zealand hosts GTA VI midnight launch"),
 (48,"OCEANIA","Oceania gamers among the first to play"),
 (49,"OCEANIA","Australia backs clean-air funding push"),
 (50,"GLOBAL","Voyager 1 confirmation due on Thursday"),
 (51,"GLOBAL","UNICEF: children in armed conflict, 1990-2025"),
 (52,"GLOBAL","ICJ to rule on Rohingya genocide case"),
]

img=Image.new("RGB",(W*S,H*S),CREAM); d=ScaledDraw(img,S)
# header
d.rectangle([0,0,W,90],fill=NAVY)
d.rectangle([16,8,96,82],fill=WHITE)
txt(d,26,12,"NOV",f("arialbd.ttf",12),RED)
txt(d,26,26,"19",f("timesbd.ttf",32),NAVY)
txt(d,22,66,"THU · 2026",f("arialbd.ttf",7),NAVY)
txt(d,112,12,"THE DAY IN WORLD NEWS",f("arialbd.ttf",11),GOLD)
txt(d,110,26,"Thursday 19 November 2026",F_TITLE,WHITE)
txt(d,112,68,"Everything on this page happened, or was first reported, on Thursday 19 November 2026.",F_SUB,(206,220,240))
txt(d,660,12,"11 STORIES · 7 REGIONS · 11 DRAWN · MARKETS",f("arialbd.ttf",9),GOLD)
rule(d,0,90,W,90,GOLD,3)

# region bar (counts derived from the stories)
all_regions=[s[0] for s in LEADS]+[s[1] for s in CARDS[:8]]

STOCKS=[("PANW","339.92","+9.9%"),("AMD","530.14","+5.3%"),("AMZN","267.74","+3.8%"),
        ("AVGO","354.05","+3.6%"),("BABA","84.37","+2.6%"),("INTU","313.24","+2.4%"),
        ("CSCO","97.18","+2.2%"),("TSLA","383.72","+0.9%"),("MU","705.27","-1.1%"),
        ("MSFT","508.29","+0.4%")]
LOSERS=[("UNH","349.91","-10.2%"),("SAP","210.76","-5.3%"),("NVDA","150.96","-2.9%")]
CRYPTO=[("BTC","63,241","-2.6%"),("ETH","1,771","-2.2%"),("SOL","73.01","-1.9%"),
        ("BNB","585.99","-1.0%"),("XRP","0.97","-1.3%"),("TRX","0.31","+1.3%"),
        ("USDT","1.00","+0.0%"),("DOGE","0.058","-1.7%"),("LINK","9.00","-2.4%"),
        ("USDC","1.00","+0.0%")]
FOREX=[("EUR/USD","1.0962","-0.21%"),("USD/JPY","159.57","+0.12%"),
       ("GBP/USD","1.3131","-0.48%"),("USD/CHF","0.8427","+0.34%"),
       ("USD/CAD","1.4305","+0.24%"),("AUD/USD","0.6678","-0.69%"),
       ("EUR/JPY","174.86","-0.09%"),("GBP/JPY","209.46","-0.05%"),
       ("USD/INR","93.45","+0.02%"),("NZD/USD","0.5845","-0.30%")]
COMDTY=[("GOLD","3,774.92","-2.31%"),("SILVER","45.58","-3.76%"),
        ("BRENT OIL","89.45","-2.72%"),("WTI OIL","82.37","-1.07%"),
        ("COPPER","5.67","+0.13%"),("VIX","24.56","-3.53%"),
        ("SOY","1,218","+0.10%"),("COFFEE","276.05","-3.68%"),
        ("WHEAT","588.00","+3.16%"),("COTTON","80.23","+3.76%")]
chips=[("ASIA",PURPLE,146),("EUROPE",BLUE,148),("AMERICAS",GREEN,182),("AFRICA",ORANGE,126),
       ("MIDDLE EAST",RED,160),("OCEANIA",TEAL,124),("GLOBAL",GRAY,106)]
cx=16
for name,col,wid in chips:
    d.rectangle([cx,96,cx+wid,112],fill=col)
    label=f"{name} {all_regions.count(name)}"
    tw=d.textlength(label,font=F_REG)
    txt(d,cx+(wid-tw)/2,99,label,F_REG,WHITE)
    cx+=wid
# leads (larger: full captions)
LW=(992-16)//3
for i,(reg,tag,src,kick,banner,head,cap,art) in enumerate(LEADS):
    x0=16+i*(LW+8); x1=x0+LW-1
    art(d,x0,118,x1,250)
    d.rectangle([x0,250,x1,274],fill=NAVY)
    tw=d.textlength(kick,font=F_SM)
    txt(d,x0+(LW-tw)/2,255,kick,F_SM,GOLD)
    d.rectangle([x0,274,x1,302],fill=RED if i==1 else NAVY)
    tw=d.textlength(banner,font=F_BAN)
    txt(d,x0+(LW-tw)/2,280,banner,F_BAN,WHITE)
    y=308
    badge(d,x0,y,i+1,REGCOL[reg]); txt(d,x0+20,y,reg+" · "+tag,F_SM,REGCOL[reg])
    sw=d.textlength(src,font=F_MICRO); txt(d,x1-sw,y,src,F_MICRO,GRAY)
    y+=20
    for ln in wrap(head,F_HEAD,x1-x0,d): txt(d,x0,y,ln,F_HEAD,NAVY); y+=21
    y+=4
    for ln in wrap(cap,F_CAP,x1-x0,d): txt(d,x0,y,ln,F_CAP,(70,76,90)); y+=12
    d.rectangle([x0,118,x1,400],outline=GRAY,width=1)

# UTC timeline strip (compact)
d.rectangle([16,404,1008,420],fill=(232,236,242))
txt(d,22,407,"UTC TIMELINE",f("arialbd.ttf",8),NAVY)
tl=[("00",RED,"Gulf strikes"),("06",BLUE,"Berlin"),("09",PURPLE,"Shenzhen"),
    ("13",GREEN,"Wall St opens"),("18",ORANGE,"NSA down"),("23",TEAL,"NZ launch")]
tx=124
for hh,col,label in tl:
    d.ellipse([tx,409,tx+8,417],fill=col)
    txt(d,tx+12,406,f"{hh}:00",f("arialbd.ttf",7),NAVY)
    txt(d,tx+12,413,label,f("arial.ttf",7),(90,96,110))
    tx+=148

# 8 compact illustrated cards (headline + caption, no wasted space)
CW=(992-24)//4; CH=124
for j,(n,reg,tag,src,banner,head,cap,art) in enumerate(CARDS[:8]):
    col=j%4; row=j//4
    x0=16+col*(CW+8); y0=424+row*(CH+6); x1=x0+CW; y1=y0+CH
    art(d,x0,y0,x1,y0+44)
    d.rectangle([x0,y0+30,x1,y0+52],fill=NAVY)
    tw=d.textlength(banner,font=F_MICRO)
    txt(d,x0+(CW-tw)/2,y0+36,banner,F_MICRO,WHITE)
    y=y0+55
    badge(d,x0,y,n,REGCOL[reg],11); txt(d,x0+16,y,reg+" · "+tag,F_MICRO,REGCOL[reg])
    sw=d.textlength(src,font=F_MICRO); txt(d,x1-sw,y,src,F_MICRO,GRAY)
    y+=13
    for ln in wrap(head,F_BIG,x1-x0,d)[:2]: txt(d,x0,y,ln,F_BIG,NAVY); y+=13
    y+=1
    for ln in wrap(cap,F_TINY,x1-x0,d)[:2]: txt(d,x0,y,ln,F_TINY,(80,86,100)); y+=10
    d.rectangle([x0,y0,x1,y1],outline=GRAY,width=1)

# markets panel: stocks, crypto, major FX pairs and commodities
d.rectangle([16,686,1008,934],fill=(244,248,250),outline=GRAY,width=1)
d.rectangle([16,686,1008,710],fill=NAVY)
txt(d,24,692,"MARKETS · 19 NOV 2026",F_SM,WHITE)
txt(d,690,692,"STOCKS · COINS · FX · COMMODITIES",F_MICRO,GOLD)
txt(d,24,714,"NASDAQ 24,418.31 +0.37%   |   S&P 500 7,323.63 -0.23%   |   DOW 50,198.17 -1.11%   |   CRYPTO CAP $2.17T -0.81%",F_MICRO,(70,76,92))
rule(d,16,728,1008,728,GRAY,1)
for dx in (264,512,760):
    rule(d,dx,730,dx,932,GRAY,1)
heads=[(24,"BEST STOCKS",GREEN),(272,"CRYPTO",BLUE),(520,"MAJOR FX",ORANGE),(768,"GOLD / OIL / ETC",RED)]
for hx,label,col in heads: txt(d,hx,732,label,F_SM,col)
def mkt_rows(x,rows):
    for i,(sym,px,ch) in enumerate(rows):
        y=750+i*14
        txt(d,x,y,sym,F_MICRO,NAVY); txt(d,x+96,y,px,F_MICRO,INK)
        txt(d,x+188,y,ch,F_MICRO,GREEN if ch.startswith('+') else RED)
mkt_rows(24,STOCKS)
mkt_rows(272,CRYPTO)
mkt_rows(520,FOREX)
mkt_rows(768,COMDTY)
txt(d,24,912,"Worst stocks: " + "  ".join(f"{s} {c}" for s,_,c in LOSERS),F_MICRO,RED)

# date check
d.rectangle([16,944,1008,986],fill=(250,236,236),outline=RED,width=2)
txt(d,24,948,"DATE CHECK",f("arialbd.ttf",11),RED)
txt(d,110,948,"Left out, as first reported on Wednesday 18 November: Trump's red-carpet welcome; the Xi-Putin talks; the Qeshm strike; the",F_TINY,(110,40,40))
txt(d,110,960,"Kerch bridge span.  Not yet news: the summit's outcome, the Berlin guarantees and Friday's cyclone landfall.",F_TINY,(110,40,40))
# world clock strip (UTC and the time difference across the day's news rooms)
d.rectangle([0,990,W,H],fill=NAVY)
txt(d,16,992,"WORLD CLOCK · UTC",f("arialbd.ttf",9),GOLD)
txt(d,120,992,"00:00 UTC  ·  19:00 NEW YORK (18 NOV, UTC-5)  ·  00:00 LONDON (UTC+0)  ·  05:30 KOLKATA (UTC+5:30)",F_MICRO,WHITE)
txt(d,120,1003,"08:00 SHENZHEN (UTC+8)  ·  09:00 TOKYO (UTC+9)  ·  11:00 SYDNEY (UTC+11)  ·  the date changes first in the west",F_MICRO,WHITE)

out=os.environ.get("MAKEFUN_OUTPUT","C:\\Users\\User\\Aws\\agent\\entry_build_1119\\preview.png")
parent=os.path.dirname(out)
if parent: os.makedirs(parent,exist_ok=True)
img = img.resize((W,H), Image.LANCZOS)
img.save(out,"PNG",optimize=True)
print("Wrote",out,os.path.getsize(out),"bytes")
