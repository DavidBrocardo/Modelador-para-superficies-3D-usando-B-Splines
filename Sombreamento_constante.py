"""c.	Sombreamento constante
i.	Computar o valor de iluminação total (cor) de cada face

Só vai calcular das faces visiveis, calculo de visibilidade pela normal
já vai ter sido feito!

Já vai ter todas as infos calculadas tbm! evitar recalculos
(centroide da face, vetor normal da face, etc...)
"""

"""Iluminação ambiente [Ia = Ila . Ka]			
   Iluminação difusa [Id = Il . Kd . (n.l)]		
   Iluminação especular [Is = Il . Ks . (r.s)^n]				
"""

class Sombreamento_constante:
    def __init__(self):




if __name__ == "__main__":
    
    vertices = [
        [0.8, 0.0, -0.7071067811865476, 0.0], 
        [-0.40824829046386313, 0.8164965809277258, -0.40824829046386313, 4.440892098500626e-16], 
        [0.5773502691896258, 0.5773502691896258, 0.5773502691896258, -1.7320508075688776], 
        [0, 0, 0, 1] 
    ]

    ila = 120  #luz ambiente

    il = 150 
    x = 70  
    y = 20    #lampada
    z = 35

    ka = 0,4
    kd = 0,7  #Propriedades do material (superficie)
    ks = 0,5
    n = 2,15





    sombrear = Sombreamento_constante(vertices)

