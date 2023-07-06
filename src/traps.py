import pygame
import json

from config import *
from assistant import Assistant

class Traps:
    """
    Clase que instancia objetos de tipo Traps que serán utilizados en este juego para matar al Player.

    """
    def __init__(self, animations:dict, pos_x:int, pos_y:int, scale:int) -> None:
        """
        Método constructor de la clase.

        Args:
            pos_x (int): Posición en el eje x donde se ubicada la trampa.
            pos_y (int): Posición en el eje y donde se ubicada la trampa.
            animations (dict): Diccionario que contiene el path de la imagen y cuantas columnas tiene la imagen.
            scale (int | float) Escala de la imagen del objeto.
        """
        if(isinstance(animations, dict) and animations and isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and 
           pos_y and isinstance(scale, (int, float))):
            self.image_trap = Assistant.get_surface_sprite(PATH_IMAGE+animations["path"],animations["columns"],1,False,scale)
            self.frame = 0
            self.animation = self.image_trap
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.scale = scale
            self.animation_elapsed_time = 0
            self.frame_rate = 30
            if self.scale == 2:
                self.radius = 35
            else:
                self.radius = 25

    
    @staticmethod
    def create_traps_json(json_file:str) -> list | None:
        """
        Método estático que se encarga de construir trampas a traves de un archivo Json.

        Args:
            json_file (str): Archivo json que contiene el path de la imagen y las columnas que tiene esa imagen.

        Returns:
            list: Retorna la lista de Players o None en caso de error.
        """
        try:
            trap_list = []

            with open (json_file, "r") as file:
                data = json.load(file)

                if "traps" in data:
                    traps_data = data["traps"]

                    for trap in traps_data:
                        animations = trap["animations"]
                        pos_x = trap["pos_x"]
                        pos_y = trap["pos_y"]
                        scale = trap["scale"]

                        trap = Traps(animations, pos_x, pos_y, scale)
                        trap_list.append(trap)
            
            return trap_list

        except (FileNotFoundError, json.JSONDecodeError):
            return None
    

    def has_collided(self, player) -> bool:
        """
        Verifica si la trampa ha colisionado con el jugador utilizando colisiones de círculo, mediante el radio.

        Args:
            player (Player): Instancia de la clase Player.

        Returns:
            bool: Retorna True si al distancia es menor a la suma de los radios False de lo contrario.
        """
        if player:
            delta_x = self.rect.centerx - player.rect_collision_body.centerx
            delta_y = self.rect.centery - player.rect_collision_body.centery

            distance = (delta_x ** 2 + delta_y ** 2) ** 0.5

            return distance < self.radius + player.radius

    
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

    
    def update(self, delta_ms:int) -> None:
        """
        Método que se llama en cada iteración del bucle principal del juego, llama al método "do_animation" que necesita
        verificarse constantemente.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
        """
        if isinstance(delta_ms, int) and delta_ms:
            self.do_animation(delta_ms)

    
    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar las trampas en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            self.image =  self.animation[self.frame]
            window.blit(self.image, self.rect)

