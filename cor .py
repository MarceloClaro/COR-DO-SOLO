import os
from collections import Counter

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans


def rgb2hex(rgb):
    hex = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    return hex

PATH = './solo1.jpg'
WIDTH = 128
HEIGHT = 128
CLUSTERS = 6

image = Image.open(PATH)

image.size

print("Loaded {f} image. Size: {s:.2f} KB. Dimensions: ({d})".format(
    f=image.format, s=os.path.getsize(PATH) / 1024, d=image.size))


def calculate_new_size(image):
    if image.width >= image.height:
        wpercent = (WIDTH / float(image.width))
        hsize = int((float(image.height) * float(wpercent)))
        new_width, new_height = WIDTH, hsize
    else:
        hpercent = (HEIGHT / float(image.height))
        wsize = int((float(image.width) * float(hpercent)))
        new_width, new_height = wsize, HEIGHT
    return new_width, new_height


calculate_new_size(image)

new_width, new_height = calculate_new_size(image)

image.resize((new_width, new_height), Image.ANTIALIAS)

image = image.resize((new_width, new_height), Image.ANTIALIAS)

img_array = np.array(image)

img_vector = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))

model = KMeans(n_clusters=CLUSTERS)

labels = model.fit_predict(img_vector)

label_counts = Counter(labels)

total_count = sum(label_counts.values())

hex_colors = [
    rgb2hex(center) for center in model.cluster_centers_
]
hex_colors

list(zip(hex_colors, list(label_counts.values())))

plt.figure(figsize=(14, 8))
plt.subplot(221)
plt.imshow(image)
plt.axis('off')

plt.subplot(222)
plt.pie(label_counts.values(), labels=hex_colors, colors=[color / 255 for color in model.cluster_centers_],
        autopct='%1.1f%%',
        shadow=True, startangle=90)
plt.axis('equal')
plt.title('CORES DO SOLO')
plt.show()
