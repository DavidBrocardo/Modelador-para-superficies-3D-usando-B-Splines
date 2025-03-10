import math

class ProjecaoAxonometrica:
   
    def __init__(self, vertices, VRP, P, Y, windows, viewport):
        # Inicializando variaveis
        #self.vertices = vertices
        self.vertices = vertices
        #print(self.vertices)
        self.VRP = VRP
        self.P = P
        self.Y = Y
        self.windows = windows
        self.viewport = viewport



    # Recebe um vetor e o retorna o unitario
    def Unitario (self, Vetor , Vetor_normalizado):    
        unitario = [0] * 3
        for i in range(3):
            unitario[i] = Vetor[i] / Vetor_normalizado 
        return unitario

    # Recebe dois vetores e retorna o produto vetorial
    def calcular_produto_vetorial(self, v, n):        
        matriz = [
            ["i", "j", "k"],
            v,
            n
        ]    
        # Componentes do produto vetorial
        u = [0] * (3)
        u[0] = v[1] * n[2] - v[2] * n[1]
        u[1] = -(v[0] * n[2] - v[2] * n[0])
        u[2] = v[0] * n[1] - v[1] * n[0]  
        return u

    # Recebe duas matrizes e as multiplica
    def calcula_Mult_Matriz(self, A, B):
        if len(A[0]) != len(B):
            raise ValueError("Número de colunas de A deve ser igual ao número de linhas de B.")
        
        m = len(A)  
        n = len(B)  
        p = len(B[0])  
        resultado = [[0 for _ in range(p)] for _ in range(m)]    

        for i in range(m):
            for j in range(p):
                for k in range(n):
                    resultado[i][j] += A[i][k] * B[k][j]

        # **Transformação para manter a estrutura correta**
        #resultado_corrigido = list(map(list, zip(*resultado)))  # Transpõe a matriz

        return resultado
    #Realiza todo o processo de transformação de um objeto 3D para uma projecao axometrica em 2D
    def Axometrica(self):
        N = [0] * (3)
        n_quadrado = 0
        
        #Calculo realizado abaixo : N = VRP -P
        for i in range(3):
            N[i] = self.VRP[i] - self.P[i]
            
            n_quadrado += N[i] **2
        #print("N", N)
        #Calculo realizado abaixo : n = N/|N|
        n_quadrado = math.sqrt(n_quadrado)
        n_unitario = self.Unitario(N, n_quadrado )
        #print("n_unitario", n_unitario)
        #print("|N|", n_quadrado)
        #Calculo realizado abaixo : V = Y - (Y.n).n
        mult_YN = 0
        v_quadrado= 0
        for i in range(3):
            mult_YN += self.Y[i]*n_unitario[i]
        V = [0] * 3   
        for i in range(3):
            V[i] =  self.Y[i] - mult_YN*n_unitario[i]
            v_quadrado += V[i] **2
        v_quadrado = math.sqrt(v_quadrado)
        v_unitario = self.Unitario(V, v_quadrado )    
        #print("V ", V)
        #print("v_unitario", v_unitario)
        #print("|V| ", v_quadrado)
        #Calculo realizado abaixo : u =  v x n 
        u = self.calcular_produto_vetorial(v_unitario, n_unitario)
        #print("u:", u)
        #Calculo realizado abaixo : M(SRU, SRC) = R.T        
        matriz_R = [
            u + [0],
            v_unitario + [0],
            n_unitario + [0],
            [0, 0, 0, 1]
        ]        
        matriz_T = [
            [1, 0 , 0] + [-self.VRP[0]],
            [0, 1 , 0] + [-self.VRP[1]],
            [0, 0 , 1] + [-self.VRP[2]],
            [0, 0 , 0, 1]
        ]
        matriz_SRC = self.calcula_Mult_Matriz(matriz_R,matriz_T) # Matriz SRC  = R * T
        #print("\nMatriz R" , matriz_R)               
        #print("\nMatriz T" , matriz_T)
        #print("\nMatriz SRC" , matriz_SRC)  
        #Ultima etapa da PROJEÇÃO AXONOMÉTRICA
        M_proj = [
            [1, 0 , 0, 0],
            [0, 1 , 0, 0],
            [0, 0 , 1, 0],
            [0, 0 , 0, 1]
        ]        
        M_jp = [
        [((self.viewport[2]-self.viewport[0])/(self.windows[2]-self.windows[0])), 0	,0,	(-self.windows[0] *(self.viewport[2]-self.viewport[0])/(self.windows[2]-self.windows[0]) + self.viewport[0])],
        [0,	((self.viewport[1]-self.viewport[3])/(self.windows[3]-self.windows[1])), 0, (self.windows[1] * (self.viewport[3]-self.viewport[1])/(self.windows[3]-self.windows[1]) + self.viewport[3]) ],
        [0,	0,	1,	0],
        [0,	0,	0,	1]
        ]
        #print("\nMatriz Transformacao ", M_jp)
        #Calculo realizado abaixo : matriz_SRTSRU =  M_jp * (M_proj*matriz_SRC)
        matriz_SRT = self.calcula_Mult_Matriz(M_jp, self.calcula_Mult_Matriz(M_proj,matriz_SRC))  
                
        #Objeto em projeção axonométrica
        #Calculo realizado abaixo : objeto_projetado =  matriz_SRT * vertices
        objeto_projetado = self.calcula_Mult_Matriz(matriz_SRT, self.vertices)      
       
        return objeto_projetado
        


    def main(self):
            # Calcular a projeção
            projecao_axometrica = self.Axometrica()
            #print(projecao_axometrica)
            return projecao_axometrica
            # Desenhar a projeção
            #self.draw_projection(projecao_axometrica)

if __name__ == "__main__":
    # Parâmetros da superfície
    vertices =  [[21.2, 34.1, 18.8, 5.9, 20],
                [0.7,  3.4,  5.6,  2.9, 20.9],
                [42.3, 27.2, 14.6, 29.7,31.6],
                [  1,   1 ,   1,     1,  1]]
    VRP = [25,15,80,1]
    P = [20, 10, 25, 1]
    Y = [0, 1, 0]
    windows = [-20, -15, 20, 15]
    viewport = [0, 0, 319, 239]

    projecao = ProjecaoAxonometrica(vertices, VRP, P, Y, windows, viewport)
    projecao = projecao.main() 

    print("\nProjecao Axonometrica\n" ,projecao[0],"\n",projecao[1],"\n",projecao[2])

