class Recorte3D:
    def __init__(self, znear, zfar, vertices):
        self.znear = znear
        self.zfar = zfar
        #Converte a matriz de vertices para uma lista de listas (mais facil de manipular)
        self.vertices = [[vertices[0][i], vertices[1][i], vertices[2][i]] 
                         for i in range(len(vertices[0]))]  #tem q te, gpt

    def Recortar3D(self):
        novo_poligono = [] 

        for vertice in self.vertices:
            z = vertice[2]  

            #o poligono ta dentro do volume visivel ou nao
            if self.znear <= z <= self.zfar:
                novo_poligono.append(vertice)  #mantido

        return novo_poligono 


if __name__ == "__main__":
    vertices = [[  0,  250, 480],  # X
                [250,  430,   0],  # Y
                [30,  -65,  510]]  # Z
    
    znear = 10   #perto d+ da camera, tampa ela inteira, por isso deve ser recortado 
    zfar = 500   #longe d+ da camera, só gasta processamento e nem da pra direito

    recorte = Recorte3D(znear, zfar, vertices)
    vertices_visiveis = recorte.Recortar3D()

    print("Vértices após o recorte:", vertices_visiveis)


##
##   Ver com o professor se o nosso z do que é visivel é negativo???
##