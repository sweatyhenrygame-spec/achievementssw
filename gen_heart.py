from PIL import Image, ImageDraw, ImageFilter

S = 4  # supersampling
W, H = 512 * S, 512 * S
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def sc(*p):
    if all(isinstance(v, (int, float)) for v in p) and len(p) % 2 == 0:
        p = [(p[i], p[i + 1]) for i in range(0, len(p), 2)]
    return [(x * S, y * S) for x, y in p]


# --- background: golden divine gradient circle badge ---
cx, cy, r = 256, 250, 235
for i in range(r, 0, -2):
    t = i / r
    col = (int(255 - 40 * t), int(215 - 90 * t), int(120 - 60 * t), 255)
    d.ellipse([(cx - i) * S, (cy - i) * S, (cx + i) * S, (cy + i) * S], fill=col)

# outer ring
d.ellipse([(cx - r - 10) * S, (cy - r - 10) * S, (cx + r + 10) * S, (cy + r + 10) * S],
          outline=(255, 240, 180, 255), width=6 * S)

# --- light rays behind heart ---
ray_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ray_layer)
import math
for k in range(12):
    ang = k * math.pi / 6
    x1 = cx + math.cos(ang) * 90
    y1 = cy + math.sin(ang) * 90
    x2 = cx + math.cos(ang) * 215
    y2 = cy + math.sin(ang) * 215
    rd.line(sc(x1, y1, x2, y2), fill=(255, 255, 230, 90), width=10 * S)
ray_layer = ray_layer.filter(ImageFilter.GaussianBlur(4 * S))
img = Image.alpha_composite(img, ray_layer)
d = ImageDraw.Draw(img)


# --- heart shape via two circles + triangle ---
def heart(draw, scale=1.0, dx=0, dy=0, fill=None, outline=None, width=1):
    lw, lh = 78 * scale, 66 * scale          # lobes radius/offset
    top_y = 175 + dy
    bot_y = 375 + dy
    mid_x = 256 + dx
    # left lobe
    draw.ellipse([(mid_x - lw - lw * 0.15), top_y - lh, (mid_x - lw * 0.15), top_y + lh],
                 fill=fill, outline=outline, width=width * S)
    # right lobe
    draw.ellipse([(mid_x + lw * 0.15), top_y - lh, (mid_x + lw + lw * 0.15), top_y + lh],
                 fill=fill, outline=outline, width=width * S)
    # bottom triangle
    draw.polygon(sc(mid_x - lw - lw * 0.10, top_y + lh * 0.45,
                    mid_x + lw + lw * 0.10, top_y + lh * 0.45,
                    mid_x, bot_y), fill=fill, outline=outline)


# heart shadow
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
heart(ImageDraw.Draw(sh), fill=(60, 0, 20, 120), dx=6, dy=10)
sh = sh.filter(ImageFilter.GaussianBlur(12 * S))
img = Image.alpha_composite(img, sh)
d = ImageDraw.Draw(img)

# main red heart
heart(d, fill=(225, 30, 60, 255), outline=(150, 10, 40, 255), width=4)

# darker shading on lower-right of heart
shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
heart(ImageDraw.Draw(shade), scale=0.985, fill=(160, 15, 45, 110), dx=8, dy=4)
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rectangle([0, 250 * S, W, H])
img.paste(Image.composite(shade, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask), (0, 0),
          Image.composite(shade, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask))
d = ImageDraw.Draw(img)

# glossy highlight (white ellipse top-left)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse(sc(175, 130, 235, 190), fill=(255, 255, 255, 200))
gd.ellipse(sc(160, 160, 195, 200), fill=(255, 255, 255, 140))
glow = glow.filter(ImageFilter.GaussianBlur(8 * S))
img = Image.alpha_composite(img, glow)
d = ImageDraw.Draw(img)

# small sparkles
for (sx, sy, sr) in [(130, 105, 10), (395, 130, 8), (410, 320, 9), (110, 330, 7)]:
    d.polygon(sc(sx, sy - sr, sx + sr * 0.30, sy - sr * 0.30, sx + sr, sy,
                 sx + sr * 0.30, sy + sr * 0.30, sx, sy + sr,
                 sx - sr * 0.30, sy + sr * 0.30, sx - sr, sy,
                 sx - sr * 0.30, sy - sr * 0.30), fill=(255, 255, 240, 230))

# resize down
img = img.resize((512, 512), Image.LANCZOS)
img.save("images/lesha-love-vadik.png")
print("saved images/lesha-love-vadik.png")
