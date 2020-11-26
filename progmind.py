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
        # Deve certificar-se de que cada quadro gasta pelo menos 1/30 segundos neste loop
        # desvantagem é o sono desperdiçado em hardware rápido e hardware lento vai atrasar
        # mas o hardware lento sempre vai atrasar e implementar um baseado em time delta
        # loop para este jogo simples é um exagero IMHO.
        clock.tick(30)

        # Processar eventos do sistema (pressionamentos de tecla, joystick, etc)
        gf.check_events(settings, screen, tile_map)

    
        # Atualize o PROGMIND (isso atualizará todos os subobjetos e os renderizará na tela)
        gf.update_screen(settings, screen, tile_map, Settings.level_number)
    
# Invoca a função acima quando o script é executado
run_game()
