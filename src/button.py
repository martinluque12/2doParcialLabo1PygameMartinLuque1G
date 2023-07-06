import pygame

class Button:
    """
    Clase que instancia objetos de tipo Button que se utilizaran en el juego para entrar en las diferentes pantallas.
    
    """
    def __init__(self, coordinate:tuple, regular_image:str, highlighted_image:str, size:tuple) -> None:
        """
        Método constructor de la clase.

        Args:
            coordinate (tuple): Coordenadas en el eje x e y donde se va ubicar el botón.
            regular_image (str): La imagen normal del botón.
            highlighted_image (str): La imagen que se muestra al pasar el mouse por encima del botón.
            size (tuple): Tamaño del botón (ancho y alto).
        """
        if(isinstance(coordinate, tuple) and coordinate and isinstance(regular_image, str) and regular_image and
           isinstance(highlighted_image, str) and highlighted_image and isinstance(size, tuple) and size):
            self.x = coordinate[0]
            self.y = coordinate[1]
            self.regular_image = pygame.image.load(regular_image).convert()
            self.regular_image = pygame.transform.scale(self.regular_image, size)
            self.highlighted_image = pygame.image.load(highlighted_image).convert()
            self.highlighted_image = pygame.transform.scale(self.highlighted_image, size)
            self.current_image = self.regular_image
            self.rect = self.regular_image.get_rect()
            self.rect.topleft = (self.x, self.y) 


    def update(self) -> None:
        """
        Método que se llama en cada iteración del bucle principal del juego, se obtiene la posición del mouse 
        y se verifica si la posición del mouse se encuentra dentro del rectángulo del botón, si es asi se muestra
        la imagen resaltada.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_image = self.highlighted_image
        else:
            self.current_image = self.regular_image


    def draw(self, window:pygame.Surface) -> None:
        """
        Método que se encarga de dibujar las instancias de Button en la ventana.

        Args:
            window (pygame.Surface): Es la ventana principal del juego.
        """
        if isinstance(window, pygame.Surface) and window:
            window.blit(self.current_image, self.rect)
	