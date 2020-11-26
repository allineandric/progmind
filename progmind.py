"""This module is the main entry for the Progmind game"""

from tkinter import *  
from tkinter import scrolledtext 
import src.game_functions as gf
from src.image_resources import ImageResources
from src.settings import Settings
from src.tilemap import Tilemap
from src.level_timer import LevelTimer
import random
import pygame

def run_game():
    """Main entry point for Progmind"""



    pygame.init()
    
    pygame.mixer.init()

    pygame.mixer.music.load('Jason Farnham No Copyright Music.mp3')
    pygame.mixer.music.set_volume(0.03)

    pygame.mixer.music.play(-1)

        # Startup pygame object
    root = Tk() 
    root.title("PROGMIND") 
    root.configure(background='#24235c')
    root.geometry("600x600")   
    root.resizable(width=True, height=True)      

    # CONTEÚDO


    img = PhotoImage(file="images/progmind-logo.gif")
    img =  img.subsample(2, 2)

    label_imagem = Label(root, image=img).grid(row=1)

   
    # Create a Button 
    Button(root, text = 'COMEÇAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
    command = root.destroy,  width = 20).place(x = 200, y = 350)  

    

    root.mainloop()

    random.seed()

    # Load our settings object and image resources, disk I/O that can be done in advance
    settings = Settings()
    image_res = ImageResources(settings)
    # Add to the cache so it's accessible where needed
    settings.image_res = image_res

    # Create the main screen to render to based on settings
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.caption)
    
    # Create a 2D tilemap - this takes a list of indices and an image list to produce a tiled surface
    tile_map = Tilemap(settings, screen, settings.map_indicies, image_res.tile_images, 
        image_res.block_image, image_res.box_image, image_res.blob_exit_images, image_res.player_sprite_images, image_res.enemy_blob_images)

    # Overwrite default indices with generated map 
    tile_map.generate_basic_map(settings.map_number_floors , settings.map_number_subfloors)

    # Reset the game
    gf.reset_game(tile_map)

    # Use pygame's simple loop management for a fixed 30 FPS
    clock = pygame.time.Clock()
    
    while True:
        # Should make sure each frame spends at least 1/30 seconds in this loop
        # downside is wasted sleep on fast hardware and slow hardware will lag
        # but slow hardware will always lag and implementing a time-delta based
        # loop for this simple game is IMHO overkill.
        clock.tick(30)

        # Process system events (key-presses, joystick, etc)
        gf.check_events(settings, screen, tile_map)

    
        # Update the game (this will update all sub-object and render them to the screen)
        gf.update_screen(settings, screen, tile_map, Settings.level_number)
    
# Invokes the function above when the script is run
run_game()
