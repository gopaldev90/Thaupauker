import tkinter as tk
from tkinter import filedialog
import copy
import json
import os, time, platform

if platform.system()=='Linux':
    import sys
    sys.path.append('/storage/emulated/0/pvz2/plant 1000 bnao/Tool/')
    
import Aftkr

root = tk.Tk()

# Create an instance of the PVZ2Modifier class
modifier = Aftkr.PVZ2Modifier()

def startfindnam(data):
    name = Tatonbox.get()
    tmp = modifier.gettaton(data, name)
    if tmp >= 0:
        Tatonbox.delete(0, tk.END)
        Tatonbox.insert(tk.END, tmp)
        khojbtn.config(text="Khoj")
        khojklk()
    else:
        Staus.config(text="Aisa koi paudha nhin h")

def sabalag(pragati, root):
    st = time.time()
    sablgbtn.config(state=tk.DISABLED)
    sabkmbtn.config(state=tk.DISABLED)
    global data
    global saveto
    global file_path
    st = time.time()
    modifier.sabalaga(data, saveto, pragati, root)
    setdata(file_path)
    ed = time.time()
    lga = ed - st
    Staus.config(text=f"samay lga sab \n alag karne main seconds: {lga}")

def khojklk():
    global data, taton, paun_folder, saveto, oldtaton, file_path
    Seema = modifier.getSeema(data)
    try:
        if khojbtn.cget("text") == "Confirm":
            st = time.time()
            paun_folder = Staus.cget('text')
            data = modifier.update_json(taton, data, checkbox_var.get(), paun_folder)
            data["#vyakhya"] = f"{paun_folder} Hacked by Pvz2pagalpan Id: {taton}"
            data["#Kab"]= modifier.getcurtime()
            
            modifier.savejson(saveto, f"{str(taton)}.{paun_folder}", data)
            lga = time.time() - st
            setdata(file_path)
            Staus.config(text=f"{paun_folder} Successfully \n hacked in {lga} seconds")
            sabkmbtn.config(state=tk.DISABLED)
            sablgbtn.config(state=tk.DISABLED)
            khojbtn.config(text="Khoj")
        else:
            taton = Tatonbox.get()
            if not taton.isdigit():
                startfindnam(data)
            else:
                taton = int(taton)
                if not (0 <= taton <= Seema):
                    raise ValueError(f"Seema se paar. Seema: {Seema}")
                else:
                    oldtaton = taton
                    Staus.config(text=modifier.naamde(data, taton))
                    khojbtn.config(text="Confirm")
                    checkbox.config(state=tk.NORMAL)
    except Exception as e:
        #raise ValueError(e)
        Staus.config(text=f"Gadbad hai: {e}")

def ekmsb(pragati, root):
    sabkmbtn.config(state=tk.DISABLED)
    sablgbtn.config(state=tk.DISABLED)
    global data, saveto, file_path
    st = time.time()
    modifier.ekamsab(data, saveto, pragati, root)
    setdata(file_path)
    endm = time.time()
    lga = endm - st
    Staus.config(text=f"samay lga sab \n ek karne main seconds: {lga}")

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if file_path:
        global saveto
        saveto = os.path.dirname(file_path) + "/Edited/"
        sabkmbtn.config(state=tk.NORMAL)
        khojbtn.config(state=tk.NORMAL)
        sablgbtn.config(state=tk.NORMAL)
        setdata(file_path)
      
def setdata(file_path):
    global data
    with open(file_path, 'r') as file:
        ndata = json.load(file)
    data = copy.deepcopy(ndata)
    
def textbdla(event):
    try:
        global oldtaton
        taton = int(Tatonbox.get())
        if taton != oldtaton:
            khojbtn.config(text="Khoj")
        else:
            khojbtn.config(text="Confirm")
    except Exception as e:
        khojbtn.config(text="Khoj")

pragati = tk.Label(root, text="", fg="green")
pragati.place(relx=0.5, rely=0.56, anchor=tk.CENTER)

button = tk.Button(root, text="Select JSON File", command=open_file_dialog)
button.pack(pady=20)

sablgbtn = tk.Button(root, text="Sab Alag", command=lambda: sabalag(pragati, root))
sablgbtn.config(state=tk.DISABLED)
sablgbtn.place(relx=0.20, rely=0.18, anchor=tk.CENTER)

sabkmbtn = tk.Button(root, text="Sab Ekam", command=lambda: ekmsb(pragati, root))
sabkmbtn.config(state=tk.DISABLED)
sabkmbtn.place(relx=0.5, rely=0.29, anchor=tk.CENTER)

khojbtn = tk.Button(root, text="Khoj", command=khojklk)
khojbtn.config(state=tk.DISABLED)
khojbtn.place(relx=0.73, rely=0.18, anchor=tk.CENTER)

Tatonbox = tk.Entry(root)
Tatonbox.pack()
Tatonbox.bind("<KeyRelease>", textbdla)

checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="Change PFPC", variable=checkbox_var)
checkbox.place(relx=0.5, rely=0.63, anchor=tk.CENTER)
checkbox.config(state=tk.DISABLED)

Staus = tk.Label(root, text="")
Staus.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

root.resizable(False, False)
root.geometry("400x400")
root.mainloop()
