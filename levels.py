import random
import pygame

class Level():

    #initialise character class
    def __init__(self, rounds, enemylists, Map, Layers, Tiles):
        self.Timer_Started = False
        self.start_time = 0
        self.round_intro = False
        self.round_intro_time = pygame.time.get_ticks()
        self.Tiles = Tiles
        self.Layers = Layers
        self.Map = Map
        self.Rounds =  rounds
        self.level_attempt_counter = 1
        self.Spawn_Delay = 1000
        self.Last_Spawn_Time = pygame.time.get_ticks()
        self.Completed = False
        self.Congratulations = False
        self.Congratulations_Time = pygame.time.get_ticks()
        self.Time_to_complete = -1

        self.currentround = 0

        #0 -Not Started, 1 -Started
        self.currentround_state = 0

        self.enemylists = enemylists

        #create list for current enemies
        self.current_enemies = []

        #pre-create fonts once instead of every frame
        self.font_small = pygame.font.SysFont("Comic Sans", 15)
        self.font_medium = pygame.font.SysFont("Comic Sans", 20)
        self.font_large = pygame.font.SysFont("Comic Sans", 30)
    
    #function to get text
    def get_text(self, text, font, colour):
        text = font.render(text, False, colour)
        return text

    #handle all the events during the level
    def update(self, character, surface, spawnpoints):

        #change spawnrate of enemies based on round
        spawn_delays = [2000, 1000, 500]
        self.Spawn_Delay = spawn_delays[min(self.currentround, len(spawn_delays) - 1)]
        
        #start the game timer
        if not self.Timer_Started:
            self.start_time = pygame.time.get_ticks()
            self.Timer_Started = True
        
        #add to list of current enemies
        if self.currentround_state == 0:
            for enemy in self.enemylists[self.currentround]:
                self.current_enemies.append(enemy)
            self.currentround_state = 1


        #if there is no text on the screen
        if not self.round_intro and not self.Congratulations:
            
            #spawn in every enemies in current enemies
            for enemy in self.current_enemies:
                if not enemy.Spawned and pygame.time.get_ticks() - self.Last_Spawn_Time > self.Spawn_Delay:
                    x = random.randint(0,3)
                    enemy.rect.x, enemy.rect.y = spawnpoints[x][0], spawnpoints[x][1]
                    enemy.Spawned = True
                    self.Last_Spawn_Time = pygame.time.get_ticks()

        #draw map and gui
        self.Map.draw_level(surface, self.Layers[0], self.Tiles)  
        self.Map.draw_level(surface, self.Layers[1], self.Tiles)
        surface.blit(self.get_text("Attempt Counter:   " + str(self.level_attempt_counter), self.font_small, (255,255,255)), (600, 10))
        surface.blit(self.get_text("Enemies remaining:   " + str(len(self.current_enemies)), self.font_small, (255,255,255)), (600, 30))
        surface.blit(self.get_text(("Round:   " + str((self.currentround + 1))), self.font_medium, (255,255,255)), (400, 10))
        surface.blit(self.get_text("Timer: " + str((pygame.time.get_ticks() - self.start_time)//1000) + "." + str(((pygame.time.get_ticks() - self.start_time)%1000)//10), self.font_medium, (255,255,255)), (250, 10))

        #update character
        character.move(self.Map.array, self.Layers[len(self.Layers) - 1])  
        character.update()  
        character.draw(surface)
        
        #if no text on screen (no intermission)
        if not self.round_intro and not self.Congratulations:

            for enemy in self.current_enemies[:]:
                enemy.update()
                enemy.move(character.get_xy())
                character.Char_attack_hit(enemy, surface)
                enemy.draw(surface)
                enemy.Attack(character)

                #remove enemy from the list if they die
                if not enemy.Alive:
                    self.current_enemies.remove(enemy)
        
        #if all enemies in the round are killed, complete the round
        if len(self.current_enemies) == 0:
            #queue the next round
            if self.currentround != self.Rounds - 1:
                self.currentround_state = 0
                self.currentround += 1
                self.round_intro = True
                self.round_intro_time = pygame.time.get_ticks()
            else:
                #if the final round is completed, queue the congratulations screen
                if not self.Congratulations:
                    self.Congratulations = True
                    self.Time_to_complete = (pygame.time.get_ticks() - self.start_time)//1000 + (((pygame.time.get_ticks() - self.start_time)%1000)//10)/100
                    self.Congratulations_Time = pygame.time.get_ticks()

        #draw text onto the screen at the end of rounds and level  
        if self.round_intro and pygame.time.get_ticks() - self.round_intro_time < 1000:
            surface.blit(self.get_text("Round complete!, Get ready for the next one.", self.font_large, (255,255,255)), (100, 300))
        else:
            self.round_intro = False
        if self.Congratulations and pygame.time.get_ticks() - self.Congratulations_Time < 4000:
            surface.blit(self.get_text("CONGRATULATIONS! LEVEL COMPLETED!", self.font_large, (255,255,255)), (100, 300))
        
        #if the congratulations has been queued, mark the round as complete, and start the end of the congratulation
        elif self.Congratulations:
            self.Completed = True
            self.Congratulations = False

    #method to reset the level and character back to their original parameter values
    def reset(self,character):
        self.Completed = False
        self.Timer_Started = False
        character.reset()
        self.currentround = 0
        self.currentround_state = 0 
        self.level_attempt_counter += 1

        #reset every enemy in enemy list
        for round in self.enemylists:
            for enemy in round:
                enemy.reset()

        #empty the enemies in the current enemies lisy
        self.current_enemies = []

