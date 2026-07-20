#!/usr/bin/env python3
# Moldura Davision para o vídeo 2 (meme): cobre a faixa de texto no topo
# com o cabeçalho estilo tweet e deixa a filmagem intacta embaixo.
from PIL import Image, ImageDraw, ImageFont
from make_header import (W, PAD, FONT_BOLD, FONT_REG, load_logo, make_badge, wrap)

CANVAS_H = 1280
FOOTAGE_TOP = 452          # a filmagem começa aqui; acima é a faixa preta do texto
HOOK = "A ARGENTINA PERDEU PRA ESPANHA E O BRASIL NÃO PERDOOU."
NAME = "Davision"
HANDLE = "@davision.eth"

def build():
    chrome = Image.new("RGBA", (W, CANVAS_H), (0, 0, 0, 0))
    band = Image.new("RGBA", (W, FOOTAGE_TOP), (0, 0, 0, 255))  # faixa opaca do cabeçalho
    d = ImageDraw.Draw(band)

    logo_size = 88
    logo, real = load_logo(logo_size)
    badge = make_badge(32)
    f_name = ImageFont.truetype(FONT_BOLD, 34)
    f_handle = ImageFont.truetype(FONT_REG, 29)

    top_pad = 46
    lx, ly = PAD, top_pad
    band.paste(logo, (lx, ly), logo)
    tx = lx + logo_size + 18
    n_asc, n_desc = f_name.getmetrics()
    h_asc, h_desc = f_handle.getmetrics()
    gap_id = 4
    block_h = (n_asc + n_desc) + gap_id + (h_asc + h_desc)
    name_y = ly + (logo_size - block_h) // 2
    d.text((tx, name_y), NAME, font=f_name, fill=(255, 255, 255, 255))
    nw = d.textlength(NAME, font=f_name)
    bx = int(tx + nw + 10)
    by = int(name_y + n_asc - badge.size[1] + 2)
    band.paste(badge, (bx, by), badge)
    handle_y = name_y + (n_asc + n_desc) + gap_id
    d.text((tx, handle_y), HANDLE, font=f_handle, fill=(113, 118, 123, 255))

    # hook
    max_w = W - 2*PAD
    hook_size = 50
    while hook_size >= 34:
        f_hook = ImageFont.truetype(FONT_BOLD, hook_size)
        lines = wrap(d, HOOK, f_hook, max_w)
        if len(lines) <= 3:
            break
        hook_size -= 2
    f_hook = ImageFont.truetype(FONT_BOLD, hook_size)
    lines = wrap(d, HOOK, f_hook, max_w)
    line_gap = int(hook_size * 0.34)
    a2, d2 = f_hook.getmetrics()
    line_h = a2 + d2
    y = ly + logo_size + 30
    for ln in lines:
        d.text((PAD, y), ln, font=f_hook, fill=(255, 255, 255, 255))
        y += line_h + line_gap

    chrome.paste(band, (0, 0), band)
    chrome.save("chrome2.png")
    print("chrome2.png", chrome.size, "| faixa 0..%d" % FOOTAGE_TOP,
          "| hook", hook_size, "px /", len(lines), "linhas | logo real:", real,
          "| hook_end_y", y)

if __name__ == "__main__":
    build()
