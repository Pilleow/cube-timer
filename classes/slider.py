import pygame


class Slider:
    def __init__(self, pos: list, size: list, init_value: float, fg_color: list = [255, 244, 232], bg_color: list = [147, 109, 77], border: int = 2):
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.value = init_value
        self.border = border
        self.rect = pygame.Rect(
            pos[0],
            pos[1],
            size[0],
            size[1]
        )

    def set_value(self, new_value: float, round_to: int = -1) -> None:
        if round_to == -1:
            self.value = new_value
        else:
            self.value = round(new_value, round_to)

    def is_over(self, pos: list) -> bool:
        return self.rect.colliderect(pygame.Rect(pos[0], pos[1], 1, 1))

    def render(self, display: object) -> None:
        pygame.draw.rect(display, self.fg_color, self.rect)
        pygame.draw.rect(display, self.bg_color, (
            self.rect[0] + self.border, self.rect[1] + self.border, 
            self.rect[2] - 2*self.border, self.rect[3] - 2*self.border
            ))
        pygame.draw.rect(display, self.fg_color, (
            self.rect[0] + self.border, self.rect[1] + self.border, 
            (self.rect[2] - 2*self.border) * self.value, self.rect[3] - 2*self.border
        ))