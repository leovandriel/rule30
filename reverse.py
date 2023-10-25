import pygame
import sys

STEPS = 4000  # 10000
SCREEN_SIZE = (1920, 1080)
RULES = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}
COLORS = [(255, 255, 255), (0, 0, 0)]
RECORDING = False

current = [int(s) for s in open("state.txt").read()]
size = len(current)
history: list[list[int]] = []
offset = [(SCREEN_SIZE[0] - size) // 2, 0]
scroll = (0, 0)

pygame.init()
pygame.display.set_caption("Rule 30")
surface = pygame.display.set_mode(SCREEN_SIZE)
surface.fill(COLORS[0])

for y in range(STEPS):
    if y >= size // 2 + SCREEN_SIZE[0] // 2 + SCREEN_SIZE[1] * 9 // 10:
        scroll = (1, 1)
    elif y >= size // 2 + SCREEN_SIZE[1] // 2:
        scroll = (2, 1)
    elif y >= SCREEN_SIZE[1]:
        scroll = (0, 1)
    surface.scroll(scroll[0], scroll[1])
    offset[0] += scroll[0]
    offset[1] += scroll[1]
    for yy in range(1, SCREEN_SIZE[1]):
        for x in range(0, scroll[0]):
            surface.set_at((x, yy), COLORS[history[-yy][x + y - offset[0] - yy - 1]])
    for x in range(SCREEN_SIZE[0]):
        surface.set_at(
            (x, SCREEN_SIZE[1] - 1 - y + offset[1]),
            COLORS[current[x + y - offset[0]] if x + y - offset[0] < size else 0],
        )
    history.append(current.copy())
    for x in range(size - 1, -1, -1):
        if x == size - 1:
            current[x] = RULES[(current[x], 0, 0)]
        elif x == size - 2:
            current[x] = RULES[(current[x], current[x + 1], 0)]
        else:
            current[x] = RULES[(current[x], current[x + 1], current[x + 2])]
    pygame.display.update()
    pygame.display.set_caption(f"Rule 30 [{100 * y / STEPS:.0f}%]")
    if RECORDING:
        pygame.image.save(surface, f"recording/reverse/{y}.png")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
