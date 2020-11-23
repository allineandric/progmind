"""This module implements the enemy blob type for Progmind"""

import pygame
from pygame.sprite import Sprite
from src.animation import Animation
from src.animated_sprite import AnimatedSprite

class Blob(AnimatedSprite):
    """Blob enemy object"""

    def __init__(self, settings, screen, images):
        """Initialize the blob"""
        super().__init__(settings, screen, images)
        
        # Override the start position
        self.dx = self.settings.enemy_blob_dx
        
        # Set the blob-specific animations
        self.animations[self.settings.anim_name_walk_left] = Animation([0, 1, 2, 1], 2)
        self.animations[self.settings.anim_name_walk_right] = Animation([3, 4, 5, 4], 2)
        self.animations[self.settings.anim_name_jump_down_left] = Animation([6], 1)
        self.animations[self.settings.anim_name_jump_down_right] = Animation([6], 1)
        self.animations[self.settings.anim_name_dead] = Animation([7], 60)
        self.current_animation = self.settings.anim_name_walk_right
        self.facing_left = False

    def update_current_animation(self):
        """Set the correct animation based on state"""
        # DYING
        if self.dying:
            self.set_current_animation(self.settings.anim_name_dead)
        # WALKING
        elif self.dy == 0:
            if self.dx < 0:
                self.set_current_animation(self.settings.anim_name_walk_left)
            else:
                self.set_current_animation(self.settings.anim_name_walk_right)
        # JUMPING
        else:
            if self.dy > 0:
                if self.facing_left:
                    self.set_current_animation(self.settings.anim_name_jump_down_left)
                else:
                    self.set_current_animation(self.settings.anim_name_jump_down_right)

    def update(self, tile_map):
        """Atualiza a posição do sprite blob"""
        
        if not self.dying:
            last_dx = self.dx
            super().update(tile_map, tile_map.block_group)
            # Blobs só param quando atingem uma parede, então reverta o curso
            if last_dx != 0 and self.dx == 0:
                self.facing_left = not self.facing_left
                if self.facing_left:
                    self.dx = 1.0
                else:
                    self.dx = -1.0

            # verifique se o blob está sobre a "saída" para os inimigos, e se estiver, solte-o
            if tile_map.drainrect.colliderect(self.rect):
                self.dying = True
                self.falling = True
                self.falling_frames = 1
        else:
            if self.dy < self.settings.terminal_velocity:
                self.dy += self.settings.gravity
            
            self.rect.centery += self.dy
            self.falling_frames += 1

            if self.rect.top > self.screen_rect.bottom:
                self.kill()

        self.finish_update()

    def handle_collision(self, collision_list, group):
        """Dada uma lista de sprites que colidem com o sprite, altere o estado, como posição, velocidade, etc"""
        # Se houver apenas 1 bloco, então estamos no limite, então não faça nada nesse caso
        # e apenas deixe o sprite cair, caso contrário, prenda-se ao topo do bloco
        if collision_list:
            if len(collision_list) > 1:
                self.falling = False
                self.falling_frames = 1
                self.dy = 0
                self.rect.bottom = collision_list[0].rect.top
            elif len(collision_list) == 1:
                if self.facing_left and self.rect.right > collision_list[0].rect.left:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top
                elif not self.facing_left and self.rect.left < collision_list[0].rect.right:
                    self.falling = False
                    self.falling_frames = 1
                    self.dy = 0
                    self.rect.bottom = collision_list[0].rect.top
