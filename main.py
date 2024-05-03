import sys
import random
from PIL import Image
sys.path.insert(0, './src')
import streamlit as st
from src.ceaser_encrypt import encryptImage
from src.rsa_encrypt import encrypt_image_with_rsa,get_e,generate_prime,rsa_encryption
from src.lsb_stegno import lsb_encode,lsb_decode
from src.n_share import nshares
from send_mails import EmailSender
from merge_k_shares import mergeToKShare
from decryption import decrypt_image


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
        # try:
        #     img.save('images/img1.jpg')
        # except:
        #     img.save('images/img1.png')
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
            imtoencrypt=lsb_encode(img,txt)
            imtoencrypt.save("images/final_image.jpg")
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

    # Inputs for each recipient
    recipient_emails = []
    recipient_subjects = []
    recipient_bodies = []
    recipient_attachments = []
    for i in range(num_recipients):
        st.write(f"Recipient {i+1}")
        to_email = st.text_input(f"Recipient {i+1}'s Email")
        recipient_emails.append(to_email)
        subject = st.text_input(f"Subject for Recipient {i+1}")
        recipient_subjects.append(subject)
        body = st.text_area(f"Body for Recipient {i+1}")
        recipient_bodies.append(body)
        attachment_path = st.file_uploader(f"Upload Attachment for Recipient {i+1}", type=["jpg", "jpeg", "png", "pdf"])
        recipient_attachments.append(attachment_path)
    if st.button("Send Emails"):
        if all(recipient_emails) and all(recipient_subjects) and all(recipient_bodies) and all(recipient_attachments):
            if len(set(recipient_emails)) == len(recipient_emails):
                sender = EmailSender()
                for i in range(num_recipients):
                    sender.send_email(recipient_emails[i], recipient_subjects[i], recipient_bodies[i], recipient_attachments[i])
                st.success("Emails sent successfully!")
            else:
                st.error("Please provide unique email addresses for each recipient.")
        else:
            st.error("Please provide email addresses, subjects, bodies, and upload attachments for all recipients.")


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
        
        # Display decrypted image
        st.image(decrypted_image, caption='Decrypted image', use_column_width=True)
        decrypted_image.save("images/decoded_image.jpg")
        if st.button('Decode message'):
            st.success('Decoded message: ' + lsb_decode("images/final_image.jpg"))

