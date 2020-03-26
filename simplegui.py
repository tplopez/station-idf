from tkinter import *


window = Tk()
# window.geometry('350x200')
window.title("Historical IDF Curves")

f1 = Frame(width=350, height=200, background="gray")
f2 = Frame(width=325, height=175)

f1.pack(fill="both", expand=True, padx=20, pady=20)
f2.place(in_=f1, anchor="c", relx=.5, rely=.5)

# S = tk.Scrollbar(window)
# T = tk.Text(window, height=4, width=50).grid(row=0, columnspan=2)

# S.config(command=T.yview)
# T.config(yscrollcommand=S.set)
# quote = """This is a very simple tool to see
# the output from constructIDF """
# T.insert(tk.END, quote)


window.title("Historical IDF Curves")
lbl = Label(f2, text='This is a very simple GUI to display IDF')
lbl2 = Label(f2, text='Input the required fields (*)')
lbl.grid(columnspan=2)
lbl2.grid(row=2, columnspan=2)
Label(f2, text="File path*").grid(row=3)  # this is placed in 0 0
Entry(f2).grid(row=3, column=1)  # this is placed in 0 1
Label(f2, text="Save path*").grid(row=4)  # this is placed in 0 0
Entry(f2).grid(row=4, column=1)

btn = Button(f2, text="Click Me")  # , #command=clicked)

btn.grid(row=5, columnspan=2)
window.mainloop()
# from tkinter import *

# window = Tk()

# window.title("Historical IDF Curves")

# window.geometry('350x200')

# lbl = Label(window, text="Hello")

# lbl.grid(column=0, row=0)

# txt = Entry(window, width=10)

# txt.grid(column=1, row=0)


# def clicked():

#     lbl.configure(text="Button was clicked !!")


# btn = Button(window, text="Click Me", command=clicked)

# btn.grid(column=2, row=0)

# window.mainloop()
