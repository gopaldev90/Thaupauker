import tkinter as tk
from tkinter import filedialog
import copy
import json
import os, time, platform

if platform.system() == 'Linux':
    import sys
    sys.path.append('/storage/emulated/0/pvz2/plant 1000 bnao/Tool/')
    
import Aftkr

class PVZ2App:
    def __init__(self, root):
        self.root = root
        self.phone = platform.system() == 'Linux'
        self.modifier = Aftkr.PVZ2Modifier()
        self.file_path = self.data = self.saveto = self.paun_folder = self.oldtaton = self.taton = None
        self.initisetxt()
        # Initialize the GUI
        self.init_gui()
        
    def initisetxt(self):
    	self.khojtxt = "Khoj"
    	self.confirmtxt = "Pushti krain"
    	self.grouptxt = "Grout update"
    
    
    
    def init_gui(self):
        self.pragati = tk.Label(self.root, text="", fg="green")
        self.pragati.place(relx=0.5, rely=0.58, anchor=tk.CENTER)

        button = tk.Button(self.root, text="Select JSON File", fg='white', bg='green', command=self.open_file_dialog)
        button.pack(pady=20)

        self.sablgbtn = tk.Button(self.root, text="Sab Alag", command=self.sabalag)
        self.sablgbtn.config(state=tk.DISABLED)
        self.sablgbtn.place(relx=0.20, rely=0.18, anchor=tk.CENTER)

        self.sabkmbtn = tk.Button(self.root, text="Sab Ekam", command=self.ekmsb)
        self.sabkmbtn.config(state=tk.DISABLED)
        self.sabkmbtn.place(relx=0.5, rely=0.29, anchor=tk.CENTER)

        self.rerechbtn = tk.Button(self.root, text="0 Cooldown", command=self.zeromana)
        self.rerechbtn.config(state=tk.DISABLED)
        self.rerechbtn.place(relx=0.5, rely=0.38, anchor=tk.CENTER)

        self.khojbtn = tk.Button(self.root, text=self.khojtxt, command=self.khojklk)
        self.khojbtn.config(state=tk.DISABLED)
        self.khojbtn.place(relx=0.73, rely=0.18, anchor=tk.CENTER)

        self.Tatonbox = tk.Entry(self.root)
        self.Tatonbox.pack()
        self.Tatonbox.bind("<KeyRelease>", self.textbdla)

        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self.root, text="Change PFPC", variable=self.checkbox_var)
        self.checkbox.place(relx=0.5, rely=0.69, anchor=tk.CENTER)
        self.checkbox.config(state=tk.DISABLED)

        self.Staus = tk.Label(self.root, text="")
        self.Staus.place(relx=0.5, rely=0.49, anchor=tk.CENTER)
        
        self.stm = tk.Label(self.root, text='Made in Bharat')
        self.stm.place(relx=0.5, rely=0.98, anchor=tk.CENTER)
        
        self.root.resizable(False, False)
        self.root.geometry("400x400")
        
        if self.phone:
            self.open_file_dialog(True)
    
    def open_file_dialog(self,auto=False):
        if ((not self.phone)or(not auto)):
            self.file_path = filedialog.askopenfilename(
                title="Select a JSON file",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
        else:
            self.file_path = '/storage/emulated/0/pvz2/plant 1000 bnao/Tool/PlantLevels.json'
        
        if self.file_path:
            self.saveto = os.path.dirname(self.file_path) + "/Edited/"
            self.sabkmbtn.config(state=tk.NORMAL)
            self.khojbtn.config(state=tk.NORMAL)
            self.sablgbtn.config(state=tk.NORMAL)
            self.rerechbtn.config(state=tk.NORMAL)
            self.setdata()
    
    def setdata(self):
        with open(self.file_path, 'r') as file:
            ndata = json.load(file)
        self.data = copy.deepcopy(ndata)
    
    def startfindnam(self, name):
        tmp = self.modifier.gettaton(self.data, name)
        if tmp >= 0:
            self.Tatonbox.delete(0, tk.END)
            self.Tatonbox.insert(tk.END, tmp)
            self.khojbtn.config(text=self.khojtxt)
            self.khojklk()
        else:
            self.Staus.config(text="Aisa koi paudha nhin h",fg='red')
    
    def zeromana(self):
        st = time.time()
        self.sablgbtn.config(state=tk.DISABLED)
        self.sabkmbtn.config(state=tk.DISABLED)
        self.rerechbtn.config(state=tk.DISABLED)
        self.data = self.modifier.zeromana(self.data, self.pragati, self.root)
        self.modifier.savejson(self.saveto, "0 Cooldown", self.data, True)
        self.setdata()
        ed = time.time()
        lga = ed - st
        self.Staus.config(text=f"samay lga zero mana\n karne main seconds: {lga}")

    def sabalag(self):
        st = time.time()
        self.sablgbtn.config(state=tk.DISABLED)
        self.sabkmbtn.config(state=tk.DISABLED)
        self.modifier.sabalaga(self.data, self.saveto, self.pragati, self.root)
        self.setdata()
        ed = time.time()
        lga = ed - st
        self.Staus.config(text=f"samay lga sab \n alag karne main seconds: {lga}")

    def ekmsb(self):
        self.sabkmbtn.config(state=tk.DISABLED)
        self.sablgbtn.config(state=tk.DISABLED)
        st = time.time()
        self.modifier.ekamsab(self.data, self.saveto, self.pragati, self.root)
        self.setdata()
        endm = time.time()
        lga = endm - st
        self.Staus.config(text=f"samay lga sab \n ek karne main seconds: {lga}")

    def khojklk(self):
        Seema = self.modifier.getSeema(self.data)
        try:
            if self.khojbtn.cget("text") == self.confirmtxt:
                st = time.time()
                self.paun_folder = self.Staus.cget('text')
                if self.paun_folder == self.grouptxt:
                    sf = "group"
                    self.data = self.modifier.groupupdate(self.data, self.checkbox_var.get(), self.taton)
                else:
                    sf = f"{str(self.taton)}.{self.paun_folder}"
                    self.data = self.modifier.update_json(self.taton, self.data, self.checkbox_var.get(), self.paun_folder)
                    self.data["#vyakhya"] = f"{self.paun_folder} Hacked by Pvz2pagalpan Id: {self.taton}"
                self.data["#Kab"] = self.modifier.getcurtime()
                self.modifier.savejson(self.saveto, sf, self.data, True)
                lga = time.time() - st
                self.setdata()
                self.Staus.config(text=f"{self.paun_folder} Successfully \n hacked in {lga} seconds")
                self.sabkmbtn.config(state=tk.DISABLED)
                self.sablgbtn.config(state=tk.DISABLED)
                self.khojbtn.config(text=self.khojtxt)
            else:
                self.taton = self.Tatonbox.get()
                if not self.taton.isdigit() and "," not in self.taton:
                    self.startfindnam(self.taton)
                elif "," in self.taton:
                    self.taton = [int(i) for i in self.taton.split(',')]
                    if any(not (0 <= i <= Seema) for i in self.taton):
                        raise ValueError(f"Koi number seema se paar Seema: {Seema}")
                    self.Staus.config(text=self.grouptxt)
                    self.khojbtn.config(text=self.confirmtxt)
                    self.checkbox.config(state=tk.NORMAL)
                else:
                    self.taton = int(self.taton)
                    if not (0 <= self.taton <= Seema):
                        raise ValueError(f"Seema se paar. Seema: {Seema}")
                    else:
                        self.oldtaton = self.taton
                        self.Staus.config(text=self.modifier.naamde(self.data, self.taton))
                        self.khojbtn.config(text=self.confirmtxt)
                        self.checkbox.config(state=tk.NORMAL)
        except Exception as e:
            v=0
            if v:
            	raise Exception(e)
            self.Staus.config(text=f"Gadbad hai: {e}",fg='red')

    def textbdla(self, event):
        try:
            taton = int(self.Tatonbox.get())
            self.khojbtn.config(text=self.khojtxt)
            self.khojklk()
            
        except ValueError:
            self.khojbtn.config(text=self.khojtxt)

if __name__ == "__main__":
    root = tk.Tk()
    app = PVZ2App(root)
    root.mainloop()
    