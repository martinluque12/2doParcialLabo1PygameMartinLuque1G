import pygame, sys
import json, os

from config import *
from button import *
from player import Player
from platforms import Platform
from collectibles import Collectible
from enemy import Enemy
from traps import Traps

class Game:
    """
    Clase principal del juego, donde se manejan los eventos y los cambios de pantallas.
    """
    def __init__(self) -> None:
        """
        Constructor de la clase. 
        """
        pygame.init()
        pygame.display.set_caption("Catch me if you can")

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.is_playing = False
        self.paused = True
        self.paused_time = 0
        self.font = pygame.font.Font(FONT_BREAKING, 46)
        self.font_pause = pygame.font.Font(FONT_BREAKING, 150)
        self.start_time = None
        self.score_level_1 = 0
        self.score_level_2 = 0
        self.score_level_3 = 0
        self.score_total = self.score_level_1 + self.score_level_2 + self.score_level_3
        self.color_active = WHITE 
        self.color_passive = GREY
        self.active = False
        self.elapsed_time = None
                
        self.main_screen_buttons = [
            Button((400, 400), PATH_IMAGE + "Botones/boton_play.jpg", PATH_IMAGE + "Botones/boton_play_hover.jpg", (350,100)),
            Button((400, 525), PATH_IMAGE + "Botones/boton_controles.jpg", PATH_IMAGE + "Botones/boton_controles_hover.jpg",(350,100)),
            Button((400, 650), PATH_IMAGE + "Botones/boton_exit.jpg", PATH_IMAGE + "Botones/boton_exit_hover.jpg",(350,100))
        ]
        self.controls_screen_buttons = [
            Button((420, 700), PATH_IMAGE + "Botones/boton_back.jpg", PATH_IMAGE + "Botones/boton_back_hover.jpg", (350,100))
        ]
        self.pause_screen_buttons = [
            Button((10,10),PATH_IMAGE+"Botones/Play.png",PATH_IMAGE+"Botones/Play.png",(80,80)),
            Button((10,110),PATH_IMAGE+"Botones/Volume.png",PATH_IMAGE+"Botones/Volume.png",(80,80)),
            Button((10,210),PATH_IMAGE+"Botones/Volumen_off.png",PATH_IMAGE+"Botones/Volumen_off.png",(80,80)),
            Button((10,310),PATH_IMAGE+"Botones/Home.png",PATH_IMAGE+"Botones/Home.png",(80,80))
        ]
        self.screen_game_over_buttons = [
            Button((500,470),PATH_IMAGE+"Botones/boton_yes.png",PATH_IMAGE+"Botones/boton_yes.png",(100,100)),
            Button((600,470),PATH_IMAGE+"Botones/boton_no.png",PATH_IMAGE+"Botones/boton_no.png",(100,100))
        ]
        self.play_again_buttons = [
            Button((460,420),PATH_IMAGE+"Botones/boton_yes_winner.png",PATH_IMAGE+"Botones/boton_yes_winner.png",(100,100)),
            Button((600,420),PATH_IMAGE+"Botones/boton_no_winner.png",PATH_IMAGE+"Botones/boton_no_winner.png",(100,100))
        ]


    def main_screen(self) -> None:
        """
        Pantalla principal que se muestra al ejecutar el juego, con botones de "Play", "Controls" y "Exit".
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_principal.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"Sound_menu.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        while True:

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.main_screen_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.main_screen_buttons[0]:
                                self.level_one_screen()
                            if button == self.main_screen_buttons[1]:
                                self.screen_controls()
                            if button == self.main_screen_buttons[2]:
                                pygame.quit()
                                sys.exit()

            self.render(self.main_screen_buttons, background)
    
    
    def screen_controls(self) -> None:
        """
        Pantalla donde se muestran los controles a usar en el juego se accede a ella mediante los botones que tiene la
        pantalla principal. 
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_controlss.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        while True:

            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.controls_screen_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.controls_screen_buttons[0]:
                                self.main_screen()

            self.render(self.controls_screen_buttons, background)


    def level_one_screen(self) -> None:
        """
        Pantalla del nivel 1 se instancias todos los objetos que intervendrán en el juego, se muestra el tiempo desde
        que se empezó el nivel la cantidad de vidas, y el score.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_nivel_1.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"nivel_1.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        list_player = Player.create_player_json("src/Files Json/nivel_1.json")
        list_platforms = Platform.create_platform_json("src/Files Json/nivel_1.json")
        list_collectibles = Collectible.create_collectible_json("src/Files Json/nivel_1.json")
        list_enemy = Enemy.create_enemy_json("src/Files Json/nivel_1.json")
        list_tramps = Traps.create_traps_json("src/Files Json/nivel_1.json")
        
        self.start_time = pygame.time.get_ticks()

        while True:
            
            delta_ms = self.clock.tick(FPS)
            self.window.blit(background, background.get_rect())
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        change_mode()
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                        self.start_time += pygame.time.get_ticks() - self.pause_start
            
            keys = pygame.key.get_pressed()

            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            text_surface = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, BLUE)
            text_rect = text_surface.get_rect(topleft=(10, 5))
            self.window.blit(text_surface, text_rect)

            for tramp in list_tramps:
                tramp.update(delta_ms)
                tramp.draw(self.window)

            for platform in list_platforms:
                platform.draw(self.window)

            for rewards in list_collectibles:
                rewards.update(delta_ms)
                rewards.draw(self.window)
            
            for enemy in list_enemy:
                enemy.update(delta_ms, list_platforms, list_player[0])            
                enemy.draw(self.window)
               
            for player in list_player:
                player.update(delta_ms, list_platforms, list_collectibles, list_enemy, list_tramps, keys)
                player.draw(self.window)
                player.draw_lives(self.window)

                self.score_level_1 = player.score
                
                if player.lives == 0 and player.rect.y > HEIGHT:
                    self.game_over_screen()

            score_text = f"Score: {self.score_level_1}"
            render_text = self.font.render(score_text, True, BLUE)
            self.window.blit(render_text, (1000, 5))
            
            if len(list_collectibles) == 0:
                self.level_two_screen()

            pygame.display.update()   
        
        
    def level_two_screen(self) -> None:
        """
        Pantalla del nivel 2 se instancias todos los objetos que intervendrán en el juego, se muestra el tiempo desde
        que se empezó el nivel la cantidad de vidas, y el score.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_level_2.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"nivel_2.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        list_player = Player.create_player_json("src/Files Json/nivel_2.json")
        list_platforms = Platform.create_platform_json("src/Files Json/nivel_2.json")
        list_collectibles = Collectible.create_collectible_json("src/Files Json/nivel_2.json")
        list_enemy = Enemy.create_enemy_json("src/Files Json/nivel_2.json")
        list_tramps = Traps.create_traps_json("src/Files Json/nivel_2.json")

        while True:

            delta_ms = self.clock.tick(FPS)
            self.window.blit(background, background.get_rect())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        change_mode()
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                        self.start_time += pygame.time.get_ticks() - self.pause_start
            
            keys = pygame.key.get_pressed()

            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            text_surface = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, BLUE)
            text_rect = text_surface.get_rect(topleft=(10, 5))
            self.window.blit(text_surface, text_rect)

            for tramp in list_tramps:
                tramp.update(delta_ms)
                tramp.draw(self.window)

            for platform in list_platforms:
                platform.draw(self.window)

            for rewards in list_collectibles:
                rewards.update(delta_ms)
                rewards.draw(self.window)
            
            for enemy in list_enemy:
                enemy.update(delta_ms, list_platforms, list_player[0])            
                enemy.draw(self.window)
            
            for player in list_player:
                player.update(delta_ms, list_platforms, list_collectibles, list_enemy, list_tramps, keys)
                player.draw(self.window)
                player.draw_lives(self.window)

                self.score_level_2 = player.score
                
                if player.lives == 0 and player.rect.y > HEIGHT:
                    self.game_over_screen()

            score_text = f"Score: {self.score_level_1+self.score_level_2}"
            render_text = self.font.render(score_text, True, BLUE)
            self.window.blit(render_text, (1000, 5))
            
            if len(list_collectibles) == 0:
                self.level_three_screen()

            pygame.display.update() 


    def level_three_screen(self) -> None:
        """
        Pantalla del nivel 3 se instancias todos los objetos que intervendrán en el juego, se muestra el tiempo desde
        que se empezó el nivel la cantidad de vidas, y el score.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_level_3.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"sound_level_3.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        list_player = Player.create_player_json("src/Files Json/nivel_3.json")
        list_platforms = Platform.create_platform_json("src/Files Json/nivel_3.json")
        list_collectibles = Collectible.create_collectible_json("src/Files Json/nivel_3.json")
        list_enemy = Enemy.create_enemy_json("src/Files Json/nivel_3.json")
        list_tramps = Traps.create_traps_json("src/Files Json/nivel_3.json")
        
        while True:

            delta_ms = self.clock.tick(FPS)
            self.window.blit(background, background.get_rect())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        change_mode()
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                        self.start_time += pygame.time.get_ticks() - self.pause_start
            
            keys = pygame.key.get_pressed()

            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            text_surface = self.font.render(f"Tiempo: {minutes:02d}:{seconds:02d}", True, BLUE)
            text_rect = text_surface.get_rect(topleft=(10, 5))
            self.window.blit(text_surface, text_rect)

            for tramp in list_tramps:
                tramp.update(delta_ms)
                tramp.draw(self.window)

            for platform in list_platforms:
                platform.draw(self.window)

            for rewards in list_collectibles:
                rewards.update(delta_ms)
                rewards.draw(self.window)
            
            for enemy in list_enemy:
                enemy.update(delta_ms, list_platforms, list_player[0])            
                enemy.draw(self.window)
               
            for player in list_player:
                player.update(delta_ms, list_platforms, list_collectibles, list_enemy, list_tramps, keys)
                player.draw(self.window)
                player.draw_lives(self.window)

                self.score_level_3 = player.score
                
                if player.lives == 0 and player.rect.y > HEIGHT:
                    self.game_over_screen()

            score_text = f"Score: {self.score_level_3+self.score_level_2+self.score_level_1}"
            render_text = self.font.render(score_text, True, BLUE)
            self.window.blit(render_text, (1000, 5))
            
            if len(list_collectibles) == 0: 
                self.winner_screen()

            self.score_total = self.score_level_1 + self.score_level_2 + self.score_level_3
            
            pygame.display.update()   
        
        
    def pause_screen(self) -> None:
        """
        Pantalla de pausa, se accede presionando la tecla "esc", tiene botones para volver al menu principal, para silenciar
        la música de fondo del nivel, para volver activar el sonido y para reanudar el juego.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/window_pause.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        text_surface = self.font_pause.render("Pause", True, (BLACK))

        self.pause_start = pygame.time.get_ticks()
        paused = True
        
        while paused:

            self.clock.tick(FPS)

            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 7))
            self.window.blit(text_surface, text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.pause_screen_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.pause_screen_buttons[0]:
                                paused = False
                            if button == self.pause_screen_buttons[1]:
                                pygame.mixer.music.play()
                            if button == self.pause_screen_buttons[2]:
                                pygame.mixer.music.stop()
                            if button == self.pause_screen_buttons[3]:
                                self.main_screen()

            self.render(self.pause_screen_buttons, background)


    def game_over_screen(self) -> None:
        """
        Pantalla que se muestra si el player perdió sus 3 vidas.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_game_over.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"sound_game_over.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.screen_game_over_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.screen_game_over_buttons[0]:
                                self.level_one_screen()
                            if button == self.screen_game_over_buttons[1]:
                                self.main_screen()
                            
            self.render(self.screen_game_over_buttons, background)


    def winner_screen(self) -> None:
        """
        Pantalla que se muestra luego de ganar los 3 niveles y pide el nombre del usuario par aguardarlo junto
        con el tiempo que tardo en terminar el juego y los puntos que hizo durante todo el juego.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo_winner.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        pygame.mixer.music.load(PATH_SOUND+"winner.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

        username = ""
        input_rect = pygame.Rect(400, 570, 400, 50)
        
        color = self.color_passive

        while True:

            self.clock.tick(FPS)
            self.window.blit(background, background.get_rect())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        self.active = True
                    else:
                        self.active = False

                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    if event.key == pygame.K_RETURN:
                        self.upload_json(username, self.elapsed_time, self.score_total)
                        self.play_again()

            if self.active:
                color = self.color_active
            else:
                color = self.color_passive

            pygame.draw.rect(self.window, color, input_rect, 2)

            text_surface = self.font.render(username, True, WHITE)
            self.window.blit(text_surface, (input_rect.x + 5, input_rect.y-2))

            input_rect.w = max(400, text_surface.get_width()+9)

            pygame.display.update()

    
    def play_again(self) -> None:
        """
        Pantalla que se muestra luego de ingresar el nombre del usuario. Tiene botones para reiniciar el juego y para 
        volver al menu principal.
        """
        background = pygame.image.load(PATH_IMAGE + "Fondos/fondo.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.play_again_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button == self.play_again_buttons[0]:
                                self.level_one_screen()
                            if button == self.play_again_buttons[1]:
                                self.main_screen()
                            
            self.render(self.play_again_buttons, background)
            

    def upload_json(self, username:str, game_time:int, score:int) -> None:
        """
        Función para subir la información del ranking a un json, crea un diccionario con los datos, verifica si existe
        el archivo json, si no existe crea una lista vacía y agrega los datos a la lista, luego los ordena primero por
        score de forma descendente y luego por tiempo de forma ascendente luego reescribe el archivo json con los datos
        ordenados.

        Args:
            username (str): Nombre que ingresa el usuario.
            game_time (int): Tiempo que tardo el usuario en completar el nivel.
            score (int): Puntos totales que hizo el usuario durante el juego.
        """
        if(isinstance(username, str) and username and isinstance(game_time, int) and game_time and
           isinstance(score, int) and score):
            
            username = username.strip()
            
            minutes = game_time // 60
            seconds = game_time % 60
            game_time_str = f"{minutes:02d}:{seconds:02d}"

            data = {
                "Username": username,
                "Game_time": game_time_str,
                "Score": score
            }

            if os.path.exists("ranking.json"):
                with open("ranking.json", "r") as file:
                    ranking = [json.loads(line) for line in file]
            else:
                ranking = []

            ranking.append(data)

            ranking = sorted(ranking, key=lambda x: (-x["Score"], x["Game_time"]))

            with open("ranking.json", "w") as file:
                for record in ranking:
                    json.dump(record, file)
                    file.write("\n")


    def render(self, buttons:list, background:pygame.Surface) -> None:
        """
        Método que renderiza la imagen de fondo en la pantalla.

        Args:
            buttons (list): Lista de botones a recorrer para dibujar los botones en pantalla.
            background (pygame.Surface): Fondo de la pantalla.
        """
        if isinstance(buttons, list) and buttons and isinstance(background, pygame.Surface) and background:
            self.window.blit(background, background.get_rect())

            for button in buttons:
                button.draw(self.window)
                button.update()

            pygame.display.update()