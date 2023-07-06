import pygame

class Assistant:
    """
    Clase auxiliar para manejar los sprite sheet.

    """

    @staticmethod
    def get_surface_sprite(path: str, columns: int, rows: int, flip=False, scale=1) -> list | None:
        """
        Método estático que genera coordenadas de una hoja de sprite, para manejar las animaciones.
        Calcula el ancho y alto dependiendo las columnas y las filas del sprite sheet.

        Args:
            path (str): La ruta donde se encuentra la hoja de sprite.
            columns (int): Cantidad de columnas que tiene el sprite.
            rows (int): Cantidad de filas que tiene el sprite.
            flip (bool, optional): Booleano que si se pasa en True voltea la imagen. Defaults to False
            scale (int or float optional): Tamaño al que se quiere escalar la imagen. Defaults to 1.

        Returns:
            list | None: Si la validación fue exitosa retorna la lista que en cada indice contendrá cada fotograma
            de la imagen, None en caso de no cumplirse la validación.
        """       
        if isinstance(path, str) and path and isinstance(columns, int) and columns and isinstance(rows, int) and rows:
            sprite_list = []

            image_surface = pygame.image.load(path)
            wide_frame = int(image_surface.get_width() / columns)
            high_frame = int(image_surface.get_height() / rows)
            wide_frame_scaling = int(wide_frame * scale)
            high_frame_scaling = int(high_frame * scale)

            for fila in range(rows):
                for columna in range(columns):
                    x = columna * wide_frame
                    y = fila * high_frame
                    frame_surface = image_surface.subsurface(x, y, wide_frame, high_frame)

                    if scale != 1:
                        frame_surface = pygame.transform.scale(frame_surface, (wide_frame_scaling, high_frame_scaling)).convert_alpha()
                    if flip:
                        frame_surface = pygame.transform.flip(frame_surface, True, False).convert_alpha()
                    
                    sprite_list.append(frame_surface)

            return sprite_list
        else:
            return None

