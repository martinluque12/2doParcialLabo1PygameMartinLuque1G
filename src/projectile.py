import pygame

from config import *

class Projectile(pygame.sprite.Sprite):
    """
    Clase que instancia objetos de tipo Projectile que serán utilizados para disparar por el Player de este juego.

    Args:
        pygame.sprite.Sprite (Clase Sprite): Hereda de la Biblioteca "pygame" y del modulo "sprite" la clase "Sprite".
    """
    
    def __init__(self, pos_x:int, pos_y:int) -> None:
        """
        Constructor de la clase.

        Args:
            pos_x (int): Un entero que representa la posición en el eje x en el cual comenzara el Projectile.
            pos_y (int): Un entero que representa la posición en el eje y en el cual comenzara el Projectile.
        """
        super().__init__()
        """
        Constructor de la clase de la cual hereda la clase Projectile.
        """
        if isinstance(pos_x, int) and pos_x and isinstance(pos_y, int) and pos_y:
            self.image = pygame.image.load(PATH_IMAGE+"Varios/Cositas/Enemies/Trunk/Bullet.png")
            self.image = pygame.transform.scale(self.image, (30,30))
            self.rect = self.image.get_rect()
            self.rect.center = (pos_x, pos_y)
            self.speed = 5
            self.sound = pygame.mixer.Sound(PATH_SOUND+"disparo.mp3")
            self.sound.set_volume(0.2)
            self.sound.play()


    def collided_enemy(self, enemy_list:list) -> None:
        """
        Método que verifica si el proyectil colisiono con un enemigo si es asi elimina el proyectil, reproduce el
        sonido de muerte del enemigo y aplica gravedad al enemigo para que caiga fuera de la pantalla. 

        Args:
            enemy_list (list): Lista de enemigos.
        """
        if isinstance(enemy_list, list) and enemy_list:
            for enemy in enemy_list:
                if self.rect.colliderect(enemy.rect_collision_body):
                    enemy.was_hit = True
                    self.kill()
                    enemy.sound_death.play()
                if enemy.was_hit:
                    enemy.add_y(enemy.gravity)
                    enemy.move_x = 0


    def collided_traps(self, traps_list:list) -> None:
        """
        Método que verifica si el proyectil colisiono con una trampa, si es asi elimina el proyectil.

        Args:
            traps_list (list): Lista de trampas.
        """
        if isinstance(traps_list, list) and traps_list:
            for trap in traps_list:
                if self.rect.colliderect(trap.rect):
                    self.kill()


    def collided_platform(self, platform_list:list) -> None:
        """
        Método que verifica si el proyectil colisiono con una plataforma, si es asi elimina el proyectil.

        Args:
            platform_list (list): Lista de plataformas.
        """
        if isinstance(platform_list, list) and platform_list:
            for platform in platform_list:
                if platform.collided and self.rect.colliderect(platform.rect):
                    self.kill()


    def add_x(self, delta_x:int) -> None:
        """
        Método que actualiza la posición en el eje x del rectángulo del proyectil.

        Args:
            delta_x (int): Entero que representa lo que se va a mover el rectángulo en ele eje x.
        """
        if isinstance(delta_x, int) and delta_x:
            self.rect.x += delta_x


    def update(self, enemy_list:list, traps_list:list, platform_list:list) -> None:
        """
        Método que se llama en cada iteración del bucle principal del juego, llama a los métodos de colisión.

        Args:
            enemy_list (list): Lista de enemigos.
            traps_list (list): Lista de trampas.
            platform_list (list): Lista de plataformas.
        """
        if(isinstance(enemy_list, list) and enemy_list and isinstance(traps_list, list) and traps_list and
           isinstance(platform_list, list) and platform_list):
            self.collided_enemy(enemy_list)
            self.collided_traps(traps_list)
            self.collided_traps(platform_list)
            self.add_x(self.speed)
            