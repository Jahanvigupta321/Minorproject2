from PIL import Image
import random
import os
def nshares(img,number_of_shares):
    # Assuming no is the number of shares you want to generate
    # Define the total number of pixels in the image
    no =int(number_of_shares)
    total_pix = img.size[0] * img.size[1]

    # Initialize a 3D list to store the shares
    n_share = [[[0, 0, 0] for _ in range(total_pix)] for _ in range(no)]
    folder_name = "images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    # Divide the encrypted image into n shares
    for i in range(total_pix):
        a = list(range(no))
        size = no
        for h in range(no):
            r = random.choice(a)
            ind = a.index(r)
            a[ind] = a[size - 1]
            n_share[r][i] = img.getdata()[i]

    # Save each share as an image
    for i in range(no):
        im = Image.new("RGB", img.size)
        pix = im.load()
        name = f"{folder_name}/share_{i+1}.png"
        index = 0
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                pix[x, y] = tuple(n_share[i][index])
                index += 1
        im.show()
        im.save(name)