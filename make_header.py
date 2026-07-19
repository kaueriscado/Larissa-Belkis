#!/usr/bin/env python3
# Gera o cabeçalho estilo post do X (Twitter) para o vídeo do @davision.eth
import os, math
from PIL import Image, ImageDraw, ImageFont

W = 720                     # largura do vídeo original
PAD = 44                    # margem lateral
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

HOOK = "O GOL MAIS BONITO DA VIDA DE PELÉ NUNCA FOI FILMADO. A IA RECRIOU ELE."
NAME = "Davision"
HANDLE = "@davision.eth"

# ---------- logo ----------
def make_logo(size=140):
    """Círculo amarelo com um olho, fundo transparente (stand-in do logo.png)."""
    s = size * 4  # supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    yellow = (245, 197, 24, 255)
    d.ellipse([0, 0, s, s], fill=yellow)
    # olho: amêndoa branca centralizada
    cx, cy = s/2, s/2
    ew, eh = s*0.62, s*0.34
    d.ellipse([cx-ew/2, cy-eh/2, cx+ew/2, cy+eh/2], fill=(255, 255, 255, 255))
    # íris
    ir = s*0.15
    d.ellipse([cx-ir, cy-ir, cx+ir, cy+ir], fill=(20, 20, 24, 255))
    # pupila
    pr = s*0.07
    d.ellipse([cx-pr, cy-pr, cx+pr, cy+pr], fill=(0, 0, 0, 255))
    # brilho
    gr = s*0.03
    d.ellipse([cx-ir*0.4-gr, cy-ir*0.4-gr, cx-ir*0.4+gr, cy-ir*0.4+gr], fill=(255, 255, 255, 255))
    return img.resize((size, size), Image.LANCZOS)

def load_logo(size=140):
    for p in ("logo.png", "../logo.png"):
        if os.path.exists(p):
            lg = Image.open(p).convert("RGBA")
            # recorte redondo de segurança
            lg = lg.resize((size, size), Image.LANCZOS)
            mask = Image.new("L", (size*4, size*4), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, size*4, size*4], fill=255)
            mask = mask.resize((size, size), Image.LANCZOS)
            out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            out.paste(lg, (0, 0), lg)
            out.putalpha(mask)
            return out, True
    return make_logo(size), False

# ---------- selo verificado (azul, estilo X) ----------
def make_badge(size=48):
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blue = (29, 155, 240, 255)
    cx, cy, R = s/2, s/2, s*0.42
    bumps = 8
    pts = []
    steps = 720
    for i in range(steps):
        a = 2*math.pi*i/steps
        r = R * (1 + 0.14*math.cos(bumps*a))
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    d.polygon(pts, fill=blue)
    # check branco
    lw = int(s*0.09)
    d.line([(cx-s*0.17, cy+s*0.02), (cx-s*0.03, cy+s*0.16), (cx+s*0.20, cy-s*0.15)],
           fill=(255, 255, 255, 255), width=lw, joint="curve")
    return img.resize((size, size), Image.LANCZOS)

# ---------- quebra de linha ----------
def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def build_header():
    logo_size = 132
    logo, real = load_logo(logo_size)
    badge = make_badge(46)

    f_name = ImageFont.truetype(FONT_BOLD, 40)
    f_handle = ImageFont.truetype(FONT_REG, 32)

    # Ajuste dinâmico do tamanho do hook para caber em no máx. 3 linhas
    max_w = W - 2*PAD
    tmp = Image.new("RGB", (10, 10))
    td = ImageDraw.Draw(tmp)
    hook_size = 52
    while hook_size >= 34:
        f_hook = ImageFont.truetype(FONT_BOLD, hook_size)
        lines = wrap(td, HOOK, f_hook, max_w)
        if len(lines) <= 3:
            break
        hook_size -= 2
    f_hook = ImageFont.truetype(FONT_BOLD, hook_size)
    lines = wrap(td, HOOK, f_hook, max_w)
    line_gap = int(hook_size * 0.34)
    asc, desc = f_hook.getmetrics()
    line_h = asc + desc

    top_pad = 40
    id_h = logo_size
    gap_id_hook = 34
    hook_block = len(lines)*line_h + (len(lines)-1)*line_gap
    bottom_pad = 44
    H = top_pad + id_h + gap_id_hook + hook_block + bottom_pad

    hdr = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(hdr)

    # identidade
    lx, ly = PAD, top_pad
    hdr.paste(logo, (lx, ly), logo)
    tx = lx + logo_size + 22
    name_y = ly + 20
    d.text((tx, name_y), NAME, font=f_name, fill=(255, 255, 255))
    nw = d.textlength(NAME, font=f_name)
    bx = int(tx + nw + 12)
    by = int(name_y + (f_name.getmetrics()[0]) - badge.size[1] + 6)
    hdr.paste(badge, (bx, by), badge)
    d.text((tx, name_y + 48), HANDLE, font=f_handle, fill=(136, 143, 152))

    # hook
    y = ly + id_h + gap_id_hook
    for ln in lines:
        d.text((PAD, y), ln, font=f_hook, fill=(255, 255, 255))
        y += line_h + line_gap

    hdr.save("header.png")
    with open("header_h.txt", "w") as fh:
        fh.write(str(H))
    print("header.png", W, "x", H, "| hook_size", hook_size, "| linhas", len(lines),
          "| logo real:", real)
    return H

if __name__ == "__main__":
    build_header()
