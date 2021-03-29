##--Dydy2412--##
import pygame as pg
from lib.labygen_exr import gen_matrix, gen_laby_ex
import sys

#TOOL
COLOR = {
    "BLACK" : (0, 0, 0),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 0, 0),
    "GREEN" : (0, 255, 0),
    "BLUE" : (0, 0, 255),
    "YELLOW" : (255, 255, 0),
    "MAGENTA" : (255, 0, 255),
    "CYAN" : (0, 255, 255),
    "LIGHT_DARK_BLUE": (133, 136, 215)
}

##--CONST--##
LONG = 50
LARGE = 50

WALL_SIZE = 10
WALL_WIDTH = 2
WIN_TITLE = 'LabyGame'
WIN_FPS = 60

PLAYER_SIZE = int(0.2*WALL_SIZE)
PLAYER_COORD = (int(WALL_SIZE*0.25), int(WALL_SIZE*0.25))
PALYER_SPEED = 2

class Player(pg.sprite.Sprite):
    '''Sprite that control the user'''

    def __init__(self, size : int, coord : tuple, speed : int):
        super().__init__()

        #Parameter
        self.size = size
        self.x = coord[0]
        self.y = coord[1]
        self.speed = speed

        #Image
        self.image = pg.Surface((self.size, self.size)).convert_alpha()
        self.image.fill(COLOR["RED"])

        #Rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        '''Constantly update by all-sprite group'''

        #keyboard input
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pg.K_UP]:
            self.rect.y -= self.speed

        if keys[pg.K_DOWN]:
            self.rect.y += self.speed

    def reset_pos(self):
        '''Reset Player Position'''
        self.rect.x = self.x
        self.rect. y = self.y

class Wall(pg.sprite.Sprite):
    '''Wall of the Labyrinth'''

    def __init__(self, height : int, width : int, coords : tuple):
        super().__init__()

        #Parameter
        self.height = height
        self.width = width
        self.x = coords[0]
        self.y = coords[1]

        #Image
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill(COLOR["BLACK"])

        #Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Finish(pg.sprite.Sprite):
    '''End arera'''

    def __init__(self, height : int, width : int, coords : tuple):
        super().__init__()

        #Parameter
        self.height = height
        self.width = width
        self.x = coords[0]
        self.y = coords[1]

        #Image
        self.image = pg.Surface((self.width, self.height)).convert_alpha()
        self.image.fill(COLOR["CYAN"])

        #Rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Application():
    '''Main Frame'''

    def __init__(self, name : str, win_size : tuple, laby_size : tuple, wall_size : tuple, fps : int):
        
        #Parameter
        self.long = laby_size[0]
        self.large = laby_size[1]

        self.walls_height = wall_size[0]
        self.wall_width = wall_size[1]
        
        self.win_height = win_size[0]
        self.win_width = win_size[1]
        self.fps = fps

        # Set the Frame
        pg.display.set_caption(name)
        self.screen = pg.display.set_mode((self.win_height, self.win_width))
        self.clock = pg.time.Clock()

        # Process
        self.is_running = True

        #Game object
        self.player = None
        
        #Sprite Group
        self.all_sprites = pg.sprite.Group()
        self.walls_sprites = pg.sprite.Group()

    def collide_group(self, sprite_1, sprites_2):
        return pg.sprite.spritecollide(sprite_1, sprites_2, False, pg.sprite.collide_mask)

    def collide_sprite(self, sprite_1, sprite_2):
        return pg.sprite.collide_mask(sprite_1, sprite_2)

    def setup_laby(self, vwalls : list, hwalls : list, wall_size : int, wall_width : int):
        '''Place wall on the screen'''
        
        for i in range(len(vwalls)):
            for j in range(len(vwalls[i])):
                x1 = wall_size*j
                y1 = wall_size*i
                if not vwalls[i][j]:
                    wall = Wall(wall_size+wall_width, wall_width, (x1,y1))
                    self.all_sprites.add(wall)
                    self.walls_sprites.add(wall)

        for i in range(len(hwalls)):
            for j in range(len(hwalls[i])):
                x1 = wall_size*j
                y1 = wall_size*i
                if not hwalls[i][j]:
                    wall = Wall(wall_width, wall_size+wall_width, (x1,y1))
                    self.all_sprites.add(wall)
                    self.walls_sprites.add(wall)

    def reset(self):
        '''Reset before run'''
        
        #clear groups
        self.all_sprites.empty()
        self.walls_sprites.empty()

        #Create Player
        self.player = Player(PLAYER_SIZE, PLAYER_COORD, PALYER_SPEED)
        self.all_sprites.add(self.player)

        #Genrate labyrinth
        cells, vwalls, hwalls = gen_matrix(LONG, LARGE)
        cells, vwalls, hwalls = gen_laby_ex(vwalls, hwalls, cells, self.long, self.large, False)
        self.setup_laby(vwalls, hwalls, self.walls_height, self.wall_width)

        #Place finish
        self.finish = Finish(int(self.walls_height/2), int(self.walls_height/2), (int(self.win_height-0.75*self.walls_height), int(self.win_width-0.75*self.walls_height)))
        self.all_sprites.add(self.finish)

        #run the game
        self.run()


    def run(self):
        '''GameLoop'''

        while self.is_running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def events(self):
        '''Handle all events beetwin user and game'''

        for event in pg.event.get():
            
            #Close the window if tha player samsh the red cross
            if event.type == pg.QUIT:
                self.is_running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.reset()

    def update(self):
        '''update pos and state of sprite'''
        self.all_sprites.update()

        hits = self.collide_group(self.player, self.walls_sprites)
        if hits:
            self.player.reset_pos()

        arrived = self.collide_sprite(self.player, self.finish)
        if arrived:
            self.reset()

    def draw(self):
        '''Draw on screen'''

        self.screen.fill(COLOR["WHITE"])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

if __name__ == "__main__":
    sys.setrecursionlimit(5000) #Allow bigger generation
    app = Application(WIN_TITLE, 
                        (WALL_SIZE*LARGE+WALL_WIDTH,
                            WALL_SIZE*LONG+WALL_WIDTH),
                        (LONG, LARGE), 
                        (WALL_SIZE, WALL_WIDTH), 
                        WIN_FPS)
    
    while app.is_running:
        app.reset()