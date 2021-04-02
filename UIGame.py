##--Dydy2412--##
import pygame as pg
import threading
import socket
import pickle
import uuid
import sys
Vec = pg.math.Vector2

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
LONG = 10
LARGE = 10

WALL_SIZE = 40
WALL_WIDTH = 2
WIN_TITLE = 'LabyGame'
WIN_FPS = 60

PLAYER_SIZE = int(0.2*WALL_SIZE)
PLAYER_COORD = (int(WALL_SIZE*0.25), int(WALL_SIZE*0.25))
PALYER_SPEED = 0.4
PLAYER_FRICT = -0.1

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555
SERVER_FORMAT = 'utf-8'

class Player(pg.sprite.Sprite):
    '''Sprite that control the user'''

    def __init__(self, size : int, coord : tuple, speed : int, frict : int, appli, id):
        super().__init__()

        #Parameter
        self.size = size
        self.x = coord[0]
        self.y = coord[1]
        self.speed = speed
        self.frict = frict
        self.appli = appli
        self.id = id

        #Image
        self.image = pg.Surface((self.size, self.size)).convert_alpha()
        self.image.fill(COLOR["RED"])

        #PHYSICS
        self.pos = Vec(self.x, self.y)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

        #Rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        '''Constantly update by all-sprite group'''
        self.acc = Vec(0, 0)

        #keyboard input
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -self.speed
        
        if keys[pg.K_RIGHT]:
            self.acc.x = self.speed

        if keys[pg.K_UP]:
            self.acc.y = -self.speed

        if keys[pg.K_DOWN]:
            self.acc.y = self.speed

        self.acc += self.vel*self.frict
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if round(self.vel.x) != 0 or round(self.vel.y) != 0:
            self.appli.client.csend('POS',(self.id, (int(self.pos.x), int(self.pos.y))))

    def reset_pos(self):
        '''Reset Player Position'''
        self.pos = Vec(self.x, self.y)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

class Phamtom(pg.sprite.Sprite):
    def __init__(self, size : int, coord : tuple, id):
        super().__init__()

        #Parameter
        self.size = size
        self.x = coord[0]
        self.y = coord[1]
        self.id = id

        #Image
        self.image = pg.Surface((self.size, self.size)).convert_alpha()
        self.image.fill(COLOR["RED"])

        #Rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

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

class Client(socket.socket):

    def __init__(self, host:str, port:int, form:int, appli):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        #Parmater
        self.appli = appli
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.id = appli.id
        print(f'Your Id is {self.id}')
        self.format = form

        #Setup
        self.connect(self.addr)
        self.send(pickle.dumps((self.id, self.appli.player.rect.center)))
        appli.players = pickle.loads(self.recv(2048))

    def receive(self):
        while self.appli.is_running:
            try:
                message = pickle.loads(self.recv(2048))

                if message[0] == 'JOIN':
                    player_info = message[1]
                    if player_info[0] != self.appli.id:
                        print(f'[JOIN]: {player_info[0]} joined the game in pos: {player_info[0]}')
                        player_obj = Phamtom(PLAYER_SIZE, player_info[1], player_info[0])
                        self.appli.all_sprites.add(player_obj)
                        self.appli.players_obj.append(player_obj)
                elif message[0] == 'QUIT':
                    player_id = message[1]
                    for player in self.appli.players_obj:
                        if player.id == player_id:
                            print(f'[QUIT]: {player_id} exited the game')
                            self.appli.players_obj.remove(player)
                            player.kill()
                elif message[0] == 'POSS':
                    print('[MOVED]: positions actualized')
                    self.appli.players = message[1]
                    print(self.appli.players)
                else:
                    print('[INFO]:' + message)

            except:
                #Close Connection when error
                print('You have been kicked or disconnected')
                self.appli.is_running =False
                break

    def csend(self, info, message):
        print(f'Sending {info} {message}')
        paquet = (info, message)
        self.send(pickle.dumps(paquet))

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

        #CLient Network
        self.players = {}
        self.players_obj  = []
        self.id = str(uuid.uuid1())
        self.client = None
        self.client_thread = None

    def collide_group(self, sprite_1, sprites_2):
        return pg.sprite.spritecollide(sprite_1, sprites_2, False, pg.sprite.collide_mask)

    def collide_sprite(self, sprite_1, sprite_2):
        return pg.sprite.collide_mask(sprite_1, sprite_2)

    def start(self):
        '''Set before run'''
        
        #clear groups
        self.all_sprites.empty()
        self.walls_sprites.empty()

        #Create Player
        self.player = Player(PLAYER_SIZE, PLAYER_COORD, PALYER_SPEED, PLAYER_FRICT, self, self.id)
        self.all_sprites.add(self.player)

        # Set Connection
        self.players = {}
        self.players_obj  = []
        self.client = Client(SERVER_HOST, SERVER_PORT, SERVER_FORMAT, self)
        self.client_thread = threading.Thread(target=self.client.receive)
        self.client_thread.start()
        
        # Add other already connected player
        for player in self.players:
            if player != self.id:
                print(f'player already added: {player}, {self.players[player]}')
                phantom = Phamtom(PLAYER_SIZE, self.players[player], player) 
                self.players_obj.append(phantom)
                self.all_sprites.add(phantom)

        #run the game
        self.run()


    def run(self):
        '''GameLoop'''

        while self.is_running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()
        
        self.client.close()

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

        #Update Phantom Posistions
        for player in self.players_obj:
            player.rect.center = self.players[player.id]

        hits = self.collide_group(self.player, self.walls_sprites)
        if hits:
            self.player.reset_pos()

    def draw(self):
        '''Draw on screen'''

        self.screen.fill(COLOR["WHITE"])
        self.all_sprites.draw(self.screen)

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    sys.setrecursionlimit(5000) #Allow bigger generation
    app = Application(WIN_TITLE, 
                        (WALL_SIZE*LARGE+WALL_WIDTH,
                            WALL_SIZE*LONG+WALL_WIDTH),
                        (LONG, LARGE), 
                        (WALL_SIZE, WALL_WIDTH), 
                        WIN_FPS)
    
    app.start()