import pygame
import sprites
import snipets


class Game:
    def __init__(self):
        pygame.font.init()
        self.screen_x = 1000
        self.screen_y = 1000
        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("tilegame")
        self.back_ground = pygame.image.load("back_ground.png")
        self.back_ground = pygame.transform.scale(self.back_ground, (self.screen_x, self.screen_y))
        self.White = 250, 250, 250
        self.clock = pygame.time.Clock()
        self.score = 0

        self.rock_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.player_sheet = sprites.SpriteSheet("ninja_f.png")
        self.coin_sheet = sprites.SpriteSheet("coin_rot_anim.png")
        self.enemy_sheet = sprites.SpriteSheet("enemy.png")
        self.create_map()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.directions = ["right", "left", "up", "down"]
        self.player = None

    def create_map(self):
        for x, row in enumerate(snipets.tile_map):
            for y, column in enumerate(row):
                if column == "P":
                    self.player = sprites.Player(1.2, self.player_group, x, y, self)

        for x, row in enumerate(snipets.tile_map):
            for y, column in enumerate(row):
                if column == "R":
                    sprites.Rock((snipets.tile_size_x, snipets.tile_size_y + 35), self.rock_group, x, y)
                if column == "C":
                    sprites.Coin(self, x, y, self.coin_group, 1.4)
                if column == "E":
                    sprites.Enemy(self, x, y, self.enemy_group, 1, self.player)

    def draw(self):
        self.screen.blit(self.back_ground, (0, 0))
        self.rock_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.coin_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        score_text = self.font.render(f"score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 30))
        pygame.display.update()

    def main(self):
        run = True
        while run:
            self.clock.tick(snipets.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.player_group.update()
            self.coin_group.update()
            self.enemy_group.update()
            self.draw()


game = Game()

game.main()
