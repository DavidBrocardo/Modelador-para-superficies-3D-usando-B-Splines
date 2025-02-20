import tkinter as tk
from tkinter import simpledialog, messagebox
from Superfice_BSplines import BSplines
import math
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
        self.criar_botoes()
        self.click_x = tk.IntVar()
        self.click_y = tk.IntVar()

        self.canvas.bind("<Button-1>", self.clique)

        self.main()

    

    def criar_menu(self):
        """Cria a barra de menu suspenso."""
        menu_principal = tk.Menu(self.tela)

        # Menu Superfice
        menu_superfice = tk.Menu(menu_principal, tearoff=0)
        menu_superfice.add_command(label="Pontos de Controle", command=self.definir_ponto_controle)
        menu_superfice.add_command(label="Ponto Focal", command=self.ponto_focal)
        menu_superfice.add_command(label="Camera", command=self.definir_camera)
        menu_superfice.add_command(label="Viewport", command=self.definir_viewport)
        menu_superfice.add_command(label="Windows", command=self.definir_windows)
        menu_principal.add_cascade(label="Superfice", menu=menu_superfice)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label="Abrir", command=self.abrir_arquivo)
        menu_arquivo.add_command(label="Salvar", command=self.salvar_arquivo)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.sair, accelerator="Ctrl+Q")
        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Pintura
        menu_pintor = tk.Menu(menu_principal, tearoff=0)
        menu_pintor.add_command(label="Cor Frente")
        menu_pintor.add_command(label="Cor Fundo")
        menu_principal.add_cascade(label="Pintura", menu=menu_pintor)

        # Menu Sobreamento

        menu_sobra = tk.Menu(menu_principal, tearoff=0)
        menu_sobra.add_command(label="Sombreamento Constante")
        menu_sobra.add_command(label="Sombreamento Gouraud")
        menu_sobra.add_command(label="Sombreamento Phong ")        
        menu_principal.add_cascade(label="Sombreamento", menu=menu_sobra)

        self.tela.config(menu=menu_principal)

    def criar_botoes(self):
        
        frame_botoes = tk.Frame(self.tela)
        frame_botoes.pack(pady=10)

        btn_pontos = tk.Button(frame_botoes, text="Nova Superfice", command=self.definir_tamanho_matriz, width=25, bg="blue")
        btn_pontos.grid(row=0, column=0, padx=5)

    def abrir_arquivo(self):
        messagebox.showinfo("Abrir", "Abrindo arquivo...")

    def salvar_arquivo(self):
        messagebox.showinfo("Salvar", "Salvando arquivo...")

    def sair(self):
        self.tela.quit()

    def clique(self, event):
        self.click_x.set(event.x)
        self.click_y.set(event.y) 
    
    def definir_ponto_controle(self):
        messagebox.showinfo("", "Clique proximo ao ponto que deseja altera")
        self.desenhar_pontoControle()

        self.tela.wait_variable(self.click_x)  # Espera um clique
        x_alvo, y_alvo = self.click_x.get(), self.click_y.get()
        print(x_alvo , y_alvo)
        print("Lens Pacu")    
        ponto_mais_proximo = None
        menor_distancia = float('inf')

        for i in range(self.pontos_controleX + 1):
            for j in range(self.pontos_controleY + 1):
                x = self.inp_Axo[i][j][0]
                y = self.inp_Axo[i][j][1] 
                distancia = math.sqrt((x - x_alvo)**2 + (y - y_alvo)**2 )
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    posi_i = i
                    posi_j = j
                    ponto_mais_proximo = (int(x), int(y))

              
        
        messagebox.showinfo("Ponto selecionado:", ponto_mais_proximo)

        janela = tk.Toplevel(self.tela)
        janela.title("Definir Novo Ponto Controle (Cordenadas de Tela)")


        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y").grid(row=0, column=1)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

       
        
        def Salvar():
            self.inp_Axo[posi_i][posi_j][0] =  int(entrada_x.get())
            self.inp_Axo[posi_i][posi_j][1] =  int(entrada_y.get())
            print(self.inp_Axo[posi_i][posi_j][0], self.inp_Axo[posi_i][posi_j][1])

            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp_Axo, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,False)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=2)
        

        
        
    def definir_tamanho_matriz(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Tamanho da Matriz")

        tk.Label(janela, text="Linhas (X):").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Colunas (Y):").grid(row=0, column=1)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)
        
        def Salvar():
            self.pontos_controleX = int(entrada_x.get())
            self.pontos_controleY = int(entrada_y.get())

            print(entrada_x, entrada_y)
            self.criar_pontos_controle() 
            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=2)

    def ponto_focal(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Novo Ponto Focal")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y").grid(row=0, column=1)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z").grid(row=0, column=2)
        entrada_z = tk.Entry(janela)
        entrada_z.grid(row=1, column=2)
        
        def Salvar():
            x = float(entrada_x.get())
            y = float(entrada_y.get())
            z = float(entrada_z.get())
            self.P = []
            self.P =  [x, y , z, 1]
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=3)

    def definir_windows(self):
        #windows = [-100, -100, 100, 100]
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Viewport")

        tk.Label(janela, text="X min:").grid(row=0, column=0)
        entrada_xMin = tk.Entry(janela)
        entrada_xMin.grid(row=1, column=0)

        tk.Label(janela, text="X max").grid(row=0, column=1)
        entrada_xMax = tk.Entry(janela)
        entrada_xMax.grid(row=1, column=1)

        tk.Label(janela, text="Y min:").grid(row=0, column=2)
        entrada_yMin = tk.Entry(janela)
        entrada_yMin.grid(row=1, column=2)

        tk.Label(janela, text="Y max:").grid(row=0, column=3)
        entrada_yMax = tk.Entry(janela)
        entrada_yMax.grid(row=1, column=3)
        
        def Salvar():
            x_min = float(entrada_xMin.get())
            x_max = float(entrada_xMax.get())
            y_min = float(entrada_yMin.get())
            y_max = float(entrada_yMax.get())
            self.windows = []
            self.windows =  [x_min, y_min, x_max, y_max]
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=4)

        


    def definir_viewport(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Viewport")

        tk.Label(janela, text="U min:").grid(row=0, column=0)
        entrada_uMin = tk.Entry(janela)
        entrada_uMin.grid(row=1, column=0)

        tk.Label(janela, text="U max").grid(row=0, column=1)
        entrada_uMax = tk.Entry(janela)
        entrada_uMax.grid(row=1, column=1)

        tk.Label(janela, text="V min:").grid(row=0, column=2)
        entrada_vMin = tk.Entry(janela)
        entrada_vMin.grid(row=1, column=2)

        tk.Label(janela, text="V max:").grid(row=0, column=3)
        entrada_vMax = tk.Entry(janela)
        entrada_vMax.grid(row=1, column=3)
        
        def Salvar():
            u_min = float(entrada_uMin.get())
            u_max = float(entrada_uMax.get())
            v_min = float(entrada_vMin.get())
            v_max = float(entrada_vMax.get())
            self.viewport = []
            self.viewport =  [u_min, v_min, u_max, v_max]
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=4)

    """def definir_camera(self):
        #VRP = [0, 0 ,0.7, 1]
               
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Camera")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=100, increment=1, width=5)
        entrada_x.grid(row=1, column=0)
        spinbox.pack()

        tk.Label(janela, text="Y").grid(row=0, column=1)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z").grid(row=0, column=2)
        entrada_z = tk.Entry(janela)
        entrada_z.grid(row=1, column=2)
        
        def Salvar():
            x = float(entrada_x.get())
            y = float(entrada_y.get())
            z = float(entrada_z.get())
            self.VRP = []
            self.VRP =  [x, y , z, 1]
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            bspline = BSplines(self.pontos_controleX,self.pontos_controleY , self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                            self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
            self.inp_Axo, self.outp = bspline.main()
            self.desenhar_superficie()

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=3)
            """

    def definir_camera(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Camera")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=100, increment=1, width=5)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y:").grid(row=0, column=1)  # Adicionado dois pontos para consistência
        entrada_y = tk.Spinbox(janela, from_=0, to=100, increment=1, width=5) # Spinbox para Y
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=0, column=2) # Adicionado dois pontos para consistência
        entrada_z = tk.Spinbox(janela, from_=0, to=100, increment=1, width=5) # Spinbox para Z
        entrada_z.grid(row=1, column=2)

        def Salvar():
            try:  # Tratamento de erros para entradas inválidas
                x = float(entrada_x.get())
                y = float(entrada_y.get())
                z = float(entrada_z.get())
                self.VRP = [x, y, z, 1]

                janela.destroy()

                # Calcula a superfície B-Spline (mantido como estava)
                bspline = BSplines(self.pontos_controleX, self.pontos_controleY, self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                                self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport, True)
                self.inp_Axo, self.outp = bspline.main()
                self.desenhar_superficie()

            except ValueError:
                tk.messagebox.showerror("Erro", "Por favor, insira números válidos.")  # Mensagem de erro

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=3)

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


    def desenhar_pontoControle(self):
        # Desenha os pontos de controle
        for i in range(self.pontos_controleX + 1):
            for j in range(self.pontos_controleY + 1):
                x = self.inp_Axo[i][j][0]
                y = self.inp_Axo[i][j][1] 
                #print (x ,  y)
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
            
    def desenhar_superficie(self):
        """Desenha a superfície B-Spline no Canvas."""
        self.canvas.delete("all")
                 

        # Desenha a superfície usando linhas
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                x1, y1 =   self.outp[i][j][0] ,   self.outp[i][j][1] 
                x2, y2 =  self.outp[i][j+1][0] ,  self.outp[i][j+1][1] 
                x3, y3 =  self.outp[i+1][j+1][0] ,  self.outp[i+1][j+1][1]
                x4, y4 =   self.outp[i+1][j][0] ,  self.outp[i+1][j][1]              

                
                self.canvas.create_line(x1, y1, x4, y4, fill="black", width=1)
                self.canvas.create_line(x4, y4, x3, y3, fill="black", width=1)
                self.canvas.create_line(x3, y3, x2, y2, fill="black", width=1)
                self.canvas.create_line(x2, y2, x1, y1, fill="black", width=1)

    def main(self):
        """Executa os cálculos e desenha a superfície."""
        
        self.criar_pontos_controle()
        self.inp_Axo = []
        # Calcula a superfície B-Spline
        bspline = BSplines(self.pontos_controleX, self.pontos_controleY, self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                           self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,True)
        self.inp_Axo, self.outp = bspline.main()
        
        #print("\n\nPontos da superfície:", self.outp)
        #print("\n\nPontos de controle:", self.inp_Axo)
        

        self.desenhar_superficie()

if __name__ == "__main__":
    # Parâmetros da superfície
    pontos_controleX, pontos_controleY = 5, 5  
    TI, TJ = 4, 4  
    RESOLUTIONI, RESOLUTIONJ = 30, 30  
    espacamento = 20
    VRP = [10, 20 ,10, 1]
    P = [0, 0, 0, 1]
    Y = [0, 1, 0]
    dp = 40
    windows = [-100, -100, 100, 100]
    viewport = [0, 0, 500, 500]

    root = tk.Tk()
    app = Interface(root, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, espacamento, VRP, P, Y, dp, windows, viewport)
    root.mainloop()
