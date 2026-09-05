#import necessary libraries
import pygame  
import math

class Character():  

    #initialise character class
    def __init__(self, animation_sprites, health, stamina, speed, x, y, width, height, weapon_sprites):
        self.Rolling = False
        self.Spawned = False
        self.EndofDeath = False
        self.Alive = True
        self.Heavy_Attacking = False
        self.Heavy_dmg = 40
        self.Light_Attacking = False
        self.Light_dmg = 10
        self.animation_state = "Idle"
        self.flip = False
        self.original_speed = speed  
        self.speed = speed
        self.diagspeed = self.speed*0.70710678118
        self.charnum = 0
        self.animation_sprites = animation_sprites
        self.HitStun = False
        self.Roll_debounce = pygame.time.get_ticks()
        self.Hittime = pygame.time.get_ticks()
        self.stun_debounce = pygame.time.get_ticks()
        self.heavy_debounce = pygame.time.get_ticks()
        self.light_debounce = pygame.time.get_ticks()
        self.char_animation_refresh = pygame.time.get_ticks()
        self.heavy_attack_refresh = pygame.time.get_ticks()
        self.heavy_attack_animation_refresh = pygame.time.get_ticks()
        self.light_attack_refresh = pygame.time.get_ticks()
        self.light_attack_animation_refresh = pygame.time.get_ticks()
        self.image = animation_sprites[self.charnum]
        self.original_health = health
        self.health = health  
        self.stamina = stamina  
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        if weapon_sprites != False:
            self.weapon_sprites = weapon_sprites
            self.weaponnum = 0
            self.weapon_image = weapon_sprites[self.weaponnum]
            self.weapon_rect = pygame.Rect(self.x, self.y, 50, 60)
        else:
            pass
        self.rect = pygame.Rect(self.x, self.y, width - 40, height - 30)  
        self.Qheld = False
        self.Wheld = False  
        self.Sheld = False  
        self.Aheld = False  
        self.Dheld = False 

    #method to reset the class back to original values
    def reset(self):
        self.HitStun = False
        self.EndofDeath = False
        self.Alive = True
        self.health = 6
        self.Heavy_Attacking = False
        self.Light_Attacking = False
        self.animation_state = "Idle"
        self.flip = False  
        self.charnum = 0
    
    #method to check if an Attack has been queued, and queue the corresponding animation and attacking states
    def Attack(self, event):
        heavy_attack_cd = 1500
        light_attack_cd = 500
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
             if pygame.time.get_ticks() - self.heavy_attack_refresh > heavy_attack_cd:
                  self.Heavy_Attacking = True
                  self.weaponnum = 3
                  self.heavy_attack_refresh = pygame.time.get_ticks()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.time.get_ticks() - self.light_attack_refresh > light_attack_cd:
                self.Light_Attacking = True
                self.weaponnum = 12
                self.light_attack_refresh = pygame.time.get_ticks()

    #method to update the animation state of the character
    def update(self):
        
        #if the character dies, initiate the deah animation sequence
        if not self.Alive:
            self.animation_state = "Death"
        
        #if the character starts a heavy attack, initiate the heavy attack animation
        elif self.Heavy_Attacking:
            heavy_attack_anim_cd = 150
            self.weapon_image = self.weapon_sprites[self.weaponnum]

            #animation time between frames
            if pygame.time.get_ticks() - self.light_attack_animation_refresh > heavy_attack_anim_cd:
                self.weaponnum += 1
                self.light_attack_animation_refresh = pygame.time.get_ticks()
            if self.weaponnum > 7:
                self.Heavy_Attacking = False
            
        #if the character starts a light attack, initiate the light attack animation
        elif self.Light_Attacking:
            light_attack_anim_cd = 100
            self.weapon_image = self.weapon_sprites[self.weaponnum]

            #animation time between frames
            if pygame.time.get_ticks() - self.light_attack_animation_refresh > light_attack_anim_cd:
                self.weaponnum += 1
                self.light_attack_animation_refresh = pygame.time.get_ticks()
            if self.weaponnum > 15:   
                self.Light_Attacking = False


        #how long to wait between changes in state in ticks (cooldown)
        if self.Rolling:
            anim_cd = 100
        elif self.animation_state == "Idle":
            anim_cd = 200
        elif self.animation_state == "Running":
            anim_cd = 100       
        elif self.animation_state == "Death":
            anim_cd = 300
            if self.charnum == 39:
                anim_cd = 1000
        
        #change the frame of the character with the corresponding character number
        self.image = self.animation_sprites[self.charnum]
        if pygame.time.get_ticks() - self.char_animation_refresh > anim_cd:
            self.charnum += 1
            self.char_animation_refresh = pygame.time.get_ticks()

        #Keep animation within relevant loop
        if self.animation_state == "Death" and self.charnum <= 35:
            self.charnum = 35
        elif self.Rolling and (self.charnum <= 19 or self.charnum >= 28):
            self.charnum = 20
        elif self.HitStun and (self.charnum <= 31 or self.charnum >= 36):
            self.charnum = 32
        elif not self.Rolling and not self.HitStun and self.animation_state == "Idle" and self.charnum > 3:
            self.charnum = 0
        elif not self.Rolling and not self.HitStun and self.animation_state == "Running" and (self.charnum <= 3 or self.charnum >=12) :
            self.charnum = 4
        if self.charnum >= 40:
            self.EndofDeath = True
        if self.charnum == 35:
            self.HitStun = False

        #reset the speed when you get to the last frame of rolling animation
        if self.charnum == 27:
            self.Rolling = False
            self.speed = self.original_speed
        
    #method to check if a movement key is held down
    def movement_key_status(self ,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                    self.Rolling = True
            if event.key == pygame.K_w:  
                    self.Wheld = True  
            elif event.key == pygame.K_s:  
                    self.Sheld = True  
            elif event.key == pygame.K_a:  
                    self.Aheld = True  
            elif event.key == pygame.K_d:  
                    self.Dheld = True  
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                    self.Rolling = False  
            if event.key == pygame.K_w:  
                    self.Wheld = False  
            elif event.key == pygame.K_s:  
                    self.Sheld = False  
            elif event.key == pygame.K_a:  
                    self.Aheld = False  
            elif event.key == pygame.K_d:  
                    self.Dheld = False  
    
    #method to move character
    def move(self, tiles, bitmap):

        #adjust the x and y values of the character 
        if self.Wheld:
            if self.Aheld:
                dx = -self.diagspeed
                dy = -self.diagspeed
            elif self.Dheld:
                dx = self.diagspeed
                dy = -self.diagspeed
            elif self.Sheld:
                dx = 0
                dy = 0
                pass
            else:
                dx = 0
                dy = -self.speed    
        elif self.Sheld:
            if self.Aheld:
                dx = -self.diagspeed
                dy = self.diagspeed
            elif self.Dheld:
                dx = self.diagspeed
                dy = self.diagspeed
            elif self.Wheld:
                dx = 0
                dy = 0
                pass
            else: 
                dx = 0
                dy = self.speed 
        elif self.Dheld: 
            if self.Aheld:
                 dx = 0
                 dy = 0
                 pass
            else:
                dx = self.speed
                dy = 0  
        elif self.Aheld: 
            dx = -self.speed
            dy = 0
        else:
            dx = 0
            dy = 0

        #change between "Running" and "Idle" States depending on movement
        if dx == 0 and dy == 0:
            self.animation_state = "Idle"
        elif dx > 0:
            self.flip = False
            self.animation_state = "Running"            
        elif dx < 0:
            self.flip = True
            self.animation_state = "Running" 

        #move the position of the rect if the character is alive and not attacking
        if not self.Heavy_Attacking and self.Alive:

            #check for collisions in the x
            self.rect.move_ip(dx, 0)
            collisions = self.getcollisions(tiles, bitmap) 
            if len(collisions) != 0:

                #reposition the character if a boundary is hit
                if dx > 0:
                    self.rect.x = collisions[0].x - self.rect.width
                elif dx < 0:
                    self.rect.x = collisions[0].x + 32

            #check for collisions in the y
            self.rect.move_ip(0, dy)
            collisions = self.getcollisions(tiles, bitmap) 
            if len(collisions) != 0:

                #reposition the character if a boundary is hit
                if dy < 0:
                    self.rect.y = collisions[0].y + 32
                elif dy > 0:
                    self.rect.y = collisions[0].y - self.rect.height

        #reposition the weapon rect to fit the animation
        self.weapon_rect.y = self.rect.y - 10
        if self.flip:
            self.weapon_rect.x = self.rect.x - self.weapon_rect.width
        else:
            self.weapon_rect.x = self.rect.x + 18

    #method to check if an enemy has been hit by any player attacks. If so, the enemy will take damage  
    def Char_attack_hit(self, enemy, surface):

        #check if alive to carry on
        if self.Alive:
            if self.Heavy_Attacking:
                if self.weapon_rect.colliderect(enemy.rect):
                    if pygame.time.get_ticks() - self.heavy_debounce > 800:
                        enemy.take_damage(self.Heavy_dmg)
                        self.heavy_debounce = pygame.time.get_ticks()

            
            elif self.Light_Attacking:
                if self.weapon_rect.colliderect(enemy.rect):
                    if pygame.time.get_ticks() - self.light_debounce > 410:
                        enemy.take_damage(self.Light_dmg)
                        self.light_debounce = pygame.time.get_ticks()
        
    #method to draw the character onto the screen
    def draw(self, surface):

        #flip the character if they go into the opposite direction
        flipped_char = pygame.transform.flip(self.image, self.flip, False).convert_alpha()
        surface.blit(flipped_char, (self.rect.x - 20, self.rect.y - 22))

        #If Alive draw
        if self.Alive:

            #reposition the weapon rect to fit the animation
            if self.weaponnum < 5 and self.flip:
                self.weapon_rect.move_ip(10,0)
            elif self.weaponnum < 5 and not self.flip:
                self.weapon_rect.move_ip(-10,0)
            if self.weaponnum > 4:
                adjusted_sword = pygame.transform.rotate(self.weapon_image, -90)
                if self.weaponnum < 8:
                    self.weapon_rect.move_ip(0,10)
            else:
                adjusted_sword = self.weapon_image
            if self.weaponnum > 13 and self.flip:
                self.weapon_rect.move_ip(-5,0)
            elif self.weaponnum > 13 and not self.flip:
                self.weapon_rect.move_ip(5,0)
                    

            flipped_sword = pygame.transform.flip(adjusted_sword, self.flip, False).convert_alpha()

            if self.Light_Attacking or self.Heavy_Attacking:
                surface.blit(flipped_sword, (self.weapon_rect.x, self.weapon_rect.y))

            #reposition the weapon rect to fit the animation
            if self.weaponnum < 5 and self.flip:
                self.weapon_rect.move_ip(-10,0)
            elif self.weaponnum < 5 and not self.flip:
                self.weapon_rect.move_ip(10,0)
            elif self.weaponnum > 4 and self.weaponnum < 8:
                self.weapon_rect.move_ip(0,-10)
            elif self.weaponnum > 13 and self.flip:
                self.weapon_rect.move_ip(5,0)
            elif self.weaponnum > 13 and not self.flip:
                self.weapon_rect.move_ip(-5,0)
    
    #return x, y
    def get_xy(self):
         return [self.rect.x, self.rect.y]
    
    #return the tiles that the character collides with
    def getcollisions(self, tiles, bitmap):
        collisions = []
        
        # Calculate grid coordinates based on 32x32 tiles
        player_col = self.rect.x // 32
        player_row = self.rect.y // 32
        
        # Only check immediately adjacent tiles
        for row in range(max(0, player_row - 2), min(len(tiles), player_row + 3)):
            for tile in range(max(0, player_col - 2), min(len(tiles[row]), player_col + 3)):
                if bitmap[row][tile] == "0":
                    if self.rect.colliderect(tiles[row][tile]):
                        collisions.append(tiles[row][tile])
        return collisions
    
    #method to get player health
    def get_health(self):
        return self.health
    
    #method to reduce player health
    def take_damage(self, damage):
        if self.Alive and not self.Rolling:
            self.HitStun = True
            self.health -= damage
            if self.health <= 0:
                self.Alive = False

class Enemy (Character):

    #initialise Enemy class
    def update(self):
        #how long to wait between changes in state in ticks (cooldown)
        char_animation_cd = 150
        self.image = self.animation_sprites[self.charnum]
        if pygame.time.get_ticks() - self.char_animation_refresh > char_animation_cd:
            self.charnum += 1
            self.char_animation_refresh = pygame.time.get_ticks()
        #Keep the animation within its loop
        if self.charnum > 3:
            self.charnum = 0
    
    #every 500 ticks, allow the enemy to attack the player if they are within a 30pixel circle radius
    def Attack(self, enemy):
        if pygame.time.get_ticks() - self.light_debounce > 500:
            dx = enemy.rect.x - self.rect.x
            dy = enemy.rect.y - self.rect.y
            if math.sqrt((dx)**2 + (dy)**2) < 30:
                enemy.take_damage(1)
            
            self.light_debounce = pygame.time.get_ticks()

    #draw the enemy onto the surface
    def draw(self, surface):    
        surface.blit(self.image, self.rect)  

    #method to move the enemy, flip the image if the enemy is moving in the opposite direction
    def move(self, player_xy):
        dx = player_xy[0] - self.rect.x
        dy = player_xy[1] - self.rect.y
        if dx > 0:
            self.flip = False         
        elif dx < 0:
            self.flip = True
        
        #follow the player if they are further than 30 pixels
        if not (math.sqrt((dx)**2 + (dy)**2) < 30 ):
            self.rect.move_ip(self.speed*((dx)/(abs(dx) + abs(dy))), self.speed*((dy)/(abs(dy) + abs(dx))))
    
    #reset the enemies back to original values
    def reset(self):
        self.Alive = True
        self.health = self.original_health
        self.Spawned = False
        self.rect.x = 10000
        self.rect.y = 10000
        