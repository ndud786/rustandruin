#import necessary libraries
import pygame
import constants
import os
import csv

class Map():
    #initialise map class
    def __init__(self, tiles):
        self.array = []
        self.tiles = tiles
        self.tilelength = constants.SCREEN_WIDTH//tiles 
    
    #method to read csv files and return an array which can be used in the code
    def read_csv(self, filename):
        bitmap = []
        with open(os.path.join('files', filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                bitmap.append(list(row))
        return bitmap
         
    #generate Rects to act as the tiles in the map
    def gen_tiles(self):
        #loop through rows
        for row in range(self.tiles):
             #create a row
             self.array.append([])

             #loop through tiles
             for tile in range(self.tiles):
                
                #add tiles to each row
                self.array[row].append(pygame.Rect((0 + tile*(self.tilelength)), (0 + row*self.tilelength), self.tilelength, self.tilelength))

    #draw the sprite for each tile onto the rects
    def draw_level(self, surface, bitmap, sprites):
        for row in range(self.tiles):
            for tile in range(self.tiles):
                        surface.blit(sprites[int(bitmap[row][tile])], (self.array[row][tile].x,self.array[row][tile].y))


class spritesheet():
    #initialise spritesheet class
    def __init__(self, img):
        self.spritesheet = img

    #method to return a cut out from the spritesheet so that it they can be used as sprites
    def get_image(self, row, column, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.spritesheet, (0,0), (width * column , height * row, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image
    
    #method to return an array of sprites from a spritesheet.
    def create_array(self, sheetwidth, sheetheight, width, height, scale, colour):
        array = []
        for i in range(sheetheight):
            for j in range(sheetwidth):
                array.append(self.get_image(i, j, width, height, scale, colour))
        return array
    