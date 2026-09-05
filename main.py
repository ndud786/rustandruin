#import necessary libraries
import pygame
import constants
import characters
import sprites
import levels
import os



#initialise character class    
pygame.init()

#create clock to manage the fps and time
clock = pygame.time.Clock()

#create function to add text to buttons
def get_text(text, nfont, size, colour):
    font = pygame.font.SysFont(nfont, size)
    text = font.render(text, False, colour)
    return text

#make map and generate array of tiles
Map = sprites.Map(25)
Map.gen_tiles()

#Class to create a screen fade effect
class ScreenTransition():
  
  #initialise screen class
    def __init__(self, speed, colour):
        self.speed = speed
        self.fade_counter = 0
        self.colour = colour

    #method to create the fade on the screen
    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, self.colour, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True
            return fade_complete

#create text for each button + screens
Start_Text = get_text("START",  "arialblack", 50, (134,35,42))
Controls_Text = get_text("CONTROLS", "Corbel", 30, (134,35,42))
Exit_Text = get_text("EXIT", "Corbel", 30, (134,35,42))
Back_Text = get_text("BACK", "comic sans", 30, (134,35,42))
Scores_Text = get_text("HighScores", "comic sans", 30, (134,35,42))


#define buttons
Start_Button = pygame.Rect((constants.SCREEN_WIDTH//2 - 150) ,(constants.SCREEN_HEIGHT//2 - 100 ),300,100)  
Controls_Button = pygame.Rect((constants.SCREEN_WIDTH//2 - 100) ,(constants.SCREEN_HEIGHT//2 + 10 ),200,80)  
Exit_Button = pygame.Rect((constants.SCREEN_WIDTH//2 - 100) ,(constants.SCREEN_HEIGHT//2 + 100 ),200,80)
Back_Button = pygame.Rect((constants.SCREEN_WIDTH//2 - 100) ,(constants.SCREEN_HEIGHT//2 + 300 ),200,80)
Scores_Button = pygame.Rect(10, 710, 200, 80)


#put all buttons into an array with hover status and text
Menu_Buttons = [[Start_Button, False, Start_Text], [Controls_Button, False, Controls_Text], [Exit_Button, False, Exit_Text], [Scores_Button, False, Scores_Text]]
Controls_Buttons = [Back_Button, False, Back_Text]

#make display
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("RUST AND RUIN")

#create fade for screen
fade_1 = ScreenTransition(8, (74,61,88))
fade_2 = ScreenTransition(14, (0,0,0))


#define spritesheets for animations
character_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'character', 'mordred_.png')).convert_alpha())
skelly_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'DecrepitBones.png')).convert_alpha())
Feeder_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'CarcassFeeder.png')).convert_alpha())
Cadaver_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'BoundCadaver.png')).convert_alpha())
Hound_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'ToxicHound.png')).convert_alpha())
Crawler_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'UnravelingCrawler.png')).convert_alpha())
health_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'character', 'hearts-red.png')).convert_alpha())
sword_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'character', 'excalibur_.png')).convert_alpha())
Eye_sprites = sprites.spritesheet(pygame.image.load(os.path.join('files', 'enemies', 'GhastlyEye.png')).convert_alpha())

#initialise a list for animations.
character_animations = []
skelly_animations = []
Cadaver_animations = []
Hound_animations = []
Crawler_animations = []
Feeder_animations = []
health_animations = []
sword_animations = []
Eye_animations = []

#load the character's frames of their animations for idle [0:3] and running [4:11] and scale them
for i in range(1,11):
    for j in range(4):
        character_animations.append((sprites.spritesheet.get_image(character_sprites, i, j, 32, 32, 2.25, (0,0,0))))

#load the monsters' frames of their animations [0:3]
for i in range(4):
    skelly_animations.append((sprites.spritesheet.get_image(skelly_sprites, 0, i, 16, 16, 3, (0,0,0))))
    Cadaver_animations.append((sprites.spritesheet.get_image(Cadaver_sprites, 0, i, 16, 16, 3, (0,0,0))))
    Hound_animations.append((sprites.spritesheet.get_image(Hound_sprites, 0, i, 16, 16, 3, (0,0,0))))
    Crawler_animations.append((sprites.spritesheet.get_image(Crawler_sprites, 0, i, 16, 16, 3, (0,0,0))))
    Feeder_animations.append((sprites.spritesheet.get_image(Feeder_sprites, 0, i, 16, 16, 3, (0,0,0))))
    Eye_animations.append((sprites.spritesheet.get_image(Eye_sprites, 0, i, 16, 16, 7, (0,0,0))))

#load heart sprites [0:6] 0 -3 hearts 6 -0 hearts
for i in range(3):
    for j in range(3):
        health_animations.append((sprites.spritesheet.get_image(health_sprites, i, j, 800, 320, 0.2, (0,0,0))))

#load sword animation row 1 column 1 idle, row 2 swing right, row 4 jab (all 4 sprites long)
for i in range(4):
    for j in range(4):
        sword_animations.append((sprites.spritesheet.get_image(sword_sprites, i, j, 32, 32, 2, (0,0,0))))

#load the csv files for all layers of Level1, including collisions
level1_Layer1 = Map.read_csv(os.path.join("tiles", "Level 1", "Level 1_Tile Layer 1.csv"))
level1_Layer2 = Map.read_csv(os.path.join("tiles", "Level 1", "Level 1_items.csv"))
level1_collisions = Map.read_csv(os.path.join("tiles", "Level 1", "Level 1_Collisions.csv"))

Level1_Layers = [level1_Layer1, level1_Layer2, level1_collisions]

#define spritesheet for level 1, and create tiles
level1_spritesheet = sprites.spritesheet(pygame.image.load(os.path.join("files", "tiles", "Level 1", "Dungeon tileset.png")).convert_alpha())
level1_tiles = sprites.spritesheet.create_array(level1_spritesheet, 24, 12, 16, 16, 2, (0,0,0))

#enemy spawn locations
spawnpoints = [(364,60), (364, 750), (100,364), (700, 364)]

#levels
round1_enemies = []
round2_enemies = []
round3_enemies = []
round4_enemies = []

#add enemies to a list in each round, with appropriate health and speed
for i in range(3):
    round1_enemies.append(characters.Enemy(skelly_animations, 20, 50, 2, 10000,10000 , 72, 72, False))
    round2_enemies.append(characters.Enemy(Cadaver_animations, 50, 50, 2.5, 10000,10000 , 72, 72, False))
    round2_enemies.append(characters.Enemy(Feeder_animations, 20, 50, 4, 10000,10000 , 72, 72, False))
    round3_enemies.append(characters.Enemy(skelly_animations, 30, 50, 3, 10000,10000 , 72, 72, False))
    round3_enemies.append(characters.Enemy(Cadaver_animations, 60, 50, 4.5, 10000,10000 , 72, 72, False))
    round3_enemies.append(characters.Enemy(Feeder_animations, 80, 50, 5, 10000,10000 , 72, 72, False))
    round3_enemies.append(characters.Enemy(Hound_animations, 80, 50, 4.75, 10000,10000 , 72, 72, False))
    round3_enemies.append(characters.Enemy(Crawler_animations, 50, 50, 4, 10000,10000 , 72, 72, False))#

#Add Boss to final round
round4_enemies.append(characters.Enemy(Eye_animations, 200, 50, 4, 10000,10000 , 150, 150, False))
    
#add list of enemy of each round to an overall level list.
level1_enemylists = [round1_enemies, round2_enemies, round3_enemies, round4_enemies]

#create level class for level 1
level_1 = levels.Level(4, level1_enemylists, Map, Level1_Layers, level1_tiles)

#load assets
background = pygame.image.load(os.path.join('files', 'background.png'))



#create character
character = characters.Character(character_animations, 6, 100, 5, 400, 400, 72, 72, sword_animations)

#game loop
Menu_Start = False
Round_State = "Not Started"
Game_State = "Menu"
Game_Active = True
Level1_Attempt_Counter = 0
while Game_Active:
    #reset the screen with a blank background
    screen.fill((0,0,0))

    #Check which state the game is in
    if Game_State == "Menu":
        screen.blit(background, (0,0))
        #loop through all buttons and draw them onto the screen depending on their hover status
        for button in Menu_Buttons:
            if not button[1]:
                pygame.draw.rect(screen, (0,0,0), button[0])
            else:
                pygame.draw.rect(screen, (50, 50, 50), button[0])
            screen.blit(button[2], ((button[0].centerx - button[2].get_width()//2),(button[0].centery - button[2].get_height()//2)))

        #event handling
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                Game_Active = False

            #Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()

                #Change GameState when buttons are pressed
                if Start_Button.collidepoint(mousepos):
                    Play_Start = True
                    Game_State = "Playing"
                if Exit_Button.collidepoint(mousepos):
                    Game_Active = False
                if Controls_Button.collidepoint(mousepos):
                    Game_State = "Controls"
                if Scores_Button.collidepoint(mousepos):
                    Game_State = "Scores"

            #Check for mouse motion
            if event.type == pygame.MOUSEMOTION:

                #If mouse is hovering then change hovering to true
                mousepos = pygame.mouse.get_pos()
                for button in Menu_Buttons:
                    if button[0].collidepoint(mousepos):
                        button[1] = True
                    else:
                        button[1] = False
        
        #If the menu has just started
        if Menu_Start:
            if fade_2.fade(screen):
                Menu_Start = False
                fade_2.fade_counter = 0

    #Check which state the game is in
    elif Game_State == "Controls":
        #loop through all buttons and draw them onto the screen depending on their hover status
        screen.fill((175,175,175))
        if Controls_Buttons[1] == False:
            pygame.draw.rect(screen, (255,255,255), Controls_Buttons[0])
        else:
            pygame.draw.rect(screen, (200,200,200), Controls_Buttons[0])

        #draw the buttons and text onto the screen
        screen.blit(Controls_Buttons[2], ((Controls_Buttons[0].centerx - Controls_Buttons[2].get_width()//2),(Controls_Buttons[0].centery - Controls_Buttons[2].get_height()//2)))
        screen.blit(get_text("W A S D  -   USED TO MOVE", "Comic Sans", 20, (0,0,0)), (10, 150))
        screen.blit(get_text("Q  -  tactical roll (dodge attacks)", "Comic Sans", 20, (0,0,0)), (10, 200))
        screen.blit(get_text("left mouse button  -   light attack (less damage, lower cooldown, easy to land)", "Comic Sans", 20, (0,0,0)), (10, 250))
        screen.blit(get_text("right mouse button  -   heavy attack (more damage, higher cooldown, hard to land)", "Comic Sans", 20, (0,0,0)), (10, 300))
        
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_Active = False

            #Check mouse clicks
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
            #Check gamestate when buttons are held
                if Controls_Buttons[0].collidepoint(mousepos):
                    Game_State = "Menu"

            #Check mouse motion
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                
                #If mouse is hovering then change hovering to true
                if Back_Button.collidepoint(mousepos):
                    Controls_Buttons[1] = True
                else:
                    Controls_Buttons[1] = False
    
    #check which state the game is in
    elif Game_State == "Scores":

        #loop through all buttons and draw them onto the screen depending on their hover status
        screen.fill((175,175,175))
        if Controls_Buttons[1] == False:
            pygame.draw.rect(screen, (255,255,255), Controls_Buttons[0])
        else:
            pygame.draw.rect(screen, (200,200,200), Controls_Buttons[0])
        screen.blit(Controls_Buttons[2], ((Controls_Buttons[0].centerx - Controls_Buttons[2].get_width()//2),(Controls_Buttons[0].centery - Controls_Buttons[2].get_height()//2)))

        #print out the highscores and draw them onto the screen
        screen.blit(get_text("Highscores!", "Comic Sans", 90, (246,209,85)), (40, 10))
        screen.blit(get_text("Best times recorded", "Comic Sans", 90, (246,209,85)), (40, 110))
        
        try:
            with open("highscores.txt", "r") as high_score_file:
                scores = high_score_file.read().splitlines()
        except FileNotFoundError:
            scores = []
        for i in range(min(5, len(scores))):
            screen.blit(get_text(f"HighScore {i+1}  :   " + scores[i] + " (s)", "Ariel", 40, (0,0,0)), (150, 400 + i*50))


        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_Active = False

            #Check mouse clicks
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos = pygame.mouse.get_pos()
            #Check gamestate when buttons are held
                if Controls_Buttons[0].collidepoint(mousepos):
                    Game_State = "Menu"

            #Check mouse motion
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                
                #If mouse is hovering then change hovering to true
                if Back_Button.collidepoint(mousepos):
                    Controls_Buttons[1] = True
                else:
                    Controls_Buttons[1] = False

    #Check which state the game is in            
    elif Game_State == "Playing":
        #draw background
        screen.fill((0,0,0))

        #event handling
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                Game_Active = False  
              
            character.movement_key_status(event)
            character.Attack(event) 
        
        #update level
        level_1.update(character, screen, spawnpoints)

        #draw the GUI
        screen.blit(health_animations[6-character.get_health()], (20,0))

        #if the round end, reset the level and character, and change the game state
        if character.EndofDeath or level_1.Completed:

            #If the level was completed, add the newest time to complete level to the text file, and resort them in ascending order
            if level_1.Completed:
                #read existing high scores
                try:
                    with open("highscores.txt", "r") as high_score_file:
                        highscores = [float(score) for score in high_score_file.read().splitlines()]
                except FileNotFoundError:
                    highscores = []

                #insert the new time, sort ascending, keep only the top 5
                highscores.append(level_1.Time_to_complete)
                highscores.sort()
                highscores = highscores[:5]

                #write the updated top 5 back to the file
                with open("highscores.txt", "w") as high_score_file:
                    for score in highscores:
                        high_score_file.write(str(score) + "\n")

            #reset the  leve, character and game states
            level_1.reset(character)
            Menu_Start = True
            Game_State = "Menu"


        #when the game begins, open the screen with a fade
        if Play_Start:
            if fade_1.fade(screen):
                Play_Start = False
                fade_1.fade_counter = 0


    #update display and maintain consistent framerate with clock
    pygame.display.update()
    clock.tick(60)

#end the program
pygame.quit()