from collections import deque
class BFS:
    def __init__(self, maze, start, end, buttons):
        self.queue = deque([start])
        self.visited = set([start])
        self.maze = maze
        self.start = start
        self.buttons = buttons
        self.end = end
        self.parent = {}
    def step(self):
        while self.queue:
            r, c = self.queue.popleft()
            if (r, c) == self.end:
                break
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.maze.size and 0 <= nc < self.maze.size:
                    if self.maze.grid[nr][nc] != 1 and (nr, nc) not in self.visited:
                        self.queue.append((nr, nc))
                        self.visited.add((nr, nc))
                        self.parent[(nr, nc)] = (r, c)
                        self.buttons[nr][nc].base_color = (0, 0, 255)  # Change color to indicate visited
