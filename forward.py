import pygame
import sys

# total number of iterations, i.e. number of frames in animation
STEPS = 2000  # 10000

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
RECORDING = False

# number of cells in the state array
size = STEPS + SCREEN_SIZE[0] // 2

# state array, initialized to all zeros
current = [0] * size

# next state, used as a temporary buffer
next = [0] * size

# initial state with a single black cell in the middle
current[size // 2] = 1

# offset of screen relative to state, allows larger state and scrolling
offset = [(size - SCREEN_SIZE[0]) // 2, 0]

# set up Pygame for drawing to screen
pygame.init()
pygame.display.set_caption("Rule 30")
surface = pygame.display.set_mode(SCREEN_SIZE)
surface.fill(COLORS[0])

# progress line by line, starting at the top
for y in range(STEPS):
    # once we reach the bottom, start scrolling
    if y >= SCREEN_SIZE[1]:
        surface.scroll(0, -1)
        offset[1] -= 1
    # draw the current state to the screen
    for x in range(SCREEN_SIZE[0]):
        surface.set_at((x, y + offset[1]), COLORS[current[(x + offset[0]) % size]])
    # store the last accurate state, to be used by reverse.py
    if y == size // 2 - 2:  # minus width of initial state + 1
        open("state.txt", "w").write("".join(str(x) for x in current))
    # calculate the next state
    for x in range(0, size):
        next[x] = RULES[(current[x - 1], current[x], current[(x + 1) % size])]
    # apply next state by flipping buffers
    current, next = next, current
    # update the screen, indicate progress
    pygame.display.update()
    pygame.display.set_caption(f"Rule 30 [{100 * y / STEPS:.0f}%]")
    # write the frame to disk if recording
    if RECORDING:
        pygame.image.save(surface, f"recording/forward/{y}.png")
    # handle events
    pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # press space to pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
        if not pause:
            break
