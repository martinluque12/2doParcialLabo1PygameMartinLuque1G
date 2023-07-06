import pygame
import json

from config import *
from assistant import Assistant
from projectile import Projectile


class Player:
    """
    Clase que instancia objetos de tipo Player que serán utilizados por los usuarios de este juego.

    """
    def __init__(self, animations:dict, pos_x:int, pos_y:int) -> None:
        """
        Constructor de la clase.

        Args:
            animations (dict): Un diccionario que contiene las animaciones y el numero de columna por animación.
            pos_x (int): Un entero que representa la posición en el eje x en el cual comenzara el Player.
            pos_y (int): Un entero que representa la posición en el eje y en el cual comenzara el Player.
        """
        super().__init__()
        """
        Constructor de a clase de la cual hereda la clase Player.
        """
        if isinstance(animations, dict) and animations and isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and pos_y:
            self.still_r = Assistant.get_surface_sprite(PATH_IMAGE+animations["still_r"]["path"],animations["still_r"]["columns"],1,False,2)
            self.still_l = Assistant.get_surface_sprite(PATH_IMAGE+animations["still_l"]["path"],animations["still_l"]["columns"],1,True,2)
            self.walking_r = Assistant.get_surface_sprite(PATH_IMAGE+animations["walking_r"]["path"],animations["walking_r"]["columns"],1,False,2)
            self.walking_l = Assistant.get_surface_sprite(PATH_IMAGE+animations["walking_l"]["path"],animations["walking_l"]["columns"],1,True,2)
            self.jumping_r = Assistant.get_surface_sprite(PATH_IMAGE+animations["jumping_r"]["path"],animations["jumping_r"]["columns"],1,False,2)
            self.jumping_l = Assistant.get_surface_sprite(PATH_IMAGE+animations["jumping_l"]["path"],animations["jumping_l"]["columns"],1,True,2)
            self.heart_red = pygame.image.load(PATH_IMAGE+"Varios/lives.png").convert_alpha()
            self.heart_red = pygame.transform.scale(self.heart_red, (60, 50))
            self.heart_gray = pygame.image.load(PATH_IMAGE+"Varios/live_lost.png").convert_alpha()
            self.heart_gray = pygame.transform.scale(self.heart_gray, (60, 50))
            self.frame = 0
            self.direction = DIRECTION_R
            self.animation = self.still_r
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.rect_collision_feet = pygame.Rect((self.rect.x+20), (self.rect.y+self.rect.h-3), (self.rect.w//3+4),4)
            self.rect_collision_body = pygame.Rect((self.rect.x+15), (self.rect.y+13), (self.rect.w//2), 40)
            self.move_x = 0
            self.move_y = 0
            self.lives = 3
            self.score = 0
            self.gravity = 8
            self.walking_speed = 5
            self.jumping_power = 25
            self.y_start_jump = 0
            self.jump_height = 136
            self.is_jumping = False
            self.animation_elapsed_time = 0
            self.frame_rate = 35
            self.movement_elapsed_time = 0
            self.move_rate = 10
            self.rotated_image = pygame.transform.rotate(self.image, 180)
            self.falling = False
            self.hit_cooldown = 0
            self.projectile = pygame.sprite.Group()
            self.is_shooting = False
            self.facing_right = True
            self.can_shooting = False
            self.sound_jump = pygame.mixer.Sound(PATH_SOUND+"salto.mp3")
            self.sound_jump.set_volume(0.1)
            self.sound_death = pygame.mixer.Sound(PATH_SOUND+"muerte_player.mp3")
            self.sound_death.set_volume(0.3)
            self.radius = 31


    @staticmethod
    def create_player_json(json_file:str) -> list | None:
        """
        Método estático que se encarga de construir Players a traves de un archivo Json.

        Args:
            json_file (str): Archivo json que contiene las animaciones y la cantidad de columnas de cada animación,
            la posición en el eje x e y.

        Returns:
            list: Retorna la lista de Players o None en caso de error.
        """
        try:
            player_list = []

            with open (json_file, "r") as file:
                data = json.load(file)

                if "players" in data:
                    player_data = data["players"]

                    for player in player_data:

                        animations = player["animations"]
                        pos_x = player["pos_x"]
                        pos_y = player["pos_y"]

                        player = Player(animations, pos_x, pos_y)
                        player_list.append(player)

            return player_list

        except (FileNotFoundError, json.JSONDecodeError):
            return None


    def still(self) -> None:
        """
        Método que carga la imagen "quieto" del Player dependiendo de para que lado este posicionado el Player.
        """
        if self.animation != self.still_r and self.animation != self.still_l:
            self.move_x = 0
            self.move_y = 0
            self.frame = 0

            if self.direction == DIRECTION_R:
                self.animation = self.still_r
            else:
                self.animation = self.still_l


    def walking(self, direction:int) -> None:
        """
        Método que carga la animación de "caminando" dependiendo la dirección del Player en ese momento,
        también le asigna la velocidad de el Player caminando (hacia la izquierda o la derecha).

        Args:
            direction (int): Dirección que va a tener el Player en el momento al cual se llame a este método.
        """
        if isinstance(direction, int) and direction:
            if self.direction != direction or (self.animation != self.walking_r and self.animation != self.walking_l):
                self.frame = 0
                self.direction = direction

                if self.direction == DIRECTION_R:
                    self.move_x = self.walking_speed
                    self.animation = self.walking_r
                else:
                    self.move_x = -self.walking_speed
                    self.animation = self.walking_l


    def jumping(self) -> None:
        """
        Método que carga la animación de "saltando" dependiendo la dirección del Player en ese momento,
        si esta corriendo y salta se le agrega un salto mas potente y se le agrega un pequeño movimiento en el eje x,
        si esta caminando tiene un salto mas normal.
        """
        if not self.is_jumping:
            self.frame = 0
            self.is_jumping = True
            self.y_start_jump = self.rect.y
            self.sound_jump.play()

            if self.direction == DIRECTION_R:
                self.move_y = -self.jumping_power
                self.animation = self.jumping_r
            else:
                self.move_y = -self.jumping_power
                self.animation = self.jumping_l
        else:
            self.is_jumping = False
            self.still()


    def shoot(self) -> None:
        """
        Método que se encarga de los disparos del Player si es que puede disparar.
        """
        if self.can_shooting:
            if self.direction == DIRECTION_R:
                projectile = Projectile(self.rect.x+20, self.rect.y+40)
            else:
                self.facing_right = False
                projectile = Projectile(self.rect.x+20, self.rect.y+40)
                projectile.speed *= -1
            self.projectile.add(projectile)


    def respawn(self) -> None:
        """
        Método que se encarga de Reaparecer al Player cuando un enemigo colisiona con el o una trampa,
        mientras las vidas sean mayor a 0.
        """
        if self.rect.y > HEIGHT:
            if self.lives > 0:
                self.can_shooting = False
                self.rect.x = 10
                self.rect.y = 561
                self.rect_collision_feet.x = self.rect.x+20
                self.rect_collision_feet.y = self.rect.y+self.rect.h-3
                self.rect_collision_body.x = self.rect.x+15
                self.rect_collision_body.y = self.rect.y+13

                self.falling = False
                if self.score > 0:
                    self.score -= 50


    def collided_platform(self, platform_list:list) -> bool | None:
        """
        Método que se encarga de verificar si el Player colisiono con una plataforma.

        Args:
            platform_list (list): Lista de plataformas.

        Returns:
            bool: Si detecta que el Player esta en una plataforma y si paso la validación retorna True,
            de lo contrario retorna False o None en caso de no pasar la validación.
        """
        if isinstance(platform_list, list) and platform_list:
            is_platform = False
            if self.rect.y >= GROUND:
                is_platform = True
            else:
                for platform in platform_list:
                    if platform.collided:
                        if self.rect_collision_feet.colliderect(platform.rect_collision_top):
                            is_platform = True
                            break
                        if self.rect_collision_body.colliderect(platform.rect_collision_bottom):
                            self.move_y = 0

            return is_platform
        else:
            return None


    def collided_collectibles(self, collectibles_list:list) -> None:
        """
        Método que verifica si el Player colisiono con una objeto recogible, si es asi elimina el objeto de la lista
        y le suma 100 al score del Player.

        Args:
            collectibles_list (list): Lista de objetos recolectables.
        """
        if isinstance(collectibles_list, list) and collectibles_list:
            for collectibles in collectibles_list:
                if self.rect_collision_body.colliderect(collectibles.rect):
                    collectibles.collected = True
                    collectibles.sound.play()
                if collectibles.collected:
                    collectibles.counter += 1
                    if collectibles.counter > 7:
                        collectibles_list.remove(collectibles)
                        if collectibles.type == "special":
                            self.score += 150
                        else:
                            self.score += 100
                        if collectibles.type == "special":
                            self.can_shooting = True
                    break


    def collided_enemy(self, enemy_list:list) -> None:
        """
        Método que verifica si un enemigo colisiono con el Player, si asi es se muestra la animación "golpeado"
        y el Player pierde una vida.

        Args:
            enemy_list (list): Lista de enemigos.
        """
        if isinstance(enemy_list, list) and enemy_list:
            for enemy in enemy_list:
                if(enemy.rect_collision_body.colliderect(self.rect_collision_body) and not self.falling and
                   self.hit_cooldown == 0):
                    self.falling = True
                    self.move_x = 0
                    self.lives -= 1
                    self.hit_cooldown = 60
                    self.sound_death.play()


    def collided_tramps(self, trap_list:list) -> None:
        """
        Método que verifica si el Player colisiono con una trampa, si asi es se muestra la animación "golpeado"
        y el Player pierde una vida.

        Args:
            trap_list (list): Lista de trampas.
        """
        if isinstance(trap_list, list) and trap_list:
            for trap in trap_list:
                if trap.has_collided(self) and not self.falling and self.hit_cooldown == 0:
                    self.falling = True
                    self.move_x = 0
                    self.lives -= 1
                    self.hit_cooldown = 60
                    self.sound_death.play()


    def apply_gravity(self, platform_list:list) -> None:
        """
        Método que aplica gravedad al Player y maneja el salto cuando eñl player no colisiona con una plataforma.

        Args:
            platform_list (list): Lista de plataformas.
        """
        if isinstance(platform_list, list) and platform_list:
            if not self.collided_platform(platform_list):
                self.add_y(self.gravity)
            elif self.is_jumping:
                self.jumping()


    def do_movement(self, delta_ms:int, platform_list:list) -> None:
        """
        Método que realiza el movimiento del personaje en el juego. Actualiza la posición del personaje según el tiempo
        transcurrido y aplica la gravedad. El movimiento se basa en las variables de movimiento (move_x y move_y) y
        el tiempo delta_ms.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
            platform_list (list): Lista de plataformas.
        """
        if isinstance(delta_ms, int) and delta_ms and isinstance(platform_list, list) and platform_list:
            self.movement_elapsed_time += delta_ms

            if self.movement_elapsed_time >= self.move_rate:
                if (abs(self.y_start_jump) - abs(self.rect.y)) > self.jump_height and self.is_jumping:
                    self.move_y = 0

                self.movement_elapsed_time = 0
                self.add_x(self.move_x)
                self.add_y(self.move_y)

                self.apply_gravity(platform_list)


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

                self.frame = (self.frame + 1) % len(self.animation)



    def add_x(self, delta_x:int) -> None:
        """
        Método que actualiza la posición en el eje x de los rectángulos del Player.

        Args:
            delta_x (int): Entero que representa lo que se van a mover los rectángulos en el eje x.
        """
        if isinstance(delta_x, int) and delta_x:
            new_x = self.rect.x + delta_x
            if 0 <= new_x <= WIDTH - self.rect.width:
                self.rect.x = new_x
                self.rect_collision_feet.x += delta_x
                self.rect_collision_body.x += delta_x


    def add_y(self, delta_y:int) -> None:
        """Método que actualiza la posición en el eje y de los rectángulos del Player.

        Args:
            delta_y (int): Entero que representa lo que se van a mover los rectángulos en el eje y.
        """
        if isinstance(delta_y, int) and delta_y:
            new_y = self.rect.y + delta_y
            if -80 <= new_y:
                self.rect.y = new_y
                self.rect_collision_feet.y += delta_y
                self.rect_collision_body.y += delta_y


    def controls(self, keys:pygame.key.ScancodeWrapper) -> None:
        """
        Método que se encarga de verificar qué tecla se presionó y realizar las acciones correspondientes.

        Args:
            keys (list): Lista de teclas presionadas.
        """
        if not self.falling:
            if isinstance(keys, pygame.key.ScancodeWrapper) and keys:
                if keys[pygame.K_UP] :
                    if not self.is_jumping:
                        self.jumping()
                elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    self.walking(DIRECTION_R)
                elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    self.walking(DIRECTION_L)
                else:
                    self.still()

                if keys[pygame.K_SPACE] and not self.is_shooting:
                    self.shoot()
                    self.is_shooting = True

                if not keys[pygame.K_SPACE]:
                    self.is_shooting = False


    def update(self, delta_ms:int, platform_list:list, collectibles_list:list, enemy_list:list, trap_list:list, keys:pygame.key.ScancodeWrapper) -> None:
        """
        Método que se llama en cada iteración del bucle principal del juego, llama a todos los métodos que necesitan
        verificarse constantemente.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
            platform_list (list): Lista de plataformas.
            collectibles_list (list): Lista de objetos que el player recolecta.
            enemy_list (list): Lista de enemigos.
            trap_list (list): Lista de trampas.
            keys (pygame.key.ScancodeWrapper): Lista de teclas presionadas.
        """
        if(isinstance(delta_ms, int) and delta_ms and isinstance(platform_list, list) and platform_list and
           isinstance(collectibles_list, list) and collectibles_list and isinstance(enemy_list, list) and enemy_list and
           isinstance(trap_list, list) and trap_list) and isinstance(keys, pygame.key.ScancodeWrapper) and keys:

            self.controls(keys)
            self.do_movement(delta_ms, platform_list)
            self.do_animation(delta_ms)
            self.collided_collectibles(collectibles_list)
            self.collided_enemy(enemy_list)
            self.collided_tramps(trap_list)
            self.projectile.update(enemy_list, trap_list, platform_list)

            if self.falling:
                self.add_y(2)

            if self.hit_cooldown > 0:
                self.hit_cooldown -= 1
            self.respawn()


    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar al Player en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            if get_mode():
                pygame.draw.rect(window, BLUE, self.rect_collision_feet)
                pygame.draw.rect(window, GREEN, self.rect_collision_body)

            self.image = self.animation[self.frame]

            if self.falling:
                window.blit(self.rotated_image, self.rect)
            else:
                window.blit(self.image, self.rect)
                self.projectile.draw(window)
    

    def draw_lives(self, window:pygame.Surface) -> None:
        """
        Método que dibuja las vidas del Player en la ventana del juego.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            heart_x = 500
            heart_y = 10
            heart_spacing = 30 

            for i in range(self.lives):
                heart_rect = self.heart_red.get_rect()
                heart_rect.x = heart_x + i * heart_spacing
                heart_rect.y = heart_y
                window.blit(self.heart_red, heart_rect)


            for i in range(self.lives, 3):
                heart_rect = self.heart_gray.get_rect()
                heart_rect.x = heart_x + i * heart_spacing
                heart_rect.y = heart_y
                window.blit(self.heart_gray, heart_rect)