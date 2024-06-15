from PIL import Image
from typing import List


def mirror(raw: List[List[List[int]]])-> None:
    """
    Assume raw is image data. Modifies raw by reversing all the rows
    of the data.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> mirror(raw)
    >>> raw
    [[[255, 255, 255], [0, 0, 0], [233, 100, 115]],
     [[255, 255, 255], [1, 9, 0], [199, 201, 116]]]
    """
    for row in raw:
        row.reverse()



def grey(raw: List[List[List[int]]])-> None:
    """
    Assume raw is image data. Modifies raw "averaging out" each
    pixel of raw. Specifically, for each pixel it totals the RGB
    values, integer divides by three, and sets the all RGB values
    equal to this new value.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 255]],
               [[199, 201, 116], [1, 9, 0], [255, 255, 255]]]
    >>> grey(raw)
    >>> raw
    [[[149, 149, 149], [0, 0, 0], [255, 255, 255]],
     [[172, 172, 172], [3, 3, 3], [255, 255, 255]]]
    """
    for row in raw:
        for pixel in row:
            avg = sum(pixel) // 3
            for i in range(3):
                pixel[i] = avg



def invert(raw: List[List[List[int]]])-> None:
    """
    Assume raw is image data. Modifies raw inverting each pixel.
    To invert a pixel, you swap all the max values, with all the
    minimum values. 

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]]]
    >>> invert(raw)
    >>> raw
    [[[100, 233, 115], [0, 0, 0], [0, 0, 255]],
     [[199, 116, 201], [1, 0, 9], [100, 255, 255]]]
    """
    for row in raw:
        for pixel in row:
            minimum = min(pixel)
            maximum = max(pixel)
            for i in range(3):
                if pixel[i] == minimum:
                    pixel[i] = maximum
                elif pixel[i] == maximum:
                    pixel[i] = minimum



def merge(raw1: List[List[List[int]]], raw2: List[List[List[int]]])-> List[List[List[int]]]:
    """
    Merges raw1 and raw2 into new raw image data and returns it.
    It merges them using the following rule/procedure.
    1) The new raw image data has height equal to the max height of raw1 and raw2
    2) The new raw image data has width equal to the max width of raw1 and raw2
    3) The pixel data at cell (i,j) in the new raw image data will be (in this order):
       3.1) a black pixel [255, 255, 255], if there is no pixel data in raw1 or raw2
       at cell (i,j)
       3.2) raw1[i][j] if there is no pixel data at raw2[i][j]
       3.3) raw2[i][j] if there is no pixel data at raw1[i][j]
       3.4) raw1[i][j] if i is even
       3.5) raw2[i][j] if i is odd
    """
    """
        >>> raw1 size = [1][4]
        >>> raw2 size = [3][1]
        >>> merge size is [3][4]
        
        merge = [[[raw1[0,0], raw1[0,1], raw1[0,2], raw1[0,3], raw1[0,4]],
                 [[raw2[1,0], blackPixel, blackPixel, blackPixel, blackPixel],
                 [[raw2[2,0], blackPixel, blackPixel, blackPixel, blackPixel]]
                 
        i.e.
        raw1 = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [1,2,3]]]
        raw2 = [[[199, 201, 116]],
                [[1, 9, 0]],
                [[255, 100, 100]]]
        merge = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [1,2,3]],
                 [[1, 9, 0], [255 ,255 ,255], [255 ,255 ,255], [255 ,255 ,255]],
                 [[255, 100, 100], [255 ,255 ,255], [255 ,255 ,255], [255 ,255 ,255]]]
                 
        >>> raw1 size = [2][4]
        >>> raw2 size = [3][3]
        >>> merge size is [3][4]
        
        i.e.
        raw1 = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [1,2,3]],
                [[200, 200, 200], [1, 9, 0], [255, 100, 100], [99, 99, 0]]]
                
        raw2 = [[[199, 201, 116], [2, 3, 4], [4, 5, 5]],
                [[1, 9, 0], [5, 6, 6], [7, 7, 8]],
                [[255, 100, 100], [8, 9, 10], [11, 12, 12]]]
                
        merge = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [1,2,3]],
                 [[1, 9, 0], [5, 6, 6,], [7, 7, 8], [99, 99, 0]],
                 [[255, 100, 100], [8 ,9 ,10], [11 ,12 , 12], [255 ,255 ,255]]]
    """
    max_height = max(len(raw1), len(raw2))
    max_width = max(len(raw1[0]), len(raw2[0]))
    merged_raw = []
    
    for i in range(max_height):
        row = []
        if i % 2 == 0:
            for j in range(max_width):
                try:
                    pixel = raw1[i][j]
                except:
                    try:
                        pixel = raw2[i][j]
                    except:
                        pixel = [255,255,255]
                row.append(pixel)
        else:
            for j in range(max_width):
                try:
                    pixel = raw2[i][j]
                except:
                    try:
                        pixel = raw1[i][j]
                    except:
                        pixel = [255,255,255]
                row.append(pixel)
        merged_raw.append(row)
        
    return merged_raw


def compress(raw: List[List[List[int]]])-> List[List[List[int]]]:
    """
    Compresses raw by going through the pixels and combining a pixel with
    the ones directly to the right, below and diagonally to the lower right.
    For each RGB values it takes the average of these four pixels using integer
    division. If is is a pixel on the "edge" of the image, it only takes the
    relevant pixels to average across.

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0], [3, 6, 7]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[200, 200, 200], [1, 9, 0], [255, 100, 100], [99, 99, 0]],
               [[50, 100, 150], [1, 9, 0], [211, 5, 22], [199, 0, 10]]]
    >>> compress(raw)
    >>> compressed_raw
    [[[108, 77, 57], [153, 115, 26]],
     [[63, 79, 87], [191, 51, 33]]]

    >>> raw = [[[233, 100, 115], [0, 0, 0], [255, 255, 0]],
               [[199, 201, 116], [1, 9, 0], [255, 100, 100]],
               [[123, 233, 151], [111, 99, 10], [0, 1, 1]]]
    >>> compress(raw)
    >>> compressed_raw
    [[[108, 77, 57], [255, 177, 50]],
     [[117, 166, 80], [0, 1, 1]]]
    """
    compressed_raw = []
    cols = len(raw)
    rows = len(raw[0])
    
    for i in range(0, cols, 2):
        new_row = []
        
        for j in range(0, rows, 2):
            pixels = []
            red = 0
            green = 0
            blue = 0
            
            for x in range(2):
                for y in range(2):
                    if i + x < cols and j + y < rows:
                        red += raw[i + x][j + y][0]
                        green += raw[i + x][j + y][1]
                        blue += raw[i + x][j + y][2]
                        
                        pixels.append(raw[i + x][j + y])
            
            avg_red = red // len(pixels)
            avg_green = green // len(pixels)
            avg_blue = blue // len(pixels)
            
            new_row.append([avg_red, avg_green, avg_blue])
        
        compressed_raw.append(new_row)
    return compressed_raw



"""
**********************************************************

Do not worry about the code below. However, if you wish,
you can us it to read in images, modify the data, and save
new images.

**********************************************************
"""

def get_raw_image(name: str)-> List[List[List[int]]]:
    
    image = Image.open(name)
    num_rows = image.height
    num_columns = image.width
    pixels = image.getdata()
    new_data = []
    
    for i in range(num_rows):
        new_row = []
        for j in range(num_columns):
            new_pixel = list(pixels[i*num_columns + j])
            new_row.append(new_pixel)
        new_data.append(new_row)

    image.close()
    return new_data


def image_from_raw(raw: List[List[List[int]]], name: str)->None:
    image = Image.new("RGB", (len(raw[0]),len(raw)))
    pixels = []
    for row in raw:
        for pixel in row:
            pixels.append(tuple(pixel))
    image.putdata(pixels)
    image.save(name)
                      
                      




    
