import pygame, random
from pygame import mixer
from pygame.locals import *
from abc import ABC, abstractmethod
from os import path

# Environment Setting
# Sebagai "Canvas" game
windowW = 360
windowH = 640
FPS = 30

# Game Setting
# Digunakan untuk men-set segala sesuatu parameter yang digunakan
# di dalam game

# Object
Obstacle_Width=80
Obstacle_Height=500
Obstacle_Gap=300

GROUND_HEIGHT =100
GROUND_WIDHT =2 * windowW

# Mechanism
gravity = 0.5
characterSpeed = 7.5
GAME_SPEED=15
HighScore_File="./Highscore.txt"
#HS=1

# Assets
# Inisialisasi semua assets yang akan digunakan di dalam game
# Font
fntGame = "Assets/font/FlappyBirdy.ttf"

# Music
bgm = "Assets/sound/fix.wav"
tap = "Assets/sound/fly.wav"
die = "Assets/sound/die.wav"
tapButton = "Assets/sound/powerup.wav"
skillActive = ["Assets/sound/chikorita.wav",
                "Assets/sound/fletchling.wav",
                "Assets/sound/swablu.wav"]
bgmStageGame = ["Assets/sound/BG-twilight.wav",
                "Assets/sound/BG-Hellzone.wav",
                "Assets/sound/BG-iceage.wav"]
# Image Resource
bgGameSprites = ["Assets/img/bg-twill.png",
                 "Assets/img/bg-lava.png",
                 "Assets/img/bg-ice.jpg" ]

baseGroundSprites = ["Assets/img/grdbase-twill.png",
                     "Assets/img/grdbase-lava.png",
                     "Assets/img/grdbase-ice.png" ]

obstacleSprites = ["Assets/img/obs-twill.png",
                   "Assets/img/obs-lava.png",
                   "Assets/img/obs-ice.png" ]

hpSprites = ["Assets/img/hp1.png",
             "Assets/img/hp2.png",
             "Assets/img/hp3.png"]

menuSprites = ["Assets/img/menu_header_title.png",
               "Assets/img/menu_btn_start.png",
               "Assets/img/menu_btn_quit.png",
               "Assets/img/menu_btn_start_normal.png",
               "Assets/img/menu_btn_start_hover.png",
               "Assets/img/menu_btn_quit_normal.png",
               "Assets/img/menu_btn_quit_hover.png"]
charDesc = ["Assets/img/chikorita_desc.png",
            "Assets/img/fletchling_desc.png",
            "Assets/img/swablu_desc.png"]
gameInteruptScr = [["Assets/img/pause_txt_bnnr.png"],
                   ["Assets/img/gameover_txt_bnnr.png"]]
gameStartBtn = "Assets/img/game_btn_start.png"
transparentBg = pygame.image.load("Assets/img/bg_transparent.png")
transparentBg = pygame.transform.scale(transparentBg, (windowW, windowH))

pygame.init()

font = pygame.font.SysFont(fntGame,45)
white=(0,0,0 )
screen = pygame.display.set_mode((windowW, windowH))
pygame.display.set_caption("FlappyMon - 0.2.6-Alpha")
clock = pygame.time.Clock()

class character(pygame.sprite.Sprite, ABC) :
    def __init__(self) :
        super().__init__()
        self.skill=False
        self.score=0
        self.speed = characterSpeed

    def fallMove(self) :
        self.speed += gravity
        self.rect.y += self.speed
        self.current_img = (self.current_img + 1) % 3
        self.image = self.images[self.current_img]

    def moveUp(self) :
        self.speed = -characterSpeed

    def get_score(self):
        Pos_Detection=False
        if pokeObject.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
            and pokeObject.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
                and Pos_Detection==False:
                    Pos_Detection=True
        if Pos_Detection== True: 
            if pokeObject.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right:

                self.score+=1

    @abstractmethod
    def castSkill() :
        pass

    @abstractmethod
    def drownHP() :
        pass

    @abstractmethod
    def getHP() :
        pass

    @abstractmethod
    def getID() :
        pass

class poke1(character) :
    def __init__(self) :
        super().__init__()
        self.__hp = 3
        self.__idObject = "001"
        self.images = [pygame.image.load("Assets/img/chikorita_up.png").convert_alpha(), 
                       pygame.image.load("Assets/img/chikorita_normal.png").convert_alpha(), 
                       pygame.image.load("Assets/img/chikorita_down.png").convert_alpha()]
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 35
        self.rect.y = int(windowH / 2)
                       

   
    def castSkill(self) :
        if self.score%10==0 and self.__hp<3:
            Pos_Detection=False
            if pokeObject.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
                and pokeObject.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
                    and Pos_Detection==False:
                        Pos_Detection=True
                        self.sound = mixer.Sound(skillActive[0])
                        self.sound.play()
            if Pos_Detection== True: 
                if pokeObject.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right:
                    self.__hp+=1



    def drownHP(self):
        self.__hp -= 1
    
    def getHP(self) :
        return self.__hp
    
    def getID(self) :
        return self.__idObject

class poke2(character) :
    def __init__(self) :
        super().__init__()
        self.__hp = 3
        self.__idObject = "002"
        self.images = [pygame.image.load("Assets/img/fletchling_up.png").convert_alpha(), 
                       pygame.image.load("Assets/img/fletchling_normal.png").convert_alpha(), 
                       pygame.image.load("Assets/img/fletchling_down.png").convert_alpha()]
                       
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 35
        self.rect.y = int(windowH / 2)
    
    def castSkill(self) :
        if self.score%10==0 and self.score>0:
            self.skill=True
            self.sound = mixer.Sound(skillActive[1])
            self.sound.play()
            self.score += 1
        elif((self.score-6)%10==0):
            self.skill=False
        if self.skill==True:
            self.get_score()

    def drownHP(self):
        self.__hp -= 1
        
    
    def getHP(self) :
        return self.__hp

    def getID(self) :
        return self.__idObject

class poke3(character) :
    def __init__(self) :
        super().__init__()
        self.__hp = 3
        self.__idObject = "003"
        self.last_hp=0
        self.images = [pygame.image.load("Assets/img/swablue_up.png").convert_alpha(), 
                       pygame.image.load("Assets/img/swablue_normal.png").convert_alpha(), 
                       pygame.image.load("Assets/img/swablue_down.png").convert_alpha()]
                       
        self.current_img = 0
        self.image = self.images[self.current_img]
        self.rect = self.image.get_rect()
        self.rect.x = 35
        self.rect.y = int(windowH / 2)
    
    def castSkill(self) :
        if self.score%10==0 and self.score>0 :
            self.skill=True
            self.last_hp=self.__hp
            self.sound = mixer.Sound(skillActive[2])
            self.sound.play()
            self.score += 1
        elif((self.score-6)%10==0 and self.score>10):
            self.skill=False
        if self.skill==True:
            self.__hp=self.last_hp    

    def drownHP(self):
        self.__hp -= 1
        return 1
   
    def getHP(self) :
        return self.__hp

    def getID(self) :
        return self.__idObject

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize,img_dir):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(img_dir).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Obstacle_Width, Obstacle_Height))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = Obstacle_Height - ysize
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, choosenCharacter):
        super().__init__()
        for i in range(len(baseGroundSprites)) :
            if(i == int(choosenCharacter.getID()) - 1) :
                image_dir = baseGroundSprites[i]
                break
        self.image = pygame.image.load(image_dir).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = windowH - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED

def get_random_pipes(xpos, obstacleAssets):
    size = random.randint(100, 300)
    for i in range(len(obstacleSprites)) :
        if(i == int(obstacleAssets.getID()) - 1) :
            Obs = Obstacle(False, xpos, size, obstacleSprites[i])
            Obs_inverted = Obstacle(True, xpos, windowH - size - Obstacle_Gap, obstacleSprites[i])
            break
    return Obs, Obs_inverted

def show_score(text,font,color,x,y):
    img=font.render(text,True,color)
    screen.blit(img  ,(x,y))

def load_Highscore():
    file = open(HighScore_File, "r")
    highscore_data = int(file.read())
    file.close()
    return highscore_data

def change_highscore(new_hs):
    f=open("./Highscore.txt","r+")
    f.write(str(new_hs))
    f.close()

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def show_text(text, font_size, font_colour,x,y):
    font = pygame.font.SysFont(None,font_size)
    font_surface = font.render(text, True,font_colour)
    screen.blit(font_surface,(x,y))

chikorita = poke1()
fletchling = poke2()
swablu = poke3()

pokeObject = pygame.sprite.Group()
ground_group = pygame.sprite.Group()

# Main
isGameRun = True
isFromPause = False
isFromDie = False
gameState = "menuGame" # default = menuGame
after_collide = False
after_collide_interval = 4
sfxButton = mixer.Sound(tapButton)
sfxCharacter = [mixer.Sound(skillActive[0]), mixer.Sound(skillActive[1]), mixer.Sound(skillActive[2])]

# Play BGM Music
mixer.music.load(bgm)
mixer.music.play(-1)

while isGameRun :
    
    bgMenuGame = pygame.image.load(bgGameSprites[random.randint(0, 2)])
    bgMenuGame = pygame.transform.scale(bgMenuGame,(windowW, windowH))
    groundMenuGame = [chikorita, fletchling, swablu]
    groundMenuGame = groundMenuGame[random.randint(0,2)]
    for i in range (2):
        ground = Ground(GROUND_WIDHT * i, groundMenuGame)
        ground_group.add(ground)
        
    while(gameState == "menuGame") :
        clock.tick(FPS)
        screen.blit(bgMenuGame, (0,0))

        menu_mouse_POS = pygame.mouse.get_pos()
        menu_Text = pygame.image.load(menuSprites[0])
        menu_Rect = menu_Text.get_rect(center=(windowW / 2, 100))

        btn_play = pygame.image.load(menuSprites[3])
        btn_play_Rect = btn_play.get_rect(center=(windowW / 2, 280))
        btn_quit = pygame.image.load(menuSprites[5])
        btn_quit_Rect = btn_quit.get_rect(center=(windowW / 2, 370))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20, groundMenuGame)
            ground_group.add(new_ground)
        ground_group.update()
        ground_group.draw(screen)

        screen.blit(menu_Text, menu_Rect)
        screen.blit(btn_play, btn_play_Rect)
        screen.blit(btn_quit, btn_quit_Rect)

        if(menu_mouse_POS[0] in range(btn_play_Rect.left, btn_play_Rect.right) and 
           menu_mouse_POS[1] in range(btn_play_Rect.top, btn_play_Rect.bottom)) :
            btn_play = pygame.image.load(menuSprites[4])
            screen.blit(btn_play, btn_play_Rect)
        
        if(menu_mouse_POS[0] in range(btn_quit_Rect.left, btn_play_Rect.right) and 
           menu_mouse_POS[1] in range(btn_quit_Rect.top, btn_quit_Rect.bottom)) :
            btn_quit = pygame.image.load(menuSprites[6])
            screen.blit(btn_quit, btn_quit_Rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "netralState"
                isGameRun = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(menu_mouse_POS[0] in range(btn_play_Rect.left, btn_play_Rect.right) and menu_mouse_POS[1] in range(btn_play_Rect.top, btn_play_Rect.bottom)) :
                    gameState = "chooseCharacter"
                    sfxButton.play() 
        
                if(menu_mouse_POS[0] in range(btn_quit_Rect.left, btn_quit_Rect.right) and menu_mouse_POS[1] in range(btn_quit_Rect.top, btn_quit_Rect.bottom)) :
                    gameState = "netralState"
                    isGameRun = False

        pygame.display.update()
    
    bgMenuGame = pygame.image.load(bgGameSprites[random.randint(0, 2)])
    bgMenuGame = pygame.transform.scale(bgMenuGame,(windowW, windowH))
    groundMenuGame = [chikorita, fletchling, swablu]
    groundMenuGame = groundMenuGame[random.randint(0,2)]
    for i in range (2):
        ground = Ground(GROUND_WIDHT * i, groundMenuGame)
        ground_group.add(ground)
        
    delay_menu = 5
    isCharChoosed = False
    if(isFromDie) :
        mixer.music.load(bgm)
        mixer.music.play(-1)
        isFromDie = False
    while(gameState == "chooseCharacter") :
        clock.tick(FPS)
        screen.blit(bgMenuGame, (0,0))

        select_mouse_POS = pygame.mouse.get_pos()
        select_Text = pygame.image.load(menuSprites[0])
        select_Rect = select_Text.get_rect(center=(windowW / 2, 200))

        btn_chiko = pygame.image.load("Assets/img/chikorita_normal.png")
        btn_chiko_Rect = btn_chiko.get_rect(center=(50, windowH / 2 - 50))
        btn_fletch = pygame.image.load("Assets/img/fletchling_normal.png")
        btn_fletch_Rect = btn_fletch.get_rect(center=(windowW / 2, windowH / 2 - 50))
        btn_swab = pygame.image.load("Assets/img/swablue_normal.png")
        btn_swab_Rect = btn_swab.get_rect(center=(300, windowH / 2 - 50))

        screen.blit(select_Text, select_Rect)
        screen.blit(btn_chiko, btn_chiko_Rect)
        screen.blit(btn_fletch, btn_fletch_Rect)
        screen.blit(btn_swab, btn_swab_Rect)

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20, groundMenuGame)
            ground_group.add(new_ground)
        ground_group.update()
        ground_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "netralState"
                isGameRun = False
            if(delay_menu > 0) :
                delay_menu -= 1
                print(delay_menu)
                pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(select_mouse_POS[0] in range(btn_chiko_Rect.left, btn_chiko_Rect.right) and 
                   select_mouse_POS[1] in range(btn_chiko_Rect.top, btn_chiko_Rect.bottom)) :
                    sfxCharacter[0].play()
                    if(isCharChoosed):
                        pokeObject.remove(pokeObject.sprites()[0])
                    charSelect = chikorita
                    isCharChoosed = True
                    for i in range(len(bgGameSprites)) :
                        if(i == int(charSelect.getID()) - 1) :
                            bgGame = pygame.image.load(bgGameSprites[i])
                            bgGame = pygame.transform.scale(bgGame,(windowW, windowH))
                            bgMenuGame = pygame.image.load(bgGameSprites[i])
                            bgMenuGame = pygame.transform.scale(bgMenuGame,(windowW, windowH))                           
                            break
                    pokeObject.add(charSelect)
                    for i in range (2):
                        ground = Ground(GROUND_WIDHT * i,charSelect)
                        ground_group.add(ground)

                    pipe_group = pygame.sprite.Group()
                    for i in range (2):
                        pipes = get_random_pipes(windowW * i + 800, charSelect)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])
        
                if(select_mouse_POS[0] in range(btn_fletch_Rect.left, btn_fletch_Rect.right) and 
                   select_mouse_POS[1] in range(btn_fletch_Rect.top, btn_fletch_Rect.bottom)) :
                    sfxCharacter[1].play()
                    if(isCharChoosed):
                        pokeObject.remove(pokeObject.sprites()[0])
                    charSelect = fletchling
                    isCharChoosed = True
                    for i in range(len(bgGameSprites)) :
                        if(i == int(charSelect.getID()) - 1) :
                            bgGame = pygame.image.load(bgGameSprites[i])
                            bgGame = pygame.transform.scale(bgGame,(windowW, windowH))
                            bgMenuGame = pygame.image.load(bgGameSprites[i])
                            bgMenuGame = pygame.transform.scale(bgMenuGame,(windowW, windowH))    
                            break
                    pokeObject.add(charSelect)
                    for i in range (2):
                        ground = Ground(GROUND_WIDHT * i,charSelect)
                        ground_group.add(ground)

                    pipe_group = pygame.sprite.Group()
                    for i in range (2):
                        pipes = get_random_pipes(windowW * i + 800, charSelect)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                if(select_mouse_POS[0] in range(btn_swab_Rect.left, btn_swab_Rect.right) and 
                   select_mouse_POS[1] in range(btn_swab_Rect.top, btn_swab_Rect.bottom)) :
                    sfxCharacter[2].play()
                    if(isCharChoosed):
                        pokeObject.remove(pokeObject.sprites()[0])
                    charSelect = swablu
                    isCharChoosed = True
                    for i in range(len(bgGameSprites)) :
                        if(i == int(charSelect.getID()) - 1) :
                            bgGame = pygame.image.load(bgGameSprites[i])
                            bgGame = pygame.transform.scale(bgGame,(windowW, windowH))
                            bgMenuGame = pygame.image.load(bgGameSprites[i])
                            bgMenuGame = pygame.transform.scale(bgMenuGame,(windowW, windowH))    
                            break
                    pokeObject.add(charSelect)
                    for i in range (2):
                        ground = Ground(GROUND_WIDHT * i,charSelect)
                        ground_group.add(ground)

                    pipe_group = pygame.sprite.Group()
                    for i in range (2):
                        pipes = get_random_pipes(windowW * i + 800, charSelect)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])
                
                if(select_mouse_POS[0] in range(137, 223) and 
                   select_mouse_POS[1] in range(448, 493)) :
                    sfxButton.play()
                    gameState = "playGame"
        if(isCharChoosed) :
            deskripsiPoke = pygame.image.load(charDesc[int(charSelect.getID())-1])
            deskripsiPoke_Rect = deskripsiPoke.get_rect(center=(180, (windowH / 2 - 50) + 100))
            screen.blit(deskripsiPoke,deskripsiPoke_Rect)
            startBtn = pygame.image.load(gameStartBtn)
            startBtn_Rect = startBtn.get_rect(center=(windowW / 2, (windowH / 2 - 50) + 200))
            screen.blit(startBtn, startBtn_Rect)
    
        pygame.display.update()

    if(isFromPause) :
        isFromPause = False
    else :
        mixer.music.stop()
        for i in range(len(bgmStageGame)) :
            if(i == int(charSelect.getID()) - 1) :
                mixer.music.load(bgmStageGame[i])
                mixer.music.play(-1)
                break
    while(gameState == "playGame") :
        clock.tick(FPS)
        
        play_menu_POS = pygame.mouse.get_pos()
        for event in pygame.event.get() :
            if(event.type == QUIT) :
                gameState = "netralState"
                isGameRun = False
            if(event.type == KEYDOWN) :
                if(event.key == K_SPACE or event.key == K_UP) :
                    charSelect.moveUp()
                    tap_sound = mixer.Sound(tap)
                    tap_sound.play()
                elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    mixer.music.pause()
                    gameState = "pauseGame"
            if(event.type == pygame.MOUSEBUTTONDOWN) :
                charSelect.moveUp()
                tap_sound = mixer.Sound(tap)
                tap_sound.play()

        if(charSelect.getHP() == 3) :
            hpImg = pygame.image.load(hpSprites[2])
            hpImg = pygame.transform.scale(hpImg, (47,20))
        elif(charSelect.getHP() == 2) :
            hpImg = pygame.image.load(hpSprites[1])
            hpImg = pygame.transform.scale(hpImg, (33,20))
        else :
            hpImg = pygame.image.load(hpSprites[0])
            hpImg = pygame.transform.scale(hpImg, (20,20))
    
        charSelect.fallMove()
        screen.blit(bgGame, (0,0))
        screen.blit(hpImg, (0,5))
        pokeObject.update()
        pokeObject.draw(screen)
        screen.blit(bgGame, (0, 0))
        screen.blit(hpImg, (0,5))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20, charSelect)
            ground_group.add(new_ground)
    
        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            
            pipes = get_random_pipes(windowW * 2, charSelect)
            
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        ground_group.update()
        pipe_group.update()

        pokeObject.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
    
        charSelect.castSkill()
        if len(pipe_group)>0:
            charSelect.get_score()
        show_score(str(charSelect.score),font ,(255,234,0),int(windowW/2)-30,20)
    
        pygame.display.update()
        pygame.display.flip()
        if(pygame.sprite.groupcollide(pokeObject, ground_group, False,False, pygame.sprite.collide_mask)) :
            if(charSelect.getHP() == 0) :
                die_sound = mixer.Sound(die)
                die_sound.play()  
                gameState = "gameOver"
            
            charSelect.drownHP()
            charSelect.rect.x = 35
            charSelect.rect.y = int(windowH / 2) - 20
            charSelect.speed = characterSpeed
            continue

        if (pygame.sprite.groupcollide(pokeObject, pipe_group, False, False, pygame.sprite.collide_mask)):
            if(charSelect.getHP() <= 0) :
                die_sound = mixer.Sound(die)
                die_sound.play()  
                gameState = "gameOver"
        
            if(after_collide) :
                after_collide_interval -= 1
                if(after_collide_interval == 0) :
                    after_collide = False
                    after_collide_interval = 4 
                continue
            else :
                charSelect.drownHP()
                after_collide = True
                continue

    isPauseRunOnce = True    
    while(gameState == "pauseGame") :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "netralState"
                isGameRun = False
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    mixer.music.unpause()
                    isFromPause = True
                    gameState = "playGame"
                elif event.key == pygame.K_q:
                    gameState = "netralState"
                    isGameRun = False
            elif event.type == pygame.MOUSEBUTTONDOWN :
                    mixer.music.unpause()
                    isFromPause = True
                    gameState = "playGame"

        text_banner = pygame.image.load(gameInteruptScr[0][0])
        text_banner_Rect = text_banner.get_rect(center=(windowW / 2, 100))
        screen.blit(transparentBg, (0, 0))
        screen.blit(text_banner, text_banner_Rect)
        show_text("Press C/click screen to continue", 25, (255,255,255),windowW//8 ,windowH//2.5)
        show_text("Press Q to exit game", 25, (255,255,255), windowW//8 ,windowH//2.5 + 20)
        while isPauseRunOnce :
            pygame.display.update()
            isPauseRunOnce = False
        clock.tick(5)

    if(isFromPause) :
        continue
    else :
        mixer.music.stop()
    isGameOverScr = True
    while(gameState == "gameOver") :
        for event in pygame.event.get():
            if event.type == QUIT :
                gameState = "netralState"
                isGameRun = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_r :
                    gameState = "chooseCharacter"
                    isFromDie = True
                    
        screen.blit(transparentBg, (0, 0))
        text_banner = pygame.image.load(gameInteruptScr[1][0])
        text_banner_Rect = text_banner.get_rect(center=(windowW / 2, 100))
        screen.blit(text_banner, text_banner_Rect)
        show_text("Score Anda =  {}".format(charSelect.score),25,(255,255,255),windowW//2 - 50,windowH//4 + 100)
        show_text("Press R to Character Menu",25,(255,255,255),windowW//2 - 95,windowH//4 + 50)
        if charSelect.score > int(load_Highscore()):
            show_text("New Highscore = "+str(charSelect.score),30,(255,255,255),windowW//2 - 75,windowH//4 + 150 )
            change_highscore(charSelect.score)
        else:    
            show_text("HighScore = "+str(load_Highscore()),30,(255,255,255),windowW//2 - 55,windowH//4 + 150 )
        while isGameOverScr :
            pygame.display.update()
            isGameOverScr = False
        clock.tick(5)

pygame.quit()