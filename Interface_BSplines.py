import tkinter as tk
from tkinter import simpledialog, messagebox
from Superfice_BSplines import BSplines
import random

class Interface:
    def __init__(self, tela, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, espacamento, VRP, P, Y, dp, windows, viewport):
        self.tela = tela        
        self.tela.title("Superfície Spline")
        self.tela.geometry("600x600")

        self.canvas = tk.Canvas(self.tela, width=500, height=500, bg="white")
        self.canvas.pack(pady=10)

        # Parâmetros
        self.pontos_controleX = pontos_controleX
        self.pontos_controleY = pontos_controleY
        self.TI = TI
        self.TJ = TJ
        self.RESOLUTIONI = RESOLUTIONI
        self.RESOLUTIONJ = RESOLUTIONJ
        self.espacamento = espacamento
        self.VRP = VRP
        self.P = P
        self.Y = Y
        self.dp = dp
        self.windows = windows
        self.viewport = viewport
        self.inp = []
        self.outp = []

        # Criar interface
        self.criar_menu()
        self.main()

    def criar_menu(self):
        """Cria a barra de menu suspenso."""
        menu_principal = tk.Menu(self.tela)

        # Menu Superfice
        menu_superfice = tk.Menu(menu_principal, tearoff=0)
        menu_superfice.add_command(label="Pontos de Controle", command=self.definir_ponto_controle)
        menu_superfice.add_command(label="Tamanho da Matrix", command=self.definir_tamanho_matriz)
        menu_superfice.add_command(label="Camera", command=self.salvar_arquivo)
        menu_superfice.add_command(label="Viewport", command=self.salvar_arquivo)
        menu_superfice.add_command(label="Windows", command=self.salvar_arquivo)
        menu_principal.add_cascade(label="Superfice", menu=menu_superfice)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label="Abrir", command=self.abrir_arquivo)
        menu_arquivo.add_command(label="Salvar", command=self.salvar_arquivo)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.sair, accelerator="Ctrl+Q")
        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Pintura
        menu_editar = tk.Menu(menu_principal, tearoff=0)
        menu_editar.add_command(label="Copiar")
        menu_editar.add_command(label="Colar")
        menu_principal.add_cascade(label="Editar", menu=menu_editar)

        # Menu Sobreamento

        self.tela.config(menu=menu_principal)
        self.tela.bind_all("<Control-q>", lambda event: self.sair())

    def abrir_arquivo(self):
        messagebox.showinfo("Abrir", "Abrindo arquivo...")

    def salvar_arquivo(self):
        messagebox.showinfo("Salvar", "Salvando arquivo...")

    def sair(self):
        self.tela.quit()

    def definir_ponto_controle(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Ponto de Controle")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=0, column=1)

        tk.Label(janela, text="Y:").grid(row=1, column=0)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=2, column=0)
        entrada_z = tk.Entry(janela)
        entrada_z.grid(row=2, column=1)

        #tk.Button(janela, text="Salvar", command=salvar_ponto).grid(row=3, columnspan=2)

    def definir_tamanho_matriz(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Tamanho da Matriz")

        tk.Label(janela, text="Linhas (X):").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=0, column=1)

        tk.Label(janela, text="Colunas (Y):").grid(row=1, column=0)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        def Salvar():
            self.pontos_controleX =  entrada_x
            self.pontos_controleY =  entrada_y
            self.criar_pontos_controle()                       
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX, self.pontos_controleY, self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            self.inp, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=2)

    def definir_windows(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Tamanho da Matriz")

        tk.Label(janela, text="Linhas (X):").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=0, column=1)

        tk.Label(janela, text="Colunas (Y):").grid(row=1, column=0)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        


    def definir_viewport(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Tamanho da Matriz")

        tk.Label(janela, text="Linhas (X):").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=0, column=1)

        tk.Label(janela, text="Colunas (Y):").grid(row=1, column=0)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)


    def definir_camera(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Tamanho da Matriz")

        tk.Label(janela, text="Linhas (X):").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=0, column=1)

        tk.Label(janela, text="Colunas (Y):").grid(row=1, column=0)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)








    def criar_pontos_controle(self):
        """Cria a matriz de pontos de controle."""
        self.inp = []
        for i in range(self.pontos_controleX + 1):
            linha = []
            for j in range(self.pontos_controleY + 1):
                x = i * self.espacamento
                y = j * self.espacamento
                z = random.uniform(-10, 10)  # Altura aleatória
                linha.append([x, y, z])
            self.inp.append(linha)

    def desenhar_superficie(self):
        """Desenha a superfície B-Spline no Canvas."""
        self.canvas.delete("all")
        escala = 1
        deslocamento_x, deslocamento_y = 50, 250  # Ajuste para centralizar

        # Desenha os pontos de controle
        for i in range(self.pontos_controleX + 1):
            for j in range(self.pontos_controleY + 1):
                x = deslocamento_x + self.inp[i][j][0] * escala
                y = deslocamento_y - self.inp[i][j][2] * escala
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")

        # Desenha a superfície usando linhas
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                x1, y1 = deslocamento_x + self.outp[i][j][0] * escala, deslocamento_y - self.outp[i][j][2] * escala
                x2, y2 = deslocamento_x + self.outp[i][j+1][0] * escala, deslocamento_y - self.outp[i][j+1][2] * escala
                x3, y3 = deslocamento_x + self.outp[i+1][j+1][0] * escala, deslocamento_y - self.outp[i+1][j+1][2] * escala
                x4, y4 = deslocamento_x + self.outp[i+1][j][0] * escala, deslocamento_y - self.outp[i+1][j][2] * escala
                
                self.canvas.create_line(x1, y1, x2, y2, fill="black")
                self.canvas.create_line(x2, y2, x3, y3, fill="black")
                self.canvas.create_line(x3, y3, x4, y4, fill="black")
                self.canvas.create_line(x4, y4, x1, y1, fill="black")

    def main(self):
        """Executa os cálculos e desenha a superfície."""
        self.criar_pontos_controle()
        
        # Calcula a superfície B-Spline
        bspline = BSplines(self.pontos_controleX, self.pontos_controleY, self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                           self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
        self.inp, self.outp = bspline.main()
        
        print("\n\nPontos da superfície:", self.outp)
        print("\n\nPontos de controle:", self.inp)

        self.desenhar_superficie()

if __name__ == "__main__":
    # Parâmetros da superfície
    pontos_controleX, pontos_controleY = 5, 5  
    TI, TJ = 4, 4  
    RESOLUTIONI, RESOLUTIONJ = 10, 10  
    espacamento = 20
    VRP = [10, 10, 10, 1]
    P = [0, 0, 0, 1]
    Y = [0, 1, 0]
    dp = 40
    windows = [-100, -100, 100, 100]
    viewport = [0, 0, 500, 500]

    root = tk.Tk()
    app = Interface(root, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, espacamento, VRP, P, Y, dp, windows, viewport)
    root.mainloop()
