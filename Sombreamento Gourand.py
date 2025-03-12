import numpy as np

"""c.	Sombreamento Gourand: 
1) Determinar o vetor normal unitário médio em
cada vértice do objeto;
2) Aplicar a função de iluminação calculando a
intensidade total em cada vértice do objeto;
3) Interpolar linearmente as intensidades dos
vértices para o restante de cada face do objeto.

i.	Vetores normais médios unitários nos vértices
ii.	Gouraud: Calcular a iluminação total nos vértices

"""
#DEPOIS APAGAR
class Sombreamento_Gouraud:
    def __init__(self, ila, il, ka, kd, ks, n, luz_pos, vertices, faces):
        self.ila = ila  
        self.il = il    
        self.ka = ka   
        self.kd = kd    
        self.ks = ks   
        self.n = n     
        self.luz_pos = np.array(luz_pos)  
        self.vertices = np.array(vertices)  
        self.faces = np.array(faces)  

        # Calcula normais médias para cada vértice
        self.normais_vertices = self.calcular_normais_vertices()

    def calcular_normais_vertices(self):
        """ Calcula a normal média unitária para cada vértice. """
        normais_vertices = {i: [] for i in range(len(self.vertices))}

        # Para cada face, atribuímos sua normal aos seus vértices
        for face in self.faces:
            v0, v1, v2, v3 = [self.vertices[i] for i in face]
            
            # Calcula normal da face (produto vetorial entre dois vetores da face)
            normal = np.cross(v1 - v0, v2 - v0)
            normal /= np.linalg.norm(normal)  # Normaliza
            
            # Associa normal aos vértices da face
            for idx in face:
                normais_vertices[idx].append(normal)

        # Média das normais das faces adjacentes a cada vértice
        normais_finais = []
        for i in range(len(self.vertices)):
            media_normal = np.mean(normais_vertices[i], axis=0)
            media_normal /= np.linalg.norm(media_normal)  # Normaliza
            normais_finais.append(media_normal)

        return np.array(normais_finais)

    def calcular_iluminacao_ambiente(self):
        """ Iluminação ambiente (Ia = Ila * Ka) """
        return self.ila * self.ka

    def calcular_iluminacao_difusa(self, normal):
        """ Iluminação difusa (Id = Il * Kd * (n.l)) """
        vetor_L = self.luz_pos - normal
        vetor_L /= np.linalg.norm(vetor_L)
        n_dot_l = max(np.dot(normal, vetor_L), 0)
        return self.il * self.kd * n_dot_l

    def calcular_iluminacao_especular(self, normal, s):
        """ Iluminação especular (Is = Il * Ks * (r.s)^n) """
        vetor_L = self.luz_pos - normal
        vetor_L /= np.linalg.norm(vetor_L)

        n_dot_l = np.dot(normal, vetor_L)
        vetor_R = 2 * n_dot_l * normal - vetor_L
        vetor_R /= np.linalg.norm(vetor_R)

        r_dot_s = max(np.dot(vetor_R, s), 0)
        return self.il * self.ks * (r_dot_s ** self.n)

    def calcular_iluminacao_vertices(self):
        """ Calcula a iluminação total em cada vértice. """
        Ia = self.calcular_iluminacao_ambiente()
        iluminacoes = []
        
        for i in range(len(self.vertices)):
            normal = self.normais_vertices[i]
            Id = self.calcular_iluminacao_difusa(normal)
            Is = self.calcular_iluminacao_especular(normal, normal)  # Aqui usamos normal como s por simplicidade
            iluminacoes.append(Ia + Id + Is)

        return iluminacoes

    def calcular_iluminacao_faces(self):
        """ Interpola a iluminação dos vértices para a face. """
        iluminacoes_vertices = self.calcular_iluminacao_vertices()
        iluminacoes_faces = []
        
        for face in self.faces:
            # Média das iluminações dos vértices da face
            iluminacao_face = np.mean([iluminacoes_vertices[i] for i in face])
            iluminacoes_faces.append(iluminacao_face)

        return iluminacoes_faces


if __name__ == "__main__":
    ila = 120  # Luz ambiente
    il = 150   # Intensidade da lâmpada
    luz_pos = [70, 20, 35]  # Posição da lâmpada

    ka = 0.4  # Coeficiente de reflexão ambiente
    kd = 0.7  # Coeficiente de reflexão difusa
    ks = 0.5  # Coeficiente de reflexão especular
    n = 2.15  # Expoente especular

    # Lista de vértices (cada ponto do objeto)
    vertices = [
    [151.914, 340.497, -39.024],  # Vértice A
    [369.403, 223.801, -52.594],  # Vértice B
    [-59.425, 231.028, -52.703],  # Vértice D
    [149.556, -51.107, -47.924]   # Vértice E
]


    # Faces definidas por índices dos vértices
    faces = [
    [0, 1, 3, 2],  # Face ABE
    [1, 3, 2, 0],  # Face BCE
    [2, 3, 0, 1],  # Face CDE
    [0, 2, 1, 3],  # Face DAE
    [0, 2, 3, 1]  # Face ADCB
]

    # Instância da classe
    sombrear = Sombreamento_Gouraud(ila, il, ka, kd, ks, n, luz_pos, vertices, faces)

    iluminacoes = sombrear.calcular_iluminacao_faces()

    for i, ilum in enumerate(iluminacoes):
        print(f"Iluminação da face {i}: {ilum:.3f}")
