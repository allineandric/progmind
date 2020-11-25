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

    if settings.rodada == 2:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "desta expressão: 20 é maior (>) que 4 ?", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre a caixa com o simbolo do operador relacional", settings.font_color)
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

    if settings.rodada == 4:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Quebre as caixas com valores FLOAT", settings.font_color)
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

    if settings.rodada == 5:
        y = screen.get_rect().bottom - 300
        font.render_to(screen, (10,y), "", settings.font_color)
        y -= 35
        font.render_to(screen, (10,y), "Empurre caixas com valores pares até o centro", settings.font_color)
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
        font.render_to(screen, (800,y), "Desafios cumpridos: 2 ", settings.font_color)
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
           # Creating tkinter main window 
            root = Tk() 
            root.title("Nível 1") 
            root.configure(background='#231336')
            root.geometry("750x450")   
            root.resizable(width=True, height=True)
            # CONTEÚDO NÍVEL 1
            Label(root,  
                text = "_______________________________________________________________________________________________" +
                "\n\n\n#EXPRESSÕES ARITMÉTICAS \n\n\nExistem quatro operações aritméticas básicas, que você já conhece do seu dia a dia: " +
                "\nSoma: representada pelo símbolo +, que pode ser chamado de operador soma"
                "\nSubtração: representada pelo símbolo –, também chamado de operador subtração;"
                "\nDivisão: representada pelo símbolo /, também chamado de operador divisão;"
                "\nMultiplicação: representada pelo símbolo *, também chamado de operador multiplicação."
                    "\n_______________________________________________________________________________________________" +
                    "\n\n EXEMPLO: \n\n 22 + 10 = 32 ",
                font = ("Arial", 12),  
                background = '#231336',  
                justify="left",
                foreground = "white").grid(column = 15, 
                    row = 15) 
            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#231336', bg='#ffffff',
                command = root.destroy).place(x = 600, y = 350)  
            root.mainloop() 
 
        #LEVEL 2
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
           # Creating tkinter main window 
            root = Tk() 
            root.title("Nível 2") 
            root.configure(background='#231336')
            root.geometry("750x450")   
            root.resizable(width=True, height=True)
            # CONTEÚDO
            Label(root,  
                text = "_______________________________________________________________________________________________" +
                "\n\n\n#EXPRESSÕES RELACIONAIS \n\n\nOs operadores relacionais são utilizado para comparar valores, o resultado " +
                "de uma expressão é um valor\n booleano (verdeiro ou falso).\nEles são representados pelos seguinte próximos simbolos: \n\n "+
                "IGUAL ( == )\n DIFERENTE ( != ) \n MAIOR ( > ) \n MENOR ( < ) \n MAIOR OU IGUAL ( >= ) \n MENOR OU IGUAL (<=)" +
                    "\n_______________________________________________________________________________________________" +
                    "\n\n EXEMPLO: \n\n 4 é igual (=) 2 x 2 \n 3 é menor (<) que 4 \n 'A' é diferente de 'B' ",
                font = ("Arial", 12),  
                background = '#231336',  
                justify="left",
                foreground = "white").grid(column = 15, 
                    row = 15) 
            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#231336', bg='#ffffff',
                command = root.destroy).place(x = 600, y = 350)  
            root.mainloop() 

        #LEVEL 3
        if settings.rodada == 3:
            settings.resposta_1 = '4'
            settings.resposta_2 = '5.5'
            settings.resposta_3 = 'A'
            settings.resposta_4 = '='
            settings.resposta_5 = 'b'
            settings.resposta_6 = '('
            settings.resposta_7 = 'D'
            settings.resposta_8 = 'C'
            settings.resposta_1_correta = True 
           # Creating tkinter main window 
            root = Tk() 
            root.title("Nível 3") 
            root.configure(background='#231336')
            root.geometry("750x450")   
            root.resizable(width=True, height=True)
            # CONTEÚDO
            Label(root,  
                text = "_______________________________________________________________________________________________" +
                "\n\n\n#TIPOS DE DADOS \n\n\nNa ciência da computação existem quatro tipos primitivos de dados: inteiro, real, cadeia de caracteres e lógico (ou booleano)." +
                "\nSendo eles: "+
                "\n- inteiro: define variáveis numéricas do tipo inteiro, ou seja, sem casas decimais."
                "\n- real: define variáveis numéricas do tipo real, ou seja, com casas decimais."
                "\n- caractere: define variáveis do tipo string, ou seja, cadeia de caracteres."
                "\n- logico: define variáveis do tipo booleano, ou seja, com valor VERDADEIRO(V) ou FALSO(F)."
                    "\n_______________________________________________________________________________________________" +
                    "\n\n EXEMPLO: \n\n inteiro: 12 \n real: 7,5 \n caractere: 'abelha' \n logico: V",
                font = ("Arial", 12),  
                background = '#231336',  
                justify="left",
                foreground = "white").grid(column = 15, 
                    row = 15) 
            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#231336', bg='#ffffff',
                command = root.destroy).place(x = 600, y = 350)  
            root.mainloop() 
        
        #LEVEL 4
        if settings.rodada == 4:
            settings.resposta_1 = '4'
            settings.resposta_2 = '5.5'
            settings.resposta_3 = 'A'
            settings.resposta_4 = '='
            settings.resposta_5 = 'b'
            settings.resposta_6 = '('
            settings.resposta_7 = 'D'
            settings.resposta_8 = 'C'
            settings.resposta_5_correta = True 
           # Creating tkinter main window 
            root = Tk() 
            root.title("Nível 4") 
            root.configure(background='#231336')
            root.geometry("750x450")   
            root.resizable(width=True, height=True)
            # CONTEÚDO
            Label(root,  
                text = "_______________________________________________________________________________________________" +
                "\n\n\n#TIPOS DE DADOS \n\n\nNa ciência da computação existem quatro tipos primitivos de dados: inteiro, real, cadeia de caracteres e lógico (ou booleano)." +
                "\nSendo eles: "+
                "\n- inteiro: define variáveis numéricas do tipo inteiro, ou seja, sem casas decimais."
                "\n- real: define variáveis numéricas do tipo real, ou seja, com casas decimais."
                "\n- caractere: define variáveis do tipo string, ou seja, cadeia de caracteres."
                "\n- logico: define variáveis do tipo booleano, ou seja, com valor VERDADEIRO(V) ou FALSO(F)."
                    "\n_______________________________________________________________________________________________" +
                    "\n\n EXEMPLO: \n\n teste \n  \n  \n logico: V",
                font = ("Arial", 12),  
                background = '#231336',  
                justify="left",
                foreground = "white").grid(column = 15, 
                    row = 15) 
            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#231336', bg='#ffffff',
                command = root.destroy).place(x = 600, y = 350)  
            root.mainloop() 

        #LEVEL 5
        if settings.rodada == 5:
            settings.resposta_1 = 'TESTE 3'
            settings.resposta_2 = '?'
            settings.resposta_3 = '+'
            settings.resposta_4 = '-'
            settings.resposta_5 = 'X'
            settings.resposta_6 = '('
            settings.resposta_7 = '>'   
            settings.resposta_8 = '%'
            settings.resposta_3_correta = True   
            # Creating tkinter main window 
            root = Tk() 
            root.title("Nível 5") 
            root.configure(background='#231336')
            root.geometry("750x450")   
            root.resizable(width=True, height=True)
            Label(root,  
                text = "_______________________________________________________________________________________________" +
                "\n\n\n#ESTRUTURA DE REPETIÇÃO \n\n\nDentro da lógica de programação é uma estrutura que permite executar mais de uma vez o mesmo comando" +
                "\nou conjunto de comandos, de acordo com uma condição ou com um contador."+
		        "\nExistem 3 estruturas de repetição básica para praticamente todas as linguagens de programação:"+
                "\nWhile (enquanto) - Repete um bloco de código enquanto uma condição permanecer verdadeira."
                "\nDo… While (faça enquanto) - Muito parecido com o while, porém a condição é verificada após"
                "\nexecutar o bloco de comandos."
                "\nFor (para) - Utilizado para executar um conjunto de comandos executado por um número X de"
                "\nvezes de acordo com o valor de uma variável",
                         font = ("Arial", 12),  
                background = '#231336',  
                justify="left",
                foreground = "white").grid(column = 15, 
                    row = 15) 
            # Create a Button 
            Button(root, text = 'CONTINUAR', bd = '2', font = ("Arial", 12), fg='#231336', bg='#ffffff',
                command = root.destroy).place(x = 600, y = 350)  
            root.mainloop()
            
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