import pygame
import json
import random

from config import *
from assistant import Assistant

class Enemy:
    """
    Clase que instancia objetos de tipo Enemy que serán utilizados en este juego para tratar de matar al Player.
    
    """
    def __init__(self, animations:dict, pos_x:int, pos_y:int, right_limit:int, left_limit:int) -> None:
        """
        Constructor de la clase.

        Args:
            animations (dict): Un diccionario que contiene las animaciones y el numero de columna por animación.
            pos_x (int): Un entero que representa la posición en el eje x en el cual comenzara el enemigo.
            pos_y (int): Un entero que representa la posición en el eje y en el cual comenzara el enemigo.
            right_limit (int): Limite derecho hasta el cual se puede mover el enemigo.
            left_limit (int): Limite izquierdo hasta el cual se puede mover el enemigo.
        """
        if(isinstance(animations, dict) and animations and isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and
           pos_y and isinstance(right_limit, int) and right_limit and isinstance(left_limit, int) and left_limit):         
            self.still_r = Assistant.get_surface_sprite(PATH_IMAGE + animations["still_r"]["path"],animations["still_r"]["columns"], 1, True, 2)
            self.still_l = Assistant.get_surface_sprite(PATH_IMAGE + animations["still_l"]["path"],animations["still_l"]["columns"],1,False, 2)
            self.walking_r = Assistant.get_surface_sprite(PATH_IMAGE + animations["walking_r"]["path"],animations["walking_r"]["columns"],1, True, 2)
            self.walking_l = Assistant.get_surface_sprite(PATH_IMAGE + animations["walking_l"]["path"],animations["walking_l"]["columns"], 1, False, 2)
            self.running_r = Assistant.get_surface_sprite(PATH_IMAGE + animations["running_r"]["path"],animations["running_r"]["columns"],1, False, 2)
            self.running_l = Assistant.get_surface_sprite(PATH_IMAGE + animations["running_l"]["path"],animations["running_l"]["columns"],1, True, 2)
            self.frame = 0
            self.direction = DIRECTION_R
            self.animation = self.walking_r
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.rect_collision_head = pygame.Rect(self.rect.x+10, self.rect.y+15, self.rect.w-18, 5)
            self.rect_collision_body = pygame.Rect(self.rect.x+10, self.rect.y+35, self.rect.w-20, self.rect.h-35)
            self.rect_collision_feet = pygame.Rect(self.rect.x+25, self.rect.y+55, self.rect.w-55, 10)
            self.right_limit = right_limit
            self.left_limit = left_limit
            self.move_x = 0
            self.gravity = 3
            self.movement_elapsed_time = 0
            self.move_rate = 10
            self.animation_elapsed_time = 0
            self.frame_rate = 30
            self.rotate_image = pygame.transform.rotate(self.image, 180)
            self.was_hit = False
            self.patrol_state = "moving"
            self.patrol_wait_time = 0
            self.attack_range = 200
            self.elapsed_time_of_death = 0
            self.sound_death = pygame.mixer.Sound(PATH_SOUND+"muerte_enemigo.mp3")
            self.sound_death.set_volume(1)
            self.is_falling = False
            
        
    @staticmethod
    def create_enemy_json(json_file:str) -> list | None:
        """
        Método estático que se encarga de construir Enemies a traves de un archivo Json.

        Args:
            json_file (str): Archivo json que contiene las animaciones y la cantidad de columnas de cada animación,
            la posición en el eje x y en el eje, el limite de movimiento hacia la izquierda y la derecha.

        Returns:
            list: Retorna la lista de Enemies o None en caso de error.
        """
        try:
            enemy_list = []

            with open (json_file, "r") as file:
                data = json.load(file)

                if "enemies" in data:
                    enemy_data = data["enemies"]

                    for enemy in enemy_data:
                        animations = enemy["animations"]
                        pos_x = enemy["pos_x"]
                        pos_y = enemy["pos_y"]
                        right_limit = enemy["right_limit"]
                        left_limit = enemy["left_limit"]
                    
                        enemy = Enemy(animations, pos_x, pos_y, right_limit, left_limit)
                        enemy_list.append(enemy)

            return enemy_list
        
        except (FileNotFoundError, json.JSONDecodeError):
            return None


    def patrol(self) -> None:
        """
        Método que maneja los movimientos de patrullaje del enemigo, el enemigo va ir de izquierda a derecha entre
        las coordenadas "right_limit" y "left_limit", cuando llega a cualquiera de los limites se queda esperando 2 seg
        y vuelve a patrullar para el lado contrario.
        """
        if self.patrol_state == "moving":
            if self.direction == DIRECTION_R:
                self.animation = self.walking_r
                if self.rect.x >= self.right_limit:
                    self.animation = self.still_l
                    self.direction = DIRECTION_L
                    self.patrol_state = "waiting"
            elif self.direction == DIRECTION_L:
                self.animation = self.walking_l
                if self.rect.x <= self.left_limit:
                    self.animation = self.still_r
                    self.direction = DIRECTION_R
                    self.patrol_state = "waiting"
            self.add_x(self.direction)
        elif self.patrol_state == "waiting":
            if self.direction == DIRECTION_R:
                self.animation = self.still_l
            else:
                self.animation = self.still_r
            self.patrol_wait_time += 1
            if self.patrol_wait_time >= 120:
                self.patrol_wait_time = 0
                self.patrol_state = "moving"

    
    def attack(self, player) -> None:
        """
        Método que maneja el ataque del enemigo, si el Player se acerca hasta "attack_range" el enemigo comienza 
        a perseguirlo hasta que se aleje el Player vuelve a patrullar.

        Args:
            player (Player): Es una instancia de la clase Player.
        """
        if player:
            distance_x = player.rect.x - self.rect.x
            distance_y = player.rect.y - self.rect.y

            if not self.is_falling:
                if distance_x == 0:
                    if self.direction == DIRECTION_R:
                        self.animation = self.still_r
                    else:
                        self.animation = self.still_l
                elif abs(distance_x) < self.attack_range and abs(distance_y) <= 180:
                    if distance_x > 0:
                        self.direction = DIRECTION_L
                        self.animation = self.running_l
                    else:
                        self.direction = DIRECTION_R
                        self.animation = self.running_r
                    self.add_x(-self.direction)
                else:
                    self.patrol()

    
    def respawn(self) -> None:
        """
        Método que se encarga de reaparecer a los enemigos después de que el Player los haya matado en una coordenada
        random del eje x, y desde arriba de la ventana hasta que caigan al suelo.
        """
        self.rect.x = random.randrange(100, WIDTH - 50)
        self.rect_collision_head.x = self.rect.x
        self.rect_collision_body.x = self.rect.x
        self.rect_collision_feet.x = self.rect.x+25
        self.rect.y = 0
        self.rect_collision_body.y = self.rect.y+30
        self.rect_collision_head.y = self.rect.y+10
        self.rect_collision_feet.y = self.rect.y+52
        self.is_falling = True
        self.was_hit = False
            
        
    def collided_player(self, player, delta_ms:int) -> None:
        """
        Método que verifica si el player colisiono con el rectángulo de la cabeza el enemigo, si colisiono
        reproduce el sonido de muerte del enemigo y hace que el enemigo caiga fuera de la pantalla. 

        Args:
            player (Player): Es una instancia de la clase Player.
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
        """
        if player and isinstance(delta_ms, int) and delta_ms:
            if player.rect_collision_feet.colliderect(self.rect_collision_head) and not self.was_hit and not player.falling:
                self.was_hit = True
                self.sound_death.play()
            if self.was_hit:
                self.add_y(self.gravity)
                self.move_x = 0
                if self.rect.bottom >= HEIGHT:
                    self.elapsed_time_of_death += delta_ms
                    if self.elapsed_time_of_death > 5000:
                        self.respawn()
                        self.elapsed_time_of_death = 0

    
    def collided_platform(self, platform_list:list) -> None:
        """
        Verifica si el enemigo ha colisionado con alguna plataforma. Si el enemigo está cayendo y colisiona con una plataforma,
        se detiene la caída. Si el enemigo no colisiona con ninguna plataforma, continúa cayendo.

        Args:
            platform_list (list): Lista de plataformas
        """
        if isinstance(platform_list, list) and platform_list:
            if self.is_falling:
                self.add_y(self.gravity)
                self.animation = self.still_l
                self.move_x = 0
            for platform in platform_list:
                if self.rect_collision_feet.colliderect(platform.rect):
                    self.is_falling = False
                    break
                else:
                    self.is_falling = True
                        
                if self.rect.bottom >= GROUND+69 :
                    self.is_falling = False

            
    def do_movement(self, delta_ms:int, player) -> None:
        """
        Método que se encarga de los movimientos. Se encarga de establecer en 0 el frame cada vez que el tiempo sea mayor al
        al atributo self.frame_rate.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
            player (Player): Es una instancia de la clase Player.
        """
        if isinstance(delta_ms, int) and delta_ms and player:
            self.movement_elapsed_time += delta_ms

            if self.movement_elapsed_time >= self.move_rate:
                self.movement_elapsed_time = 0

                self.attack(player)

    
    def do_animation(self, delta_ms:int) -> None:
        """
        Método que se encarga las animaciones. Se encarga de establecer en 0 el frame cada vez que el tiempo sea mayor al
        al atributo self.frame_rate.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
        """
        if isinstance(delta_ms, int) and delta_ms:
            self.animation_elapsed_time += delta_ms
            if self.animation_elapsed_time >= self.frame_rate:
                self.animation_elapsed_time = 0
                self.frame = abs(self.frame + 1) % len(self.animation)

    
    def add_x(self, delta_x:int) -> None:
        """
        Método que actualiza la posición en el eje x de los rectángulos del enemigo.

        Args:
            delta_x (int): Entero que representa lo que se van a mover los rectángulos en el eje x.
        """
        if isinstance(delta_x, int) and delta_x:
            self.rect.x += delta_x
            self.rect_collision_head.x += delta_x
            self.rect_collision_body.x += delta_x
            self.rect_collision_feet.x += delta_x

    
    def add_y(self, delta_y:int) -> None:
        """
        Método que actualiza la posición en el eje y de los rectángulos del enemigo.

        Args:
            delta_y (int): Entero que representa lo que se van a mover los rectángulos en el eje y.
        """
        if isinstance(delta_y, int) and delta_y:
            self.rect.y += delta_y
            self.rect_collision_head.y += delta_y
            self.rect_collision_body.y += delta_y
            self.rect_collision_feet.y += delta_y

    
    def update(self, delta_ms:int, platform_list:list, player) -> None:
        """
        Método que se llama en cada iteración del bucle principal del juego, llama a los métodos de colisión, de movimiento
        y de animación.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
            player (Player): Es una instancia de la clase Player.
        """
        if isinstance(delta_ms, int) and delta_ms and isinstance(platform_list, list) and platform_list and  player:
            self.do_movement(delta_ms, player)
            self.do_animation(delta_ms)
            self.collided_player(player, delta_ms)
            self.collided_platform(platform_list)

            
    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar al enemigo en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            if get_mode():
                pygame.draw.rect(window, BLACK, self.rect_collision_head)
                pygame.draw.rect(window, BLUE, self.rect_collision_body)
                pygame.draw.rect(window, GREEN, self.rect_collision_feet)
                
            
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[self.frame]
            
            if self.was_hit:
                window.blit(self.rotate_image, self.rect)
            else:
                window.blit(self.image, self.rect)
                
