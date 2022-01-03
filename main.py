import pygame
from pygame.locals import *

from sprites import Player, Box, BoxPlace, Wall, Floor
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, MAX_FPS, BACKGROUND

pygame.init()


class Game:

    def __init__(self, debug=False):

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.window_size = (self.width, self.height)

        self.window = self.create_window(self.window_size)

        self.debug = debug

        self.running = True
        self.timer = pygame.time.Clock()
        self.max_fps = MAX_FPS

        self.title = "My Game"
        self.listeners = {}

        self.on_event(QUIT, self.shutdown)
        self.on_event(KEYDOWN, self.quit_pressed)

    def load_level(self, lvl: int = 1):

        self.objects = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.boxes = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.box_places = pygame.sprite.Group()

        self.update_title("sokoban")

        with open(f'levels/lvl-{lvl}.txt') as file:
            for row_index, row in enumerate(file.read().splitlines()):
                for col_index, cell in enumerate(row):

                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if cell == "@":    # player
                        self.player.add(Player((x, y)))
                    elif cell == "$":  # box
                        self.boxes.add(Box((x, y)))
                    elif cell == "#":  # wall
                        self.walls.add(Wall((x, y)))
                    elif cell == '%':  # box place
                        self.box_places.add(BoxPlace((x, y)))
                    if cell in ['.', '$', '@', '%']:  # floor
                        self.floors.add(Floor((x, y)))

        self.objects.add(self.floors, self.box_places, self.boxes, self.walls, self.player)

    def run(self):

        self.load_level()

        while self.running:
            self.elapsed = self.timer.tick(self.max_fps) / 1000

            self.window.fill(BACKGROUND)

            if self.debug:
                self.show_fps()

            # draw stuff to the screen.
            # update all the objects.
            self.objects.draw(self.window)
            self.objects.update()

            # process game events.
            for event in pygame.event.get():
                if event.type in self.listeners.keys():
                    self.emit(event.type, event)

                if event.type == pygame.KEYDOWN:

                    # player movement animation
                    for i in range(TILE_SIZE // self.player.sprite.move_step):
                        self.objects.draw(self.window)  # draw stuff to the screen.
                        self.objects.update()  # update all the objects.
                        self.movement_collision()
                        pygame.display.update()

                    # level restart
                    if event.key == pygame.K_v:
                        self.load_level()

            pygame.display.update()

        self.teardown()

    def movement_collision(self):
        player = self.player.sprite

        player.rect.move_ip(*player.velocity)

        for sprite in self.walls.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.velocity.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.velocity.y < 0:
                    player.rect.top = sprite.rect.bottom
                elif player.velocity.y > 0:
                    player.rect.bottom = sprite.rect.top

    def create_window(self, size):
        return pygame.display.set_mode(size)

    def get_delta_time(self):
        if hasattr(self, "elapsed") and self.elapsed is not None:
            return self.elapsed

    def show_fps(self):
        font = pygame.font.SysFont('arial', 30)
        text = font.render(str(int(self.timer.get_fps())), 1, pygame.Color((255, 0, 0)))
        self.window.blit(text, (0, 0))

    def update_title(self, title):
        if title == "":
            title = self.title
        else:
            title = "%s - %s" % (self.title, title)
        pygame.display.set_caption(title)

    def shutdown(self):
        self.running = False

    def quit_pressed(self, evt):
        if evt.key in (K_ESCAPE, K_q):
            pygame.event.post(pygame.event.Event(QUIT))

    def teardown(self):
        pygame.quit()

    def emit(self, evt_type, evt):
        for listener, args in self.listeners[evt_type]:
            listener(evt, *args)

    def on_event(self, evt_type, cb, *args):
        if evt_type not in self.listeners.keys():
            self.listeners[evt_type] = []
        self.listeners[evt_type].append((cb, args))


def main():
    app = Game(debug=True)
    app.run()


if __name__ == '__main__':
    main()
