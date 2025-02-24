import tkinter as tk
import random
from ProjecaoAxonometrica import ProjecaoAxonometrica

class BSplines:
    def __init__(self,NI, NJ, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp, VRP, P,V,dp,windows,viewport,mundo):
        # Parâmetros de controle
        self.NI = NI
        self.NJ = NJ
        self.TI = TI
        self.TJ = TJ
        self.RESOLUTIONI = RESOLUTIONI
        self.RESOLUTIONJ = RESOLUTIONJ
        self.inp = inp 
        self.VRP = VRP 
        self.P = P
        self.Y = V
        self.dp = dp 
        self.windows = windows
        self.viewport = viewport
        self.mundo = mundo

        # Vetores de nós para as direções I e J
        self.knotsI = [0] * (self.NI + self.TI + 1)
        self.knotsJ = [0] * (self.NJ + self.TJ + 1)
        #pontos da superfície calculada: dimensão (RESOLUTIONI)x(RESOLUTIONJ)
        self.outp = [[[0, 0, 0] for _ in range(self.RESOLUTIONJ)] for _ in range(self.RESOLUTIONI)]

    def calcular_nos(self, nos, n, t):
        """ Calcula os nós da spline com base no número de pontos de controle e no grau da spline """
        for j in range(n + t + 1):
            if j < t:
                nos[j] = 0
            elif j <= n:
                nos[j] = j - t + 1
            else:
                nos[j] = n - t + 2

    def calcular_blend(self, k, t, u, v):
        """ Calcula recursivamente o valor da função de base (blend) da B-Spline """
        if t == 1:
            return 1 if u[k] <= v < u[k + 1] else 0
        valor = 0
        if u[k + t - 1] != u[k]:
            valor += (v - u[k]) / (u[k + t - 1] - u[k]) * self.calcular_blend(k, t - 1, u, v)
        if u[k + t] != u[k + 1]:
            valor += (u[k + t] - v) / (u[k + t] - u[k + 1]) * self.calcular_blend(k + 1, t - 1, u, v)
        return valor

    def calcular_superficie(self):
        """ Calcula os pontos da superfície B-Spline, de forma a reproduzir o algoritmo C """
        # Calcula os nós para as direções I e J
        self.calcular_nos(self.knotsI, self.NI, self.TI)
        self.calcular_nos(self.knotsJ, self.NJ, self.TJ)

        # Determina os incrementos de parâmetro
        incrementoI = (self.NI - self.TI + 2) / (self.RESOLUTIONI - 1)
        incrementoJ = (self.NJ - self.TJ + 2) / (self.RESOLUTIONJ - 1)

        # Cálculo dos pontos internos da superfície:
        intervaloI = 0
        for i in range(self.RESOLUTIONI - 1):
            intervaloJ = 0
            for j in range(self.RESOLUTIONJ - 1):
                x, y, z = 0.0, 0.0, 0.0
                for ki in range(self.NI + 1):
                    for kj in range(self.NJ + 1):
                        bi = self.calcular_blend(ki, self.TI, self.knotsI, intervaloI)
                        bj = self.calcular_blend(kj, self.TJ, self.knotsJ, intervaloJ)
                        x += self.inp[ki][kj][0] * bi * bj
                        y += self.inp[ki][kj][1] * bi * bj
                        z += self.inp[ki][kj][2] * bi * bj
                self.outp[i][j] = [x, y, z]
                intervaloJ += incrementoJ
            intervaloI += incrementoI

        # Cálculo dos pontos na coluna final (j = RESOLUTIONJ - 1) para i de 0 a RESOLUTIONI-2:
        intervaloI = 0
        for i in range(self.RESOLUTIONI - 1):
            x, y, z = 0.0, 0.0, 0.0
            for ki in range(self.NI + 1):
                bi = self.calcular_blend(ki, self.TI, self.knotsI, intervaloI)
                # Utiliza o último ponto da coluna de controle (j = NJ)
                x += self.inp[ki][self.NJ][0] * bi
                y += self.inp[ki][self.NJ][1] * bi
                z += self.inp[ki][self.NJ][2] * bi
            self.outp[i][self.RESOLUTIONJ - 1] = [x, y, z]
            intervaloI += incrementoI

        # Cálculo dos pontos na linha final (i = RESOLUTIONI - 1) para j de 0 a RESOLUTIONJ-2:
        intervaloJ = 0
        for j in range(self.RESOLUTIONJ - 1):
            x, y, z = 0.0, 0.0, 0.0
            for kj in range(self.NJ + 1):
                bj = self.calcular_blend(kj, self.TJ, self.knotsJ, intervaloJ)
                # Utiliza o último ponto da linha de controle (i = NI)
                x += self.inp[self.NI][kj][0] * bj
                y += self.inp[self.NI][kj][1] * bj
                z += self.inp[self.NI][kj][2] * bj
            self.outp[self.RESOLUTIONI - 1][j] = [x, y, z]
            intervaloJ += incrementoJ

        # O último ponto da superfície é igual ao último ponto de controle
        self.outp[self.RESOLUTIONI - 1][self.RESOLUTIONJ - 1] = self.inp[self.NI][self.NJ]

    def desenhar_superficie(self, canvas):
        """ Desenha a superfície B-Spline no canvas """
        canvas.delete("all")
        escala = 1
        deslocamento_x, deslocamento_y = -200, 250  # Deslocamento para centralizar o desenho
        # Desenha os pontos de controle (opcional)
        for i in range(self.NI + 1):
            for j in range(self.NJ + 1):
                x = deslocamento_x + self.inp[i][j][0] * escala 
                y = deslocamento_y - self.inp[i][j][2] * escala 
                raio = 3
                
                canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="red")
        # Desenha a superfície usando os polígonos
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                x1 = deslocamento_x + self.outp[i][j][0] * escala
                y1 = deslocamento_y - self.outp[i][j][2] * escala 
                x2 = deslocamento_x + self.outp[i][j+1][0] * escala
                y2 = deslocamento_y - self.outp[i][j+1][2] * escala
                x3 = deslocamento_x + self.outp[i+1][j+1][0] * escala
                y3 = deslocamento_y - self.outp[i+1][j+1][2] * escala
                x4 = deslocamento_x + self.outp[i+1][j][0] * escala
                y4 = deslocamento_y - self.outp[i+1][j][2] * escala
                
                #canvas.create_polygon(x1, y1, x4, y4, x3, y3, x2, y2,outline="black", fill="", width=1)
                canvas.create_line(x1, y1, x4, y4, fill="black", width=1)
                canvas.create_line(x4, y4, x3, y3, fill="black", width=1)
                canvas.create_line(x3, y3, x2, y2, fill="black", width=1)
                canvas.create_line(x2, y2, x1, y1, fill="black", width=1)
                
                
                
    def main(self):       
        
        self.calcular_superficie()
        
        # 1) OBJETO MODELADO EM SRU
        # ->  self.inp  <-
        # 3)	Aplicar as matrizes do pipeline (Converter objeto do SRU para o SRT)
        
           
        projecao = ProjecaoAxonometrica(self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
        projecao = projecao.main()
    
        self.inp = []
    
        #print(projecao)
        # tem que fazer isso pq usei um formato de matriz na projecao e aqui esta em outro
        # gambiarra nao, adaptacao kkk
        # Reconstrói a matriz de pontos de controle a partir da projeção
        for i in range(self.NI + 1):
            linha = []
            for j in range(self.NJ + 1):
                indice = i * (self.NJ + 1) + j
                # projecao[0], projecao[1], projecao[2] contêm as coordenadas projetadas (desconsiderando W)
                elemento = [projecao[0][indice],
                            projecao[1][indice],
                            projecao[2][indice]]
                linha.append(elemento)
            self.inp.append(linha) 

        projecao = ProjecaoAxonometrica(self.outp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
        projecao = projecao.main()
        

        #print("Axonometrico : \n\n")
        #print("Pontos ANTES de serem axonometrico:", self.outp)
        self.outp = [] 
        # Preenchendo self.outp com os valores projetados corretamente
        # mesma coisa dos pontos de controle, so que aqui é pros demais pontos da superfice
        indice = 0
        for i in range(self.RESOLUTIONI):
            linha = []
            for j in range(self.RESOLUTIONJ):
                indice = i * self.RESOLUTIONJ + j

                elemento = [projecao[0][indice],
                            projecao[1][indice],
                            projecao[2][indice]]
                linha.append(elemento)
            self.outp.append(linha)
                
        #print(projecao)'''
        #print("\n\nPontos da superfice DEPOIS de serem axonometrico:", self.outp)
        #print("\n\nPontos de controle DEPOIS de serem axonometrico:", self.inp)
        return self.inp, self.outp



