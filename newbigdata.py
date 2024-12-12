import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()
connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

# Creating the functions
def reset_fields():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())

def reset_form():
    global tree
    tree.delete(*tree.get_children())
    reset_fields()

def display_records():
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)

def add_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()
    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute(
                'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Please note that the contact field can only contain numbers')

def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
        display_records()

def view_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
    if not tree.selection():
        mb.showerror('Error!', 'Please select a record to view')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1])
        email_strvar.set(selection[2])
        contact_strvar.set(selection[3])
        gender_strvar.set(selection[4])
        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
        dob.set_date(date)
        stream_strvar.set(selection[6])

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == 'admin' and password == 'password':
        # Hide the login page and show the main window
        login_frame.pack_forget()
        main_window.pack(fill=BOTH, expand=True)
    else:
        mb.showerror('Error', 'Invalid username or password')

# Initializing the GUI window
main_window = Frame(width=1000, height=600)
main_window.pack_forget()

# Creating the login page
login_frame = Frame(width=1000, height=600, bg='DarkGreen')  # Set background color to dark green
login_frame.pack(fill=BOTH, expand=True)

# Creating a frame for the login background panel
login_panel_frame = Frame(login_frame, bg='LightSkyBlue', width=400, height=300)
login_panel_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centered the panel

# Creating a frame for the login form
login_form_frame = Frame(login_panel_frame, bg='SpringGreen')
login_form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centered the form

# Adding a title label
Label(login_form_frame, text="Login", font=headlabelfont, bg='SpringGreen', fg='Dark Green').grid(row=0, column=0, columnspan=2, pady=20)

# Creating the username and password labels and entries
username_label = Label(login_form_frame, text="Username", font=labelfont, bg='SpringGreen')
username_label.grid(row=1, column=0, padx=10, pady=10)
password_label = Label(login_form_frame, text="Password", font=labelfont, bg='SpringGreen')
password_label.grid(row=2, column=0, padx=10, pady=10)

username_entry = Entry(login_form_frame, width=19, font=entryfont)
username_entry.grid(row=1, column=1, padx=10, pady=10)
password_entry = Entry(login_form_frame, width=19, font=entryfont, show='*')
password_entry.grid(row=2, column=1, padx=10, pady=10)

# Creating the login button
login_button = Button(login_form_frame, text='Login', font=labelfont, command=login, width=18, bg='DarkGreen', fg='LightCyan', activebackground='DarkGreen', activeforeground='LightCyan')
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Placing components in the main window
Label(main_window, text="STUDENT MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)
left_frame = Frame(main_window, bg='MediumSpringGreen')
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main_window, bg='PaleGreen')
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main_window, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg='MediumSpringGreen').place(relx=0.375, rely=0.05)
Label(left_frame, text="Contact Number", font=labelfont, bg='MediumSpringGreen').place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Address", font=labelfont, bg='MediumSpringGreen').place(relx=0.2, rely=0.31)
Label(left_frame, text="Gender", font=labelfont, bg='MediumSpringGreen').place(relx=0.3, rely=0.44)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg='MediumSpringGreen').place(relx=0.1, rely=0.57)
Label(left_frame, text="Stream", font=labelfont, bg='MediumSpringGreen').place(relx=0.3, rely=0.7)

name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)

Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).grid(row= 0, column=0, padx=10, pady=10)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).grid(row=1, column=0, padx=10, pady=10)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).grid(row=2, column=0, padx=10, pady=10)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).grid(row=3, column=0, padx=10, pady=10)

# Placing components in the right frame
Label(right_frame, text='Students Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.pack(fill=BOTH, expand=True)

display_records()

# Finalizing the GUI window
main_window.mainloop()