import pygame
import json

from config import *
from assistant import Assistant

class Collectible:
    """
    Clase que instancia objetos de tipo Collectible que serán utilizados en este juego para que el Player los recolecte y
    sume puntos a su score.
    """
    def __init__(self, pos_x:int, pos_y:int, path:str, type:str, scale:int|float) -> None:
        """
        Constructor de la clase.

        Args:
            pos_x (int): Posición en el eje x.
            pos_y (int): Posición en el eje y.
            path (str): Ruta de la imagen.
        """
        if(isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and pos_y and isinstance(path, str) and path and
           isinstance(type, str) and type and isinstance(scale, (int, float)) and scale):
            self.image_collectible = Assistant.get_surface_sprite(PATH_IMAGE+path,17,1,False,scale)
            self.image_collected = Assistant.get_surface_sprite(PATH_IMAGE+"Varios/Cositas/Items/Fruits/Collected.png",6,1,False,2)
            self.frame = 0
            self.animation = self.image_collected
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.rect_collision = pygame.Rect(self.rect.x+20, self.rect.y+15, (self.rect.w//3+2), self.rect.h-37)
            self.animation_elapsed_time = 0
            self.frame_rate = 30
            self.collected = False
            self.counter = 0
            self.type = type
            if self.type == "special":
                self.sound = pygame.mixer.Sound(PATH_SOUND+"fruit_special.mp3")
            else:
                self.sound = pygame.mixer.Sound(PATH_SOUND+"recoleccion.mp3")
            self.sound.set_volume(0.1)
    

    @staticmethod
    def create_collectible_json(json_file:str) -> list | None:
        """
        Método estático que se encarga de construir recolectables a traves de un archivo Json.

        Args:
            json_file (str): Archivo JSON que contiene la posición en el eje X e Y, así como la ruta de la imagen.

        Returns:
            list: Retorna la lista de Collectibles o None en caso de error.
        """
        try:
            collectible_list = []

            with open (json_file, "r") as file:
                data = json.load(file)

                if "collectibles" in data:
                    collectibles_data = data["collectibles"]

                    for collectible in collectibles_data:
                        pos_x = collectible["pos_x"]
                        pos_y = collectible["pos_y"]
                        path = collectible["path"]
                        type = collectible["type"]
                        scale = collectible["scale"]

                        collectible = Collectible(pos_x, pos_y, path, type, scale)
                        collectible_list.append(collectible)
                        
            return collectible_list

        except (FileNotFoundError, json.JSONDecodeError):
            return None

    
    def do_animation(self, delta_ms:int) -> None:
        """
        Método que se encarga las animaciones. Se encarga de establecer en 0 el frame cada vez que el tiempo sea mayor al
        al atributo self.frame_rate.
        También muestra la animación "self.image_collected" si es que el player colisiona con la instancia de la clase.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
        """
        if isinstance(delta_ms, int) and delta_ms:
            self.animation_elapsed_time += delta_ms

            if self.animation_elapsed_time >= self.frame_rate:
                self.animation_elapsed_time = 0
                self.frame = (self.frame + 1) % len(self.animation)
            
            if self.collected:
                self.animation = self.image_collected
            else:
                self.animation = self.image_collectible

    
    def update(self, delta_ms:int) -> None:
        """
        Método que se llama en cada iteración del bucle principal.

        Args:
            delta_ms (int): Variable que hace referencia al tiempo transcurrido desde que se actualizo la pantalla.
        """
        if isinstance(delta_ms, int) and delta_ms:
            self.do_animation(delta_ms)

    
    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar los objetos Collectibles en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            if self.collected:
                frame = min(self.frame, len(self.animation) - 1)
            else:
                frame = self.frame
                
            self.image = self.animation[frame]
            window.blit(self.image, self.rect)



