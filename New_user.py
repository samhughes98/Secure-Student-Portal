from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import re
import math
import sys
import smtplib
from Crypto.Cipher import AES
import hashlib
import string
import os
import dropbox_storage
from secrets import token_bytes
import pandas as pd
import base64

sys.setrecursionlimit(2000)

def main():

    #Checksum function called later to get checksum value of CSV file
    def checksum():
        from hashlib import md5
        md5_hash = hashlib.md5()

        file = open(r"C:\Users\samhu\Desktop\Encryption_Decryption\Chacha20_encryption_decryption\Cryptology_app\storage\enc_logins.csv", "rb")
        content = file.read()
        md5_hash.update(content)

        orig_digest = md5_hash.hexdigest()

        with open('storage\CHECKSUM.txt', 'w') as f:
            f.write(orig_digest)
            f.close()

    #Tkinter window code for register page
    h_window=Tk()
    h_window.title('Register details')
    h_window.geometry("520x300+10+20")
    h_window['bg']='#fb0'

    #storing user input in stringvar format
    F_name = StringVar()
    S_name = StringVar()
    Email_22 = StringVar()

    #tkinter fields for first name, surname and email entry
    Fname_label = Label(h_window, text="Enter First Name ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
    Fname_label.grid(row=6, column=0, padx=0 , pady=25)
    Fname_entry = Entry(h_window, font=("ariel 15 bold"), width=24, relief=GROOVE, bd=2, textvariable=F_name)
    Fname_entry.grid(row=6, column=1, padx=0, pady=25, sticky="NSEW")

    Sname_label = Label(h_window, text="Enter Surname ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
    Sname_label.grid(row=8, column=0, padx=0 , pady=25)
    Sname_entry = Entry(h_window, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2, textvariable=S_name)
    Sname_entry.grid(row=8, column=1, padx=0, pady=25, sticky="NSEW")

    email2_label = Label(h_window, text="Enter Email address ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
    email2_label.grid(row=10, column=0, padx=0 , pady=25)
    email2_entry = Entry(h_window, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2, textvariable=Email_22)
    email2_entry.grid(row=10, column=1, padx=0, pady=25, sticky="NSEW")

    #function to call later to close window
    def close_window():
        h_window.destroy()

    #randomly generate ID for user with 8 characters
    ID = ''.join(random.choice(string.digits) for _ in range(8))

    #Sending generated ID to users inputted email
    def send_ID():
       try:
           Student_ID = ID
           s = smtplib.SMTP("smtp.gmail.com" , 587)  # server mode and port number
           s.starttls()
           #my dummy account to send email from
           password='Tester101!'
           s.login('cryptotestsamhughes@gmail.com', password)
           #email message - takes user input for name and gives ID
           ID_msg = 'Subject: Your Student ID' "\nHi " + str(F_name.get()) + '\n\n' + " Your Student ID is: " + str(Student_ID) + " - Please keep this safe and use to login"
           s.sendmail("cryptotestsamhughes@gmail.com" , email2_entry.get() , ID_msg)
           messagebox.showinfo("Send Student ID via Email", f"Your student ID has been sent to you via this email:  {email2_entry.get()}")
           s.quit()
       except:
           #if email format isnt accepted by SMTP - return error and go back to validate fields
           messagebox.showinfo('', "Enter a valid email address")
           validate_fields()

    #user input field validation
    def validate_fields():
            email_format: str = r"(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

            #error message popup - ises all strings below if field is empty or invalid
            error_popup = ''

            if len(F_name.get()) == 0:
                error_popup = "error - enter a name"
                messagebox.showinfo('', error_popup)
            elif len(email2_entry.get()) == 0:
                error_popup = "error - enter an email address"
                messagebox.showinfo('', error_popup)
            elif len(Sname_entry.get()) == 0:
                error_popup = "Error - enter valid surname"
                messagebox.showinfo('', error_popup)
            elif re.match(email_format, email2_entry.get(), re.IGNORECASE):
                #if email matches format - continue to send_ID function
                print("Sign in successful")
                encrypt()
            else:
                error_popup = "Enter a valid email address"
                messagebox.showinfo('', error_popup)

    #encryption of user inputs via AES
    def encrypt():
        import hashlib
        from New_user import main

        #generate random key of 16 bytes
        def key_gen():
           key_gen = token_bytes(16)
           return key_gen

        #storing generated key
        key = key_gen()

        #padding function to make sure data is 16 bytes
        def padded_text(data_in):
            length = 16 - (len(data_in) % 16)
            data_in += bytes([length])*length
            return data_in

        #encodes all user input to utf8 and stores in variable
        f_name_in = Fname_entry.get().encode('utf8')
        S_name_in = S_name.get().encode('utf8')
        email_in = Email_22.get().encode('utf8')

        #Padding encoded user input to 16 bytes
        pad_fname = padded_text(f_name_in)
        pad_sname = padded_text(S_name_in)
        pad_email = padded_text(email_in)

        #AES encryption function - uses generated key and IV made earlier
        mode = AES.MODE_CBC

        IV = token_bytes(16)
        cipher = AES.new(key, mode, IV)

        #encryption
        fname_enc = cipher.encrypt(pad_fname)
        Sname_enc = cipher.encrypt(pad_sname)
        email_enc = cipher.encrypt(pad_email)

        #encoding to base64 for dtorage purposes
        fname_enc64 = base64.b64encode(fname_enc)
        Sname_enc64 = base64.b64encode(Sname_enc)
        email_enc64 = base64.b64encode(email_enc)


        #saving encrypted encoded data to a csv
        def save_to_csv():
            #stored checksum performed previously
            global checksum_p

            #hashing user ID to store in file for security purposes
            hashID = hashlib.sha256()
            hashID.update(ID.encode())
            hashID.hexdigest()

            data = [[hashID.hexdigest(),fname_enc64.decode('utf8'),Sname_enc64.decode('utf8'),email_enc64.decode('utf8')]]

            #Data above inputted to pandas dataframe - dataframe then placed into a csv file in binary mode
            df = pd.DataFrame(data)
            df.columns = ['ID','Fname','Sname','Email']
            df.to_csv('storage/enc_logins.csv', mode='ab', index=False, encoding="utf8", header=['ID','Fname','Sname','Email'])

            #run checksum function at start of program to see checksum value of file with inputted data
            checksum()
            #run dropbox upload function from dropbox_storage file
            dropbox_storage.dropbox_upload()
            #continue to send to DB function
            Send_to_DB()

        def Send_to_DB():
           import sqlite3
           import os.path
           print(ID)

           #hashing ID again to store in sql DB
           hashID2 = hashlib.sha256()
           hashID2.update(ID.encode())
           hashID2.hexdigest()

           #hashing user email input to compare if already exists in DB
           hashemail = hashlib.sha256()
           hashemail.update(email2_entry.get().encode())
           hashemail.hexdigest()
           hashed_email = hashemail.hexdigest()

           #sending data to DB file
           try:
               #Establish connection to database
               conn = sqlite3.connect('storage/login_details.db')
               #initialise connection
               cursor = conn.cursor()
               print("Connected to SQLite")

               #Check if hashed email already exists in DB
               cursor.execute('''SELECT * FROM Login WHERE Email2=?''',(hashed_email,))

               #if email exists, show error message
               if cursor.fetchall():
                   print("Exists already")
                   messagebox.showinfo('', "Email already exists - use your ID to login")
               else:
                   #if email doesnt exist, continue and send ID via email
                   send_ID()
                   #inserting user into Login table with specified columns
                   data_to_DB = """INSERT INTO Login(ID, Fname, Sname, Email2, enc_key, IV)
                                                 VALUES (?, ?, ?, ?, ?, ?);"""
                   #data to be inserted - all data in hashed format
                   data_tuple = (hashID2.hexdigest(), hash(fname_enc), hash(Sname_enc), hashed_email, key, IV)
                   cursor.execute(data_to_DB, data_tuple) #execute data input
                   conn.commit() # commit changes
                   print("Successfully inserted into DB")

                   #if connection exists, close connection and window, and open homepage file to send user back to home
                   if conn:
                      conn.close()
                      print("Connection closed")
                      close_window()
                      import homepage

           except sqlite3.Error as error:
               print("Failure, error: ", error)



        #continue to csv function
        save_to_csv()

    #send button formatting and instructions
    send_button = Button(h_window, text="Submit details", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=validate_fields)
    send_button.place(x=185, y=240)

    h_window.mainloop()

if __name__ == "__main__":
    main()
