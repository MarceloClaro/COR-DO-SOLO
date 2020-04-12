from numpy import array as Array
from PIL import Image

def get_color_matrix(img):
    matrix = []
    for x in range(img.width):
        matrix.append([])
        for y in range(img.height):
            matrix[x].append(img.getpixel( (x, y) ))
    return matrix

def color_counter(img):
    img = Image.open(img)

    total = 0
    colors = {}
    matrix = get_color_matrix(img)
    for x in range(img.width):
        for rgb in matrix[x]:
            if rgb not in colors:
                colors[rgb] = 1
            else:
                colors[rgb] += 1
    return {
        'colors': colors,
        'total': img.width * img.height,
        'matrix': matrix
    }

if __name__ == '__main__':
    from sys import argv as args
    print(color_counter(args[1])['colors'])
