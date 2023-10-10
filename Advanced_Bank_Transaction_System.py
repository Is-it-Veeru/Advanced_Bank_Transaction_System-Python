import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from time import gmtime, strftime

class Bank:
    def __init__(self, app_instance):
        self.account_records_file = "Accnt_Record.txt"
        self.app_instance = app_instance  # Store the App instance

    def custom_info_dialog(self, master, title, message, bg_color):
        dialog = tk.Toplevel(master)
        dialog.title(title)
        dialog.geometry("300x100")
        dialog.configure(bg=bg_color)

        label = tk.Label(dialog, text=message, font=("Arial", 12), bg='Black', fg='gold')
        label.pack(pady=20)

        dialog.transient(master)
        dialog.grab_set()
        master.wait_window(dialog)

    def is_number(self, s):
        try:
            float(s)
            return 1
        except ValueError:
            return 0

    def create_account(self, master, name, oc, pin):
        if self.is_number(name) or not self.is_number(oc) or not self.is_number(pin) or name == "":
            self.custom_info_dialog(master, "Error", "Invalid Credentials\nPlease try again.", 'red')
            master.destroy()
            return
        else:
            f1 = open("Accnt_Record.txt", 'r', encoding="utf-8")
            accnt_no = int(f1.readline())
            accnt_no += 1
            f1.close()

            f1 = open("Accnt_Record.txt", 'w', encoding="utf-8")
            f1.write(str(accnt_no))
            f1.close()

            fdet = open(str(accnt_no) + ".txt", 'w', encoding="utf-8")
            fdet.write(pin + "\n")
            fdet.write("₹" + oc + "\n")
            fdet.write(str(accnt_no) + "\n")
            fdet.write(name + "\n")
            fdet.close()

            frec = open(str(accnt_no) + "-rec.txt", 'w', encoding="utf-8")
            frec.write("         Date              Credit             Debit            Balance\n")
            frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]     ", gmtime())) + '₹' + oc + "              " + "                   " + '₹' + oc + "\n")
            frec.close()

            self.custom_info_dialog(master, "Details", "Your Account Number is:" + str(accnt_no), 'gray')
            master.destroy()
            return

    def check_log_in(self, master, name, acc_num, pin):
        if name and acc_num and pin:
            try:
                with open(acc_num + ".txt", 'r', encoding="utf-8") as f:
                    info = f.readlines()
                    stored_pw = info[0].strip()
                    stored_name = info[3].strip()

                if stored_name != name:
                    self.custom_info_dialog(master, "Error", "Invalid Name", 'red')
                elif stored_pw != pin:
                    self.custom_info_dialog(master, "Error", "Invalid PIN", 'red')
                else:
                    master.destroy()
                    self.app_instance.logged_in_menu(acc_num, name) 
            except FileNotFoundError:
                self.custom_info_dialog(master, "Error", "Account not found", 'red')
            except Exception as e:
                self.custom_info_dialog(master, "Error", str(e), 'red')
        else:
            self.custom_info_dialog(master, "Information", "Please complete all required fields.\nDon't leave them empty.", 'lightgreen')

    def credit_amount(self,master,amt,accnt,name):
        if(self.is_number(amt)==0):
            self.custom_info_dialog(master, "Error", "Invalid Credentials\nPlease try again.", 'red')
            master.destroy()
            return
        
        #Old Passbook
        fdet=open(accnt+".txt",'r',encoding="utf-8")
        info=fdet.readlines()
        pin=info[0].strip()
        Ba=info[1].strip()
        camt=int(Ba[1:])
        fdet.close()
        
        #Updated Passbook
        cb=int(amt)+camt
        
        fdet=open(accnt+".txt",'w',encoding="utf-8")
        fdet.write(pin+"\n")
        fdet.write('₹'+str(cb)+"\n")
        fdet.write(accnt+"\n")
        fdet.write(name+"\n")
        fdet.close()

        # Transction Details
        frec=open(str(accnt)+"-rec.txt",'a+',encoding="utf-8")
        frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]     ",gmtime()))+'₹'+amt+"              "+"                   "+'₹'+str(cb)+"\n")
        frec.close()

        self.custom_info_dialog(master, "Operation Successfull!!","Amount Credited Successfully!!", 'Green')
        master.destroy()
        return

    def debit_amount(self,master,amt,accnt,name):
        if(self.is_number(amt)==0):
            self.custom_info_dialog(master,"Error","Invalid Credentials\nPlease try again.",'red')
            master.destroy()
            return
        f=open(str(accnt)+'.txt','r',encoding="utf-8")
        info=f.readlines()
        pin=info[0].strip()
        S_Ba=info[1].strip()
        Ba=int(S_Ba[1:])
        f.close()

        up_ba=Ba-int(amt)
        if int(amt)<=Ba:
            f=open(str(accnt)+'.txt','w',encoding="utf-8")
            f.write(pin+'\n')
            f.write('₹'+str(up_ba)+'\n')
            f.write(str(6)+'\n')
            f.write(name)
            f.close()

            frec=open(str(accnt)+"-rec.txt",'a+',encoding="utf-8")
            frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]     ",gmtime()))+"                "+'  ₹'+amt+'               '+'₹'+str(up_ba)+"\n")
            frec.close()
            self.custom_info_dialog(master,"Operation Successfull!!","Amount Debited Successfully!!",'Green')
            master.destroy()
        else:
            self.custom_info_dialog(master,"Error!!","You dont have that amount left in your account\nPlease try again.",'red')        

    def Display_Balance(self,accnt):
        fdet=open(accnt+".txt",'r',encoding="utf-8")
        info=fdet.readlines()
        bal=info[1].strip()
        fdet.close()
        self.app_instance.display_account_balance(bal)

    def Display_Transaction(self,accnt):
        frec = open(accnt + "-rec.txt", "r",encoding="utf-8")
        self.app_instance.display_transaction_history(frec)
        frec.close()

    def Home_Return(self, master):
        master.destroy()
        self.app_instance.root.deiconify()

    def logout(self,master):
        self.custom_info_dialog(master, "Logged Out", "You Have Been Successfully \nLogged Out!!!", 'pink2')
        master.destroy()
        self.app_instance.root.deiconify()

        
class App:
    def __init__(self,root):
        self.root = root
        self.root.geometry("900x500")
        self.root.title("Bank Management System")
        self.root.configure(background='pink3')
        self.bank = Bank(self)  # Pass the App instance to the Bank class
        self.create_main_menu()

    def create_main_menu(self):
        title = tk.Message(self.root, text="BANK MANAGEMENT SYSTEM", relief="raised", width=800,
                           padx=400, pady=0, fg="white", bg="blue4", justify="center",
                           anchor="center", font=("Verdana", "28", "bold"))
        title.pack(side="top")

        login_button = tk.Button(self.root, background='#0044cc', foreground='white', activebackground='#0077ff',
                                 activeforeground='gray', width=7, height=1, border=2, cursor='hand1',
                                 text='Login', font=('Arial', 15, 'bold'),
                                 command=self.log_in_menu)

        create_button = tk.Button(self.root, background='#4CAF50', foreground='white', activebackground='#66ff66',
                                  activeforeground='gray', width=18, height=1, border=4, cursor='hand1',
                                  text='Create New Account', font=('Arial', 15, 'bold'),
                                  command=self.create_account_menu)

        quit_button = tk.Button(self.root, bg='#990000', fg='white', activebackground='#ff0000',
                                width=7, height=1, border=2, cursor='hand1',
                                text='Quit', font=('Arial', 15, 'bold'), command=self.root.destroy)

        login_button.place(x=600, y=180)
        create_button.place(x=530, y=280)
        quit_button.place(x=600, y=380)

        self.root.mainloop()


    def log_in_menu(self):
        self.root.withdraw()
        loginwn = tk.Tk()
        loginwn.geometry("600x400")
        loginwn.title("Log in")
        loginwn.configure(bg="gray")
        title = tk.Message(loginwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=800,
                           padx=400, pady=0, fg="white", bg="blue1", justify="center",
                           anchor="center", font=("Arial", "18", "bold"))
        title.pack(side="top")
        l1 = tk.Label(loginwn, text="Enter Name:", font=("Times", 16), relief="raised")
        l1.pack(side="top")
        e1 = tk.Entry(loginwn)
        e1.pack(side="top")
        l2 = tk.Label(loginwn, text="Enter account number:", font=("Times", 16), relief="raised")
        l2.pack(side="top")
        e2 = tk.Entry(loginwn)
        e2.pack(side="top")
        l3 = tk.Label(loginwn, text="Enter your PIN:", font=("Times", 16), relief="raised")
        l3.pack(side="top")
        e3 = tk.Entry(loginwn, show="*")
        e3.pack(side="top")

        # Intercept the close event of the second window
        loginwn.protocol("WM_DELETE_WINDOW", lambda: self.bank.Home_Return(loginwn))
        
        b = tk.Button(loginwn, text="Submit", font=("Times", 14), relief="raised",
                      command=lambda: self.bank.check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
        b.pack(side="top")
        b1 = tk.Button(loginwn,text="HOME", font=("Times", 16), relief="raised", bg="blue4", fg="white",
                       command=lambda: self.bank.Home_Return(loginwn))
        b1.pack(side="top")
        loginwn.bind("<Return>",
                     lambda x: self.bank.check_log_in(loginwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
        

    def create_account_menu(self):
        crwn = tk.Tk()
        crwn.geometry("600x300")
        crwn.title("Create Account")
        crwn.configure(bg="#4CAF50")
        title = tk.Message(crwn, text="BANK MANAGEMENT SYSTEM", relief="raised", width=800,
                           padx=300, pady=0, fg="white", bg="blue4", justify="center",
                           anchor="center", font=("Arial", "28", "bold"))
        title.pack(side="top")
        l1 = tk.Label(crwn, text="Enter Name:", font=("Times", 12), relief="raised")
        l1.pack(side="top")
        e1 = tk.Entry(crwn)
        e1.pack(side="top")
        l2 = tk.Label(crwn, text="Enter opening credit:", font=("Times", 16), relief="raised")
        l2.pack(side="top")
        e2 = tk.Entry(crwn)
        e2.pack(side="top")
        l3 = tk.Label(crwn, text="Enter desired PIN:", font=("Times", 16), relief="raised")
        l3.pack(side="top")
        e3 = tk.Entry(crwn, show="*")
        e3.pack(side="top")
        b = tk.Button(crwn, text="Submit", font=("Times", 16),
                      command=lambda: self.bank.create_account(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))
        b.pack(side="top")
        crwn.bind("<Return>",
                  lambda event: self.bank.create_account(crwn, e1.get().strip(), e2.get().strip(), e3.get().strip()))

    def logged_in_menu(self, acc_num, name):
        rootwn=tk.Tk()
        rootwn.geometry("900x500")
        rootwn.title(" Bank | Welcome - "+name)
        rootwn.configure(background='Gray')
        fr1=tk.Frame(rootwn)
        fr1.pack(side="top")
        title=tk.Message(rootwn,text="BANK MANAGEMENT SYSTEM ",relief="raised",width=800,
                         padx=400,pady=0,fg="white",bg="blue4",justify="center",
                         anchor="center",font=("Verdana","25","bold"))
        title.pack(side="top")
        label=tk.Label(rootwn,text="Logged in as: "+name,relief="raised",bg="blue3",
                       font=("Times",16),fg="white",anchor="center",justify="center")
        label.pack(side="top")
        
        # Intercept the close event of the second window
        rootwn.protocol("WM_DELETE_WINDOW", lambda: self.bank.Home_Return(rootwn))


        b1 = tk.Button(rootwn, bg='#003366', fg='white', activebackground='#65e7ff',
                       activeforeground='gray', width=18, height=1, border=3, cursor='hand1',
                       text='Credit Amount', font=('Arial', 15, 'bold'),
                       command=lambda: self.credit_menu(acc_num,name))

        b2 = tk.Button(rootwn, bg='#008000', fg='white', activebackground='#66ff66',
                       activeforeground='gray', width=18, height=1, border=3, cursor='hand1',
                       text='Deposit Amount', font=('Arial', 15, 'bold'),
                       command=lambda: self.debit_menu(acc_num,name))

        b3 = tk.Button(rootwn, bg='#003366', fg='White', activebackground='lightblue',
                       activeforeground='White', width=13, height=1, border=3, cursor='hand1',
                       text='Show Balance', font=('Arial', 15, 'bold'),
                       command=lambda: self.bank.Display_Balance(acc_num))

        b4 = tk.Button(rootwn, bg='#3399FF', fg='BLACK', activebackground='#65e7ff',
                       activeforeground='BLACK', width=18, height=1, border=4, cursor='hand1',
                       text='Transaction History', font=('Arial', 15, 'bold'),
                       command=lambda: self.bank.Display_Transaction(acc_num))

        b5 = tk.Button(rootwn,bg="pink4",fg="white",activebackground="pink1",
                       activeforeground="gray4",width=13,height=1,border=3,
                       cursor='hand1',text='Logout',font=('Arial', 15, 'bold'),
                       command=lambda: self.bank.logout(rootwn))


            
        b1.place(x=100,y=150)
        b2.place(x=100,y=220)
        b3.place(x=628,y=150)
        b4.place(x=600,y=220)
        b5.place(x=390,y=380)

    def credit_menu(self,accnt,name):
        creditwn=tk.Tk()
        creditwn.geometry("500x300") 
        creditwn.title("Credit Amount")
        creditwn.configure(bg="#003366")
        fr1=tk.Frame(creditwn,bg="blue")
        title=tk.Message(creditwn,text="BANK MANAGEMENT SYSTEM",relief="raised",
                             width=800,padx=400,pady=0,fg="white",bg="blue4",justify="center",
                             anchor="center",font=("Arial","22","bold"))
        title.pack(side="top")
        l1=tk.Label(creditwn,relief="raised",font=("Times",17),text="Enter Amount to be credited: ")
        e1=tk.Entry(creditwn,relief="raised",font=10)
        l1.pack(side="top")
        e1.pack(side="top")
        b=tk.Button(creditwn,text="Credit",font=("Times",14),relief="raised",command=lambda:self.bank.credit_amount(creditwn,e1.get(),accnt,name))
        b.pack(side="top")
        creditwn.bind("<Return>",lambda x:self.bank.credit_amount(creditwn,e1.get(),accnt,name))


    def debit_menu(self,accnt,name):
        debitwn=tk.Tk()
        debitwn.geometry("500x300")
        debitwn.title("Debit Amount")
        debitwn.configure(bg="#008000")
        fr1=tk.Frame(debitwn,bg="blue")
        title=tk.Message(debitwn,text="BANK MANAGEMENT SYSTEM",relief="raised",width=800,
                         padx=400,pady=0,fg="white",bg="blue4",justify="center",
                         anchor="center",font=("Arial","22","bold"))
        title.pack(side="top")
        l1=tk.Label(debitwn,relief="raised",font=("Times",17),text="Enter Amount to be debited: ")
        e1=tk.Entry(debitwn,relief="raised",font=10)
        l1.pack(side="top")
        e1.pack(side="top")
        b=tk.Button(debitwn,text="Debit",font=("Times",14),relief="raised",command=lambda:self.bank.debit_amount(debitwn,e1.get(),accnt,name))
        b.pack(side="top")
        debitwn.bind("<Return>",lambda x:self.bank.debit_amount(debitwn,e1.get(),accnt,name))

    def display_account_balance(self,bal):
        rw=tk.Tk()
        rw.geometry("370x250")
        rw.configure(bg="SteelBlue")
        rw.title("Show Balance")
        L=tk.Label(rw,text="Balance:\n"+bal,bg="gray",fg="Black",font=10)
        L.place(x=140,y=80)
        rw.mainloop()

    def display_transaction_history(self,frec):
        disp_wn = tk.Tk()
        disp_wn.geometry("700x500") 
        disp_wn.title("Transaction History")
        disp_wn.configure(bg="Black")

        title = tk.Message(disp_wn,text="BANK MANAGEMENT SYSTEM",relief="raised",
                           width=800,padx=400,pady=0,fg="white",bg="blue4",
                           justify="center",anchor="center",font=("Arial", "20", "bold"))
        title.pack(side="top")

        l1 = tk.Message(disp_wn,text="Your Transaction History:",font=("Times", 16),
                        padx=100,pady=10,width=600,bg="blue4",fg="SteelBlue1",relief="raised",)
        l1.pack(side="top")

        history_text = ScrolledText(
            disp_wn, wrap=tk.WORD, width=80, height=20, relief="raised"
        )
        for hist in frec:
            history_text.insert(tk.END, hist)
            history_text.pack(side="top")

        b = tk.Button(disp_wn, text="Quit", relief="raised", command=disp_wn.destroy,font=10)
        b.pack(side="top")

        disp_wn.mainloop()


if __name__ == "__main__":
    root=tk.Tk()
    app = App(root)
    root.mainloop()
