#=((-1*$A7^3+3*$A7^2-3*$A7+1)*$A$2+(3*$A7^3-6*$A7^2+4)*$B$2+(-3*$A7^3+3*$A7^2+3*$A7+1)*$C$2+($A7^3)*$D$2)/6
# T 0 a 1
# T aumenta 0,125 por calculo 
# Cada curva usa 4 pontos e gera ao todo 9 coordenadas
# Vertices - 4 

import math
import numpy as np
import tkinter as tk

class bSlines:

    def __init__(self, acrescimo, coordenadas):
       #Inicializa as variaveis
       self.acrescimo = acrescimo
       self.coordenadas = coordenadas

    #Recebe duas matrizes e as multiplica
    def calcula_Mult_Matriz(self,A, B):
        if len(A[0]) != len(B):
            raise ValueError("Número de colunas de A deve ser igual ao número de linhas de B.")
        m = len(A)  
        n = len(B) 
        p = len(B[0]) 
        resultado = [[0 for _ in range(p)] for _ in range(m)]    
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    # Tem que dividir por 6 o resultado
                    resultado[i][j] += (A[i][k] * B[k][j])/6
        #print(resultado)
        return resultado

    #Realiza os calculo da B_Splines
    def curvas(self):
        T = 0
        matriz_Bsline = {}
        #Percore de 0 a 1 aumentando T a cada rodada
        while T <= 1:
            #Calculos da Taxa 
            T = round(float(T), 3) 
            Tcubo = pow(T,3)
            Tquadrado = pow(T,2)
            matriz_T = [
                [-1*Tcubo + 3*Tquadrado -3*T +1],
                [3*Tcubo -6*Tquadrado +4],
                [-3*Tcubo + 3*Tquadrado +3*T +1],
                [Tcubo]
                ] 
            if T not in matriz_Bsline:
                    matriz_Bsline[T] = []
            
            resultado = self.calcula_Mult_Matriz(self.coordenadas, matriz_T)
            matriz_Bsline[T].append(resultado)
            print( T , " : ", matriz_Bsline[T])
            T = T + self.acrescimo
        return matriz_Bsline      
            
   
    def main(self):
            curvas = self.curvas()
            
            
if __name__ == "__main__":
    vertices = [
            [1, 5, 12, 16],
            [3, -1, 8, 5],
            [8, 12, -4, 7]
        ]
    acrescimo = 0.1
    curvas = bSlines(acrescimo,vertices)
    curvas.main()


