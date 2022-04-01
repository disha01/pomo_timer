import imp
from tkinter import *
import math
import time

 # import required module
from playsound import playsound
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
PURPLE="#D8BFD8"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"
reps = 0
timer = None

#--------------------clock------------------------
def digital_clock(): 
   time_live = time.strftime("%H:%M:%S")
   label.config(text=time_live) 
   label.after(200, digital_clock)


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    '''resets the timer to 00:00'''
    global reps

    root.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks_label.config(text="")
    reps = 0


# ---------------------------- TIMER AND BREAKS ------------------------------- # 
def start_timer():
    ''' convert minute to seconds and check text according to timer'''
    global reps
    reps += 1

    # Convert minutes to seconds
    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    # Check how much time to count down
    if reps % 8 == 0:
        count_down(long_break_seconds)
        title_label.config(text="Break",fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_seconds)
        title_label.config(text="Break",fg=RED)
    else:
        count_down(work_seconds)
        title_label.config(text="Work",fg="black")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    '''
    convert the time passed into  minutes and seconds
    present the time string on screen and play sound as time get over 
    '''
    count_minutes = math.floor(count / 60)
    count_seconds = count % 60

    if count_seconds<10:
        count_seconds = f"0{count_seconds}"

    # timer canvas text
    canvas.itemconfig(timer_text, text=f"{count_minutes}:{count_seconds}")

    # Check if the timer value greater than 0.
    if count > 0:
        global timer
        timer = root.after(1000, count_down, count - 1)
    else:
        # Start the next timer
        start_timer()
        playsound('this.mp3')
        print('playing sound using playsound')
        # Add check mark
        marks = ""
        work_session = math.floor(reps / 2)

        for _ in range(work_session):
            marks += CHECK_MARK
        check_marks_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
# root SETUP
'''creating a resizable window with background '''
root = Tk()
root.title("Pomodoro")
root.config(padx=100, pady=50, bg=PURPLE)
root.resizable(True, True)

# Create Canvas
'''add a image on backgroung'''
canvas = Canvas(width=300, height=304, bg=PURPLE, highlightthickness=0)  # highlightthickness removes the canvas border
tomato_img = PhotoImage(file="one.png")

# Add tomato image and text
'''create a canvas to display timer'''
canvas.create_image(200, 200, image=tomato_img)
timer_text = canvas.create_text(160, 160, text="00:00", fill="black", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Add Title Label
title_label = Label()
title_label.config(text="pomo-Timer", font=(FONT_NAME, 50), fg="black", bg=PURPLE)
title_label.grid(column=1, row=0)
#----------------------for clock------------
#top=Toplevel()
'''create a frame to display clock '''
F1=Frame(root,borderwidth=10,bg="black")
F1.grid(row=0,column=66)
label = Label(F1, font=FONT_NAME, bg="black", fg=PURPLE) 
label.grid(row=0, column=30)
digital_clock()

# Add start and reset button
start_button = Button(text="Start",fg="white", bg="black", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=4)

reset_button = Button(text="Reset", fg="white",bg="black", highlightthickness=0, command=reset_timer)
reset_button.grid(column=22, row=4)

# Add check marks Label
check_marks_label = Label(font=(FONT_NAME, 21), bg=PURPLE, fg="black")
check_marks_label.grid(column=1, row=3)
#------------------------drop down timer menu-----------------------
def show():
    ''' function to create timer of different time interval '''
    text=clicked.get()
    text=text*60   #given the fact user enter time in minutes 
    count_down(text)


#variable that set default drop down
clicked=IntVar()
clicked.set(25)
#create a drop down
#drop=OptionMenu(root,clicked,5,10,15,20,30,35,40,45)
#drop.grid(F2)

#menu_button=Button(F2,text="select time",command=show)
#menu_button.grid(column=22,row=5)


#-------------------------------------todolist-----------------------------------------

# Initializing the python to do list GUI window
def list():
    '''create a list to write your things 
    add and deltere buttons and scroll bar'''
    r = Toplevel()
    r.title('enter your routine')
    r.geometry('300x400')
    r.resizable(0, 0)
    r.config(bg=PURPLE)

# Heading Label
    Label(r, text='To Do List', bg=PURPLE, font=("Comic Sans MS", 15), wraplength=300).place(x=35, y=0)

# Listbox with all the tasks with a Scrollbar
    tasks = Listbox(r, selectbackground='Gold', bg='Silver', font=('Helvetica', 12), height=12, width=25)

    scroller = Scrollbar(r, orient=VERTICAL, command=tasks.yview)
    scroller.place(x=260, y=50, height=232)

    tasks.config(yscrollcommand=scroller.set)

    tasks.place(x=35, y=50)

# Adding items to the Listbox
    with open('tasks.txt', 'r+') as tasks_list:
        for task in tasks_list:
            tasks.insert(END, task)
        tasks_list.close()

# Creating the Entry widget where the user can enter a new item
    new_item_entry = Entry(r, width=37)
    new_item_entry.place(x=35, y=310)

# Creating the Buttons
    add_btn = Button(r, text='Add Item', bg="black",fg="white", width=10, font=('Helvetica', 12),
                     command=lambda: add_item(new_item_entry, tasks))
    add_btn.place(x=45, y=350)

    delete_btn = Button(r, text='Delete Item', bg="black",fg="white", width=10, font=('Helvetica', 12),
                     command=lambda: delete_item(tasks))
    delete_btn.place(x=150, y=350)

# Adding and Deleting items functions
    def add_item(entry: Entry, listbox: Listbox):
        '''to add element in list'''
        new_task = entry.get()

        listbox.insert(END, new_task)

        with open('tasks.txt', 'a') as tasks_list_file:
            tasks_list_file.write(f'\n{new_task}')


    def delete_item(listbox: Listbox):
        '''to delete elements'''
        listbox.delete(ACTIVE)

        with open('tasks.txt', 'r+') as tasks_list_file:
            lines = tasks_list_file.readlines()
            
            #tasks_list_file.truncate()
            del lines[1]
            tasks_list_file.truncate(0) #set file size to 0 byte basically clears it
            tasks_list_file.close()
           


    
# Finalizing the window

    r.mainloop()

#a frame for time and list
F2=Frame(root,width=500,height=500,borderwidth=10,bg="black")
F2.grid(row=1,column=66)
F3 = Frame(F2,bg=PURPLE,width=100,height=100)
F3.grid(row=0,column=0)
#F4 = Frame(F2,bg=PURPLE,width=100,height=100)
#F4.grid(row=6,column=0)

#button that open the todo list    
list_button = Button(F3,text="to-do", command=list,padx=25,pady=10,bg="black",fg="white")
list_button.grid(column=22, row=1)

#create a drop down---------------------
'''create a drop down menu for changable timer'''
drop=OptionMenu(F3,clicked,2,5,10,15,20,30,35,40,45)
drop.config(bg="black",fg="white")
drop.grid(column=22,row=5,padx=10,pady=10)
#button for drop down menu-----------------------
menu_button=Button(F3,text="set timer",command=show,padx=30,pady=10,bg="black",fg="white")
menu_button.grid(column=22,row=7,padx=20,pady=10)

#----------------------dark/light mode----------------
button_mode=True
def custom():
    '''function that change light mode to dark mode and vice versa
    basically toggle the drk/light theme'''
    global button_mode
    if button_mode:
        Button_toggle.config(image=off,bg="#26242f",activebackground="#26242f")
        root.config(bg="#26242f")
        canvas.config(bg="#26242f")
        title_label.config( font=(FONT_NAME, 50), fg="black", bg="#26242f")
        check_marks_label.config(bg="#26242f")
        button_mode=False
    else:
        Button_toggle.config(image=on,bg=PURPLE,activebackground=PURPLE)
        root.config(bg=PURPLE)
        check_marks_label.config(bg=PURPLE)
        title_label.config( font=(FONT_NAME, 50), fg="black", bg=PURPLE)
        button_mode=True    
#on=open("download.png")

on=PhotoImage(file="download.png")
#on=on.resize((20,20))
off=PhotoImage(file="light-mode.png")

Button_toggle=Button(root,image=on,bg="white",bd=0,activebackground="white",command=custom)
Button_toggle.grid(row=0,column=0)


root.mainloop()