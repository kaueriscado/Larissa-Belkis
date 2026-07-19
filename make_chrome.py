#!/usr/bin/env python3
# Monta a "moldura" da Davision (720x1280): cabeçalho estilo tweet no topo,
# fundo preto, e uma janela arredondada transparente onde a filmagem aparece.
from PIL import Image, ImageDraw, ImageFont
from make_header import (W, PAD, FONT_BOLD, FONT_REG, HOOK, NAME, HANDLE,
                         load_logo, make_badge, wrap)

CANVAS_H = 1280
# posição do card de vídeo detectada no vídeo original
CARD_X, CARD_Y, CARD_W, CARD_H = 56, 602, 608, 342
RADIUS = 18

def build_chrome():
    chrome = Image.new("RGBA", (W, CANVAS_H), (0, 0, 0, 255))
    d = ImageDraw.Draw(chrome)

    # ----- identidade (avatar pequeno + nome + selo + handle) -----
    logo_size = 88
    logo, real = load_logo(logo_size)
    badge = make_badge(32)
    f_name = ImageFont.truetype(FONT_BOLD, 34)
    f_handle = ImageFont.truetype(FONT_REG, 29)

    top_pad = 44
    lx, ly = PAD, top_pad
    chrome.paste(logo, (lx, ly), logo)
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
    chrome.paste(badge, (bx, by), badge)
    handle_y = name_y + (n_asc + n_desc) + gap_id
    d.text((tx, handle_y), HANDLE, font=f_handle, fill=(113, 118, 123, 255))

    # ----- hook (branco, caixa alta, negrito, 2-3 linhas) -----
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

    # ----- janela arredondada transparente para o vídeo -----
    hole = Image.new("L", (W, CANVAS_H), 0)
    ImageDraw.Draw(hole).rounded_rectangle(
        [CARD_X, CARD_Y, CARD_X + CARD_W - 1, CARD_Y + CARD_H - 1],
        radius=RADIUS, fill=255)
    alpha = chrome.split()[3]
    alpha = Image.composite(Image.new("L", (W, CANVAS_H), 0), alpha, hole)
    chrome.putalpha(alpha)

    chrome.save("chrome.png")
    print("chrome.png", chrome.size, "| hook", hook_size, "px /", len(lines),
          "linhas | card", (CARD_X, CARD_Y, CARD_W, CARD_H), "| logo real:", real)

if __name__ == "__main__":
    build_chrome()
