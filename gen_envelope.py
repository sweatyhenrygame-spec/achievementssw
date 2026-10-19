from PIL import Image, ImageDraw, ImageFilter

S = 4  # supersampling
W, H = 512*S, 512*S
img = Image.new("RGBA", (W, H), (0,0,0,0))
d = ImageDraw.Draw(img)

def sc(*p):
    if all(isinstance(v, (int, float)) for v in p) and len(p) % 2 == 0:
        p = [(p[i], p[i+1]) for i in range(0, len(p), 2)]
    return [(x*S, y*S) for x, y in p]

# --- background: soft radial-ish gradient circle badge ---
cx, cy, r = 256, 250, 235
for i in range(r, 0, -2):
    t = i/r
    col = (int(96+80*t), int(70+50*t), int(200-40*t), 255)
    d.ellipse([ (cx-i)*S,(cy-i)*S,(cx+i)*S,(cy+i)*S ], fill=col)

# outer ring
d.ellipse([(cx-r-10)*S,(cy-r-10)*S,(cx+r+10)*S,(cy+r+10)*S], outline=(255,215,120,255), width=6*S)

# --- envelope shadow ---
sh = Image.new("RGBA",(W,H),(0,0,0,0))
sd = ImageDraw.Draw(sh)
sd.polygon(sc(120,190, 400,190, 415,345, 105,345), fill=(0,0,0,110))
sh = sh.filter(ImageFilter.GaussianBlur(10*S))
img = Image.alpha_composite(img, sh)
d = ImageDraw.Draw(img)

# --- envelope body ---
env_l, env_t, env_r, env_b = 110, 175, 402, 340
d.polygon(sc(env_l,env_t, env_r,env_t, env_r,env_b, env_l,env_b), fill=(250,247,240,255), outline=(200,190,170,255))

# side folds (subtle shading)
d.polygon(sc(env_l,env_b, env_l+3,env_b-6, env_r*0.55,env_b-78, env_l+3,env_t+6), fill=(235,228,215,255))
d.polygon(sc(env_r,env_b, env_r-3,env_b-6, env_r*0.45,env_b-78, env_r-3,env_t+6), fill=(235,228,215,255))
d.line(sc((env_l,env_b),( (env_l+env_r)/2, env_b-70)), fill=(220,212,196,255), width=2*S)
d.line(sc((env_r,env_b),( (env_l+env_r)/2, env_b-70)), fill=(220,212,196,255), width=2*S)

# --- open flap (triangle pointing up-back) ---
flap = sc(108,178, 404,178, 256,68)
d.polygon(flap, fill=(243,238,228,255), outline=(200,190,170,255))
# flap inner shade line
d.line(sc(108,178, 404,178), fill=(210,200,182,255), width=3*S)

# --- letter sticking out ---
let_l, let_t, let_r, let_b = 150, 92, 362, 190
d.rectangle(sc(let_l,let_t, let_r,let_b), fill=(255,255,255,255), outline=(205,205,205,255))
# letter text lines
for i, lw in enumerate([0.72, 0.58, 0.66]):
    y = let_t + 22 + i*22
    d.line(sc(let_l+18, y, let_l+18+(let_r-let_l-36)*lw, y), fill=(150,160,190,255), width=5*S)

# re-draw flap edges over letter bottom? no — letter is behind flap top; draw flap front V over letter base area partially:
d.polygon(sc(108,178, 256,120, 404,178), fill=(243,238,228,255))
d.line(sc(108,178, 256,120, 404,178), fill=(200,190,170,255), width=3*S)

# --- wax seal on the V-flap ---
sx, sy = 256, 158
d.ellipse(sc(sx-24,sy-24, sx+24,sy+24), fill=(200,40,60,255), outline=(150,20,40,255))
d.ellipse(sc(sx-16,sy-16, sx+16,sy+16), outline=(240,120,130,255), width=2*S)
d.line(sc(sx,sy-9, sx,sy+9), fill=(255,200,205,255), width=3*S)
d.line(sc(sx-9,sy, sx+9,sy), fill=(255,200,205,255), width=3*S)

# --- sparkles ---
def star(x,y,sz,col=(255,235,160,255)):
    d.polygon(sc(x, y-sz, x+sz*0.28, y-sz*0.28, x+sz, y, x+sz*0.28, y+sz*0.28,
                 x, y+sz, x-sz*0.28, y+sz*0.28, x-sz, y, x-sz*0.28, y-sz*0.28), fill=col)
star(430, 110, 22); star(85, 120, 16); star(455, 300, 14); star(60, 285, 18)

# resize with antialias
img = img.resize((512,512), Image.LANCZOS)
img.save("/workspace/images/katya-novaya.png")
print("saved")
