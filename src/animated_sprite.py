"""This module implements a shared subclass for animated sprites for Progmind"""

import pygame
from pygame.sprite import Sprite

class AnimatedSprite(Sprite):
    """Animated Sprite object holding shared logic"""

    def __init__(self, settings, screen, images):
        """Init the Animated Sprite logic"""
        super().__init__()
        # cache these objects
        self.settings = settings
        self.screen = screen
        self.images = images
        self.screen_rect = screen.get_rect()

        # All images are the same size, so set the rect to the first one
        self.rect = images[0].get_rect()

        # Inicialmente sem se mover e sem cair
        self.dx = 50
        self.dy = 0.0
        self.falling = False
        self.falling_frames = 0
        self.dying = False

        # These are designed to be overridden by the parent class
        self.animations = {}
        self.current_animation = None
        self.facing_left = False
        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0

        # Overrides
        self.bound_by_the_laws_of_physics = True
        self.bound_by_map = True

        # Collision check callback (optional)
        self.collision_check = None

    def set_current_animation(self, animation_id):
        """Update and reset the animation sequence - does nothing if id is the same as current, use reset() for that"""
        if (self.current_animation != animation_id):
            self.current_animation = animation_id
            self.animations[self.current_animation].reset()

    def handle_collision(self, collision_list, group):
        """Should be implemented by the derived class"""
        pass
    
    def update_current_animation(self):
        """Should be implemented by the derived class"""
        pass

    def apply_physics(self, tile_map):
        """Gravity in this case"""
        # O dy deve ser controlado pela 'gravidade' apenas por agora - os saltos irão dar um
         # Velocidade inicial de aumento (feita no manipulador de teclas), então a gravidade atua aqui na atualização.
         # Sem algum tipo de aproximação da gravidade, os sprites se moveriam na mesma velocidade
         # enquanto estão no ar e parecem muito leves, como se estivessem caminhando na lua em baixa gravidade
         # apenas pior. Não é um problema para um jogo 2D de cima para baixo :)
        # If not on the ground floor, just assume we're falling (for now this will be true)
        if self.rect.bottom < tile_map.player_bounds_rect.bottom and self.falling == False:
            self.falling = True
            self.falling_frames = 1

        if self.falling:
            # As long as the sprite is continually falling, the 'speed' increases each
            # frame by the acceleration until some terminal speed
            if self.dy < self.settings.terminal_velocity:
                self.dy += self.settings.gravity
            self.rect.centery += self.dy
            self.falling_frames += 1

    def basic_bounds_containment(self, tile_map):
        """Contains the sprite to the player bounds"""
        # Bounds check on bottom edge
        if self.rect.bottom > tile_map.player_bounds_rect.bottom:
            self.rect.bottom = tile_map.player_bounds_rect.bottom
            self.dy = 0.0
            self.falling = False

        # Left/Right bounds containment check
        # RIGHT
        if self.dx > 0: 
            self.rect.centerx += self.dx
            if self.rect.right - self.margin_right > tile_map.player_bounds_rect.right:
                self.rect.right = tile_map.player_bounds_rect.right + self.margin_right
                self.dx = 0.0

        if self.dx < 0:
            self.rect.centerx += self.dx
            if self.rect.left + self.margin_left < tile_map.player_bounds_rect.left:
                self.rect.left = tile_map.player_bounds_rect.left - self.margin_left
                self.dx = 0.0

    def update(self, tile_map, collision_check_group=None):
        """Atualiza a posição básica do sprite, a colisão mais detalhada é deixada para a classe derivada"""
        if self.bound_by_the_laws_of_physics:
            self.apply_physics(tile_map)

        if self.bound_by_map:
            self.basic_bounds_containment(tile_map)
        
         # Sprite collision
        if collision_check_group:
            intersected_sprites = pygame.sprite.spritecollide(self, collision_check_group, False, self.collision_check)
            # This is required by the implementing class, this function will allow the sub-types of
            # sprite objects to handle the collisions differently - just like the self.collision_check
            # function allows them to alter the actual collision detection (e.g. based on transparent margins)
            self.handle_collision(intersected_sprites, collision_check_group)

    def finish_update(self):
        """Common code to close out a frame update"""
        self.update_current_animation()
        self.animations[self.current_animation].animate()

    def draw(self):
        """Draws the animated sprite's current frame at its current position on the screen"""
        frame_index = self.animations[self.current_animation].get_current_frame()
        self.screen.blit(self.images[frame_index], self.rect)