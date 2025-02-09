import random
import tkinter as tk

class XYZ:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

def SplineKnots(num_control_points, degree):
    n = num_control_points
    p = degree
    m = n + p + 1  # Número total de nós
    knots = [0.0] * m
    for i in range(m):
        if i <= p:
            knots[i] = 0.0
        elif i > n:
            knots[i] = n - p + 1
        else:
            knots[i] = i - p
    return knots

def basis_function(i, degree, knots, t):
    if degree == 0:
        return 1.0 if knots[i] <= t < knots[i+1] else 0.0
    else:
        denom1 = knots[i + degree] - knots[i]
        term1 = 0.0
        if denom1 != 0.0:
            term1 = ((t - knots[i]) / denom1) * basis_function(i, degree-1, knots, t)
        
        denom2 = knots[i + degree + 1] - knots[i + 1]
        term2 = 0.0
        if denom2 != 0.0:
            term2 = ((knots[i + degree + 1] - t) / denom2) * basis_function(i+1, degree-1, knots, t)
        
        return term1 + term2

def main():
    NI, NJ = 3, 4
    TI, TJ = 3, 3
    RESOLUTIONI, RESOLUTIONJ = 30, 40

    # Pontos de controle
    random.seed(1111)
    inp = [[XYZ(i, j, (random.randint(0, 9999) / 5000.0 - 1)) for j in range(NJ+1)] for i in range(NI+1)]

    # Calcular nós
    knotsI = SplineKnots(NI, TI)
    knotsJ = SplineKnots(NJ, TJ)

    # Inicializar pontos de saída
    outp = [[XYZ() for _ in range(RESOLUTIONJ)] for __ in range(RESOLUTIONI)]
    incrementI = (NI - TI + 2) / (RESOLUTIONI - 1)
    incrementJ = (NJ - TJ + 2) / (RESOLUTIONJ - 1)

    # Calcular a superfície
    for i in range(RESOLUTIONI):
        intervalI = i * incrementI
        for j in range(RESOLUTIONJ):
            intervalJ = j * incrementJ
            x, y, z = 0.0, 0.0, 0.0
            for ki in range(NI + 1):
                bi = basis_function(ki, TI, knotsI, intervalI)
                for kj in range(NJ + 1):
                    bj = basis_function(kj, TJ, knotsJ, intervalJ)
                    x += inp[ki][kj].x * bi * bj
                    y += inp[ki][kj].y * bi * bj
                    z += inp[ki][kj].z * bi * bj
            outp[i][j] = XYZ(x, y, z)

    # Configurar Tkinter
    root = tk.Tk()
    root.title("Superfície de Spline")
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # Função de projeção isométrica
    def project(x, y, z):
        iso_x = (x - y) * 30 + 400
        iso_y = (x + y) * 15 - z * 30 + 200
        return iso_x, iso_y

    # Desenhar a superfície
    for i in range(RESOLUTIONI - 1):
        for j in range(RESOLUTIONJ - 1):
            p1 = outp[i][j]
            p2 = outp[i][j+1]
            p3 = outp[i+1][j+1]
            p4 = outp[i+1][j]
            points = [p1, p2, p3, p4]
            for k in range(4):
                x1, y1 = project(points[k].x, points[k].y, points[k].z)
                x2, y2 = project(points[(k+1)%4].x, points[(k+1)%4].y, points[(k+1)%4].z)
                canvas.create_line(x1, y1, x2, y2, fill='blue')

    # Desenhar pontos de controle
    for i in range(NI + 1):
        for j in range(NJ + 1):
            x, y = project(inp[i][j].x, inp[i][j].y, inp[i][j].z)
            canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')

    root.mainloop()

if __name__ == "__main__":
    main()