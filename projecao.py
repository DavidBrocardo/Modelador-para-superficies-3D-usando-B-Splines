import tkinter as tk
import math
import numpy as np

def Unitario (Vetor , Vetor_normalizado):    
    unitario = [0] * 3
    for i in range(3):
        unitario[i] = Vetor[i] / Vetor_normalizado 
    return unitario

def calcular_produto_vetorial(v, n):
    
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

def calcula_Mult_Matriz(A, B):
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

    return resultado
def Axometrica(vertices, VRP, P, Y, dp, windows,viewport):
    N = [0] * (3)
    n_quadrado = 0
    #N = VRP -P
    for i in range(3):
        N[i] = VRP[i] - P[i]
        n_quadrado += N[i] **2
    #print(N)

    #n = N/|N|
    n_quadrado = math.sqrt(n_quadrado)
    n_unitario = Unitario(N, n_quadrado )
    #print(n_unitario)


    #V = Y - (Y.n).n
    mult_YN = 0
    v_quadrado= 0
    for i in range(3):
        mult_YN += Y[i]*n_unitario[i]

    V = [0] * 3   
    for i in range(3):
        V[i] =  Y[i] - mult_YN*n_unitario[i]
        v_quadrado += V[i] **2

    v_quadrado = math.sqrt(v_quadrado)
    v_unitario = Unitario(V, v_quadrado )    
    #print(v_unitario)
    
    # u =  v x n 
    u = calcular_produto_vetorial(v_unitario, n_unitario)
    #print("Produto vetorial: " , u)

    #M(SRU, SRC) = R.T

    matriz_R = [
        u + [0],
        v_unitario + [0],
        n_unitario + [0],
        [0, 0, 0, 1]
    ]

    matriz_T = [
        [1, 0 , 0] + [-VRP[0]],
        [0, 1 , 0] + [-VRP[1]],
        [0, 0 , 1] + [-VRP[2]],
        [0, 0 , 0, 1]
    ]
    matriz_SRU = calcula_Mult_Matriz(matriz_R,matriz_T)

    #print(matriz_SRU)

    #PROJEÇÃO AXONOMÉTRICA

    M_proj = [
        [1, 0 , 0, 0],
        [0, 1 , 0, 0],
        [0, 0 , 1, 0],
        [0, 0 , 0, 1]
    ]
    
    M_jp = [
        [((viewport[2]-viewport[0])/(windows[2]-windows[0])), 0	,0,	(-windows[0] *(viewport[2]-viewport[0])/(windows[2]-windows[0]) + viewport[0])],
        [0,	((viewport[1]-viewport[3])/(windows[3]-windows[1])), 0, (windows[1] * (viewport[3]-viewport[1])/(windows[3]-windows[1]) + viewport[3]) ],
        [0,	0,	1,	0],
        [0,	0,	0,	1]
    ]
    
    matriz_SRT = calcula_Mult_Matriz(M_jp, calcula_Mult_Matriz(M_proj,matriz_SRU))  

    #print(matriz_SRT)

    #Objeto em projeção axonométrica

    objeto_projetado = calcula_Mult_Matriz(matriz_SRT, vertices)

    print(objeto_projetado)
    return objeto_projetado
#GPTzada so pra ver o resultado 

def draw_projection(vertices):
    # Criar a janela Tkinter
    root = tk.Tk()
    root.title("Projeção Axonométrica")
    canvas = tk.Canvas(root, width=500, height=500, bg="white")
    canvas.pack()

    # Configurar escala e deslocamento
    scale = 0.5  # Ajuste conforme necessário
    offset_x = 250  # Centro do Canvas no eixo X
    offset_y = 250  # Centro do Canvas no eixo Y

    # Verificar todos os pontos e desenhá-los
    for i in range(len(vertices[0])):
        x = vertices[0][i] * scale + offset_x  # Coordenada x escalada e deslocada
        y = vertices[1][i] * scale + offset_y  # Coordenada y escalada e deslocada

        # Desenhar o ponto
        canvas.create_oval(
            x - 3, y - 3,  # Ponto superior esquerdo
            x + 3, y + 3,  # Ponto inferior direito
            fill="blue"
        )
    
    root.mainloop()


    
def main():
    vertices = [
        [21.2, 34.1, 18.8, 5.9, 20],
        [0.7,  3.4,  5.6,  2.9, 20.9],
        [42.3, 27.2, 14.6, 29.7,31.6],
        [1,     1 ,   1,   1,  1]
    ]
    
    VRP = [25, 15, 80, 1]  
    P = [20, 10, 25, 1]    
    Y = [0, 1, 0]       
    dp = 40    

    windows = [-8, -6, 8, 6]
    viewport = [0, 0, 319, 239]    
    
    # Calcular a projeção
    projecao_axometrica = Axometrica(vertices, VRP, P, Y, dp,windows,viewport)
    draw_projection(projecao_axometrica)


if __name__ == "__main__":
    main()
