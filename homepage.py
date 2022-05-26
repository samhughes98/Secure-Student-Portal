from tkinter import *
from tkinter import messagebox
import tkinter as tk

#create homepage window
homepage = Tk()
homepage.title("Welcome to the student portal")
homepage.geometry("565x250")
homepage['bg']='#fb0'

#header text to welcome user
Fname_label = Label(homepage, text="Welcome to the student portal", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
Fname_label.place(x=120, y=40)

#send to login page
def sendtologin():
    import login_page

#send to otp verification page
def sendtoregister():
    import OTP_verification

#close current window when calledg
def close_window():
    homepage.destroy()

#send to login button for user
login_button = Button(homepage, text="Login", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=lambda:[close_window(), sendtologin()])
login_button.place(x=320, y=100)

#send to register button for user
register_button = Button(homepage, text="Register", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=lambda:[close_window(), sendtoregister()])
register_button.place(x=150, y=100)

homepage.mainloop()
