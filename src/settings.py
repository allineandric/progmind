"""This module implements settings for Progmind."""
import pygame.freetype

class Settings():
    """A class to store all settings for Progmind."""
    level_number = 1 # Variável global que controla o que vai aparecer na tela de acordo com o level

    def __init__(self):
        """Initialize the game's settings."""
        
        # configurações de tela
        self.screen_width = 1255
        self.screen_height = 600
        self.caption = "Progmind" # ALTERADO O NOME DO JOGO PARA PROGMIND
        self.bg_color = (36, 35, 92) # ALTERADA A COR DE FUNDO DO JOGO
        self.color_key = (255, 0, 255)
        self.fullscreen = False

        # fonte rápida
        self.font = pygame.freetype.SysFont(None, 16)
        self.font_color = (255, 255, 255)

        # Fonte bônus
        self.bonus_font = pygame.freetype.SysFont(None, 10)

        # Configurações globais de sprite
        self.gravity = 1.4
        self.terminal_velocity = 12
        
        # Configurações de sprite do jogador
        self.player_width = 24
        self.player_height = 32
        self.player_jump_velocity = -21 # ALTERADA A VELOCIDADE DO PULO DE -15 PARA -21
        self.player_air_jump_velocity = -20
        self.player_max_air_jumps = 2
        self.player_dx = 6 # ALTERADA A VELOCIDADE DE 2 PARA 4

        # pixels transparentes para deslocar para colisão horizontal (dependente da imagem)
        self.player_sprite_horz_margin = 3
        # pixels transparentes para compensar para colisão vertical (por exemplo, saltos)
        self.player_sprite_top_margin = 9

        # Nomes de animação
        self.anim_name_idle_left = 'IDLE.L'
        self.anim_name_idle_right = 'IDLE.R'
        self.anim_name_walk_left = 'WALK.L'
        self.anim_name_walk_right = 'WALK.R'
        self.anim_name_jump_up_left = 'JUMPUP.L'
        self.anim_name_jump_down_left = 'JUMPDOWN.L'
        self.anim_name_jump_up_right = 'JUMPUP.R'
        self.anim_name_jump_down_right = 'JUMPDOWN.R'
        self.anim_name_dead = 'DEAD'
        self.anim_name_exit = 'EXIT'

        #tamanhos de dígitos de nível
        self.digit_width = 36
        self.digit_height = 48

        # Dígitos do cronômetro (estilo LCD)
        self.lcd_digit_width = 16
        self.lcd_digit_height = 24

        # Timer frame
        # Pixels from either side to the digit area
        self.lcd_frame_padding_horz = 5
        # Pixels above and below the digit area
        self.lcd_frame_padding_vert = 4
        # Horz spacing between related digits e.g. M M or S S
        self.lcd_frame_digit_padding_horz_minor = 2
        # Horz spacing between unrelated digits e.g. MM:SS or SS:mm
        self.lcd_frame_digit_padding_horz_major = 8
        
        # Configurações do Blob inimigo
        self.enemy_blob_width = 16
        self.enemy_blob_height = 16
        self.enemy_blob_dx = 1
        # Upwards velocity when killed by player from block break
        self.enemy_death_dy = -10
        # starting rate
        self.enemy_generation_base_rate = 120
        # current rate
        self.enemy_generation_rate = self.enemy_generation_base_rate
        # amount to decrease rate per level
        self.enemy_generation_level_rate = 5
        
        # Tile settings
        self.tile_width = 24
        self.tile_height = 24

        # Gerador de partículas
        self.particle_gen_color = (255, 0, 0)
        self.particle_gen_dx_range = (-8, 8)
        self.particle_gen_dy_range = (5, 20)
        self.particle_gen_max_frames = 40
        self.particle_gen_per_frame = 5
        
        # Configurações do mapa
        self.map_width = 16
        self.map_height = 10
        self.map_playable_width = 10
        self.map_indicies = [-1]
        self.map_number_floors = 8
        self.map_number_subfloors = 1


      
        # Posição da resposta 1
        self.resposta_1 = '-'
        self.resposta_1_X = 558
        self.resposta_1_Y = 463
        self.resposta_1_correta = False
        
        # Posição da resposta 2
        self.resposta_2 = '+'
        self.resposta_2_X = 679
        self.resposta_2_Y = 463
        self.resposta_2_correta = True
        
        # Posição da resposta 3
        self.resposta_3 = '/'
        self.resposta_3_X = 558
        self.resposta_3_Y = 320
        self.resposta_3_correta = False

        # Posição da resposta 4 
        self.resposta_4 = '%'
        self.resposta_4_X = 679
        self.resposta_4_Y = 320
        self.resposta_4_correta = False      
     
        # Posição da resposta _5
        self.resposta_5 = '&'
        self.resposta_5_X = 558
        self.resposta_5_Y = 176
        self.resposta_5_correta = False
        
        # Posição da resposta _6 
        self.resposta_6 = 'X'
        self.resposta_6_X = 682
        self.resposta_6_Y = 172
        self.resposta_6_correta = True
        
        # Posição da resposta 7
        self.resposta_7 = ')'
        self.resposta_7_X = 558
        self.resposta_7_Y = 32        
        self.resposta_7_correta = False

       # Posição da resposta 8
        self.resposta_8 = '<>'
        self.resposta_8_X = 679
        self.resposta_8_Y = 32
        self.resposta_8_correta = False

        # Desafio concluído
        self.desafio_concluido = True

        # Nivel Desafio
        self.desafio_Facil = 0
        self.desafio_Medio = 3
        self.desafio_Dificil = 4
        self.contador_nivel = 0
        self.rodada = 0
        self.inicio_jogo = True
        self.morte = False
        
