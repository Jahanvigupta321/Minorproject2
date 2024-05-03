from PIL import Image
import random

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime():
    while True:
        num = random.randint(100, 1000)  # Adjust range as per your requirements
        if is_prime(num):
            return num
        

def get_e(p, q, fn):
    e = 1
    for i in range(2, fn):
        if gcd(fn, i) == 1 and (i != p and i != q):
            e = i
            break
    return e

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def rsa_encryption(new_list, e, n):
    print("Encryption........")
    enc_list = []
    for i in range(len(new_list)):
        r = enc(new_list[i][0], e, n)
        g = enc(new_list[i][1], e, n)
        b = enc(new_list[i][2], e, n)
        enc_list.append((r, g, b))
    print("Encryption done.....")
    return enc_list

def enc(m, e, n):
    return pow(m, e, n)

# Example usage
def encrypt_image_with_rsa(img, e, n):
    # Open the image
    
    
    # Get the width and height of the image
    width, height = img.size
    
    # Iterate over each pixel in the image
    pixel_values = list(img.getdata())
    
    # Encrypt each pixel value using RSA
    encrypted3_pixels = rsa_encryption(pixel_values, e, n)
    
    # Create a new image with the encrypted pixel values
    encrypted3_img = Image.new(img.mode, img.size)
    encrypted3_img.putdata(encrypted3_pixels)
    
    return encrypted3_img