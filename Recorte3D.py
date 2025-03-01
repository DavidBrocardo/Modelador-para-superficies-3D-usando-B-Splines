class Recorte3D:
    def __init__(self, znear, zfar, vertices):
        self.znear = znear
        self.zfar = zfar
        self.vertices = vertices  

    def Recortar3D(self):
        novo_poligono = []
        for vertice in self.vertices[:-1]:  # Evita acessar a [0, 0, 0, 1]
            z = vertice[2]
           
             #o poligono ta dentro do volume visivel ou nao
            if self.znear <= z <= self.zfar:

                novo_poligono.append(vertice)
    
        novo_poligono.append(self.vertices[3])
        return novo_poligono


if __name__ == "__main__":
    vertices = [
        [0.8, 0.0, -0.7071067811865476, 0.0], 
        [-0.40824829046386313, 0.8164965809277258, -0.40824829046386313, 4.440892098500626e-16], 
        [0.5773502691896258, 0.5773502691896258, 0.5773502691896258, -1.7320508075688776], 
        [0, 0, 0, 1] 
    ]

    znear = -2  #perto d+ da camera, tampa ela inteira, por isso deve ser recortado 
    zfar = 1 #longe d+ da camera, só gasta processamento e nem da pra direito

    recorte = Recorte3D(znear, zfar, vertices)
    vertices_visiveis = recorte.Recortar3D()

    print("Vértices após o recorte:", vertices_visiveis)

##
##   Ver com o professor se o nosso z do que é visivel é negativo???
##