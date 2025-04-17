import pygame
import numpy as np
from colormap import ColorMap

"""
mandelbrot.py

Computes the Mandelbrot Set.

I made this script so that I could test pygame and get to know the ins and out
of the workflow. I also planned on doing something else with animation in the 
complex number plane, so I figured that this would be a good place to start. That
and it's just beautiful. Beauty will save the world, right?

Run 
      `$ python mandelbrot.py`

in a terminal to play with the features. Note that it might take a long time to 
calculate if you're using a large window size. For faster results, try changing
the num_x and num_y variables below to something smaller.

KEYBOARD COMMANDS:
    b   -   toggle set coloring (black or colormap-determined)
    c   -   cycle through different colormaps 

MOUSE INTERACTION:
    To zoom in on a region, click on the upper-left-hand corner of the region and 
    drag to the lower right corner of the region and release the mouse button. It may
    take time to recalculate before refreshing. Note that the region may not be exactly
    what you selected because the y-values (vertical) are changed to preserve the
    aspect ratio of the complex plane with respect to the viewing window.
"""

pygame.init()

# Window size
num_x = 1280        # width in pixels
num_y = 800         # height in pixels
window = pygame.display.set_mode((num_x, num_y))
pygame.display.set_caption("Mandelbrot Set")

# Complex plane bounds
real_min = -2.0     # lower horizontal bound
real_max = 1.0      # upper horizontal bound

# The upper and lower bounds are set to keep the window
# aspect ratio preserved. It will center the real (or x)
# axis in the center of the screen.
imag_max = num_y *(real_max - real_min) / (2.0 * num_x)
imag_min = -imag_max

# Values used for plotting points on complex plane
real_values = np.linspace(real_min, real_max, num_x)
imag_values = np.linspace(imag_max, imag_min, num_y)

# Used for coloring points
cmap = ColorMap(0, 255, 'viridis')

# Used to toggle whether the set is colored black, 
# or the final color in the colormap 
set_black = False

# This can be changed by initializing/changing cmap 
# cmap.num_colors defaults to 256
max_itr = cmap.number_colors

# Used to store number of iterations for each point 
px_arr = np.zeros((num_x,num_y))


# calculate_mandelbrot()
#
# If    z   =  x + i*y
# then  z^2 = (x + i*y)^2 
#           = x^2 + 2i*x*y + i^2*y^2
#           = (x^2 - y^2) + i*(2x*y)
#
# If we want to know if some constant, cz = cx + i*cy, is in the set
# or not, we have to compute
#
#  z^2 + cz = (x + i*y)^2 + cx + i*cy
#           = x^2 + 2i*x*y + i^2*y^2 + cx + i*cy
#           = (x^2 - y^2 + cx) + i*(2x*y + cy)
#
# and iterate over and over to see if it blows up (which it will if the
# magnitude, X^2 + Y^2, gets up to or above 4). If it does, then it's
# NOT in the set. So we'll keep track of how many iterations it takes 
# for it to get up to that threshold. The fewer iterations it takes, the
# faster it blows up. That's what we want to color: the rate at which a given
# constant blow up upon iteration of z <--> z^2 + c. If we've iterated 
# 'max_itr' times and it's still smaller than 4, we'll say it's in the set.
#
# When we iterate, we put the (z^2+cz)^2 = (x^2 - y^2 + cx) + i*(2x*y + cy)
# back into our new z = x + i*y. Thus, the new x component is the real part 
#
# x = x*x - y*y + cx
#
# and the new y is the imaginary
#
# y = 2*x*y + cy
#
def calculate_mandelbrot():
    for i in range(len(real_values)):
        for j in range(len(imag_values)):
            # At the i,jth pixel, get the corresponding complex number cz = cz + i*cy
            cx = real_values[i]
            cy = imag_values[j]
            itr = 0
            x = 0
            y = 0
            while itr < max_itr-1 and x*x + y*y <= 4:
                # This loop stops when the magnitude x^2+y^2 gets too big,
                # or we reach max_itr, the maximum number of iterations
                itr += 1
                newx = x*x - y*y + cx  # Use "newx" so we don't overwrite the old x value needed
                y = 2*x*y + cy         # <--- here.
                x = newx               # Now we can assign it to "x" because y is assigned
            px_arr[i,j] = itr # record the number of iterations it took for the loop to stop


# Call it here so it's ready to draw below
calculate_mandelbrot()

# Used to recalculate bounds to zoom in
mouse_down_x = 0
mouse_down_y = 0
mouse_up_x = 0
mouse_up_y = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the pixel position of the mouse when clicked down
            pos=pygame.mouse.get_pos()
            mouse_down_x = pos[0]
            mouse_down_y = pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            # After dragging to a new spot, get pixel position when
            # button is let go
            pos=event.pos
            mouse_up_x = pos[0]
            mouse_up_y = pos[1]
            # CAREFUL! Here we assume that a box is drawn from top
            # left to bottom right. The result is where we zoom in.
            real_min = real_values[mouse_down_x]
            real_max = real_values[mouse_up_x]
            imag_max = imag_values[mouse_down_y]
            imag_min = imag_max - num_y*(real_max - real_min)/num_x
            real_values = np.linspace(real_min, real_max, num_x)
            imag_values = np.linspace(imag_max, imag_min, num_y)
            print("recalculating...")
            calculate_mandelbrot()
            print("mouse_down_x:", mouse_down_x, "   mouse_down_y:", mouse_down_y)
            print("mouse_up_x:", mouse_up_x, "   mouse_up_y:", mouse_up_y)
            print("Re = [", real_min, ",", real_max, "]")
            print("Im = [", imag_min, ",", imag_max, "]")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:                     # press 'c' key to cycle through 
                cmap.cycle_colormap()                       # different color maps
                if set_black:
                    cmap.colormap_array[cmap.number_colors - 1] = (0, 0, 0)
                print("Colormap:", cmap.cmap_name)
            if event.key == pygame.K_b:                     # press 'b' key to toggle whether
                set_black = not set_black                   # the set is black, or determined by the colormap
                if set_black:
                    cmap.colormap_array[cmap.number_colors - 1] = (0, 0, 0)
                else:
                    cmap.colormap_array[cmap.number_colors - 1] = cmap.get_rgb_u8(cmap.max_value)
            if event.key == pygame.K_ESCAPE:
                run = False


    window.fill(0)

    rect = pygame.Rect(window.get_rect().center, (0, 0)).inflate(*([min(window.get_size())//2]*2))

    # This is the container for actual (r,g,b) pixel values, derived from values
    # in px_arr. 
    pixel_array = pygame.PixelArray(window)

    for i in range(len(real_values)):
        for j in range(len(imag_values)):
            # px_arr is filled with the number of iterations for each point in the image
            # for the i,jth pixel, find how many iterations it took (px_arr[i,j]) and pass
            # that into colormap_array, which will return a (r,g,b) pixel value, which we
            # assign to the i,jth pixel in pixel_array.
            pixel_array[i,j] = cmap.colormap_array[int(px_arr[i,j])]


    # Now it will be drawn to the screen
    pixel_array.close()

    pygame.display.flip()

pygame.quit()
exit()

