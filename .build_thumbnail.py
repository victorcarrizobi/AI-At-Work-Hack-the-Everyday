from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT = "D:/HACKATHON/youtube_thumbnail.png"

W, H = 1280, 720
BG = (15, 23, 42)
ACCENT = (34, 197, 94)
FG = (248, 250, 252)
MUTED = (148, 163, 184)
CRIT = (252, 165, 165)
WARN = (253, 230, 138)
HEALTH = (134, 239, 172)
CRIT_BG = (127, 29, 29)
WARN_BG = (120, 53, 15)
HEALTH_BG = (20, 83, 45)
INFO = (56, 189, 248)
EXPO = (167, 139, 250)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Fonts
def lf(name, size):
    for p in [f"C:/Windows/Fonts/{name}", name]:
        try: return ImageFont.truetype(p, size)
        except: continue
    return ImageFont.load_default()

fb = lambda s: lf("calibrib.ttf", s)
fr = lambda s: lf("calibri.ttf", s)

# --- Left accent bar ---
d.rectangle([0, 0, 8, H], fill=ACCENT)

# --- Top banner: "DATA IN THE D 2026 HACKATHON" ---
d.rectangle([0, 0, W, 52], fill=(20, 83, 45))
d.text((30, 10), "DATA IN THE D 2026 HACKATHON  |  HACK THE GRIND TRACK", fill=ACCENT, font=fb(20))

# --- Main title block ---
d.text((40, 80), "SUPPLY CHAIN", fill=FG, font=fb(72))
d.text((40, 160), "RISK MONITOR", fill=ACCENT, font=fb(72))

# Subtitle
d.text((45, 250), "AI-Powered Supplier Quality Scoring", fill=MUTED, font=fr(26))
d.text((45, 285), "Built on Snowflake in One Session with CoCo", fill=MUTED, font=fr(22))

# --- Accent line ---
d.rectangle([40, 325, 600, 329], fill=ACCENT)

# --- KPI boxes row ---
kpis = [
    ("33", "CRITICAL", CRIT, CRIT_BG),
    ("294", "WARNING", WARN, WARN_BG),
    ("73", "HEALTHY", HEALTH, HEALTH_BG),
]
for i, (val, label, color, bg) in enumerate(kpis):
    x = 40 + i * 195
    d.rounded_rectangle([x, 350, x+180, 440], radius=10, fill=bg)
    bbox = d.textbbox((0,0), val, font=fb(38))
    tw = bbox[2]-bbox[0]
    d.text((x + 90 - tw//2, 355), val, fill=color, font=fb(38))
    bbox = d.textbbox((0,0), label, font=fb(14))
    tw = bbox[2]-bbox[0]
    d.text((x + 90 - tw//2, 405), label, fill=color, font=fb(14))

# --- Feature badges ---
features = ["Dynamic Tables", "AI_CLASSIFY", "SENTIMENT", "AI_COMPLETE"]
for i, feat in enumerate(features):
    x = 40 + i * 155
    d.rounded_rectangle([x, 460, x+145, 492], radius=12, fill=(30, 41, 59), outline=(71, 85, 105))
    bbox = d.textbbox((0,0), feat, font=fr(14))
    tw = bbox[2]-bbox[0]
    d.text((x + 72 - tw//2, 467), feat, fill=INFO, font=fr(14))

features2 = ["Alert", "Task", "DMF", "Streamlit"]
for i, feat in enumerate(features2):
    x = 40 + i * 155
    d.rounded_rectangle([x, 502, x+145, 534], radius=12, fill=(30, 41, 59), outline=(71, 85, 105))
    bbox = d.textbbox((0,0), feat, font=fr(14))
    tw = bbox[2]-bbox[0]
    d.text((x + 72 - tw//2, 509), feat, fill=EXPO, font=fr(14))

# --- Right side: big exposure stat ---
d.rounded_rectangle([680, 80, W-30, 310], radius=16, fill=(30, 41, 59), outline=(71, 85, 105))
d.text((710, 95), "AT-RISK EXPOSURE", fill=MUTED, font=fb(18))
center_x = 680 + (W-30-680)//2
text = "$207B"
bbox = d.textbbox((0,0), text, font=fb(80))
tw = bbox[2]-bbox[0]
d.text((center_x - tw//2, 125), text, fill=EXPO, font=fb(80))

text2 = "16,408 Purchase Orders"
bbox = d.textbbox((0,0), text2, font=fr(22))
tw = bbox[2]-bbox[0]
d.text((center_x - tw//2, 225), text2, fill=CRIT, font=fr(22))

text3 = "400 Suppliers Monitored"
bbox = d.textbbox((0,0), text3, font=fr(20))
tw = bbox[2]-bbox[0]
d.text((center_x - tw//2, 260), text3, fill=MUTED, font=fr(20))

# --- Right side: pipeline mini diagram ---
d.rounded_rectangle([680, 330, W-30, 540], radius=16, fill=(30, 41, 59), outline=(71, 85, 105))
d.text((710, 345), "PIPELINE", fill=ACCENT, font=fb(16))

steps = ["Source Data", "\u2192", "AI Functions", "\u2192", "Dynamic Tables", "\u2192", "Dashboard"]
x = 710
for step in steps:
    if step == "\u2192":
        d.text((x, 385), step, fill=ACCENT, font=fb(20))
        x += 30
    else:
        d.text((x, 385), step, fill=FG, font=fr(15))
        x += d.textbbox((0,0), step, font=fr(15))[2] + 8

d.text((710, 425), "8,000 defects classified by AI_CLASSIFY", fill=MUTED, font=fr(14))
d.text((710, 450), "30,000 complaints scored by SENTIMENT", fill=MUTED, font=fr(14))
d.text((710, 475), "AI_COMPLETE generates risk summaries", fill=MUTED, font=fr(14))
d.text((710, 500), "Alert fires every 60 min  |  Task snapshots daily", fill=MUTED, font=fr(14))

# --- Bottom bar ---
d.rectangle([0, H-55, W, H], fill=(20, 83, 45))

# "8 Snowflake Features | 5-Tab Dashboard | Built with CoCo"
bottom = "8 Snowflake Features  |  5-Tab Dashboard  |  Dark/Light Theme  |  Built with CoCo"
bbox = d.textbbox((0,0), bottom, font=fb(18))
tw = bbox[2]-bbox[0]
d.text(((W-tw)//2, H-42), bottom, fill=ACCENT, font=fb(18))

# --- Bake score badge (top right corner) ---
d.rounded_rectangle([W-130, 60, W-20, 100], radius=15, fill=HEALTH_BG, outline=ACCENT)
text = "BAKE: 4/5"
bbox = d.textbbox((0,0), text, font=fb(18))
tw = bbox[2]-bbox[0]
d.text((W-75-tw//2, 68), text, fill=ACCENT, font=fb(18))

img.save(OUTPUT)
print(f"Thumbnail saved: {OUTPUT}")
print(f"Size: {os.path.getsize(OUTPUT)//1024}KB")
