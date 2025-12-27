import pygame
from collections import deque

# ----------------------------
# Initialize Pygame
# ----------------------------
pygame.init()
pygame.font.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
GRID_AREA = 600  # top 600px for grid
UI_HEIGHT = 100  # bottom bar

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

font = pygame.font.Font(
    "/Users/johanantony/Desktop/pathfinding-visualizer/Pathfinding-visualizer/block-blueprint-font/Blockblueprint-LV7z5.ttf",
    28
)

TITLE_FONT = pygame.font.Font(
    "/Users/johanantony/Desktop/pathfinding-visualizer/Pathfinding-visualizer/block-blueprint-font/Blockblueprint-LV7z5.ttf",
    36
)

# ----------------------------
# Button Class
# ----------------------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = (100, 100, 100)
        self.hover_color = (160, 160, 160)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.base_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)

        if self.text:
            text_surface = font.render(self.text, True, self.text_color)
            surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

# ----------------------------
# Text Input
# ----------------------------
class TextInput:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.text.isdigit():
                value = max(5, min(50, int(self.text)))
                self.active = False
                return value
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        text_surface = font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

# ----------------------------
# Maze
# ----------------------------
class Maze:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

# ----------------------------
# Grid Buttons
# ----------------------------
def create_grid(maze):
    cell_size = GRID_AREA // maze.size
    grid = []

    for r in range(maze.size):
        row = []
        for c in range(maze.size):
            x = c * cell_size
            y = r * cell_size
            btn = Button(x, y, cell_size, cell_size, "")
            btn.base_color = (74, 70, 70)
            btn.hover_color = (46, 44, 44)
            row.append(btn)
        grid.append(row)
    return grid

# ----------------------------
# algorithms
# ----------------------------



# ----------------------------
# UI Setup
# ----------------------------
start_button = Button(200, 350, 200, 50, "Get Started")
input_box = TextInput(200, 250, 200, 50)

wall_btn  = Button(30, 620, 120, 50, "Wall")
start_btn = Button(160, 620, 120, 50, "Start")
end_btn   = Button(290, 620, 120, 50, "End")
visualize_btn = Button(420, 620, 120, 50, "Visualize")
breadth_search_btn = Button(30, 620, 120, 50, "BFS")
depth_search_btn = Button(160, 620, 120, 50, "DFS")
A_search_btn = Button(290, 620, 120, 50, "A*")



# ----------------------------
# Main Loop
# ----------------------------
running = True
mode = "menu"
selected_tool = "wall"
maze = None
grid_buttons = None
start = None
end = None

while running:
    window.fill((74, 70, 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if start_btn.clicked(event):
            selected_tool = "start"

        # ---------- MENU ----------
        if mode == "menu":
            if start_button.clicked(event):
                input_box.active = True

            value = input_box.handle_event(event)
            if value:
                maze = Maze(value)
                grid_buttons = create_grid(maze)
                mode = "maze"
        # ---------- MAZE ----------
        elif mode == "maze":

            # ---- TOOL BUTTONS ----
            if wall_btn.clicked(event):
                selected_tool = "wall"

            if start_btn.clicked(event):
                selected_tool = "start"

            if end_btn.clicked(event):
                selected_tool = "end"
            
            if visualize_btn.clicked(event):
                mode = "visualizing"
                # Visualization logic would go here

            # ---- GRID INTERACTION ----
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for r, row in enumerate(grid_buttons):
                    for c, btn in enumerate(row):
                        if btn.rect.collidepoint(event.pos):

                            # WALL
                            if selected_tool == "wall":
                                if btn.base_color == (0, 255, 0) or btn.base_color == (255, 0, 0):
                                    pass
                                elif btn.base_color == (26, 23, 23):
                                    maze[r][c] = 1
                                    btn.base_color = (74, 70, 70)
                                    btn.hover_color = (46, 44, 44)
                                else:
                                    maze[r][c] = 0
                                    btn.base_color = (26, 23, 23)
                                    btn.hover_color = (15, 15, 15)

                            # START (only one)
                            elif selected_tool == "start":
                                for r, row in enumerate(grid_buttons):
                                    for c, btn in enumerate(row):
                                        if btn.base_color == (0, 255, 0):
                                            maze[r][c] = 0
                                            btn.base_color = (74, 70, 70)
                                            btn.hover_color = (46, 44, 44)
                                start = (r, c)
                                maze[r][c] = 2
                                btn.base_color = (0, 255, 0)
                                btn.hover_color = (0, 200, 0)

                            # END (only one)
                            elif selected_tool == "end":
                                for r in grid_buttons:
                                    for b in r:
                                        if b.base_color == (255, 0, 0):
                                            maze[r][c] = 0
                                            b.base_color = (74, 70, 70)
                                            b.hover_color = (46, 44, 44)
                                end = (r, c)
                                maze[r][c] = 3
                                btn.base_color = (255, 0, 0)
                                btn.hover_color = (200, 0, 0)


    # ---------- DRAW ----------
    if mode == "menu":
        title = TITLE_FONT.render("Pathfinding Visualizer", True, (255, 255, 255))
        window.blit(title, (80, 120))

        if input_box.active:
            input_box.draw(window)
        else:
            start_button.draw(window)

    elif mode == "maze":
        for row in grid_buttons:
            for btn in row:
                btn.draw(window)

        pygame.draw.rect(window, (40, 40, 40), (0, GRID_AREA, WINDOW_WIDTH, UI_HEIGHT))
        wall_btn.draw(window)
        start_btn.draw(window)
        end_btn.draw(window)
        visualize_btn.draw(window)

    elif mode == "visualizing":
        for row in grid_buttons:
            for btn in row:
                btn.draw(window)
        if breadth_search_btn.clicked(event):
            pass  # BFS visualization logic would go here
        if depth_search_btn.clicked(event):
            pass  # DFS visualization logic would go here
        if A_search_btn.clicked(event):
            pass  # A* visualization logic would go here
        pygame.draw.rect(window, (40, 40, 40), (0, GRID_AREA, WINDOW_WIDTH, UI_HEIGHT))
        breadth_search_btn.draw(window)
        depth_search_btn.draw(window)
        A_search_btn.draw(window)

    pygame.display.flip()

pygame.quit()

