from PIL import Image
def encryptImage(image, key):
    # Get the width and height of the image
    width, height = image.size
    
    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Get the RGB values of the pixel at (x, y)
            current_rgb = image.getpixel((x, y))
            # Modify the RGB values using the key
            modified_rgb = tuple((int(c + key) % 256) for c in current_rgb)
            # Update the pixel with the modified RGB values
            image.putpixel((x, y), modified_rgb)
     
    return image
