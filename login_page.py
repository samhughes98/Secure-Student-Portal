from tkinter import *
from tkinter import messagebox
import smtplib
import random
import re
import math
import dropbox
from dropbox.files import WriteMode
import csv
from csv import reader
import io
import pandas as pd
import sys
import base64
from New_user import *

sys.setrecursionlimit(2000)

#initialise window via tkinter
login_page = Tk()
login_page.title("Welcome to the student portal")
login_page.geometry("565x250")
login_page['bg']='#fb0'

#create user input field and label
L_ID_label = Label(login_page, text="Please enter your student ID ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
L_ID_label.grid(row=0, column=0, padx=15, pady=60)
L_ID_entry = Entry(login_page, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2)
L_ID_entry.grid(row=0, column=1, padx=12, pady=60)

#code to access dropbox app via API
dropbox_access_token= "sl.BFOH9gk88_xOqfapMXI_uvAc1ji2ijones_burN1ZEq_uvYWgDGQEElA7QVqccx7_Em2Q2q9vGoWZt3TDpWtawpAS-jOEo-UN7scRahOGmz1QQCN2Pqh_AyyMXSeMRylOzjOnDj99LNO"    #Enter your own access token
client = dropbox.Dropbox(dropbox_access_token)

def login():
    import sqlite3
    import os.path

    def decoder():
        from Crypto.Cipher import AES
        import hashlib
        from secrets import token_bytes

        #find matching hashed ID in DB file and fetch encryption key in the same row
        cursor.execute(
            '''
            Select enc_key, IV FROM Login where ID = (?);
            ''',
            (hashed_entry.hexdigest(), ))

        #index to select encryption key
        row = cursor.fetchone()
        if row is not None:
            keys = row[0]
            IV = row[1]

            #calling stored key from main file and reverting back to bytes
            key_original = keys

            #function to unpad decrypted data
            def unpadded_text(data_in):
                data_in = data_in[:-data_in[-1]]
                return data_in

            #model for decryption - AES
            mode = AES.MODE_CBC

            #gets enc key and IV from DB
            cipher = AES.new(key_original, mode, IV)


            #decoding from base64
            df11 = base64.b64decode(df1)
            df12 = base64.b64decode(df2)
            df13 = base64.b64decode(df3)

            #decrypting data
            d_fname = cipher.decrypt(df11)
            d_sname = cipher.decrypt(df12)
            d_email = cipher.decrypt(df13)

            #unpadding decrypted data
            unpadded_fname = unpadded_text(d_fname)
            unpadded_sname = unpadded_text(d_sname)
            unpadded_email = unpadded_text(d_email)

            def credentials_ui():
                import tkinter
                from tkinter import ttk

                #tkinter window for displaying user record
                credentials = Tk()
                credentials.title("Welcome to the student portal")
                credentials.geometry("565x250")
                credentials['bg']='#fb0'

                #table view for data
                TreeView = ttk.Treeview(credentials, height=1)
                TreeView['columns']=('ID', 'First Name', 'Surname', 'Email')
                TreeView.column('#0', width=0, stretch=NO)
                TreeView.column('ID', anchor=CENTER, width=80)
                TreeView.column('First Name', anchor=CENTER, width=80)
                TreeView.column('Surname', anchor=CENTER, width=80)
                TreeView.column('Email', anchor=CENTER, width=200)

                TreeView.heading('#0', text='', anchor=CENTER)
                TreeView.heading('ID', text='ID', anchor=CENTER)
                TreeView.heading('First Name', text='First Name', anchor=CENTER)
                TreeView.heading('Surname', text='Surname', anchor=CENTER)
                TreeView.heading('Email', text='Email', anchor=CENTER)

                #insert data from decryption into table to display for user as plaintext
                TreeView.insert(parent='', index=0, iid=0, text='', values=([L_ID_entry.get(), unpadded_fname.decode(), unpadded_sname.decode(), unpadded_email.decode()]))
                TreeView.place(x=55,y=65)

                #function to call when window closed - also opens homepage and sends user back to start
                def close_window():
                    credentials.destroy()
                    login_page.destroy()
                    import homepage

                #button to log out
                log_out_button = Button(credentials, text="Log-Out", font=("ariel 15 bold"), bg="black", fg="green2", bd=3, command=close_window)
                log_out_button.place(x=225, y=140)
            #send to credentials function
            credentials_ui()


    #connecting to db
    try:
        conn = sqlite3.connect('storage/login_details.db')
        cursor = conn.cursor()
        print("Connected to SQLite")

    except sqlite3.Error as error:
        print("Failure, error: ", error)
    finally:
        import hashlib
        #finding file from dropbox storage and reads in stream
        _, res = client.files_download("/user_details/enc_logins.csv")
        with io.BytesIO(res.content) as stream:

            #working out checksum value of file after downloaded
            from hashlib import md5
            md5_hash = hashlib.md5()

            content = stream.read()
            md5_hash.update(content)

            digest = md5_hash.hexdigest()
            print(digest)

            #getting user input ID
            ID_entry = L_ID_entry.get()

            #hashes inputted user ID to see if matches to original hashed ID
            hashed_entry = hashlib.sha256()
            hashed_entry.update(ID_entry.encode())
            hashed_entry.hexdigest()

        #second stream from dropbox for reading - after checksum
        _, res1 = client.files_download("/user_details/enc_logins.csv")
        with io.BytesIO(res1.content) as stream1:

            #opening csv and putting into CSV file
            df = pd.read_csv(stream1)

            #if ID inputted matches hashed ID stored in CSV then continue
            missing_id = df['ID'].eq(hashed_entry.hexdigest()).any()
            if missing_id == True:
                #match ID and fetch whole row from csv
                newdf = df[df['ID'] == hashed_entry.hexdigest()]

                #get specific values from row
                df1 = newdf['Fname'].values[0]
                df2 = newdf['Sname'].values[0]
                df3 = newdf['Email'].values[0]

                #if checksum value matches checksum value before upload then continue
                with open('storage\CHECKSUM.txt', 'r') as f:
                    if digest in f.read():
                        print("success")
                        decoder()
                    else:
                        print("Checksum Failed - File may have been tampered with")
                        messagebox.showinfo('', "Error 901 - please contact an administrator")

            else:
                #if ID doesnt match shoe error popup
                 messagebox.showinfo('', "ID Does not exist")

#button for logging in
login_button = Button(login_page, text="Login", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=login)
login_button.place(x=230, y=150)


login_page.mainloop()
