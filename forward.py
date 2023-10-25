import pygame
import sys

STEPS = 4000  # 10000
SCREEN_SIZE = (1920, 1080)
SIZE = STEPS + SCREEN_SIZE[0] // 2
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

current = [0] * SIZE
next = [0] * SIZE
current[SIZE // 2] = 1
offset = [(SCREEN_SIZE[0] - SIZE) // 2, 0]

pygame.init()
pygame.display.set_caption("Rule 30")
surface = pygame.display.set_mode(SCREEN_SIZE)
surface.fill(COLORS[0])

for y in range(STEPS):
    if y >= SCREEN_SIZE[1]:
        surface.scroll(0, -1)
        offset[1] += 1
    for x in range(SCREEN_SIZE[0]):
        surface.set_at((x, y - offset[1]), COLORS[current[x - offset[0]]])
    for x in range(SIZE):
        if x == 0:
            next[x] = RULES[(0, current[x], current[x + 1])]
        elif x == SIZE - 1:
            next[x] = RULES[(current[x - 1], current[x], 0)]
        else:
            next[x] = RULES[(current[x - 1], current[x], current[x + 1])]
    current, next = next, current
    pygame.display.update()
    pygame.display.set_caption(f"Rule 30 [{100 * y / STEPS:.0f}%]")
    if RECORDING:
        pygame.image.save(surface, f"recording/forward/{y}.png")
    if y == SIZE // 2 - 2:
        open("state.txt", "w").write("".join(str(x) for x in current))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
