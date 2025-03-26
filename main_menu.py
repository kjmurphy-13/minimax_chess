from config import WIDTH,TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER, FPS
import pygame
import sys

class Button:
    def __init__(self, rect, text, font, action=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# --------------------------
# Main Menu Function
# --------------------------
def main_menu(screen):
    menu_font = pygame.font.SysFont("Arial", 32)
    title_font = pygame.font.SysFont("Arial", 48)
    clock = pygame.time.Clock()

    ai_depth = 3
    ai_time = 2.0

    depth_dec_btn = Button((WIDTH // 2 - 200, 250, 50, 50), "-", menu_font)
    depth_inc_btn = Button((WIDTH // 2 + 200, 250, 50, 50), "+", menu_font)
    time_dec_btn = Button((WIDTH // 2 - 200, 350, 50, 50), "-", menu_font)
    time_inc_btn = Button((WIDTH // 2 + 200, 350, 50, 50), "+", menu_font)
    start_btn = Button((WIDTH // 2 - 75, 450, 150, 50), "Start Game", menu_font)

    running = True
    while running:
        screen.fill((30, 30, 30))
        title_surface = title_font.render("Chess Game Settings", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)

        depth_text = menu_font.render(f"AI Depth: {ai_depth}", True, TEXT_COLOR)
        time_text = menu_font.render(f"Time/Move: {ai_time:.1f}s", True, TEXT_COLOR)
        screen.blit(depth_text, depth_text.get_rect(center=(WIDTH // 2, 275)))
        screen.blit(time_text, time_text.get_rect(center=(WIDTH // 2, 375)))

        for btn in [depth_dec_btn, depth_inc_btn, time_dec_btn, time_inc_btn, start_btn]:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if depth_dec_btn.is_clicked(event):
                ai_depth = max(1, ai_depth - 1)
            if depth_inc_btn.is_clicked(event):
                ai_depth += 1
            if time_dec_btn.is_clicked(event):
                ai_time = max(0.5, ai_time - 0.5)
            if time_inc_btn.is_clicked(event):
                ai_time += 0.5
            if start_btn.is_clicked(event):
                running = False

        pygame.display.flip()
        clock.tick(FPS)
    return ai_depth, ai_time