from pygame_hide import pygame
import sys

# total number of iterations, i.e. number of frames in animation
STEPS = 4000  # 10000

# size of the screen in pixels
SCREEN_SIZE = (1920, 1080)

# Wolfram's rule 30
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

# RGB colors for states 0 (white) and 1 (black)
COLORS = [(255, 255, 255), (0, 0, 0)]

# whether to write each frame to disk
RECORDING = sys.argv[1] == "record" if len(sys.argv) > 1 else False

# read initial state from file, created by forward.py
current = [int(s) for s in open("state.txt").read()]

# number of cells in the state array
size = len(current)

# history of states, used for horizontal scrolling
history: list[list[int]] = []

# offset of screen relative to state, allows larger state and scrolling
offset = [(size - SCREEN_SIZE[0]) // 2, 0]

# current scroll direction
scroll = (0, 0)

# set up Pygame for drawing to screen
if RECORDING:
    surface = pygame.Surface(SCREEN_SIZE)
else:
    pygame.init()
    surface = pygame.display.set_mode(SCREEN_SIZE)
surface.fill(COLORS[0])

# progress line by line, starting at the bottom
for y in range(STEPS):
    # once the screen is almost fully filled with the reverse
    if y >= size // 2 + SCREEN_SIZE[0] // 2 + SCREEN_SIZE[1] * 9 // 10:
        scroll = (1, 1)
    # once we state 0 at the center
    elif y >= size // 2 + SCREEN_SIZE[1] // 2:
        scroll = (2, 1)
    # once we reach the top, start scrolling
    elif y >= SCREEN_SIZE[1]:
        scroll = (0, 1)
    # scroll the screen
    surface.scroll(scroll[0], scroll[1])
    offset[0] -= scroll[0]
    offset[1] -= scroll[1]
    # draw missing pixel due to scroll
    for yy in range(1, SCREEN_SIZE[1]):
        for x in range(0, scroll[0]):
            surface.set_at((x, yy), COLORS[history[-yy][x + y - yy + offset[0]]])
    # draw the current state to the screen and store in history
    for x in range(SCREEN_SIZE[0]):
        surface.set_at(
            (x, SCREEN_SIZE[1] - 1 - y - offset[1]),
            COLORS[current[x + y + offset[0]] if x + y + offset[0] < size else 0],
        )
    history.append(current.copy())
    if len(history) > SCREEN_SIZE[1]:
        history.pop(0)
    # calculate the next state
    current[size - 1] = RULES[(current[size - 1], 0, 0)]
    current[size - 2] = RULES[(current[size - 2], current[size - 1], 0)]
    for x in range(size - 3, -1, -1):
        current[x] = RULES[(current[x], current[x + 1], current[x + 2])]
    if RECORDING:
        # write the frame to stdout
        sys.stdout.buffer.write(surface.get_view("0").raw)
    else:
        # update the screen, indicate progress
        pygame.display.update()
        pygame.display.set_caption(f"Rule 30 [{100 * y / STEPS:.0f}%]")
    # handle events
    pause = False
    while True and not RECORDING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            # press space to pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
        if not pause:
            break
