"""This module implements standard game functions for Progmind, such as processing keypresses"""

from tkinter import *
from tkinter import scrolledtext 
import sys
import random
from src.blob_enemy import Blob
import pygame
import pygame.freetype

def check_events(settings, screen, tile_map):
    """Watch for keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(settings, event, screen, tile_map)
        elif event.type == pygame.KEYUP:
        	check_keyup_events(settings, event, screen, tile_map)

def reset_game(tile_map):
    tile_map.reset()

def check_keydown_events(settings, event, screen, tile_map):
    """Respond to key down events"""
    player = tile_map.player
    if event.key == pygame.K_ESCAPE:
        sys.exit()

    if event.key == pygame.K_a:
        generate_new_random_blob(settings, screen, settings.image_res.enemy_blob_images, tile_map)
        
    if event.key == pygame.K_r:
        reset_game(tile_map)
    
    if event.key == pygame.K_LEFT:
        if not player.idle_top:
            if player.dx == 0.0:
                player.dx = -1 * settings.player_dx
                player.facing_left = True
    
    if event.key == pygame.K_RIGHT:
        if not player.idle_top:
            if player.dx == 0.0:
                player.dx = settings.player_dx
                player.facing_left = False
    
    if event.key == pygame.K_DOWN:
        if not player.idle_top:
            if player.falling == False:
                player.dy += 50
        
    if event.key == pygame.K_F9:
        if settings.fullscreen == True:
            settings.fullscreen = False
            pygame.display.set_mode((800, 600))
        else:
            settings.fullscreen = True
            pygame.display.set_mode((800, 600), pygame.FULLSCREEN)

def check_keyup_events(settings, event, screen, tile_map):
    player = tile_map.player
    if event.key == pygame.K_SPACE:
        if not player.idle_top:
            if player.falling == False:
                player.dy = settings.player_jump_velocity
                player.falling = True
            elif player.air_jumps < player.max_air_jumps:
                player.dy = settings.player_air_jump_velocity
                player.air_jumps += 1

    if event.key == pygame.K_LEFT:
        if not player.idle_top:
            if player.dx != 0.0:
                player.dx = 0.0
        
    if event.key == pygame.K_RIGHT:
        if not player.idle_top:
            if player.dx != 0.0:
                player.dx = 0.0

def generate_new_random_blob(settings, screen, images, tile_map):
    """Generate a new blob enemy and add it to the list"""
    # How this should work:  First pick a floor, this is the middle_row of the triad created
    # when generating the map, e.g. not the floor and not a level where blocks can appear
    floor_number = random.randint(0, settings.map_number_floors - 2)

    # Secondly pick a side, left or right (this will affect placement and initial velocity, etc)
    facing_left = random.choice([True, False])

    # Calculate initial position / velocity / facing flags
    enemy = Blob(settings, screen, images)
    enemy.rect.bottom = settings.tile_height * ( 2 + (3 * floor_number))
    enemy.rect.left = 3 * settings.tile_width + tile_map.x_offset
    enemy.dx = settings.enemy_blob_dx

    if facing_left:
        enemy.rect.left += 10 * settings.tile_width
        enemy.dx *= -1.0
        enemy.facing_left = True
        enemy.set_current_animation(settings.anim_name_walk_left)
    else:
        enemy.facing_left = False
        enemy.set_current_animation(settings.anim_name_walk_right)

    # Add it to the list
    tile_map.enemies.add(enemy)
    
def blit_help_text(settings, screen, level):
    """Draws the text explaining what keys do what"""
    color_white = (255, 255, 255)
    font = settings.font
        #LEVEL 1
    if settings.rodada == 1:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "desta expressão: 20 ? 4 = 80 ", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa com o simbolo do operador aritmético", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "DESAFIO", settings.font_color)
        y = screen.get_rect().bottom - 158
        y -= 110
        font.render_to(screen, (800,y), " 3 desafios.", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Desafios cumpridos: 0", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios: 5", settings.font_color)

    #LEVEL 2
    if settings.rodada == 2:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "desta expressão: 20 > 4", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa com o resultado", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "DESAFIO", settings.font_color)
        y = screen.get_rect().bottom - 158
        y -= 110
        font.render_to(screen, (800,y), " 3 desafios.", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Desafios cumpridos: 1 ", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios: 5", settings.font_color)

    #LEVEL 3
    if settings.rodada == 3:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa com um valor inteiro", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "DESAFIO", settings.font_color)
        y = screen.get_rect().bottom - 158
        y -= 110
        font.render_to(screen, (800,y), " 3 desafios.", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Desafios cumpridos: 2 ", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios: 5", settings.font_color)

    #LEVEL 4
    if settings.rodada == 4:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "print 'Maior que Zero.'", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "if soma > 0:", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "desta expressão:", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "condicional", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa de acordo com a função sobre estrutura", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "DESAFIO", settings.font_color)
        y = screen.get_rect().bottom - 158
        y -= 110
        font.render_to(screen, (800,y), " 3 desafios.", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Desafios cumpridos: 3", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios: 5", settings.font_color)

    #LEVEL 5
    if settings.rodada == 5:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "}", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "         i + 1", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "__ x for verdadeiro FAÇA {", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "desta expressão:", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "corretamente o trecho de pseudocódigo abaixo:", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa com a estrutura de repetição que completa ", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "DESAFIO", settings.font_color)
        y = screen.get_rect().bottom - 158
        y -= 110
        font.render_to(screen, (800,y), "1 Desafio", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Desafios cumpridos: 4", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios: 5", settings.font_color)

def response_text(settings, screen, level):
    """Draws the text explaining what keys do what"""
    color_white = (255, 255, 255)
    font = settings.font   
    font.render_to(screen, ( settings.resposta_1_X, settings.resposta_1_Y), settings.resposta_1, settings.font_color)
    font.render_to(screen, ( settings.resposta_2_X, settings.resposta_2_Y), settings.resposta_2, settings.font_color)
    font.render_to(screen, ( settings.resposta_3_X, settings.resposta_3_Y), settings.resposta_3, settings.font_color)
    font.render_to(screen, ( settings.resposta_4_X, settings.resposta_4_Y), settings.resposta_4, settings.font_color)
    font.render_to(screen, ( settings.resposta_5_X, settings.resposta_5_Y), settings.resposta_5, settings.font_color)
    font.render_to(screen, ( settings.resposta_6_X, settings.resposta_6_Y), settings.resposta_6, settings.font_color)
    font.render_to(screen, ( settings.resposta_7_X, settings.resposta_7_Y), settings.resposta_7, settings.font_color)
    font.render_to(screen, ( settings.resposta_8_X, settings.resposta_8_Y), settings.resposta_8, settings.font_color)

def update_game_objects(settings, tile_map):
    tile_map.update()

def draw_game_objects(settings, screen, tile_map, level):
    # Draw the map - pass True to render a grid overlay on the tiles
    tile_map.draw()

    # Draw help text
    blit_help_text(settings, screen, level)
    
    response_text(settings, screen, level)

    
    verifica_level(settings)

def update_screen(settings, screen, tile_map, level):
    """Update images and flip screen"""

    # Redraw screen each pass
    screen.fill(settings.bg_color)

    # UPDATES...
    update_game_objects(settings, tile_map)

    # DRAWS...
    draw_game_objects(settings, screen, tile_map, level)

    # FLIP....
    pygame.display.flip()

    
    verifica_level(settings)

def verifica_level(settings):
    if settings.desafio_concluido:
        settings.rodada += 1
        limpar_todas_respostas(settings)        

        #LEVEL 1     
        if settings.rodada == 1:
            settings.resposta_1 = '+'
            settings.resposta_2 = '-'
            settings.resposta_3 = '*'
            settings.resposta_4 = '/'
            settings.resposta_5 = '>'
            settings.resposta_6 = '%'
            settings.resposta_7 = '('
            settings.resposta_8 = '^'
            settings.resposta_3_correta = True
           
            #region DESAFIO 1_1 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_1_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop()

            #endregion DESAFIO 1_1

            #region DESAFIO 1_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_1_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 1_2 
      
            #region DESAFIO 1_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_1_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 1_3

        if settings.rodada == 2:
            settings.resposta_1 = '<'
            settings.resposta_2 = '('
            settings.resposta_3 = '<='
            settings.resposta_4 = 'true'
            settings.resposta_5 = 'false'
            settings.resposta_6 = '='
            settings.resposta_7 = '>'
            settings.resposta_8 = '<>'
            settings.resposta_4_correta = True
          
            #region DESAFIO 2_1
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_2_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop()

            #endregion DESAFIO 2_3

            #region DESAFIO 2_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_2_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 1_3

            #region DESAFIO 2_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_2_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 2_3 

        if settings.rodada == 3:
            
            settings.player_dx = 4

            settings.resposta_1 = '4'
            settings.resposta_2 = '5.5'
            settings.resposta_3 = 'A'
            settings.resposta_4 = '='
            settings.resposta_5 = 'b'
            settings.resposta_6 = '10'
            settings.resposta_7 = 'D'
            settings.resposta_8 = 'C'
            settings.resposta_1_correta = True 
            settings.resposta_6_correta = True 

             #region DESAFIO 3_1 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_3_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop()

            #endregion DESAFIO 3_1

            #region DESAFIO 3_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_3_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 3_2 
      
            #region DESAFIO 3_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_3_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 3_3

        if settings.rodada == 4:
            
            settings.player_dx = 3

            settings.resposta_1 = '4'
            settings.resposta_2 = 'composta'
            settings.resposta_3 = '='
            settings.resposta_4 = 'true'
            settings.resposta_5 = 'simples'
            settings.resposta_6 = '>'
            settings.resposta_7 = 'D'
            settings.resposta_8 = 'switch'
            settings.resposta_5_correta = True
            # Creating tkinter main window 

             #region DESAFIO 4_1 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_4_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop()

            #endregion DESAFIO 4_1

            #region DESAFIO 4_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_4_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 4_2 
      
            #region DESAFIO 4_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_4_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 3_3

            settings.desafio_concluido = False
         #LEVEL 5
        
        if settings.rodada == 5:
            
            settings.player_dx = 3

            settings.resposta_1 = 'para'
            settings.resposta_2 = 'até'
            settings.resposta_3 = 'V'
            settings.resposta_4 = '1'
            settings.resposta_5 = 'enquanto'
            settings.resposta_6 = '6'
            settings.resposta_7 = 'ao fim'
            settings.resposta_8 = 'int'
            settings.resposta_5_correta = True 
            # Creating tkinter main window 

             #region DESAFIO 5_1 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_5_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop()

            #endregion DESAFIO 5_1

            #region DESAFIO 5_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_5_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 5_2 
      
            #region DESAFIO 5_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_5_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 250, y = 520)  

            root.mainloop() 
            #endregion DESAFIO 5_3

            settings.desafio_concluido = False
        
           #LEVEL 1     
       
        if settings.rodada == 6:
           #region DESAFIO 6_1 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_1.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 450, y = 620)  

            root.mainloop()

            #endregion DESAFIO 6_1

            #region DESAFIO 6_2 
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_2.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 450, y = 620)  

            root.mainloop() 
            #endregion DESAFIO 6_2 
      
            #region DESAFIO 6_3
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_3.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 450, y = 620)  

            root.mainloop() 
            #endregion DESAFIO 6_3

            
            #region DESAFIO 6_4
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_4.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 450, y = 620)  

            root.mainloop() 
            #endregion DESAFIO 6_4


            #region DESAFIO 6_5
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_5.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 180, y = 620)  

            root.mainloop() 
            #endregion DESAFIO 6_5

            
            #region DESAFIO 6_6
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_6.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 450, y = 620)  

            root.mainloop() 
            #endregion DESAFIO 6_6

            
            #region DESAFIO 6_7
            root = Tk() 
            root.title("PROGMIND") 
            root.configure(background='#24235c')
            root.geometry("660x660")   
            root.resizable(width=True, height=True)      

            # CONTEÚDO
            img = PhotoImage(file="./images/DESAFIO_6_7.gif")
            img =  img.subsample(3, 3)
            label_imagem = Label(root, image=img).grid(row=1)

            # Create a Button 
            Button(root, text = 'FECHAR', bd = '2', font = ("Arial", 12), fg='#24235c', bg='#ffffff',
            command = root.destroy,  width = 20).place(x = 460, y = 620)  
            

            root.mainloop() 
            sys.exit()
            #endregion DESAFIO 6_7
        settings.desafio_concluido = False     
def limpar_todas_respostas(settings):    
    settings.contador_nivel = 0
    settings.resposta_1_correta = False
    settings.resposta_2_correta = False
    settings.resposta_3_correta = False
    settings.resposta_4_correta = False
    settings.resposta_5_correta = False
    settings.resposta_6_correta = False
    settings.resposta_7_correta = False
    settings.resposta_8_correta = False