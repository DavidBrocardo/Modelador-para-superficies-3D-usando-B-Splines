import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox


class Interface:

    def __init__(self, tela):
        self.tela = tela
        self.tela.title("B-Splines")      

        self.canvas = tk.Canvas(tela, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)
        self.button_frame = tk.Frame(tela)
        self.button_frame.pack()


        self.btn_sair = tk.Button(self.button_frame, text="Sair", command=tela.destroy, bg="red")
        self.btn_sair.grid(row=0, column=2, padx=5)           
    

        

    

tkk = tk.Tk()
app = Interface(tkk)
tkk.mainloop()


