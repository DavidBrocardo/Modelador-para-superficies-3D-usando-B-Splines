import tkinter as tk
import random
import copy
from ProjecaoAxonometrica import ProjecaoAxonometrica
from Transformacoes_Geometricas import Transformacoes_Geometricas
from Recorte3D import Recorte3D

class BSplines:
    def __init__(self,NI, NJ, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp, VRP, P,V,dp,windows,viewport,geometrica,valores_geo):
        # Parâmetros de controle
        self.NI = NI
        self.NJ = NJ
        self.TI = TI
        self.TJ = TJ
        self.RESOLUTIONI = RESOLUTIONI
        self.RESOLUTIONJ = RESOLUTIONJ
        self.inp = inp 
        self.VRP = VRP 
        self.inp_projetado = inp
        self.P = P
        self.Y = V
        self.dp = dp 
        self.windows = windows
        self.viewport = viewport
        self.geometrica = geometrica
        self.valores_geo = valores_geo

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
                

    def converter_vertices_tradicional(self, lista_vertices):
        vertices_covertido = [[], [], [],[]]  
        for linha in lista_vertices:  
            for item in linha: 
                x, y, z = item 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
                vertices_covertido[3].append(1)
        return vertices_covertido        
    
    def converter_vertices_superfice(self, lista_vertices):
            indice = 0
            for i in range(self.RESOLUTIONI):
                linha = []
                for j in range(self.RESOLUTIONJ):
                    indice = i * self.RESOLUTIONJ + j
                    elemento = [lista_vertices[0][indice] ,
                                lista_vertices[1][indice] ,
                                lista_vertices[2][indice] ]                
                    linha.append(elemento)
                self.outp.append(linha)
    
    
    def converter_pontos_superfice(self, lista_vertices,geo):
            indice = 0
            for i in range(self.NI + 1):
                linha = []
                for j in range(self.NJ + 1):
                    indice = i * (self.NJ + 1) + j
                    # projecao[0], projecao[1], projecao[2] contêm as coordenadas projetadas (desconsiderando W)
                    elemento = [lista_vertices[0][indice],
                                lista_vertices[1][indice],
                                lista_vertices[2][indice]]
                    linha.append(elemento)
                if geo:
                    self.inp.append(linha)
                self.inp_projetado.append(linha) 

    def axonometrica(self,entrada,pontos):       
        if pontos:
            vertices=[]
            vertices = self.converter_vertices_tradicional(entrada)
            projecao = ProjecaoAxonometrica(vertices, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.inp_projetado = []
            self.converter_pontos_superfice(projecao,False)   
        else:
            # RECORTE 3D -> i.Recorte (3D) dos objetos que estejam antes do plano Near e depois do plano Far.
            vertices=[]
            vertices = self.converter_vertices_tradicional(self.outp)
            print("Antes :" , vertices)
            recorte = Recorte3D(-5000, 5000, vertices)
            vertices_visiveis = recorte.Recortar3D()
            print("\n\nDepois",vertices_visiveis)
            projecao = ProjecaoAxonometrica(vertices_visiveis, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.outp = []
            self.converter_vertices_superfice(projecao)
                
    def main(self):       
        
        self.calcular_superficie()
        
        #Transformacap_Geometrica 
        # 1)	Objetos modelados em SRU
        #       a.	Transformações geométricas (rotações, translações, escalas, cisalhamentos, etc. aplicada ao objeto).       
        # geometrica  = 0 (Nenhuma) / =1 (Escala) / = 2 (Rotacao) / = 3 (Translacao)
        if self.geometrica != 0:
            vertices=[]
            vertices = self.converter_vertices_tradicional(self.outp)
            pontos = self.converter_vertices_tradicional(self.inp)
            operacao = Transformacoes_Geometricas(vertices) 

            if self.geometrica == 1:     # ESCALA       
                resul_escala = operacao.Escala(self.valores_geo)
                self.outp = [] 
                self.converter_vertices_superfice(resul_escala)

                operacao = Transformacoes_Geometricas(pontos) 
                self.inp = []
                self.inp_projetado = []
                resul_escala = operacao.Escala(self.valores_geo)
                self.converter_pontos_superfice(resul_escala,True)
                #print(self.outp)

            if self.geometrica  == 2:    # ROTACAO
                x,y,z = self.valores_geo[0]   
                resul_rotacao_x = operacao.Rotacao_em_x(x)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_y = operacao.Rotacao_em_y(y)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_z = operacao.Rotacao_em_z(z)
                self.outp = [] 
                self.converter_vertices_superfice(resul_rotacao_z)

                operacao = Transformacoes_Geometricas(pontos)
                resul_rotacao_x = operacao.Rotacao_em_x(x)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_y = operacao.Rotacao_em_y(y)
                operacao = Transformacoes_Geometricas(resul_rotacao_x) 
                resul_rotacao_z = operacao.Rotacao_em_z(z)

                self.inp = []
                self.inp_projetado = []
                self.converter_pontos_superfice(resul_rotacao_z,True)
                

            if self.geometrica == 3: # TRANSLACAO
                x,y,z = self.valores_geo[0]
                resul_translacao = operacao.Translacao(x,y,z)
                self.outp = [] 
                self.converter_vertices_superfice(resul_translacao)

                operacao = Transformacoes_Geometricas(pontos) 
                self.inp = []
                self.inp_projetado = []
                resul_translacao = operacao.Translacao(x,y,z)
                self.converter_pontos_superfice(resul_translacao,True)



        # 3)Aplicar as matrizes do pipeline (Converter objeto do SRU para o SRT)           

        # PROJECAO AXONOMETRICA
            #PONTOS
        print(self.inp)
        self.axonometrica(self.inp,True)      
        
            

            #SUPERFICE
        self.axonometrica(self.outp,False)      
         
        print("SAIDA \n\n ",self.outp)
        return self.inp, self.inp_projetado, self.outp


