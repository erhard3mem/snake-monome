#    
#   A Python snake game improved by Erhard for monome
#   originally taken from: https://www.edureka.co/blog/snake-game-with-pygame/
#   
#   Prerequisites: TODO: 1) pip install pygame
#   
#   The original sample from the web page uses naming which is not clear in my opinion, so changed.
#

import pygame
import time
import random

import asyncio
import monome
import vlc

x=0
y=0
w=8
h=8

pygame.init()
pygame.display.set_mode((500,500));
clock = pygame.time.Clock()

def our_snake(snake_block, snake_list):
        for x in snake_list:
            grid_studies.on_grid_key(x[0],x[1],1);
            

def game(loop):


    def gameLoop():
        game_over = False
        game_stopped = False

        x1 = 8 / 2
        y1 = 8 / 2

        x1_change = 0
        y1_change = 0

        snake_List = []
        Length_of_snake = 1
        
        foodx = random.randrange(0, 7)
        foody = random.randrange(0, 7)

        while not game_stopped:

            while game_stopped == True:
                print("You lost");

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_stopped = False
                        if event.key == pygame.K_c:
                            gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("L")
                        x1_change = -1
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        print("R")
                        x1_change = 1
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        print("U")
                        y1_change = -1
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        print("D")
                        y1_change = 1
                        x1_change = 0
                    
            #if x1 >= 7 or x1 < 0 or y1 >= 7 or y1 < 0:
                #game_stopped = True
            
            x1 += x1_change
            y1 += y1_change
            
            grid_studies.on_grid_key(x1,y1,1);

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_stopped = True

            our_snake(1, snake_List)
            print("score:" ,len(snake_List));
           
            pygame.display.update()


            if x1 == foodx and y1 == foody:
                foodx = random.randrange(0, 7)
                foody = random.randrange(0, 7)
                Length_of_snake += 1
                p = vlc.MediaPlayer("file:///home/erhard/web/snake/a0.mp3")
                p.play()

            clock.tick(5)
            
            for i in range(0,8):
                for j in range(0,8):
                    grid_studies.on_grid_key(i,j,0);

            print("___FOOD:",foodx,foody)
            grid_studies.on_grid_key(foodx,foody,1);
            
            #gameCounter = gameCounter + 1

            

    gameLoop()
    pygame.quit()
   
    loop.stop()


class GridStudies(monome.GridApp):
    def __init__(self):
        super().__init__()

    def on_grid_key(self, x, y, s):
        if x > w:
            x = x-w
        elif y > h:
            y = y-h
        print("key:", x, y, s)
        self.grid.led_level_set(x, y, s*15)


grid_studies = ''
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    grid_studies = GridStudies()

    def serialosc_device_added(id, type, port):
        print('connecting to {} ({})'.format(id, type))
        asyncio.ensure_future(grid_studies.grid.connect('127.0.0.1', port))

    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)

    loop.run_until_complete(serialosc.connect())
    
    loop.call_soon(game,loop);
    loop.run_forever()