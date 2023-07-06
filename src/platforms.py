import pygame
import json

from config import *
from assistant import Assistant

class Platform:
    """
    Clase que instancia objetos de tipo Platform que serán utilizados en este juego para que el Player pueda subirse en ellas.
    
    """
    def __init__(self, pos_x:int, pos_y:int, width:int, height, type:int, collided:bool) -> None:
        """
        Constructor de la clase.

        Args:
            pos_x (int): Posición en el eje x.
            pos_y (int): Posición en el eje y.
            width (int): Anchura de la plataforma.
            height (int): Altura de la plataforma.
            type (int): Tipo de plataforma.
            collided (bool, optional): Si es True el Player puede subirse en la plataforma si es False no.
        """
        if(isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and pos_y and isinstance(width, int) 
           and width and isinstance(height, int) and height and isinstance(type, int) and type and 
           isinstance(collided, bool) and collided):
            self.image = Assistant.get_surface_sprite(PATH_IMAGE+"Varios/Bloques/sheet1.png",8,8)[type]
            self.image =  pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y
            self.collided = collided
            if self.collided:
                self.rect_collision_top = pygame.Rect(self.rect.x, self.rect.y-1, self.rect.w, 5)
                self.rect_collision_bottom = pygame.Rect(self.rect.x, self.rect.y+31, self.rect.w, 20)
                self.rect_collision_left = pygame.Rect(self.rect.x-1, self.rect.y, self.rect.w-44, 49)
                self.rect_collision_right = pygame.Rect(self.rect.x+45, self.rect.y, 5, 49)
                

    @staticmethod
    def create_platform_json(json_file:str) -> list | None:
        """
        Método estático que se encarga de construir Plataformas a traves de un archivo Json.

        Args:
            json_file (str): Archivo json que contiene la posición en el eje x e y, el alto y el ancho de la plataforma,
            el tipo de plataforma y si funciona como plataforma para colisionar o no.

        Returns:
            list: Retorna la lista de Plataformas o None en caso de error.
        """
        try:
            platform_list = []

            with open (json_file, "r") as file:
                data = json.load(file)

                if "platforms" in data:
                    platform_data = data["platforms"]

                    for platform in platform_data:
                        pos_x = platform["pos_x"]
                        pos_y = platform["pos_y"]
                        width = platform["width"]
                        height = platform["height"]
                        type = platform["type"]
                        collided = platform.get("collided", False)

                        platform = Platform(pos_x, pos_y, width, height, type, collided)
                        platform_list.append(platform)
            
            return platform_list

        except (FileNotFoundError, json.JSONDecodeError):
            return None
        

    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar la plataforma en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            window.blit(self.image, self.rect)
            
        
            