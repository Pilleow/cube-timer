import pygame


class Button:
    def __init__(self, pos: list, padding: list, text: str, fg_color: list, bg_color: list, clicked_bg_color: list, font: object):

        self.text = text
        self.font = font
        self.padding = padding
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.clicked_bg_color = clicked_bg_color
        self.rect = pygame.Rect(
            pos[0], 
            pos[1], 
            padding[0] * 2 + font.size(text)[0], 
            padding[1] * 2 + font.size(text)[1]
        )

        self.clicked = False

    def is_over(self, pos) -> bool:
        return self.rect.colliderect(pygame.Rect(pos[0], pos[1], 1, 1))

    def set_text(self, new_text: str) -> None:
        self.text = new_text

    def set_pos(self, new_pos: list) -> None:
        self.rect = pygame.Rect(
            new_pos[0], 
            new_pos[1], 
            self.padding[0] * 2 + self.font.size(self.text)[0], 
            self.padding[1] * 2 + self.font.size(self.text)[1]
        )

    def render(self, display: object, active: bool) -> None:
        if active and not self.clicked:
            pygame.draw.rect(display, self.clicked_bg_color, self.rect)
        else:
            pygame.draw.rect(display, self.bg_color, self.rect)
        display.blit(
            self.font.render(self.text, 0, self.fg_color), 
            (self.rect[0] + self.padding[0], self.rect[1] + self.padding[1])
        )
