from PIL import Image
import streamlit as st

def mergeToKShare(k_image, k_share):
    k = int(k_share)
    kth = 1
    width = 0
    height = 0
    total_len = 0
    result = []
    index = 0
    
    while kth <= k:
        kth_image_name = k_image[index]
        index += 1
        
        if kth == 1:
            im = Image.open(kth_image_name)
            result = list(im.getdata())
            width, height = im.size
            total_len = width * height
            
            for i in range(total_len):
                result[i] = list(result[i])
        else:
            im = Image.open(kth_image_name)
            kth_image = list(im.getdata())
            
            for i in range(total_len):
                r = kth_image[i][0]
                g = kth_image[i][1]
                b = kth_image[i][2]
                
                result[i][0] = result[i][0] or r
                result[i][1] = result[i][1] or g
                result[i][2] = result[i][2] or b
        
        kth += 1
    
    dec_img = Image.new("RGB", (width, height))
    dec_img.putdata([tuple(px) for px in result])
    st.image(dec_img, caption='Successful overlapping',
                use_column_width=True)
    dec_img.save("images/overlapped_image.jpg")  # Save or do further processing as needed
