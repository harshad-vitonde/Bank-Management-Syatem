from tkinter import *
from backend import *

def main_window():
    global acc
    global win
    acc = Accounts()
    win = Tk()
    win.wm_title("Bank management System")
    win.geometry("1920x1080")
    win['background']= "#856ff8"
    
    
    global main
    main = Frame(win, width=1920, height=1080)
    main.place(relx = 0.5, rely=0.5, anchor=CENTER)
    main['background']= "#856ff8"
    
    l3= Label(main, text="CITY BANK", font= ("Times New Roman", 70,UNDERLINE))
    l3.place(relx=0.5, rely=0.23, anchor=CENTER)
    l3['background']= "#856ff8"

    l1 = Label(main, text="Please Select to Proceed",font= ("Times New Roman", 30))
    l1.place(relx=0.5, rely=0.35, anchor=CENTER)
    l1['background']= "#856ff8"

    b1 = Button(main, text="Existing Account",width=24, command=login_window_command, font= ("Comic Sans MS", 15))
    b1.place(relx=0.5,rely=0.5,anchor=CENTER)

    b2 = Button(main, text="New Account",width=24, command=new_user_command,font= ("Comic Sans MS", 15))
    b2.place(relx=0.5,rely=0.45,anchor=CENTER)

    win.mainloop()

def new_user_command():
    main.destroy()
    new_user()

def new_user():
    global sign_in
    sign_in = Frame(win, width=1560, height=500)
    sign_in.grid(row=0,column=0)
    sign_in['background']= "#856ff8"
    l42= Label(sign_in, text="ACCOUNT REGISTRATION", font= ("Times New Roman", 35, UNDERLINE))
    l42.place(relx=0.5, rely=0.08, anchor=CENTER)
    l42['background']= "#856ff8"
    l2 = Label(sign_in,text = "Name",font= ("Times New Roman", 20))
    l2.place(relx= 0.22,rely=0.25, anchor= CENTER)
    l2['background']= "#856ff8"

    l3 = Label(sign_in, text = "Mobile Num",font= ("Times New Roman", 20))
    l3.place(relx= 0.55,rely=0.25, anchor= CENTER)
    l3['background']= "#856ff8"

    l4 = Label(sign_in, text = "Address",font= ("Times New Roman", 20))
    l4.place(relx= 0.22,rely=0.35, anchor= CENTER)
    l4['background']= "#856ff8"

    l5 = Label(sign_in, text = "Aadhar NO",font= ("Times New Roman", 20))
    l5.place(relx= 0.55,rely=0.35, anchor= CENTER)
    l5['background']= "#856ff8"

    l6 = Label(sign_in, text = "Password",font= ("Times New Roman", 20))
    l6.place(relx= 0.22,rely=0.45, anchor= CENTER)
    l6['background']= "#856ff8"

    l7 = Label(sign_in, width= 15, text = "Email",font= ("Times New Roman", 20))
    l7.place(relx= 0.55,rely=0.45, anchor= CENTER)
    l7['background']= "#856ff8"

    global name
    name = StringVar()
    e1 = Entry(sign_in, textvariable = name,font= ("Times New Roman", 18))
    e1.place(relx= 0.36,rely=0.25, anchor= CENTER)

    global mob_no  
    mob_no = StringVar()
    e2 = Entry(sign_in, textvariable = mob_no,font= ("Times New Roman", 18))
    e2.place(relx= 0.71,rely=0.25, anchor= CENTER)

    global address 
    address = StringVar()
    e3 = Entry(sign_in, textvariable = address,font= ("Times New Roman", 18))
    e3.place(relx= 0.36,rely=0.35, anchor= CENTER)

    global aadhar_no
    aadhar_no = StringVar()
    e4 = Entry(sign_in, textvariable = aadhar_no,font= ("Times New Roman", 18))
    e4.place(relx= 0.71,rely=0.35, anchor= CENTER)

    global password
    password = StringVar()
    e5 = Entry(sign_in, textvariable = password,font= ("Times New Roman", 18))
    e5.place(relx= 0.36,rely=0.45, anchor= CENTER)

    global email
    email = StringVar()
    e6 = Entry(sign_in, textvariable = email,font= ("Times New Roman", 18))
    e6.place(relx= 0.71,rely=0.45, anchor= CENTER)

    b3 =Button(sign_in,text="Submit",width=15,font= ("Times New Roman", 15), command=create_acc_command)
    b3.place(relx= 0.51,rely=0.65, anchor= CENTER)

def create_acc_command():
    global message_frame
    message_frame = Frame(win, width=500,height=200)
    message_frame.grid(row = 1, column= 0)
    message_frame['background']= "#856ff8"
    global msg_acc_crt
    try:
        an = int(aadhar_no.get())
        mn = int(mob_no.get())
        if name.get() == "" or mob_no.get() == "" or address.get() == "" or aadhar_no.get() == "" or  password.get() == "" or email.get() == "":
            msg_acc_crt = "The feilds can not be blank"
            label2 = Label(message_frame, text=msg_acc_crt, width=70)
            label2.grid(row=0,column=0)
        else:
            global acc_data
            acc_data = {}
            acc_data["name"] = name.get()
            acc_data["mob_no"] = mn
            acc_data["address"] = address.get()
            acc_data["aadhar_no"] = an
            acc_data["password"] = password.get()
            acc_data["email"] = email.get()
            msg_acc_crt = acc.create_account(acc_data)

            if msg_acc_crt:
                global otp_frame
                otp_frame = Frame(win)
                otp_frame.grid(row=1,column=0)
                otp_frame['background']= "#856ff8"
                
                label = Label(otp_frame,text=msg_acc_crt,font= ("Times New Roman", 20))
                label.grid(row=0,column= 0,rowspan=1, columnspan=2)
                label['background']= "#856ff8"

                global entered_otp
                entered_otp = StringVar()
                entry = Entry(otp_frame, textvariable= entered_otp,font= ("Times New Roman", 20))
                entry.grid(row=1,column=0, columnspan=1)

                btn = Button(otp_frame, text="Verify",width = 5, command= verify_otp_command,font= ("Times New Roman", 15))
                btn.grid(row=1,column=1)
            else:
                msg_acc_crt = "Account registered on Aadhar No. Already Exists Try logging in"
                label2 = Label(message_frame, text=msg_acc_crt,width = 70,font= ("Times New Roman", 15))
                label2.grid(row=0,column=0)
                label2['background']= "#856ff8"
    except ValueError:
        msg_acc_crt = "Aadhar No. and Mobile No. should not be empty string"
        label2 = Label(message_frame, text=msg_acc_crt, width=70,font= ("Times New Roman", 15))
        label2.grid(row=0,column=0)
        label2['background']= "#856ff8"

def verify_otp_command():
    try:
        verification = acc.verify_otp(int(entered_otp.get()), acc_data)
    except ValueError:
        print("Wrong OTP")
        
    if verification:
        win.destroy()
        main_window()

def login_window_command():
        main.destroy()
        global sign_in
        sign_in = Frame(win, width=1920, height=600)
        sign_in.grid(row=0,column=0)
        sign_in['background']= "#856ff8"
        l34= Label(sign_in, text="ENTER THE CREDENTIALS", font= ("Times New Roman", 35, UNDERLINE))
        l34.place(relx=0.39, rely=0.15, anchor=CENTER)
        l34['background']= "#856ff8"

        l8 = Label(sign_in, text="Account Number", font= ("Times New Roman", 25))
        l8.place(relx=0.25, rely=0.35, anchor=CENTER)
        l8['background']= "#856ff8"

        l9 = Label(sign_in, text="Password",font= ("Times New Roman", 25))
        l9.place(relx=0.25, rely=0.5, anchor=CENTER)
        l9['background']= "#856ff8"

        global account_num   
        account_num = StringVar()
        e7 = Entry(sign_in, textvariable = account_num,font= ("Times New Roman", 25))
        e7.place(relx=0.5, rely=0.35, anchor=CENTER)

        global password
        password = StringVar()
        e8 = Entry(sign_in, textvariable = password,font= ("Times New Roman", 25))
        e8.place(relx=0.5, rely=0.5, anchor=CENTER)

        b4 = Button(sign_in, text = "Login",width = 10,font= ("Times New Roman", 20), command=login_command)
        b4.place(relx=0.4, rely=0.7, anchor=CENTER)

def login_command():
    global result
    result = acc.login(account_num.get(), str(password.get()))
    account = result[0]
    is_successful = result[1]
    #print(account)
    message_frame2 = Frame(win, width= 1920, height=200)
    message_frame2.grid(row=1,column=0)
    message_frame2['background']= "#856ff8"
    if not is_successful:
        label1 = Label(message_frame2,width=40, text=account, font= ("Times New Roman", 20))
        label1.place(relx = 0.39, rely = 0.2, anchor= CENTER)
        label1['background']= "#856ff8"
    else:
        operational_window()

def operational_window():
    win.destroy()

    global op_win
    op_win =Tk()
    op_win.geometry("1920x1080")
    op_win.wm_title("Bank Management System")
    op_win['background']= "DeepSkyBlue"

    l0 = Label(op_win, text = "MAIN MENU",font= ("Times New Roman", 40,UNDERLINE) )
    l0.place(relx = 0.52, rely = 0.1, anchor= CENTER)
    l0['background']= "DeepSkyBlue"

    l1 = Label(op_win, text = "Enter Amount",font= ("Times New Roman", 20) )
    l1.place(relx = 0.4, rely = 0.2, anchor= CENTER)
    l1['background']= "DeepSkyBlue"

    global amount
    amount = StringVar()
    e1 = Entry(op_win, textvariable = amount,font= ("Times New Roman", 20))
    e1.place(relx = 0.58, rely = 0.2, anchor= CENTER)

    button1 = Button(op_win,text = "Deposit", width=15, command=deposite_command,font= ("Times New Roman", 20))
    button1.place(relx = 0.15, rely = 0.35, anchor= CENTER)

    button2 = Button(op_win,text = "Withdraw",width=15, command=withdraw_command,font= ("Times New Roman", 20))
    button2.place(relx = 0.15, rely = 0.7, anchor= CENTER)

    button3 = Button(op_win,text = "Check Balance",width=15, command=check_bal_command,font= ("Times New Roman", 20))
    button3.place(relx = 0.85, rely = 0.35, anchor= CENTER)

    button4 = Button(op_win,text = "Transaction",width=15, command=view_trasaction_command,font= ("Times New Roman", 20))
    button4.place(relx = 0.85, rely = 0.7, anchor= CENTER)

    button5 = Button(op_win,text = "Close",width=15, command=op_win.destroy,font= ("Times New Roman", 20))
    button5.place(relx = 0.5, rely = 0.85, anchor= CENTER)

    op_win.mainloop()


def deposite_command():
    flag = acc.deposite(amount.get())

    message_frame = Frame(op_win)
    message_frame.place(relx = 0.5, rely = 0.5, anchor= CENTER)

    label0 = Label(message_frame,width =50, text=flag[0],font= ("Times New Roman", 20))
    label0.grid(row=0,column=0)
    label0['background']= "DeepSkyBlue"
    
def withdraw_command():
    flag = acc.withdraw(amount.get())

    message_frame = Frame(op_win)
    message_frame.place(relx = 0.5, rely = 0.5, anchor= CENTER)

    label2 = Label(message_frame,width =50, text=flag[0],font= ("Times New Roman", 20))
    label2.grid(row = 0, column=0)
    label2['background']= "DeepSkyBlue"

def check_bal_command():
    balance = acc.check_balance()

    message_frame = Frame(op_win)
    message_frame.place(relx = 0.5, rely = 0.5, anchor= CENTER)

    label1 = Label(message_frame,width =50, text=f"Available Balance is {balance}",font= ("Times New Roman", 20))
    label1.grid(row = 0, column=0)
    label1['background']= "DeepSkyBlue"

def view_trasaction_command():
    trans = Transactions(result[0][0][0][0])
    flag = trans.view_transactions(result[0][0][0][4], True)

    message_frame = Frame(op_win)
    message_frame.place(relx = 0.5, rely = 0.5, anchor= CENTER)

    label3 = Label(message_frame,width =50, text=flag[0],font= ("Times New Roman", 20))
    label3.grid(row = 0, column=0)
    label3['background']= "DeepSkyBlue"

main_window()