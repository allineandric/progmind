"" "Este módulo implementa o objeto jogador (sprite) para o Progmind" ""

from src.animation import Animation
from src.animated_sprite import AnimatedSprite
from src.time_bonus import TimeBonus
import pygame

class Player(AnimatedSprite):
    """Objeto de jogador"""

    def __init__(self, settings, screen, images, initial_bounding_rect, tile_map):
        """Inicialize o sprite do jogador"""
        # Calls AnimatedSprite, which in turn will call pygame.Sprite __init_()
        super().__init__(settings, screen, images)

        self.tile_map = tile_map

        # Substituir a posição inicial
        self.initial_bounding_rect = initial_bounding_rect
        self.rect.bottom = initial_bounding_rect.bottom
        self.rect.left = self.screen.get_rect().width / 2

        # Defina as margens transparentes
        self.margin_left = self.settings.player_sprite_horz_margin
        self.margin_right = self.settings.player_sprite_horz_margin
        self.margin_top = self.settings.player_sprite_top_margin

        # definir o retorno de chamada de verificação de colisão opcional
        self.collision_check = self.collided

        # Estes são específicos para o objeto do jogador
        self.air_jumps = 0
        self.max_air_jumps = settings.player_max_air_jumps
        self.idle_top = False
        self.idle_counter = 0
        self.won_level = False
        self.at_top = False

        # Adicione as animações para o jogador
        self.animations[self.settings.anim_name_idle_left] = Animation([0, 1, 2, 3, 2, 1], 5)
        self.animations[self.settings.anim_name_idle_right] = Animation([5, 6, 7, 8, 7, 6], 5)
        self.animations[self.settings.anim_name_walk_left] = Animation([0, 10, 11, 10], 2)
        self.animations[self.settings.anim_name_walk_right] = Animation([5, 12, 13, 12], 2)
        self.animations[self.settings.anim_name_jump_up_left] = Animation([15], 5)
        self.animations[self.settings.anim_name_jump_down_left] = Animation([16], 5)
        self.animations[self.settings.anim_name_jump_up_right] = Animation([17], 5)
        self.animations[self.settings.anim_name_jump_down_right] = Animation([18], 5)
        self.animations[self.settings.anim_name_dead] = Animation([4], 5)
        self.current_animation = self.settings.anim_name_idle_left
        self.facing_left = True

    def reset(self):
        """Redefina o objeto do jogador para o mapa"""
        player = self
        player.rect.bottom = self.initial_bounding_rect.bottom
        player.dx = 0.0
        player.dy = 0.0
        player.dying = False
        player.idle_counter = 0
        player.idle_top = False
        player.won_level = False
        player.at_top = False

    def update_current_animation(self):
        """Defina a animação correta com base no estado"""
        # DEAD
        if self.idle_top:
            self.set_current_animation(self.settings.anim_name_idle_left)
        elif self.dying:
            self.set_current_animation(self.settings.anim_name_dead)
        # IDLE
        elif self.dx == 0 and self.dy == 0:
            if self.facing_left:
                self.set_current_animation(self.settings.anim_name_idle_left)
            else:
                self.set_current_animation(self.settings.anim_name_idle_right)
        # WALKING
        elif self.dy == 0:
            if self.dx < 0:
                self.set_current_animation(self.settings.anim_name_walk_left)
            else:
                self.set_current_animation(self.settings.anim_name_walk_right)
        # JUMPING
        else:
            if self.dy < 0:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_up_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_up_right)
            else:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_down_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_down_right)

    def collided(self, player, sprite):
        """Este retorno de chamada é usado para modificar a verificação de colisão básica para o sprite do jogador"""
        if sprite.dying:
            return False
        
        player_rect = player.rect.copy()
        # reduza o retângulo do jogador com base nas margens
        player_rect.height -= player.settings.player_sprite_top_margin
        player_rect.width -= (player.settings.player_sprite_horz_margin * 2)
        player_rect.midbottom = player.rect.midbottom
        # Agora faça uma verificação padrão com o Rect ajustado
        return player_rect.colliderect(sprite.rect)

    def update(self, tile_map, enemies):
        """Atualiza a posição do jogador sprite"""

        if not self.dying:
            # Verifique se estamos na linha superior
            if self.idle_top:
                self.idle_counter = 0
                if self.idle_counter > (30 * 3):
                    self.won_level = False
           
            # O AnimatedSprite lida com a maior parte disso, mas salve o Grupo de inimigos atuais para o manipulador
            self.enemies = enemies
            super().update(tile_map, tile_map.block_group)
            if self.dy == 0:
                self.air_jumps = 0

                # O jogador também precisa verificar o grupo de sprites inimigos
            intersected_blobs = pygame.sprite.spritecollide(self, enemies, False, self.collision_check)
            if intersected_blobs:
                self.dying = True
                self.dy = -15
                self.falling = True
                self.falling_frames = 1
                    
            player_idle = ((self.current_animation == self.settings.anim_name_idle_left) or (self.current_animation == self.settings.anim_name_idle_right))
            player_walking = ((self.current_animation == self.settings.anim_name_walk_left) or (self.current_animation == self.settings.anim_name_walk_right))
            if (self.rect.bottom <= tile_map.player_bounds_rect.top + 2 * self.settings.tile_height) and (player_idle or player_walking):
                self.idle_top = False
                self.at_top = True
                self.idle_counter = 0
        else:
            if self.rect.top > self.screen_rect.bottom:
               # Por enquanto, apenas reinicie a posição do jogador, mas nada mais
                self.rect.bottom = tile_map.player_bounds_rect.bottom
                self.dx = 0.0
                self.dy = 0.0
                self.dying = False
            else:
                if self.dy < self.settings.terminal_velocity:
                    self.dy += self.settings.gravity
                self.rect.centery += self.dy
                self.falling_frames += 1

        self.finish_update()

    def handle_collision(self, collision_list, group):
        """Dada uma lista de sprites que colidem com o jogador, altere o estado, como posição, velocidade, etc."""
        # Mesmo que seja uma lista, o primeiro item deve ser tudo de que precisamos por agora
        if collision_list:
            block = collision_list[0]

            #isso é uma colisão lateral?
            side_collision = self.rect.right > block.rect.right  or self.rect.left < block.rect.left

            # Queda é o caso padrão, então verifique primeiro
            if self.dy > 0:
                self.falling = False
                self.falling_frames = 1
                self.air_jumps = 0
                self.dy = 0
                self.rect.bottom = block.rect.top
            # Se o jogador estiver pulando, verifique se há um acerto menor
            elif self.dy < 0:
                if self.rect.bottom > block.rect.bottom:
                    self.dy = 0
                    self.rect.top = block.rect.bottom - self.settings.player_sprite_top_margin
                    # remova os blocos atingidos pela parte inferior
                    group.remove(collision_list)

                    # remova os inimigos acima desses blocos
                    self.remove_enemies_above_blocks(collision_list)
            # Agora verifique a esquerda
            elif self.dx > 0:
                if side_collision:
                    self.dx = 0
                    self.rect.right = block.rect.left + self.settings.player_sprite_horz_margin
            elif self.dx < 0:
                if side_collision:
                    self.dx = 0
                    self.rect.left = block.rect.right - self.settings.player_sprite_horz_margin

    def remove_enemies_above_blocks(self, collision_list):
        # construir um kill rect para verificar os inimigos
        kill_rect = collision_list[0].rect
        for sprite in collision_list:
            kill_rect.union_ip(sprite.rect)

        #Subir um bloco
        kill_rect.move_ip(0, collision_list[0].rect.height * -1)

        # Agora veja se algum inimigo está neste bloco
        for enemy in self.enemies:
            if kill_rect.colliderect(enemy.rect):
                enemy.dying = True
                enemy.dy = self.settings.enemy_death_dy
                bonus = TimeBonus(enemy.rect, "ACERTOU!!!", 500, self.tile_map.level_timer, self.settings.bonus_font)
                self.tile_map.bonuses.append(bonus)
