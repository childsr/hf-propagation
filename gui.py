import tkinter as tk

def say_hello():
    label.config(text="Hello, World!")

root = tk.Tk()
root.title("Simple GUI")
root

label = tk.Label(root, text="Click the button")
label.pack()

button = tk.Button(root, text="Click Me", command=say_hello)
button.pack()

root.mainloop()
