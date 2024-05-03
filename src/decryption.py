from PIL import Image
def decrypt_image(encrypted_img, e,fn, n, ceaser_key):
    # Perform RSA decryption
    d=get_d(e,fn)
    decrypted_pixels_rsa = rsa_decryption(list(encrypted_img.getdata()), d, n)
    
    # Convert decrypted pixel values to tuples of integers
    decrypted_pixels_rsa = [(int(r), int(g), int(b)) for r, g, b in decrypted_pixels_rsa]
    
    # Create a new image with the decrypted pixel values
    decrypted_img_rsa = Image.new(encrypted_img.mode, encrypted_img.size)
    decrypted_img_rsa.putdata(decrypted_pixels_rsa)
    
    # Perform Caesar cipher decryption
    decrypted_img = decrypt_image_with_caesar(decrypted_img_rsa, ceaser_key)
    
    return decrypted_img

def get_d(e, fn):
    d = inverse_mod(e, fn)
    return d

def inverse_mod(a, b):
    for i in range(1, b):
        if a * i % b == 1:
            return i
    return 0

def rsa_decryption(enc_list,d,n):
    print("Decryption.......")
    dec_list=[]
    for i in range(len(enc_list)):
        r=dec(enc_list[i][0], d, n)%n
        g=dec(enc_list[i][1], d, n)%n
        b=dec(enc_list[i][2], d, n)%n
        dec_list.append([r,g,b])
    print("Decryption Done.....")
    return dec_list
def dec(c,d,n):
 return pow(c, d, n) 

def decrypt_image_with_caesar(encrypted_img, key):
    # Get the width and height of the image
    width, height = encrypted_img.size
    
    # Convert the Caesar cipher key to an integer
    key = int(key)
    
    # Initialize an empty list to store decrypted pixel values
    decrypted_pixels = []
    
    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel at (x, y)
            current_rgb = encrypted_img.getpixel((x, y))
            
            # Decrypt the RGB values using the Caesar cipher key
            decrypted_rgb = tuple((int(c) - key) % 256 for c in current_rgb)
            
            # Add the decrypted RGB values to the list
            decrypted_pixels.append(decrypted_rgb)
    
    # Create a new image with the decrypted pixel values
    decrypted_img = Image.new(encrypted_img.mode, encrypted_img.size)
    decrypted_img.putdata(decrypted_pixels)
    
    return decrypted_img


