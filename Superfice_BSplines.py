import tkinter as tk
import random
from ProjecaoAxonometrica import ProjecaoAxonometrica


class BSplines:
    def __init__(self, NI, NJ, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp):
        self.NI = NI
        self.NJ = NJ
        self.TI = TI
        self.TJ = TJ
        self.RESOLUTIONI = RESOLUTIONI
        self.RESOLUTIONJ = RESOLUTIONJ
        self.inp = inp
        self.knotsI = [0] * (self.NI + self.TI + 1)
        self.knotsJ = [0] * (self.NJ + self.TJ + 1)
        self.outp = [[[0, 0, 0] for _ in range(self.RESOLUTIONJ)] for _ in range(self.RESOLUTIONI)]

    def calcular_nos(self, nos, n, t):
        """ Calcula os nós da spline """
        for j in range(n + t + 1):
            if j < t:
                nos[j] = 0
            elif j <= n:
                nos[j] = j - t + 1
            else:
                nos[j] = n - t + 2

    def calcular_blend(self, k, t, u, v):
        """ Calcula o valor de blending """
        if t == 1:
            return 1 if u[k] <= v < u[k + 1] else 0
        valor = 0
        if u[k + t - 1] != u[k]:
            valor += (v - u[k]) / (u[k + t - 1] - u[k]) * self.calcular_blend(k, t - 1, u, v)
        if u[k + t] != u[k + 1]:
            valor += (u[k + t] - v) / (u[k + t] - u[k + 1]) * self.calcular_blend(k + 1, t - 1, u, v)
        return valor

    def calcular_superficie(self):
        """ Calcula os pontos da superfície """
        self.calcular_nos(self.knotsI, self.NI, self.TI)
        self.calcular_nos(self.knotsJ, self.NJ, self.TJ)

        incrementoI = (self.NI - self.TI + 2) / (self.RESOLUTIONI - 1)
        incrementoJ = (self.NJ - self.TJ + 2) / (self.RESOLUTIONJ - 1)

        intervaloI = 0
        for i in range(self.RESOLUTIONI):
            intervaloJ = 0
            for j in range(self.RESOLUTIONJ):
                x, y, z = 0, 0, 0
                for ki in range(self.NI + 1):
                    bi = self.calcular_blend(ki, self.TI, self.knotsI, intervaloI)
                    for kj in range(self.NJ + 1):
                        bj = self.calcular_blend(kj, self.TJ, self.knotsJ, intervaloJ)
                        x += self.inp[ki][kj][0] * bi * bj
                        y += self.inp[ki][kj][1] * bi * bj
                        z += self.inp[ki][kj][2] * bi * bj
                self.outp[i][j] = [x, y, z]
                intervaloJ += incrementoJ
            intervaloI += incrementoI

    def desenhar_superficie(self, canvas):
        """ Desenha a superfície no Canvas """
        canvas.delete("all")
        escala = 50  # Ajustado para um valor mais visível
        deslocamento_x, deslocamento_y = 200, 200  # Centralizado melhor
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                try:
                    x1, y1 = deslocamento_x + self.outp[i][j][0] , deslocamento_y - self.outp[i][j][2] 
                    x2, y2 = deslocamento_x + self.outp[i][j+1][0] , deslocamento_y - self.outp[i][j+1][2] 
                    x3, y3 = deslocamento_x + self.outp[i+1][j+1][0] , deslocamento_y - self.outp[i+1][j+1][2] 
                    x4, y4 = deslocamento_x + self.outp[i+1][j][0] , deslocamento_y - self.outp[i+1][j][2] 

                    print(f"Desenhando polígono: ({x1},{y1}), ({x2},{y2}), ({x3},{y3}), ({x4},{y4})")
                    canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, outline="black", fill="", width=1)
                except IndexError:
                    print(f"Erro ao desenhar quadrado em ({i}, {j})")


    def main(self):
        VRP = [0, 0, 1, 1]  
        P = [0, 0, 0, 1]    
        Y = [0, 1, 0]       
        dp = 0  
        windows = [-8, -6, 8, 6]
        viewport = [0, 0, 319, 239]

        projecao = ProjecaoAxonometrica(self.inp, VRP, P, Y, dp, windows, viewport)
        projecao = projecao.main()

        self.inp = []
        for i in range(self.NI + 1):  
            linha = []
            for j in range(self.NJ + 1):  
                elemento = [projecao[0][i * (self.NJ + 1) + j],  
                            projecao[1][i * (self.NJ + 1) + j],  
                            projecao[2][i * (self.NJ + 1) + j]]  
                linha.append(elemento)  
            self.inp.append(linha)

        self.calcular_superficie()
        #print("Pontos calculados da superfície:", self.outp)

        root = tk.Tk()
        root.title("Superfície Spline")
        canvas = tk.Canvas(root, width=800, height=800, bg="white")
        canvas.pack()
        self.desenhar_superficie(canvas)
        root.mainloop()


if __name__ == "__main__":
    NI, NJ = 5, 5  
    TI, TJ = 3, 3  
    RESOLUTIONI = 30  
    RESOLUTIONJ = 30  

    inp = [[[i, j, random.uniform(-1, 1)] for j in range(NJ+1)] for i in range(NI+1)]

    bspline = BSplines(NI, NJ, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp)
    bspline.main()
