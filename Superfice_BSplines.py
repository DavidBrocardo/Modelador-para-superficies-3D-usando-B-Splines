import tkinter as tk
import random
from ProjecaoAxonometrica import ProjecaoAxonometrica


class BSplines:
    def __init__(self,NI,NJ,TI, TJ,RESOLUTIONI,RESOLUTIONJ,inp):
        # Definição de pontos de controle
        self.NI = NI
        self.NJ = NJ
        self.TI = TI
        self.TJ = TJ
        self.RESOLUTIONI = RESOLUTIONI
        self.RESOLUTIONJ = RESOLUTIONJ
        # Inicialização dos pontos de controle com valores aleatórios para a coordenada Z
        self.inp = inp
        # Vetores de nós para as direções I e J
        self.knotsI = [0] * (NI + TI + 1)
        self.knotsJ = [0] * (NJ + TJ + 1)
        # Matriz para armazenar os pontos da superfície calculada
        self.outp = [[[0, 0, 0] for _ in range(self.RESOLUTIONJ)] for _ in range(self.RESOLUTIONI)]

    def calcular_nos(self,nos, n, t):
        """ Calcula os nós da spline com base no número de pontos de controle e no grau da spline """
        for j in range(n + t + 1):
            if j < t:
                nos[j] = 0
            elif j <= n:
                nos[j] = j - t + 1
            else:
                nos[j] = n - t + 2
        print("Nos " , nos)
        return nos

    def calcular_blend(self,k, t, u, v):
        """ Calcula o valor de blending recursivamente para a spline """
        if t == 1:
            return 1 if u[k] <= v < u[k + 1] else 0
        
        valor = 0
        if u[k + t - 1] != u[k]:
            valor += (v - u[k]) / (u[k + t - 1] - u[k]) * self.calcular_blend(k, t - 1, u, v)
        if u[k + t] != u[k + 1]:
            valor += (u[k + t] - v) / (u[k + t] - u[k + 1]) * self.calcular_blend(k + 1, t - 1, u, v)
        
        return valor

    def calcular_superficie(self):
        """ Calcula os pontos da superfície spline com base nos pontos de controle """
        self.calcular_nos(self.knotsI, self.NI, self.TI)
        self.calcular_nos(self.knotsJ, self.NJ, self.TJ)
        print("Knots I:", self.knotsI)
        print("Knots J:", self.knotsJ)

        incrementoI = (self.NI - self.TI + 2) / (self.RESOLUTIONI - 1)
        incrementoJ = (self.NJ - self.TJ + 2) / (self.RESOLUTIONJ - 1)
        
        intervaloI = 0
        for i in range(self.RESOLUTIONI):
            intervaloJ = 0
            for j in range(self.RESOLUTIONJ):
                x, y, z = 0, 0, 0
                for ki in range(self.NI + 1):
                    bi = self.calcular_blend(ki, TI, self.knotsI, intervaloI)
                    for kj in range(self.NJ + 1):
                        bj = self.calcular_blend(kj, TJ, self.knotsJ, intervaloJ)
                        x += self.inp[ki][kj][0] * bi * bj
                        y += self.inp[ki][kj][1] * bi * bj
                        z += self.inp[ki][kj][2] * bi * bj
                self.outp[i][j] = [x, y, z]
                intervaloJ += incrementoJ
            intervaloI += incrementoI

    def desenhar_superficie(self,canvas):
        """ Desenha a superfície spline usando Tkinter """
        canvas.delete("all")
        escala = 50  # Fator de escala para visualização
        deslocamento_x, deslocamento_y = 100, 100  # Deslocamento para centralizar a visualização
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                x1, y1 = deslocamento_x + self.outp[i][j][0] * escala, deslocamento_y - self.outp[i][j][2] * escala
                x2, y2 = deslocamento_x + self.outp[i][j+1][0] * escala, deslocamento_y - self.outp[i][j+1][2] * escala
                x3, y3 = deslocamento_x + self.outp[i+1][j+1][0] * escala, deslocamento_y - self.outp[i+1][j+1][2] * escala
                x4, y4 = deslocamento_x + self.outp[i+1][j][0] * escala, deslocamento_y - self.outp[i+1][j][2] * escala
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, outline="black", fill="", width=1)


    def main(self):
             
        VRP = [0, 0, 1, 1]  
        P = [0, 0, 0, 1]    
        Y = [0, 1, 0]       
        dp = 0  
        windows = [-8, -6, 8, 6]
        viewport = [0, 0, 319, 239]
        #print(self.inp)
        #self.inp = ProjecaoAxonometrica(self.inp, VRP, P, Y, dp, windows, viewport)
        #projecao = ProjecaoAxonometrica(self.inp, VRP, P, Y, dp, windows, viewport)
        #self.inp= projecao.main()
        #print("Depois \n\n")
        #print(self.inp)
        self.calcular_superficie()

        """ Função principal para inicializar a interface Tkinter """
        root = tk.Tk()
        root.title("Superfície Spline")
        canvas = tk.Canvas(root, width=400, height=400, bg="white")
        canvas.pack()
        self.desenhar_superficie(canvas)
        root.mainloop()

if __name__ == "__main__":
    NI, NJ = 5, 4  # Número de pontos de controle na direção I e J
    TI, TJ = 3, 3  # Grau da spline nas direções I e J
    RESOLUTIONI = NI*NJ # max(30, NI * 10)  # Proporcional a NI, com um mínimo de 30
    RESOLUTIONJ = NI*NJ # max(40, NJ * 10)  # Proporcional a NJ, com um mínimo de 40
    # Inicialização dos pontos de controle com valores aleatórios para a coordenada Z
    inp = [[[i, j, random.uniform(-1, 1)] for j in range(NJ+1)] for i in range(NI+1)]
    #print(inp)   
    bspline = BSplines(NI,NJ,TI, TJ,RESOLUTIONI,RESOLUTIONJ,inp)
    bspline.main()
