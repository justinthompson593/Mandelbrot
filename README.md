# mandelbrot.py

### Computes the Mandelbrot Set

I made this script so that I could test pygame and get to know the ins and out
of the workflow. I also planned on doing something else with animation in the 
complex number plane, so I figured that this would be a good place to start. That,
and the [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) just beautiful. *Beauty will save the world*, right? Run 

`$ python mandelbrot.py`

in a terminal to play with the features. Note that it might take a long time to 
calculate if you're using a large window size. For faster results, try changing
the `num_x` and `num_y` variables in the source code to something smaller.

---

#### Keyboard Commands

| Key | Action |
|-----|--------|
| b | toggle set coloring (black or colormap-determined) |
| c | cycle through different colormaps |

#### Mouse Interaction 

To zoom in on a region, click on the upper-left-hand corner of the region and 
drag to the lower right corner of the region and release the mouse button. It may
take time to recalculate before refreshing. Note that the region may not be exactly
what you selected because the y-values (vertical) are changed to preserve the
aspect ratio of the complex plane with respect to the viewing window. It may take 
a *long* time to update, depending on how many pixels are in your window and how many
points in the window are in the Mandelbrot set (those take longer to iterate). When it does
finish, the new region being drawn will be printed on your terminal.

##### Note

This program is *not* capable of infinite zoom. You'll notice that as you zoom in the 
boundary isn't as sharp and detailed as it was when the set was first drawn. This is because
we're only using `float64` values in calculation, which are only accurate to about 15 decimal 
places. Beyond that, rounding error will affect the accuracy of the representation.
