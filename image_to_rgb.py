from PIL import Image

def get_color_matrix(img):
    for x in range(img.width):
        for y in range(img.height):
            yield img.getpixel( (x, y) )

if __name__ == '__main__':
    from sys import argv as args

    img = Image.open(args[1])

    colors = {}
    for rgb in get_color_matrix(img):
        if rgb not in colors:
            colors[rgb] = 1
        else:
            colors[rgb] += 1

    total = len(colors)
    for color in colors:
        print(f'{color} -> {(colors[color]*100)/total}%')
