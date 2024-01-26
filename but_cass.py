import pygame


class All_Buttons:
    def __init__(self, x, y, wight, height, text, image_p, hover_im=None, sound_but=None):
        self.x = x
        self.y = y
        self.wight = wight
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_p)
        self.image = pygame.transform.scale(self.image, (wight, height))
        self.gange = self.image
        if hover_im:
            self.gange = pygame.image.load(hover_im)
            self.gange = pygame.transform.scale(self.gange, (wight, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_but:
            self.sound = pygame.mixer.Sound(sound_but)
        self.is_but = False

    def drow_but(self, screen):
        self.now_image = self.gange if self.is_but else self.image
        screen.blit(self.now_image, self.rect.topleft)
        font = pygame.font.Font("carbona.ttf", 45)
        text_appere = font.render(self.text, True, (22, 68, 120))
        text_rect = text_appere.get_rect(center=self.rect.center)
        screen.blit(text_appere, text_rect)

    def check_mos(self, mos_pose):
        self.is_but = self.rect.collidepoint(mos_pose)

    def al_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_but:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
