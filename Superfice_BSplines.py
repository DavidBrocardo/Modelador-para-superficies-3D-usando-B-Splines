import random
import tkinter as tk
from B_splines import BSplines  # Certifique-se de que a classe BSplines está no mesmo diretório ou no caminho correto
from ProjecaoAxonometrica import ProjecaoAxonometrica


def gerar_matriz_pontos(linhas, colunas, espacamento, altura_max):
    matriz_pontos = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            x = i * espacamento
            y = random.randint(0, altura_max)  # Gera alturas aleatórias
            z = j * espacamento  
            linha.append((x, y, z))
        matriz_pontos.append(linha)
    return matriz_pontos

# Definições de resolução e parâmetros
linhas = 10
colunas = 10
espacamento = 8
altura_max = 30
acrescimo = 0.125  # Ajuste conforme necessário para suavidade da interpolação

# Geração dos pontos de controle
matriz_pontos = gerar_matriz_pontos(linhas, colunas, espacamento, altura_max)
bspline = BSplines(acrescimo, matriz_pontos)

# Calcula os pontos da B-Spline interpolada
matriz_curvas = bspline.main()

# Criar interface gráfica com Tkinter
root = tk.Tk()
root.title("Interpolação B-Spline")
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Normaliza os pontos para a escala do canvas
x_min = min(min(linha, key=lambda p: p[0])[0] for linha in matriz_pontos)
x_max = max(max(linha, key=lambda p: p[0])[0] for linha in matriz_pontos)
y_min = min(min(linha, key=lambda p: p[1])[1] for linha in matriz_pontos)
y_max = max(max(linha, key=lambda p: p[1])[1] for linha in matriz_pontos)

scale_x = 450 / (x_max - x_min)
scale_y = 450 / (y_max - y_min)

def transformar_ponto(x, y):
    return (x - x_min) * scale_x + 25, (y - y_min) * scale_y + 25

# Desenhar a malha original dos pontos de controle
for linha in matriz_pontos:
    for i in range(len(linha) - 1):
        x1, y1 = transformar_ponto(linha[i][0], linha[i][1])
        x2, y2 = transformar_ponto(linha[i + 1][0], linha[i + 1][1])
        canvas.create_line(x1, y1, x2, y2, fill="blue", dash=(4, 2))

for j in range(len(matriz_pontos[0])):
    for i in range(len(matriz_pontos) - 1):
        x1, y1 = transformar_ponto(matriz_pontos[i][j][0], matriz_pontos[i][j][1])
        x2, y2 = transformar_ponto(matriz_pontos[i + 1][j][0], matriz_pontos[i + 1][j][1])
        canvas.create_line(x1, y1, x2, y2, fill="blue", dash=(4, 2))

# Desenhar a curva B-Spline interpolada
num_pontos = len(matriz_curvas[0])
for i in range(num_pontos - 1):
    x1, y1 = transformar_ponto(matriz_curvas[0][i], matriz_curvas[1][i])
    x2, y2 = transformar_ponto(matriz_curvas[0][i+1], matriz_curvas[1][i+1])
    canvas.create_line(x1, y1, x2, y2, fill="black")

root.mainloop()
