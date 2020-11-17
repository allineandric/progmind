"""This module implements standard game functions for Progmind, such as processing keypresses"""
from tkinter import *
from tkinter import messagebox
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
    if level == 1:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "desta expressão: 4 ? 5 = 20 ", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Quebre a caixa que possui o simbolo do operador", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)

        y -= 50
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Adição (+)   Subtração (-)   Multiplicação (*)   Divisão(/)", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "simbologia em todas as linguagens de programação", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Em algoritmos eles também são simples e têm a mesma ", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "chavamaos de expressões aritméticas.", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "continhas de soma, subtração, multiplicação e divisão", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Nos primeiros anos de estudo aprendemos a fazer  ", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "EXPRESSÕES ARITMÉTICAS", settings.font_color)

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
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)

    if level == 2:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "3 = 4", settings.font_color)
        
        y -= 30
        font.render_to(screen, (10,y), "Arraste a caixa correta de acordo com o operador", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)
        y -= 50
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "expressões aritméticas", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "As expressões relacionais podem conter ", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "(ou seja, True ou False)", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "Esse dois valores são chamados de valores booleanos", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "resultado pode ser False (falso) ou True (verdadeiro) ", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Operadores relacionais comparam dois valores e o ", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "EXPRESSÕES RELACIONAIS", settings.font_color)

        y = screen.get_rect().bottom - 158
        y -= 30
        font.render_to(screen, (800,y), " 3 desafios.", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "*Para passar de level, é necessário cumprir no mínimo", settings.font_color)
        y -= 50
        font.render_to(screen, (800,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "", settings.font_color)
        y -= 40
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 20
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)
        y -= 60
        font.render_to(screen, (800,y), "<>(ou !=)             Diferente", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "     >=                    Maior ou igual", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "     <=                    Menor ou igual", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "     >                      Maior", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "     <                      Menor", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "= (ou ==)             Igual", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Operador           Função", settings.font_color)

    if level == 3:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 20
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "variáveis do tipo booleano, ou seja, com valor VERDADEIRO(V) ou FALSO(F).", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "string, ou seja, cadeia de caracteres.  - logico: define ", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "com casas decimais.  - caractere: define variáveis do tipo", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), " - real: define variáveis numéricas do tipo real, ou seja,", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "numéricas do tipo inteiro, ou seja, sem casas decimais.", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "(ou booleano). Sendo eles:  - inteiro: define variáveis", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "de dados: inteiro, real, cadeia de caracteres e lógico", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "Na ciência da computação existem quatro tipos primitivos", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "TIPOS DE DADOS", settings.font_color)

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
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)

    if level == 4:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)
        y -= 50
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "EXPRESSÕES LÓGICAS", settings.font_color)

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
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)

    if level == 5:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)
        y -= 50
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "ESTRUTURA DE REPETIÇÃO", settings.font_color)

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
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)

    if level == 6:
        y = screen.get_rect().bottom - 98
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "DESAFIO 1", settings.font_color)
        y -= 50
        font.render_to(screen, (10,y), "_________________________________________________", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 30
        font.render_to(screen, (10,y), "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", settings.font_color)
        y -= 40
        font.render_to(screen, (10,y), "ESTRUTURA DE DECISÃO", settings.font_color)

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
        font.render_to(screen, (800,y), "Desafios cumpridos:", settings.font_color)
        y -= 30
        font.render_to(screen, (800,y), "Total de desafios:", settings.font_color)

def update_game_objects(settings, tile_map):
    tile_map.update()

def draw_game_objects(settings, screen, tile_map, level):
    # Draw the map - pass True to render a grid overlay on the tiles
    tile_map.draw()

    # Draw help text
    blit_help_text(settings, screen, level)

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