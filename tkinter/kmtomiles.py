import tkinter as tk
from tkinter import ttk
def convert():
    miles = entry_int.get()
    km = miles * 1.61
    output_string.set(km)

# window
window = tk.Tk()
window.geometry('320x300')
window.title("First")


#label
label = ttk.Label(window,text="Miles to KM",font=('arial',18,'bold'))
label.pack(pady=1)

# making a frame
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable = entry_int)
button = ttk.Button(master = input_frame,text="convert", command= convert)

# now pack all the entry and button inside frame


entry.pack(side='left',padx=10)
button.pack(side='left')
input_frame.pack(pady=10)

#output label

output_string = tk.StringVar()
output_label = ttk.Label(
    master=window,
    text="sample" ,
    font=('calibiry', 18),
    textvariable = output_string
                        )
output_label.pack(pady=20)

#mainloop
window.mainloop()