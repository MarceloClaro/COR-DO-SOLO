from PIL import Image

def get_color_matrix(img):
    color_list = []
    for x in range(img.width):
        color_list.append([])
        for y in range(img.height):
            color_list[x].append(img.getpixel( (x, y) ))

    return color_list

if __name__ == '__main__':
    from sys import argv as args

    img = Image.open(args[1])

    history = {}
    color_matriz = get_color_matrix(img)
    for x in range(img.width):
        for y in range(img.height):
            for rgb in color_matriz[x][y]:
                if rgb not in history:
                    history[rgb] = 1
                else:
                    history[rgb] += 1

