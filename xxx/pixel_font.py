import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

class PixelFont:
    def __init__(self, filename="алфавіт.PNG"):
        path = os.path.join(ASSETS_DIR, filename)
        self.glyphs = {}

        if os.path.exists(path):
            sheet = pygame.image.load(path)
            if pygame.display.get_surface() is not None:
                sheet = sheet.convert_alpha()
            
            sheet_w, sheet_h = sheet.get_size()

            # Твої точні координати центрів для всіх символів
            centers = {
                'А': (132, 108), 'Б': (329, 103), 'В': (528, 104),
                'Г': (715, 95),  'Ґ': (915, 94),   'Д': (1129, 108),
                'Е': (123, 239), 'Є': (321, 239), 'Ж': (520, 241),
                'З': (722, 240), 'И': (924, 241), 'І': (1128, 241),
                'Ї': (120, 372), 'Й': (322, 375), 'К': (527, 379),
                'Л': (723, 382), 'М': (922, 379), 'Н': (1127, 379),
                'О': (120, 510), 'П': (322, 510), 'Р': (520, 505),
                'С': (726, 510), 'Т': (925, 500), 'У': (1131, 506),
                'Ф': (125, 641), 'Х': (326, 643), 'Ц': (528, 648),
                'Ч': (725, 638), 'Ш': (920, 644), 'Щ': (1127, 647),
                'Ь': (117, 786), 'Ю': (327, 777), 'Я': (529, 777),
                '0': (726, 777), '1': (922, 775), '2': (1128, 778),
                '3': (125, 911), '4': (331, 914), '5': (524, 910),
                '6': (720, 911), '7': (924, 901), '8': (1128, 911),
                '9': (125, 1040), '!': (321, 1044), '?': (525, 1034),
                ',': (723, 1055), '.': (922, 1061), ':': (1130, 1039),
                ';': (117, 1166), '—': (319, 1163), '-': (520, 1163),
                '+': (721, 1165), '=': (922, 1167), '%': (1121, 1164)
            }

            w_box, h_box = 130, 110
            for char, (cx, cy) in centers.items():
                x = max(0, cx - w_box // 2)
                y = max(0, cy - h_box // 2)
                w = min(w_box, sheet_w - x)
                h = min(h_box, sheet_h - y)
                
                if w > 0 and h > 0:
                    rect = pygame.Rect(x, y, w, h)
                    glyph_surface = sheet.subsurface(rect)
                    self.glyphs[char] = glyph_surface
                    self.glyphs[char.lower()] = glyph_surface

    def render(self, text, scale=1.0):
        # Зменшено в 2 рази (було 26, стало 13 пікселів у висоту)
        target_h = 13 
        
        text = str(text)
        if not self.glyphs:
            fallback_font = pygame.font.SysFont("Arial", 12)
            return fallback_font.render(text, True, (255, 255, 255))

        surfs = []
        chunks_w = 0

        for char in text:
            if char == " ":
                w = 6
                surfs.append(None)
                chunks_w += w
            elif char in self.glyphs:
                glyph = self.glyphs[char]
                orig_h = glyph.get_height()
                if orig_h > 0:
                    current_scale = target_h / orig_h
                    gw = max(1, int(glyph.get_width() * current_scale))
                    gh = max(1, int(glyph.get_height() * current_scale))
                    glyph = pygame.transform.scale(glyph, (gw, gh))
                surfs.append(glyph)
                chunks_w += glyph.get_width() + 1
            else:
                chunks_w += 4

        surface = pygame.Surface((chunks_w, target_h), pygame.SRCALPHA)
        current_x = 0
        for glyph in surfs:
            if glyph:
                y_offset = (target_h - glyph.get_height()) // 2
                surface.blit(glyph, (current_x, y_offset))
                current_x += glyph.get_width() + 1
            else:
                current_x += 6

        return surface

pixel_font = PixelFont()