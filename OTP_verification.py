from tkinter import *
from tkinter import messagebox
import smtplib
import random
import re
import math

#function to close window later
def close_window():
    newwindow.destroy()

#creating tkinter window for OTP verification
root = Tk()
root.title("Send OTP Via Email")
root.geometry("565x250")
root['bg']='#fb0'

username_label = Label(root, text="Enter Name: ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
username_label.place(x=30, y=50)
username_entry = Entry(root, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2)
username_entry.place(x=250, y=50)

email_label = Label(root, text="Enter Email: ", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
email_label.place(x=30, y=120)
email_entry = Entry(root, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2)
email_entry.place(x=250, y=120)

#close original window
def close_window():
    root.destroy()

def form_validation():
    #required email format
    email_format: str = r"(^[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    #get user input
    email = email_entry.get()
    name = username_entry.get()
    error_popup = ''
    #if no input then return error
    if len(name) == 0:
        error_popup = "error - enter a name"
        messagebox.showinfo('message', error_popup)

    elif len(email) == 0:
        error_popup = "error - enter an email address"
        messagebox.showinfo('message', error_popup)
    #if matches email format, run send() function
    elif re.match(email_format, email, re.IGNORECASE):
        send()
    else:
        #if doesnt match email format show error
        error_popup = "Enter a valid email address"
        messagebox.showinfo('message', error_popup)



def send():
    #otp digits to generate from
    digits="0123456789"
    OTP=""
    #generate random 6 numbers using digits assigned above
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]

    print(OTP)

    #send OTP to email given
    try:
        s = smtplib.SMTP("smtp.gmail.com" , 587)  # server and port number
        s.starttls()
        password='Tester101!' #dummy email account password
        s.login('cryptotestsamhughes@gmail.com', password) #dummy email account
        otp_msg = 'Subject: Your OTP login code' "\nHi " + str(username_entry.get()) + '\n\n' + " Your OTP is: " + str(OTP) # message to send - gets name and OTP
        s.sendmail("cryptotestsamhughes@gmail.com" , email_entry.get() , otp_msg) #send message
        messagebox.showinfo("Send OTP via Email", f"OTP passcode sent to email:  {email_entry.get()}") #message popup to confirm email has been sent to user
        s.quit()
    finally:
        close_window() # close current window

        #create new window for OTP checking
        newwindow=Tk()
        newwindow.title('Please enter your OTP code')
        newwindow.geometry("400x200+10+20")
        newwindow['bg']='#fb0'

        #field for OTP code
        OTP_checker= Label(newwindow, text="Enter OTP code", font=("ariel 15 bold"), relief=FLAT, bg='#fb0')
        OTP_checker.place(x=125, y=40)
        OTP_entry = Entry(newwindow, font=("ariel 15 bold"), width=25, relief=GROOVE, bd=2)
        OTP_entry.place(x=65, y=90)

        #close window when called
        def close_window1():
            newwindow.destroy()


        def otp_checker():
            #check if inputted OTP matches OTP generated from function above
            x= OTP_entry.get()
            y = OTP

            if x == y: #if input = OTP then continue
                messagebox.showinfo('message', "Correct OTP")
                close_window1()
                import New_user
                New_user.main()

            else: #if input doesnt match OTP show error
                messagebox.showinfo('message', "Try again")

        #button to submit
        submit_button = Button(newwindow, text="Confirm", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=otp_checker)
        submit_button.place(x=150, y=140)

        newwindow.mainloop()


#button to send OTP email
send_button = Button(root, text="Send login Email", font=("ariel 15 bold"), bg="grey", fg="black", bd=3, command=form_validation)
send_button.place(x=200, y=180)
root.mainloop()
