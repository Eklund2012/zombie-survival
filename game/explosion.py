from .assets import explosion_frames

class Explosion:
    def __init__(self, pos):
        self.frames = explosion_frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer % 10 == 0:  # Justera hastigheten på animationen
            self.index += 1
            if self.index >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.index]

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.image, self.rect)
