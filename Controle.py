from Superfice_BSplines import BSplines
from Pintor_dist import Pintor_dist
from Recorte2D import Recorte2D
from Visibilidade_calc_Normal import Visibilidade_Normal
from FillPoly import FillPoly
from ProjecaoAxonometrica import ProjecaoAxonometrica
from Transformacoes_Geometricas import Transformacoes_Geometricas
from Recorte3D import Recorte3D

class Controle:
    def __init__(self,  tela, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp, VRP, P, Y, dp, windows, viewport,geometrica,valores_geo):
                
        # Parâmetros de controle
        self.inp = inp
        self.tela = tela
        self.pontos_controleX= pontos_controleX
        self.pontos_controleY= pontos_controleY
        self.TI= TI
        self.TJ= TJ
        self.RESOLUTIONI= RESOLUTIONI
        self.RESOLUTIONJ= RESOLUTIONJ
        self.VRP = VRP
        self.P = P
        self.Y = Y
        self.dp = dp
        self.windows = windows
        self.viewport = viewport
        self.geometrica = geometrica
        self.valores_geo = valores_geo
        self.atualizarInp = False

    def converter_vertices_tradicional(self, lista_vertices):
        vertices_covertido = [[], [], [],[]]  
        for linha in lista_vertices:  
            for item in linha: 
                x, y, z = item 
                vertices_covertido[0].append(x)
                vertices_covertido[1].append(y)
                vertices_covertido[2].append(z)
                vertices_covertido[3].append(1)
        return vertices_covertido        
    
    def converter_vertices_superfice(self, lista_vertices):
            indice = 0
            saida = []
            for i in range(self.RESOLUTIONI):
                linha = []
                for j in range(self.RESOLUTIONJ):
                    indice = i * self.RESOLUTIONJ + j
                    elemento = [lista_vertices[0][indice] ,
                                lista_vertices[1][indice] ,
                                lista_vertices[2][indice] ]  
                             
                    linha.append(elemento)
                saida.append(linha)
            return saida
    
    def converter_pontos_superfice(self, lista_vertices):
            indice = 0
            saida_inp = []
            saida_projetado =[]
            for i in range(self.pontos_controleX + 1):
                linha = []
                for j in range(self.pontos_controleY + 1):
                    indice = i * (self.pontos_controleY + 1) + j
                    # projecao[0], projecao[1], projecao[2] contêm as coordenadas projetadas (desconsiderando W)
                    elemento = [lista_vertices[0][indice],
                                lista_vertices[1][indice],
                                lista_vertices[2][indice]]
                    #print(elemento)
                    linha.append(elemento)
                if self.atualizarInp:
                    saida_inp.append(linha)
                saida_projetado.append(linha) 
            return saida_projetado, saida_inp

    def axonometrica(self,entrada,pontos):       
        if pontos:
            #vertices=[]
            #vertices = self.converter_vertices_tradicional(entrada)
            projecao = ProjecaoAxonometrica(entrada, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.inp_projetado = []
            if self.atualizarInp:
                self.inp = []
                self.inp_projetado,self.inp = self.converter_pontos_superfice(projecao)   
            else:
                self.inp_projetado, _ = self.converter_pontos_superfice(projecao)   
            
        else:
            #vertices=[]      
            #vertices = self.converter_vertices_tradicional(self.outp)                   
            projecao = ProjecaoAxonometrica(entrada, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport)
            projecao = projecao.main() 
            self.outp = []
            self.outp = self.converter_vertices_superfice(projecao)

    def transformacoes_Geometricas(self,vertices,pontos):
        # geometrica  = 0 (Nenhuma) / =1 (Escala) / = 2 (Rotacao) / = 3 (Translacao)
                
        operacao = Transformacoes_Geometricas(vertices) 
        self.atualizarInp = True
        if self.geometrica == 1:     # ESCALA       
            if self.valores_geo != 1.0 and self.valores_geo  != 0:
                resul_escala_superfice = operacao.Escala(self.valores_geo)

                operacao = Transformacoes_Geometricas(pontos) 
                resul_escala_pontos = operacao.Escala(self.valores_geo)
                #self.converter_pontos_superfice(resul_escala,True)
                #print (vertices)
                print ("Escala em " , self.valores_geo)
                return resul_escala_superfice, resul_escala_pontos
            else:
                return vertices, pontos

        if self.geometrica  == 2:    # ROTACAO
            x,y,z = self.valores_geo[0]   
            resul_rotacao_x = operacao.Rotacao_em_x(x)
            operacao = Transformacoes_Geometricas(resul_rotacao_x) 
            resul_rotacao_y = operacao.Rotacao_em_y(y)
            operacao = Transformacoes_Geometricas(resul_rotacao_y) 
            resul_rotacao_z_superfice = operacao.Rotacao_em_z(z)

            operacao = Transformacoes_Geometricas(pontos)
            resul_rotacao_x = operacao.Rotacao_em_x(x)
            operacao = Transformacoes_Geometricas(resul_rotacao_x) 
            resul_rotacao_y = operacao.Rotacao_em_y(y)
            operacao = Transformacoes_Geometricas(resul_rotacao_y) 
            resul_rotacao_z_pontos = operacao.Rotacao_em_z(z)

            return resul_rotacao_z_superfice, resul_rotacao_z_pontos

        if self.geometrica == 3: # TRANSLACAO
            x,y,z = self.valores_geo[0]
            resul_translacao_superfice = operacao.Translacao(x,y,z)

            operacao = Transformacoes_Geometricas(pontos) 
            resul_translacao_pontos = operacao.Translacao(x,y,z)

            return resul_translacao_superfice, resul_translacao_pontos
        

    def facePorFace(self, vertices):
        # Percorre face por face, realizano o recorte/visibilidade...
        # Armazena junto aos valores das Faces, se é visivel e o centroide

        vertice_superfice = []
        vertice_superfice = self.converter_vertices_superfice(vertices)
        self.Faces = []
        self.Faces_visi_centroide = []
        for i in range(self.RESOLUTIONI - 1):            
            vertices_face = []

            for j in range(self.RESOLUTIONJ - 1):
                vertices_face.append(vertice_superfice[i][j])
                vertices_face.append(vertice_superfice[i][j+1]) 
                vertices_face.append(vertice_superfice[i+1][j+1]) 
                vertices_face.append(vertice_superfice[i+1][j]) 
                #Recorte 3D      
                #print(vertices_face)      
                #recorte = Recorte3D(0, 600, pontos)
                #vertices,recortou = recorte.Recortar3D() #Fazer um tratamento para tirar toda a face
                recortou =False
                if not(recortou):
                    #Visibilidade
                    visi= Visibilidade_Normal(vertices_face,[[0,1,2,3]],self.VRP[:-1],True) 
                    visibilidade = visi.main()
                    self.Faces.append([(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)])
                    self.Faces_visi_centroide.append(visibilidade)
            

                #ACHO QUE TALVEZ SEJA LEGAL JA CHAMAR O SOBREAMENTO AQUI, JA TEM O CENTROIDE POR EXEMPLO
        return  


                

    def main(self):       

        #CRIAR A SUPERFICE 
        # Calcula a superfície B-Spline
        bspline = BSplines(self.pontos_controleX, self.pontos_controleY ,self.TI, self.TJ, self.RESOLUTIONI, self.RESOLUTIONJ,
                           self.inp, self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0)
        self.pontos_SRU,  self.Superfice_SRU = bspline.main()
        
        #TRANSFORMANDO EM FORMATO Padrao de Matriz 
        matriz_superfice=[]
        matriz_pontos=[]
        matriz_pontos = self.converter_vertices_tradicional(self.pontos_SRU)
        matriz_superfice = self.converter_vertices_tradicional(self.Superfice_SRU)
        
        # 1) Objetos modelados em SRU
        #   a.Transformações geométricas (rotações, translações, escalas, cisalhamentos, etc. aplicada ao objeto).
        if self.geometrica != 0:
            print("jacu")
            matriz_superfice , matriz_pontos = self.transformacoes_Geometricas(matriz_superfice,matriz_pontos)        

        # 2) Pré-cálculos 
        #   a. Centróides de faces e de objetos
        #       i. Recorte (3D) dos objetos que estejam antes do plano Near e depois do plano Far.
        #   b. Vetores normais das faces
        self.facePorFace(matriz_superfice)    

        #   c. Sombreamento constante
        #       i. Computar o valor de iluminação total (cor) de cada face

        #   d. Sombreamento Gouraud ou Phong:
        #       i. Vetores normais médios unitários nos vértices
        #       ii. Gouraud: Calcular a iluminação total nos vértices

        # 3) Aplicar as matrizes do pipeline (Converter objeto do SRU para o SRT)
            #PONTOS
        self.axonometrica(matriz_pontos,True)          
            #SUPERFICE
        self.axonometrica(matriz_superfice,False)    


        # 4) Aplicar o teste de visibilidade pelo cálculo da normal para cada face de objeto restante.
        self.tela.delete("all") 
        # -- Aplicando o Algoritmo do Pintor -- 
        faces=[]
        for i in range(self.RESOLUTIONI - 1):
            for j in range(self.RESOLUTIONJ - 1):
                faces.append([(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)])

        pintor = Pintor_dist(self.outp, self.VRP, self.tela,self.viewport)           
        faces_ordenadas = pintor.calcular_dists_e_ordenar_faces(faces)

        for _, face in faces_ordenadas:
            pontos = []
            for i in face:
                xi, yi = i
                x = self.outp[xi][yi][0]  # Coordenada X do vértice
                y = self.outp[xi][yi][1]  # Coordenada Y do vértice
                z = self.outp[xi][yi][2]  # Coordenada z do vértice
                pontos.append((x, y, z))

            #   a. Recorte 2D
            recorte = Recorte2D(self.viewport, pontos)
            poligono_recortado = recorte.Recortar_total()

            #   b. Algoritmo da scanline (Associar neste algoritmo z-buffer e o algoritmo de rasterização – Fillpoly)
            #       i. Constante: Usar o fillpoly com a cor pré-computada anteriormente;
            FillPoly(poligono_recortado,self.tela,"white")
             #       ii. Gouraud: Usar o fillpoly interpolando as cores dos vértices que foram pré-calculadas;
        
            #       iii. Phong: Usar o fillpoly interpolando os vetores normais dos vértices que foram pré-calculados e, na sequência, calcular a iluminação total (cor) em cada pixel.

            # -- Desenhar a  superfice --             

            if len(poligono_recortado) != 0:
                x1, y1, z1 = poligono_recortado[0]
                cond = True
                for i in reversed(poligono_recortado):
                    if cond :
                        x2, y2, z2 = i
                        self.tela.create_line(x1, y1, x2, y2, fill="black", width=1)
                        cond  = False
                    else:
                        x1, y1, z1 = i
                        self.tela.create_line(x2, y2, x1, y1, fill="black", width=1)
                        x2 = x1
                        y2 = y1

        return self.inp, self.inp_projetado, self.outp
        
        
        
            
        

       
        