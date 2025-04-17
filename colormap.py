import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# The original method came from https://stackoverflow.com/questions/26108436/how-can-i-get-the-matplotlib-rgb-color-given-the-colormap-name-boundrynorm-an

class ColorMap:
    docstring = """
colormap.py

ColorMap

Easy access to named matplotlib colormaps. Designed to easily switch between colormaps
during looped applications such as those using OpenGL or pygame.

NOTE: 

    Other versions of this class do not automatically have the attribute `colormap_array`.
    In certain applications, it wasn't desirable to populate an array with thousands
    of values and have it just sitting there when a colormap (r,g,b) or (r,g,b,a) 
    value can be accessed with one of the `get_rgbX_Y()` methods. Many tests were 
    performed and we found that calling, say, `get_rgb_u8(x)` was actually (marginally) 
    quicker than calling `colormap_array[i]` to get the same data. However, in 
    mandelbrot.py calling `get_rgb_u8()` to color every pixel caused the program to 
    slow to a halt whereas calling `cmap.colormap_array[]` actually works.

USAGE:

    cmap = ColorMap([min_val], [max_val], [cmap_name], [num_colors], [array_type])
        min_val:    (default 0) Maps this value to the lowest colormap color
        max_val:    (default 255) Maps this value to the highest colormap color
        cmap_name:  (default 'viridis') [string] One of the colormap names 
                    cmap.names_all is an array with all the valid names
        num_colors: (default 256) Determines the length of cmap.colormap_array, an
                    array of (r,g,b) tuples where cmap.colomap_array[0] corresponds
                    to the min_val/lowest color and cmap.colomap_array[num_colors-1]
                    corresponds to the max_val/highest color in the colomap
        array_type: (default 'rgb_u8') [string] One of the following values: 
                    'rgb_u8'  - For colors in the form (r, g, b) where r,g, and b are
                                unsigned integers with values in [0, 255]
                    'rgba_u8' - For colors in the form (r, g, b, a) where r,g, and b are
                                unsigned integers with values in [0, 255] and a is an 
                                np.float64 in [0.0, 1.0]
                    'rgb_f'   - For colors in the form (r, g, b) where r,g, and b are
                                np.float64s with values in [0.0, 1.0]
                    'rgba_f'  - For colors in the form (r, g, b, a) where r,g,b, and a are
                                np.float64s with values in [0.0, 1.0]
                    This parameter is used to fill cmap.colormap_array
    
    cmap.cycle_colormap() 
        Cycles cmap.cmap_name through one of these values:
        ['viridis', 'plasma', 'magma', 'inferno', 'cividis', 'spring', 'summer', 'autumn', 
         'winter', 'hot', 'twilight']
        It does NOT cycle through cmap.names_all, as that would take forever. If you'd like to
        cycle through different values, add them to or remove them from 
            self.names_to_cycle
        defined in __init__ below. Any of the names in cmap.names_all can be used to set
        a new colormap name via `cmap.set_colormap_name('your_favorite_name')`
    
    r, g, b = cmap.get_rgb_f(some_scalar_value)
        When given some_scalar_value (with min_val <= some_scalar_value <= max_val) the
        corresponding colormap value is accessed and returned as an (r, g, b) tuple
        of np.float64s.
    
    r, g, b, a = cmap.colormap_array[some_int]
        If the `array_type` is 'rgba_u8' or 'rgba_f' then this will assign r,g, and b to be
        unisgned integers or floats, respectively, of the colormap value along with a as an
        np.float64, provided that we have 0 <= some_int < `cmap.num_colors`. If the 
        `array_type` is 'rgb_u8' or 'rgb_f', this will give you a ValueError because the 
        array cmap.colormap_array is an array of (r,g,b) tuples, not (r,g,b,a). 
    
    r, g, b = cmap.colormap_array[some_int]
        If the `array_type` is 'rgb_u8' or 'rgb_f' then this will assign r,g, and b to be
        unisgned integers or floats, respectively, of the colormap value, provided that we 
        have 0 <= some_int < `cmap.num_colors`. If the `array_type` is 'rgba_u8' or 'rgba_f', 
        this will give you a ValueError because the array cmap.colormap_array is an array of 
        (r,g,b,a) tuples, not (r,g,b).  
    
"""
    def __init__(self, min_val=0, max_val=255, cmap_name='viridis', num_colors=256, array_type='rgb_u8'):
        self.names_all = plt.colormaps()
        self.names_to_cycle = ['viridis', 'plasma', 'magma', 'inferno', 'cividis', 'spring',
        'summer', 'autumn', 'winter', 'hot', 'twilight']
        self.current_cycle_number = 0
        self.cmap_name = cmap_name
        self.min_value = min_val
        self.max_value = max_val
        self.number_colors = num_colors
        self.colormap_array = []
        self.array_type = array_type
        self.initialize()


    def initialize(self):
        self.cmap = plt.get_cmap(self.cmap_name)
        self.norm = mpl.colors.Normalize(vmin=self.min_value, vmax=self.max_value)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)
        # In other versions of the same class, the following is removed, but 
        # it made sense to use in mandelbrot.py. See NOTE in docstring.
        vals = np.linspace(self.min_value, self.max_value, self.number_colors)
        self.colormap_array = []
        for v in vals:
            if self.array_type == 'rgb_u8':
                self.colormap_array.append(self.get_rgb_u8(v))
            elif self.array_type == 'rgba_u8':
                self.colormap_array.append(self.get_rgba_u8(v))
            elif self.array_type == 'rgb_f':
                self.colormap_array.append(self.get_rgb_f(v))
            elif self.array_type == 'rgba_f':
                self.colormap_array.append(self.get_rgba_f(v))

    def cycle_colormap(self):
        self.current_cycle_number += 1
        self.current_cycle_number %= len(self.names_to_cycle)
        self.cmap_name = self.names_to_cycle[self.current_cycle_number]
        self.initialize()

    def set_min_max_vals(self, min_val, max_val):
        self.min_value = min_val
        self.max_value = max_val
        self.initialize()

    def set_colormap_name(self, name):
        self.cmap_name = name
        self.initialize()

    def set_array_type(self, ar_type):
        self.array_type = ar_type
        self.initialize()

    def set_number_colors(self, num_cols):
        self.number_colors = num_cols
        self.initialize()

    def get_rgb_u8(self, val):
        c = self.scalarMap.to_rgba(val)
        # c = (r, g, b, a) each a float in [0, 1]
        # convert to ints in [0, 255]
        red = round(255*c[0])
        green = round(255*c[1])
        blue = round(255*c[2])
        return (red, green, blue)

    def get_rgba_u8(self, val):
        c = self.scalarMap.to_rgba(val)
        # c = (r, g, b, a) each a float in [0, 1]
        # convert to ints in [0, 255]
        red = round(255*c[0])
        green = round(255*c[1])
        blue = round(255*c[2])
        return (red, green, blue, c[3])

    def get_rgb_f(self, val):
        c = self.scalarMap.to_rgba(val)
        return (c[0], c[1], c[2])

    def get_rgba_f(self, val):
        return self.scalarMap.to_rgba(val)
