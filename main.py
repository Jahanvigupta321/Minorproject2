import sys
import random
from PIL import Image
sys.path.insert(0, './src')
import streamlit as st
from src.ceaser_encrypt import encryptImage
from src.rsa_encrypt import encrypt_image_with_rsa,get_e,generate_prime
from src.lsb_stegno import lsb_encode,lsb_decode
from src.n_share import nshares
from src.send_mails import send_email
from src.merge_k_shares import mergeToKShare
from src.decryption import decrypt_image


menu = st.sidebar.radio('Options', [ 'Documentation','Encode','N-share division', 'Send mails' ,'Overlapping','Decode'])
ceaser_key = random.random()
p = generate_prime()
q = generate_prime()
fn = (p - 1) * (q - 1)
n = p * q
e = get_e(p, q, fn)
new_image=""
if menu == 'Encode':
    st.title('Encoding')

    # Image input by the user
    img = st.file_uploader('Upload image file', type=['jpg', 'png', 'jpeg'])
    if img is not None:
        img = Image.open(img)
        try:
            img.save('images/img1.jpg')
        except:
            img.save('images/img1.png')
        st.image(img, caption='Successful upload',
                use_column_width=True)

    # Data to be input by user
    txt = st.text_input('Message to hide')

    # Encode message button
    if st.button('Encode data'):

        # Checks
        if len(txt) == 0:
            st.warning('No data to hide')
        elif img is None:
            st.warning('No image file selected')
        #start encoding
        else:
            # lsb_steganography of txt intoimg
            imtoencrypt=lsb_encode(txt)
            imtoencrypt.save("images/final_decrypted.png")
            #Encrypt the image using ceaser cipher
            encrypted_img = encryptImage(imtoencrypt, ceaser_key)
            # Encrypt the image using RSA encryption
            encrypted2_image = encrypt_image_with_rsa(encrypted_img, e, n)
            # Show or save the encrypted image
            encrypted2_image.show()
            encrypted2_image.save("images/final_encrypted_image.jpg")
            st.write("Image has been encoded.")
            
elif menu=='N-share division':
    st.title('N-share Division')

    # Image
    previous_image = st.file_uploader('Upload image file which you encrypted previously', type=['jpg', 'png', 'jpeg'])
    if previous_image is not None:
        previous_image2 = Image.open(previous_image)
        try:
            previous_image2.save('images/img2.jpg')
        except:
            previous_image2.save('images/img2.png')
        st.image(previous_image, caption='Selected image to use for n-share division',
                use_column_width=True)
    no_of_shares = st.number_input('No. of shares')
    if st.button('Generate shares'):
        nshares(previous_image2,no_of_shares)

elif menu=='Send mails':
    st.title('Send mails')
    num_recipients = st.number_input("Number of recipients", min_value=1, step=1)

    for i in range(num_recipients):
        st.write(f"Recipient {i+1}")
        to_email = st.text_input(f"Recipient {i+1}'s Email")
        attachment_path = st.file_uploader(f"Upload Attachment for Recipient {i+1}", type=["jpg", "jpeg", "png", "pdf"])

        if st.button(f"Send Email to Recipient {i+1}"):
            if to_email:
                sender_email = "jarus6124@gmail.com"  # Your email address
                sender_password = "avtu ckhz ooxu dnri"  # Your email password
                subject = "Fixed Subject"  # Fixed subject content
                body = "This is the fixed body content of the email."  # Fixed body content
                send_email(sender_email, sender_password, to_email, subject, body, attachment_path)
                st.success(f"Email sent successfully to {to_email}!")
            else:
                st.error("Please provide email address for all recipients.")

elif menu=='Overlapping':
    st.title('Overlapping')

    # Add UI elements for merging images (optional)
        # Example usage of mergeToKShare function
    k_image = ["images/share_1.png", "images/share_2.png","images/share_3.png","images/share_4.png","images/share_5.png"]  # List of image paths
    k_share = st.number_input("Enter k_share value", min_value=1, step=1)  # Placeholder for k_share
    
    if st.button("Merge Images"):
        mergeToKShare(k_image, k_share)
        st.success("Images merged successfully!")  # Display success message


elif menu == 'Decode':
    st.title('Decode')

    # Upload the encrypted image
    encrypted_image = st.file_uploader("Upload Encrypted Image", type=["jpg", "jpeg", "png"])
    if encrypted_image is not None:
        encrypted_image = Image.open(encrypted_image)
        st.image(encrypted_image, caption='Selected encrypted image', use_column_width=True)
        
        # Call decryption function from decryption.py
        decrypted_image = decrypt_image(encrypted_image,e,fn,n,ceaser_key)
        st.image("images/final_decrypted.png", caption='Decrypted image', use_column_width=True)
        # Display decrypted image
        # st.image(decrypted_image, caption='Decrypted image', use_column_width=True)
        # decrypted_image.save("images/decoded_image.jpg")
        if st.button('Decode message'):
            st.success('Decoded message: ' + lsb_decode("images/final_decrypted.png"))

