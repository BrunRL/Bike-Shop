from tkinter import Label, Entry

def create_label(parent, text):
    label = Label(parent, text=text)
    label.pack()
    return label

def create_entry(parent, show=None):
    entry = Entry(parent, show=show)
    entry.pack()
    return entry

