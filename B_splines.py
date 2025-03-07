import math
from ProjecaoAxonometrica import ProjecaoAxonometrica
class BSplines:
    def __init__(self, acrescimo, coordenadas):
        self.acrescimo = acrescimo
        self.coordenadas = self.formatar_matriz(coordenadas)

    #Converte uma matriz de pontos de controle (m x n) no formato desejado. Recebe tuplas (x, y, z) e deixa separado
    #Acredito que vai ser necessario quando tiver manipulando com interface
    # se nao for, so corta fora
    def formatar_matriz(self,pontos_controle):
        X, Y, Z = [], [], []       
        
        for linha in pontos_controle:
            for ponto in linha:
                x, y, z = ponto
                X.append(x)
                Y.append(y)
                Z.append(z)

        return [X, Y, Z]

    def multiplica_matriz(self, A, B):
        """Multiplica duas matrizes e divide o resultado por 6."""
        if len(A[0]) != len(B):
            raise ValueError("Número de colunas de A deve ser igual ao número de linhas de B.")
        
        m, n, p = len(A), len(B), len(B[0])
        resultado = [[0 for _ in range(p)] for _ in range(m)]
        
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    resultado[i][j] += (A[i][k] * B[k][j]) / 6
        
        return resultado

    def calcular_curvas(self):
        """Calcula os pontos da curva B-Spline."""
        quant_T = round(1 / self.acrescimo) + 1
        colunas = len(self.coordenadas[0])
        matriz_bspline = [[0] * ((colunas - 3) * quant_T) for _ in range(4)]
        cont = 0
        for segmento in range(colunas - 3):
            submatriz = [linha[segmento:segmento + 4] for linha in self.coordenadas]
            T= 0
            
            while T <= 1:
                Tcubo, Tquadrado = T ** 3, T ** 2
                matriz_T = [
                    [-Tcubo + 3 * Tquadrado - 3 * T + 1],
                    [3 * Tcubo - 6 * Tquadrado + 4],
                    [-3 * Tcubo + 3 * Tquadrado + 3 * T + 1],
                    [Tcubo]
                ]

                
                resultado = self.multiplica_matriz(submatriz, matriz_T)
                #print(T)
                #print(resultado)
                #print(" ar ")
                for i in range(3):
                    matriz_bspline[i][cont] = resultado[i][0]
                matriz_bspline[3][cont] = 1
                
                T = round(T + self.acrescimo, 3)
                cont += 1
        
        return matriz_bspline

    def main(self):
        matriz_curvas =  self.calcular_curvas()
    
        VRP = [0, 0, 1, 1]  
        P = [0, 0, 0, 1]    
        Y = [0, 1, 0]       
        dp = 0  

        windows = [-8, -6, 8, 6]
        viewport = [0, 0, 319, 239]    
        
        
        #Chamando a classe projecao
        projecao = ProjecaoAxonometrica(matriz_curvas, VRP, P, Y, dp, windows, viewport)
        return projecao.main()

            

