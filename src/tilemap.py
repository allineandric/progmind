"" "Este módulo implementa um mapa de blocos 2D para o Progmind" ""
from src.player import Player
from src.block import Block
from src.box import Box
from src.blob_exit import BlobExit
from src.level_info import LevelInfo
from src.level_timer import LevelTimer
from src.time_bonus import TimeBonus
import src.game_functions as gf
import random
from pygame.sprite import Group
import pygame

class Tilemap():
    """Representa uma coleção de blocos (sprites) que representam um mapa"""

    def __init__(self, settings, screen, map_indicies, images, block_image, box_image, exit_images, player_images, blob_images):
        """Inicialize o mapa e todos os seus objetos de propriedade"""
        self.settings = settings
        self.screen = screen
        self.images = images
        self.indicies = map_indicies
        self.screen_rect = screen.get_rect()
        self.player_bounds_rect = pygame.Rect((0,0), (0,0))
        self.block_image = block_image
        self.block_group = Group()
        self.box_image = box_image
        self.x_offset = 0
        self.drainrect = pygame.Rect((0,0), (0,0))
        # self.blob_exit - > Vilões do jogo, todos métodos relacionados estão comentados
        # self.blob_exit = None
        self.exit_images = exit_images
        self.player = None
        self.player_images = player_images
        # self.blob_images = blob_images
        self.enemies = Group()
        self.new_enemy_counter = 0
        self.level_info = LevelInfo(self.settings, self.screen)
        self.level_timer = LevelTimer(self.settings, self.screen)
        self.bonuses = []
        
    def reset(self):
        """Reinicia o jogo ao estado inicial"""
        self.player.reset()
        self.enemies.empty()
        # gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)
        self.generate_platforms()
        # self.blob_exit.stop_gibbing()
        self.level_info = LevelInfo(self.settings, self.screen)
        self.settings.enemy_generation_rate = self.settings.enemy_generation_base_rate
        # self.level_timer.reset()

    def generate_basic_map(self, number_of_floors, number_of_subfloor_rows=0):
        """Constrói um mapa de blocos básico - isso depende da ordem do índice da imagem dos blocos"""
        # Cada 'piso' que não seja o fundo ou abaixo contém 3 filas de ladrilhos do mesmo padrão
        # Portanto, basta fazer number_of_floors - 1 entradas para aqueles, em seguida, gerar o 'andar' inferior
        # que tem apenas uma 3ª linha de índices diferente. Se os blocos abaixo deles forem necessários para
        # parece que todos usam o mesmo padrão

        #region ALTERADO Cada código se refere a uma posição da imagem e cada coluna referencia a coluna no layout do jogo
        empty_row = [-1, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 8, -1]
        pipe_row = [-1, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 8, -1]
        bottom_row = [-1, 6, 9,  1,  1,  1,  1, 1, 17,  1,  1,  1,  1, 10, 8, -1]
        sub_row = [-1, 6, 9,  4,  4,  4,  4,  4, 4,  4,  4,  4,  4, 10, 8, -1]
        drain_col = 8
        #endregion

        row_index = 0
        new_indices = []
        while row_index < (number_of_floors - 1):
            new_indices.extend(empty_row)
            new_indices.extend(pipe_row)
            new_indices.extend(empty_row)
            row_index += 1

        #piso inferior - sem gerador inimigo
        new_indices.extend(empty_row)
        new_indices.extend(empty_row)
        new_indices.extend(bottom_row)

        # linha opcional do piso inferior
        row_index = 0
        while row_index < number_of_subfloor_rows:
            new_indices.extend(sub_row)
            row_index += 1

        # Fora com o velho, com o novo
        self.indicies.clear()
        self.indicies.extend(new_indices)

        # Adicione as plataformas de bloco
        # self.generate_platforms()

        #Calcule o retângulo que limita o movimento externo do jogador (e inimigos na maioria dos casos)
        self.x_offset = (self.screen_rect.width - (self.settings.map_width * self.settings.tile_width)) // 2
        x_offset2 = self.x_offset + self.settings.tile_width * ((self.settings.map_width - self.settings.map_playable_width)/2)
        self.player_bounds_rect.top = 0
        self.player_bounds_rect.left = x_offset2
        self.player_bounds_rect.width = self.settings.map_playable_width * self.settings.tile_width
        self.player_bounds_rect.height = self.screen_rect.height - ((number_of_subfloor_rows + 1) * self.settings.tile_height)

        # Drenar colisão rect
        self.drainrect.width = self.settings.tile_width
        self.drainrect.height = self.settings.tile_height
        self.drainrect.top = self.player_bounds_rect.bottom
        self.drainrect.left = self.settings.tile_width * drain_col + self.x_offset
        self.drainrect.inflate_ip(self.settings.tile_width * -0.99, self.settings.tile_height * -0.75)
        self.drainrect.move_ip(0, self.settings.tile_height * -0.5)

        # Crie a 'saída'
        # self.blob_exit = BlobExit(self.settings, self.screen, self.exit_images, self)

        # Crie o jogador
        self.player = Player(self.settings, self.screen, self.player_images, self.player_bounds_rect, self)

        # Position the timer
        self.level_timer.position_frame(self.screen_rect.centery, self.player_bounds_rect.right + self.settings.tile_width * 2)

    def generate_block(self, x, y):
        """Crie um novo objeto Bloco no x, y fornecido e retorne-o"""
        new_block = Block(self.settings, self.screen, self.block_image)
        new_block.rect.top = y
        new_block.rect.left = x
        return new_block

    def generate_blocks(self, bounding_rect, group, bottom_left=False, bottom_right=False):
        """Gera uma de 4 combinações de blocos possíveis"""
        # Always add all the 4 quadrants
        image_rect = self.block_image.get_rect()
        block_top_left = self.generate_block(bounding_rect.left, bounding_rect.top)
        block_top_right = self.generate_block(bounding_rect.left + image_rect.width, bounding_rect.top)
        block_bottom_left = self.generate_block(bounding_rect.left, bounding_rect.top + image_rect.height)
        block_bottom_right = self.generate_block(bounding_rect.left + image_rect.width, bounding_rect.top + image_rect.height)
        group.add(block_top_left)
        group.add(block_top_right)
        group.add(block_bottom_left)
        group.add(block_bottom_right)

    def generate_box(self, x, y):
        """Crie um novo objeto de caixa no dado x, y e retorne-o"""
        new_box = Box(self.settings, self.screen, self.box_image)
        new_box.rect.top = y
        new_box.rect.left = x     
        return new_box

    def generate_boxes(self, bounding_rect, group, bottom_left=False, bottom_right=False):
        """Gera uma das 8 combinações de caixa possíveis"""
        # Always add all the 4 quadrants
        image_rect = self.box_image.get_rect()
        box_top_left = self.generate_box(bounding_rect.left, bounding_rect.top)
        group.add(box_top_left)

    def generate_platforms(self):
        """Faça grupos de sprites que contenham os blocos para o jogador se apoiar"""

         # Cada bloco está contido no self.player_bounds_rect

        # Encontre cada "linha" de ladrilhos que pode conter blocos e adicione alguns
        # As linhas elegíveis são a cada 3ª linha, começando da 2ª ao topo, exceto o piso inferior
        row_rect = pygame.Rect((self.player_bounds_rect.left, self.player_bounds_rect.top + (self.settings.tile_height * 2)), 
            (self.player_bounds_rect.width, self.settings.tile_width))

        self.block_group.empty()
        for row in range(0, (self.settings.map_number_floors-1)):
            new_group = Group()

            # Cada coluna na linha elegível tem 4 canais válidos para um bloco
            # Nota - existem mais permutações, estas são apenas as permitidas
            # OO OO OO OO
            # XX OX OX OO
            for col in range(1, 9): # ALTERADO O DE range(0, self.settings.map_playable_width)
                bounding_rect = pygame.Rect(0, 0, 0, 0)
                bounding_rect.top = row_rect.top
                bounding_rect.left = row_rect.left + col * self.settings.tile_width           
                self.generate_blocks(bounding_rect, new_group, random.choice([True, False]), random.choice([True, False]))

            # Método criado para colocar as caixas na tela
            for col in range(0, 6, 5):
                bounding_rect = pygame.Rect(0, 0, 0, 0)
                bounding_rect.top = row_rect.top - 24 # -24 pois são dois blocos à frente
              
                bounding_rect.left = (row_rect.left + col * self.settings.tile_width) + 48 # +48 pois são dois blocos acima
                self.generate_boxes(bounding_rect, new_group, random.choice([True, False]), random.choice([True, False]))
            
            #Cada linha é seu próprio grupo. Isso pode limitar as verificações de colisão mais tarde
            self.block_group.add(new_group.sprites())
            #Desloque o retângulo de limite para baixo
            row_rect = row_rect.move(0, self.settings.tile_height * 6) # ALTERADA A tile_height DE 3 PARA 6

    def update(self):
        """Atualize todos os objetos de sua propriedade (blocos, jogador, inimigos, etc)"""
        # if self.player.at_top:
            # self.level_timer.stop()

        #Verifique se há um sinalizador de reinicialização definido no objeto do jogador
        if self.player.won_level:
            self.player.reset()
            self.enemies.empty()
            # gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)
            self.generate_platforms()
            # self.blob_exit.stop_gibbing()
            self.level_info.increase_level()
            self.settings.enemy_generation_rate -= self.settings.enemy_generation_level_rate
            # self.level_timer.reset()

        # Atualize o jogador
        self.player.update(self, self.enemies)

        # Verifique se é hora de adicionar um novo inimigo ao mapa
        if self.settings.rodada > 1:
            self.new_enemy_counter += self.settings.rodada
            if self.new_enemy_counter >= self.settings.enemy_generation_rate:
                self.new_enemy_counter = 0
                gf.generate_new_random_blob(self.settings, self.screen, self.settings.image_res.enemy_blob_images, self)

        # Atualize os inimigos existentes
        for enemy in self.enemies:
            enemy.update(self)

        # Atualize o sprite de 'saída'
        # self.blob_exit.update (self.enemies)

        # Atualize as informações do nível
        self.level_info.update()

        # Atualize o cronômetro de nível
        # self.level_timer.update ()

        # bonuses
        for bonus in self.bonuses:
            bonus.update()
            if not bonus.alive():
                self.bonuses.remove(bonus)

    def draw_tiles(self, draw_grid_overlay=False):
        """Desenha apenas a parte do bloco do mapa"""
        # Alinhe a parte inferior do mapa com a parte inferior da tela
        number_of_rows = len(self.indicies) / self.settings.map_width
        map_height = number_of_rows * self.settings.tile_height
        y_offset = self.screen_rect.height - map_height
        rect = pygame.Rect((self.x_offset, y_offset), (self.settings.tile_width, self.settings.tile_height))
        tiles_draw_per_row = 0

        #Loop através de cada linha e renderizá-lo, simples por enquanto, o mapa se encaixa na tela
        for index in self.indicies:
            if index >= 0:
                self.screen.blit(self.images[index], rect)
                if draw_grid_overlay:
                    color_red = (255, 0, 0)
                    pygame.draw.rect(self.screen, color_red, rect, 1)
            tiles_draw_per_row += 1
            rect.left += self.settings.tile_width

            # Cada linha de ladrilhos, desça um nível e redefina a coordenação x
            if tiles_draw_per_row == self.settings.map_width:
                rect.top += self.settings.tile_height
                rect.left = self.x_offset
                tiles_draw_per_row = 0

        #Desenhe os blocos
        # Isso funciona porque cada bloco tem um membro 'imagem' definido
        self.block_group.draw(self.screen)
    
    def draw(self, draw_grid_overlay=False):
        "" "Desenha o mapa de blocos." ""
        # Desenhe os inimigos - não posso usar o método Gorup por causa de nossa lógica de animação
        for enemy in self.enemies:
            enemy.draw()

        self.draw_tiles(draw_grid_overlay)

        #Desenhe o jogador
        self.player.draw()

        # Desenhe a saída
        # self.blob_exit.draw ()

        # Desenhe as informações do nível
        self.level_info.draw()

        # Draw the level timer
        # self.level_timer.draw()

        # Sorteio de bônus
        for bonus in self.bonuses:
            bonus.draw(self.screen)
