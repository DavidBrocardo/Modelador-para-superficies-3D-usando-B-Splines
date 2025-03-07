import numpy as np

class Visibilidade_Normal:

    def __init__(self, vertices, indices_faces,VRP, pintor):
        if pintor:
            self.vertices = self.converter_vertices(vertices)
        else:
            self.vertices = vertices
        self.indices_faces = indices_faces
        self.VRP = VRP
    
    
    def converter_vertices(self, lista_vertices):
        vertices_covertido = [[], [], []]  
        for linha in lista_vertices:  
                x, y, z = linha 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
        #print(vertices_covertido)
        return vertices_covertido
    
    def Calcular_vet_normal_unitario_face(self, vertices, indice_face): #calcula de uma face

        vertices = np.array(vertices) #s├│ funfa convertendo pra array pra manipular

        p0 = vertices[:3, indice_face[0]]
        p1 = vertices[:3, indice_face[1]] #pegando os vertices da face e seus x,y,z
        p2 = vertices[:3, indice_face[2]]

        v1 = p1 - p0 
        v2 = p2 - p0  #vets 1 e 2 para calcular o vet normal

        Vnormal = np.cross(v1, v2)  #produto vetorial v1 x v2
  
        norma = np.linalg.norm(Vnormal)
        Vnormal_unitario = Vnormal / norma  #calc do vet unitario

        return Vnormal_unitario
    
    def Calcular_vet_normal_das_faces(self, vertices, indices_faces): #calcula de todas as faces armazenadas

        normais_faces = []
       
        #print("\n")
        for i, face in enumerate(indices_faces): 
            
            normal_unitaria = self.Calcular_vet_normal_unitario_face(vertices, face)
            normais_faces.append(normal_unitaria)  #calculando e salvando todos os vets normais das faces

            #print(f"Normal da face : {normal_unitaria}")
        #print("\n")

        return normais_faces

    def Calcular_centroide_face(self, vertices, indice_face):

        v = len(indice_face) # Nº de vertices da face, ex: face ABE = 3; face ABCD = 4;
        
        soma_x = 0
        soma_y = 0
        soma_z = 0

        for i in indice_face:
            soma_x += vertices[0][i]
            soma_y += vertices[1][i] #vai somando os valores xyz de cada face
            soma_z += vertices[2][i]

        centroide_x = soma_x / v
        centroide_y = soma_y / v #calcula o centroide, dividindo pelo Nº de vertices
        centroide_z = soma_z / v
    
        return centroide_x, centroide_y, centroide_z
    
    def Calcular_vet_observacao_face (self, VRP, vertices, indices_faces):

        VRP = np.array(VRP) 
        vets_de_observacao_faces = []
        
        for indice_face in indices_faces:
            centroide = self.Calcular_centroide_face(vertices, indice_face) 
            vet_observacao = VRP - centroide  

            norma = np.linalg.norm(vet_observacao)  #calc do vet de observacao unitario
            VetorO_unitario = vet_observacao / norma 

            vets_de_observacao_faces.append(VetorO_unitario) 
           
        return vets_de_observacao_faces, centroide

    def main(self):

        vets_normais = self.Calcular_vet_normal_das_faces(self.vertices, self.indices_faces)
        vets_observacao , centroide = self.Calcular_vet_observacao_face(self.VRP, self.vertices, self.indices_faces)
        produtos_escalares = [np.dot(vn, vo) for vn, vo in zip(vets_normais, vets_observacao)] #gpt cantou
        return produtos_escalares, centroide, vets_observacao , vets_normais
    
if __name__ == "__main__":
   
    
    
    indices_faces = [ [0,1,2,3]] #Os vertices de cada face, ex: Face ABE(Face 014)

    vertices =  [(147.65903385378255, 313.9165890311658, 30.326237147066724),
                (114.1610657194264, 328.7452796783735, 42.542635931800135),
                (179.57282438145648, 356.40754056424265, 66.76365340967062), 
                (213.07079251581263, 347.49360951923575, 52.874307975415476)]
    
    vertices =  [(21.2, 0.7, 42.3),
                 (5.9, 2.9, 29.7 ),
                 (18.8, 5.6, 14.6),
                 (34.1, 3.4, 27.2)
                ]
    
    	

    
    VRP = [25, 15, 80]   

    visi = Visibilidade_Normal(vertices, indices_faces,VRP ,True) #instancia da classe, so funfa assim
    visibilidade, centroide, vets_observacao , vets_normais = visi.main()

    #print(np.array(vets_observacao))  #printa como uma matriz numpy (mais facil assim)

    #print("\n")
    print(f"Centroide da face : {centroide} ")
    print(vets_observacao[0])
    print(vets_normais[0])
    
    if visibilidade[0] >= 0:
        print(f"Produto escalar da face : {visibilidade} --> A face é Visível!")
    else:
        print(f"Produto escalar da face : {visibilidade} --> A face não é visível!")

    print("\n")