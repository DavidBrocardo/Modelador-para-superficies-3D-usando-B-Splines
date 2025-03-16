import math
from Superfice_BSplines import BSplines
from Pintor_dist import Pintor_dist
from Recorte2D import Recorte2D
from Visibilidade_calc_Normal import Visibilidade_Normal
from FillPoly import FillPoly
from ProjecaoAxonometrica import ProjecaoAxonometrica
from Transformacoes_Geometricas import Transformacoes_Geometricas
from Recorte3D import Recorte3D
from Sombreamento_constante import Sombreamento_constante
from zbuffer_teste import ZBuffer
class Controle:
    def __init__(self,  tela, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, inp, VRP, P, Y, dp, windows, viewport,geometrica,valores_geo,corFrente,corFundo,constante,superfice,ila,il,luz_pos,ka,kd,ks,n):
                
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
        self.cor_aresta_frente = corFrente  
        self.cor_aresta_fundo = corFundo 
        #self.faces_ordenadas = faces
        self.superfice = superfice

        #---------Sombreamento--------------
        self.constante = constante  
        ila,il,luz_pos,ka,kd,ks,n
        self.ila = ila  # Luz ambiente
        self.il = il  # Intensidade da lampada
        self.luz_pos = luz_pos  # Posiçao da lampada

        #Propriedades do material
        self.ka = ka  # Coeficiente de reflexao ambiente
        self.kd = kd  # Coeficiente de reflexao difusa
        self.ks = ks  # Coeficiente de reflexao especular
        self.n = n  # Expoente especular
        

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
                elemento = [
                    lista_vertices[0][indice],
                    lista_vertices[1][indice],
                    lista_vertices[2][indice],
                ]
                linha.append(elemento)
            saida.append(linha)
        return saida

    def converter_pontos_superfice(self, lista_vertices):
        indice = 0
        saida_projetado = []
        for i in range(self.pontos_controleX + 1):
            linha = []
            for j in range(self.pontos_controleY + 1):
                indice = i * (self.pontos_controleY + 1) + j
                
                elemento = [
                    lista_vertices[0][indice],
                    lista_vertices[1][indice],
                    lista_vertices[2][indice]
                ]
                linha.append(elemento)
            
            saida_projetado.append(linha)
        
        return saida_projetado


    def axonometrica(self,entrada,pontos):       
        if pontos:
            projecao = ProjecaoAxonometrica(entrada, self.VRP, self.P, self.Y, self.windows, self.viewport)
            projecao = projecao.main() 
            self.inp_projetado = []
            if self.atualizarInp:
                self.inp_projetado= self.converter_pontos_superfice(projecao)   
            else:
                self.inp_projetado= self.converter_pontos_superfice(projecao)   
            
        else:             
            projecao = ProjecaoAxonometrica(entrada, self.VRP, self.P, self.Y,  self.windows, self.viewport)
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
        self.Faces_visi_centroide = {}
        for i in range(self.RESOLUTIONI - 1):            
            
            for j in range(self.RESOLUTIONJ - 1):
                vertices_face = []
                vertices_face.append(vertice_superfice[i][j])
                vertices_face.append(vertice_superfice[i][j+1]) 
                vertices_face.append(vertice_superfice[i+1][j+1]) 
                vertices_face.append(vertice_superfice[i+1][j]) 
                
                #Recorte 3D       
                recorte = Recorte3D(-100000, 1000000, vertices_face)
                
                vertices,recortou = recorte.Recortar3D() 
                if not(recortou):
                    self.recortou = recortou
                    #return self.inp, [], [], [],self.Faces_visi_centroide
                    
                    
                #Visibilidade
                #print(vertices_face)
                
                visi= Visibilidade_Normal(vertices_face,[[0,1,2,3]],self.VRP[:-1],True) 
                visibilidade, centroide, vets_observacao , vets_normais = visi.main()
                
                self.Faces.append([(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)])
                chave = ((i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j))
                self.Faces_visi_centroide[chave] = []
                                

                #Calculando o Sobreamento somente das faces visiveis
                if visibilidade[0] >= 0:
                    sombrear = Sombreamento_constante(self.ila, self.il, self.ka, self.kd, self.ks, self.n, self.luz_pos,
                                                    centroide[0], vets_normais[0], vets_observacao[0])
                    
                    iluminacoes = sombrear.Calcular_iluminacao_total() 

                    
                   
                    self.Faces_visi_centroide[chave].append([(visibilidade),(centroide),(vets_observacao),(vets_normais),(iluminacoes)])
                else:
                    print(vertices_face)
                    self.Faces_visi_centroide[chave].append([(visibilidade),(centroide),(vets_observacao),(vets_normais)])
                
        return  

    def pintor(self,faces_ordenadas, visiblidade, vertices, cor_fundo, cor_frente):
        self.tela.delete("all") 
        
        for i in faces_ordenadas:
            for _, face, superfice in i:
                    pontos = []            
                    chave = tuple(face)
                    
                    for i in face:
                        xi, yi = i
                        #print(xi,yi)
                        x = vertices[superfice][xi][yi][0]  # Coordenada X do vértice
                        y = vertices[superfice][xi][yi][1]  # Coordenada Y do vértice
                        z = vertices[superfice][xi][yi][2]  # Coordenada z do vértice
                        pontos.append((x, y, z))
                    
                    
                    visibilidadeSRU = visiblidade[superfice][chave][0][0]                               

                    #   a. Recorte 2D
                    recorte = Recorte2D(self.viewport, pontos)
                    poligono_recortado = recorte.Recortar_total()

                
                    
                    #   b. Algoritmo da scanline (Associar neste algoritmo z-buffer e o algoritmo de rasterização – Fillpoly)
                    #       i. Constante: Usar o fillpoly com a cor pré-computada anteriormente;
                    
                    if visibilidadeSRU[0] >= 0:
                        sombreamento = visiblidade[superfice][chave][0][4]
                        if(self.constante):
                            zbuffer = ZBuffer( self.viewport[2],  self.viewport[3],self.tela)
                            framebuffer, zbuffer_tela = zbuffer.triangulate_and_render(poligono_recortado, sombreamento[0])
                        #(zbuffer_tela)
                        else:

                            FillPoly(poligono_recortado,self.tela,sombreamento[0],self.constante)   
        
                            color = cor_frente[superfice]
                            if len(poligono_recortado) != 0:
                                x1, y1, z1 = poligono_recortado[0]
                                cond = True
                                for i in reversed(poligono_recortado):
                                    if cond :
                                        x2, y2, z2 = i
                                        self.tela.create_line(x1, y1, x2, y2, fill=color, width=1)
                                        cond  = False
                                    else:
                                        x1, y1, z1 = i
                                        self.tela.create_line(x2, y2, x1, y1, fill=color, width=1)
                                        x2 = x1
                                        y2 = y1
                        
                        
                    else:
                        FillPoly(poligono_recortado,self.tela,0, False)       
                        color = cor_fundo[superfice]
                        if len(poligono_recortado) != 0:
                            x1, y1, z1 = poligono_recortado[0]
                            cond = True
                            for i in reversed(poligono_recortado):
                                if cond :
                                    x2, y2, z2 = i
                                    self.tela.create_line(x1, y1, x2, y2, fill=color, width=1)
                                    cond  = False
                                else:
                                    x1, y1, z1 = i
                                    self.tela.create_line(x2, y2, x1, y1, fill=color, width=1)
                                    x2 = x1
                                    y2 = y1
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
            matriz_superfice , matriz_pontos = self.transformacoes_Geometricas(matriz_superfice,matriz_pontos)        
            
            self.inp = []
            self.inp = self.converter_pontos_superfice(matriz_pontos)
            
        
        # 2) Pré-cálculos 
        #   a. Centróides de faces e de objetos
        #       i. Recorte (3D) dos objetos que estejam antes do plano Near e depois do plano Far.
        #   b. Vetores normais das faces
        self.facePorFace(matriz_superfice)   
        
    
        if not(self.recortou):
            #Pintor
            pintor = Pintor_dist(self.converter_vertices_superfice(matriz_superfice), self.VRP, self.tela, self.viewport, self.superfice)           
            faces_ordenadas = (pintor.calcular_dists_e_ordenar_faces(self.Faces))

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
        #self.tela.delete("all") 
        # -- Aplicando o Algoritmo do Pintor -- 
            
            #print(faces_ordenadas)
            '''for _, face, _ in faces_ordenadas:
                pontos = []            
                chave = tuple(face)
                
                for i in face:
                    xi, yi = i
                    #print(xi,yi)
                    x = self.outp[xi][yi][0]  # Coordenada X do vértice
                    y = self.outp[xi][yi][1]  # Coordenada Y do vértice
                    z = self.outp[xi][yi][2]  # Coordenada z do vértice
                    pontos.append((x, y, z))
                
                
                visibilidadeSRU = self.Faces_visi_centroide[chave][0][0]
                
                
                
                # Modifica apenas as tuplas que possuem a face correta
                

                #   a. Recorte 2D
                recorte = Recorte2D(self.viewport, pontos)
                poligono_recortado = recorte.Recortar_total()

            
                
                #   b. Algoritmo da scanline (Associar neste algoritmo z-buffer e o algoritmo de rasterização – Fillpoly)
                #       i. Constante: Usar o fillpoly com a cor pré-computada anteriormente;
                
                if visibilidadeSRU[0] >= 0:
                    sombreamento = self.Faces_visi_centroide[chave][0][4]
                    FillPoly(poligono_recortado,self.tela,sombreamento[0],  self.constante)

                    color = self.cor_aresta_frente
                    if len(poligono_recortado) != 0:
                        x1, y1, z1 = poligono_recortado[0]
                        cond = True
                        for i in reversed(poligono_recortado):
                            if cond :
                                x2, y2, z2 = i
                                self.tela.create_line(x1, y1, x2, y2, fill=color, width=1)
                                cond  = False
                            else:
                                x1, y1, z1 = i
                                self.tela.create_line(x2, y2, x1, y1, fill=color, width=1)
                                x2 = x1
                                y2 = y1
                    
                    
                else:
                    FillPoly(poligono_recortado,self.tela,0, False)
                    color = self.cor_aresta_fundo
                    if len(poligono_recortado) != 0:
                        x1, y1, z1 = poligono_recortado[0]
                        cond = True
                        for i in reversed(poligono_recortado):
                            if cond :
                                x2, y2, z2 = i
                                self.tela.create_line(x1, y1, x2, y2, fill=color, width=1)
                                cond  = False
                            else:
                                x1, y1, z1 = i
                                self.tela.create_line(x2, y2, x1, y1, fill=color, width=1)
                                x2 = x1
                                y2 = y1'''
                    
            
         
                
                
                

      
        return self.inp, self.inp_projetado, self.outp, faces_ordenadas, self.Faces_visi_centroide
        
        
        
            
        

       
        