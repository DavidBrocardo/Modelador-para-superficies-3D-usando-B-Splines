import tkinter as tk
import math
import random
import ast
import re
from tkinter import simpledialog, messagebox
from Controle import Controle
from tkinter import colorchooser

 
class Interface:
    def __init__(self, tela, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, espacamento, VRP, P, Y, dp, windows, viewport):
        self.tela = tela
        self.tela.title("Superfície Spline")
        self.tela.geometry("700x700")
        self.canvas = tk.Canvas(self.tela, width=viewport[2], height=viewport[3], bg="white")
        self.canvas.pack(pady=10)

        # Parâmetros
        self.superficie_selecionada = 0
        self.pontos_controleX = {}
        self.pontos_controleY = {}
        self.pontos_controleX[self.superficie_selecionada] = pontos_controleX
        self.pontos_controleY[self.superficie_selecionada] = pontos_controleY
        self.TI = {}
        self.TJ = {}
        self.TI[self.superficie_selecionada] = TI
        self.TJ[self.superficie_selecionada] = TJ
        self.RESOLUTIONI = {}
        self.RESOLUTIONJ = {}
        self.RESOLUTIONI[self.superficie_selecionada] = RESOLUTIONI
        self.RESOLUTIONJ[self.superficie_selecionada] = RESOLUTIONJ
        self.espacamento = espacamento
        self.VRP = VRP
        self.P = P
        self.Y = Y
        self.dp = dp
        self.windows = windows
        self.viewport = viewport
        self.inp = {}
        self.outp = {}
        self.inp_Axo = {}  
        self.superficie_selecionada = 0
        self.quantidadeSuperfice = 0
        self.ponto_inicial = {}
        self.ponto_inicial[self.superficie_selecionada] = [0,0,0]
        self.cor_aresta_frente = {}
        self.cor_aresta_fundo = {}
        self.cor_aresta_frente[self.superficie_selecionada] = "Green"  
        self.cor_aresta_fundo[self.superficie_selecionada] = "Red" 
        self.faces = []
        self.constante = []
        self.sobreamento = False
        # Criar interface
        self.criar_menu()
        self.criar_botoes()
        self.click_x = tk.IntVar()
        self.click_y = tk.IntVar()

        self.canvas.bind("<Button-1>", self.clique) 

         #---------Sombreamento--------------
        
        self.ila = (80,150,250) 
        self.il = (120,40,248)
        self.Luz= (80,80,80) #20 20 70
        self.ka = {}    
        self.ka[self.superficie_selecionada] = (0.2,0.5,0.8)
        self.kd = {}  
        self.kd[self.superficie_selecionada] = (0.1,0.2,0.5) 
        self.ks = {} 
        self.ks[self.superficie_selecionada] = (0.3,0.1,0.8) 
        self.n = {}
        self.n[self.superficie_selecionada] = 3     
        #self.luz_pos = [25, 15, 80]      
       

        self.main()

    

    def criar_menu(self):
        """Cria a barra de menu suspenso."""
        menu_principal = tk.Menu(self.tela)

        # Menu Superfice
        menu_superfice = tk.Menu(menu_principal, tearoff=0)
        menu_superfice.add_command(label="Pontos de Controle", command=self.definir_ponto_controle)
        menu_superfice.add_command(label="Ponto Focal", command=self.ponto_focal)
        menu_superfice.add_command(label="Camera", command=self.definir_camera)
        menu_superfice.add_command(label="Viewport", command=self.definir_viewport)
        menu_superfice.add_command(label="Window", command=self.definir_windows)
        menu_principal.add_cascade(label="Superficie", menu=menu_superfice)
        
        # Menu Transformações Geometricas
        menu_geometrico = tk.Menu(menu_principal, tearoff=0)
        menu_geometrico.add_command(label="Escala", command=self.escala)
        menu_geometrico.add_command(label="Rotação", command=self.rotacao)
        menu_geometrico.add_command(label="Translação", command=self.translacao)
        menu_principal.add_cascade(label="Transformações Geometricas", menu=menu_geometrico)

        # Menu Arquivo
        # Exemplo de uso:


        menu_arquivo = tk.Menu(menu_principal, tearoff=0)
        menu_arquivo.add_command(label="Abrir", command=self.abrir_arquivo)
        menu_arquivo.add_command(label="Salvar", command=self.salvar_arquivo)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.sair)
        menu_principal.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Pintura
        menu_pintor = tk.Menu(menu_principal, tearoff=0)
        menu_pintor.add_command(label="Remover Sombreamento",command=self.sobra_remover)
        menu_pintor.add_command(label="Cor Aresta Frente",command=self.cor_frente)
        menu_pintor.add_command(label="Cor Aresta Fundo",command=self.cor_fundo)
        menu_principal.add_cascade(label="Pintura", menu=menu_pintor)

        # Menu Sobreamento
        menu_sobra = tk.Menu(menu_principal, tearoff=0)
        menu_sobra.add_command(label="Aplicar Sombreamento Constante", command=self.sobra_aplicar)
        menu_sobra.add_command(label="Alterar Parâmetros", command=self.sobra_parametros)     
        menu_principal.add_cascade(label="Sombreamento", menu=menu_sobra)

        self.tela.config(menu=menu_principal)

    def criar_botoes(self):
        frame_botoes = tk.Frame(self.tela)
        frame_botoes.pack(pady=10)

        btn_pontos = tk.Button(frame_botoes, text="Nova Superfície", command=self.definir_nova_superfice, width=25, bg="Gray")
        btn_pontos.grid(row=0, column=0, padx=5)

        # Botão para atualizar a lista de superfícies
        self.botao_atualizar = tk.Button(frame_botoes, text="Selecionar Superfície", command=self.atualizar_menu, width=25, bg="Gray")
        self.botao_atualizar.grid(row=0, column=1, padx=5)

        self.var_superficie = tk.StringVar()
        self.var_superficie.set("0")

        self.menu_button = tk.Menubutton(frame_botoes, textvariable=self.var_superficie, relief="raised")
        self.menu_button.grid(row=1, column=1, padx=5)

        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
      
    def salvar_arquivo(self, arquivo="superfices.txt"):
        with open(arquivo, 'w') as f:
            for atributo, valor in self.__dict__.items():                
                if(atributo != "tela" and atributo != "canvas" ):
                   
                    tipo = type(valor)
                    #if isinstance(valor, (list, tuple)):                      
                     #   valor = ','.join(map(str, valor))  # transforma tudo em  string
                    f.write(f"{tipo};{atributo};{valor}\n")
        messagebox.showinfo("Salvando", "Superfices salvas no arquivo: "+arquivo)   

    def abrir_arquivo(self, arquivo="superfices.txt"):
        with open(arquivo, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue                 
                tipo_str, var_nome, conteudo_str = linha.split(';', 2)
                # Extrai o nome do tipo 
                match = re.search(r"'(\w+)'", tipo_str)
                if not match:
                    continue  
                tipo_nome = match.group(1)

                try:
                    if tipo_nome == 'int':
                        valor = int(conteudo_str)
                    elif tipo_nome == 'float':
                        valor = float(conteudo_str)
                    elif tipo_nome == 'str':
                        valor = conteudo_str  
                    elif tipo_nome in ('dict', 'list'):
                        valor = ast.literal_eval(conteudo_str) 
                    else:
                        continue 
                except (ValueError, SyntaxError):
                    continue
                
                setattr(self, var_nome, valor)        
                    
                
                          
        self.canvas.delete("all") 
        self.outp = {}
        all_faces = []
        visibilidade = {}
        for superfice in range(self.quantidadeSuperfice):                    
                control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                            self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                all_faces.append(faces)
        if (self.sobreamento):
            for superfice in range(self.quantidadeSuperfice):
                
                control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
        else:
            faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
            control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)

    def sair(self):
        self.tela.quit()

    def clique(self, event):
        self.click_x.set(event.x)
        self.click_y.set(event.y) 

    def atualizar_menu(self):
        self.menu.delete(0, "end")  # Remove opções antigas
        for superficie in range(self.quantidadeSuperfice):
            self.menu.add_command(
                label=f"{superficie}",
                command=lambda s=superficie: self.atualizar_selecao(s)  # Captura o valor atual corretamente
            )
        

    def atualizar_selecao(self, superficie):        
        self.var_superficie.set(f"{superficie}")
        self.superficie_selecionada = int(self.var_superficie.get())
        

    def definir_ponto_controle(self):
        messagebox.showinfo("", "Clique proximo ao ponto que deseja alterar")
        self.desenhar_pontoControle()
        self.atualizar_menu()
        self.tela.wait_variable(self.click_x)  # Espera um clique
        x_alvo, y_alvo = self.click_x.get(), self.click_y.get()
        
        ponto_mais_proximo = None
        menor_distancia = float('inf')

        for i in range(self.pontos_controleX[self.superficie_selecionada] + 1):
            for j in range(self.pontos_controleY[self.superficie_selecionada] + 1):
                x = self.inp_Axo[self.superficie_selecionada][i][j][0]
                y = self.inp_Axo[self.superficie_selecionada][i][j][1] 
                distancia = math.sqrt((x - x_alvo)**2 + (y - y_alvo)**2 )
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    posi_i = i
                    posi_j = j
                    x = self.inp[self.superficie_selecionada][i][j][0]
                    y = self.inp[self.superficie_selecionada][i][j][1] 
                    z = self.inp[self.superficie_selecionada][i][j][2] 
                    ponto_mais_proximo = (int(x), int(y), int(z))

              
        
        messagebox.showinfo("Ponto selecionado:", ponto_mais_proximo)

        janela = tk.Toplevel(self.tela)
        janela.title("Definir Novo Ponto Controle (Cordenadas de Mundo)")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Entry(janela)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y").grid(row=0, column=1)
        entrada_y = tk.Entry(janela)
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z").grid(row=0, column=2)
        entrada_z = tk.Entry(janela)
        entrada_z.grid(row=1, column=2)
        
        def Salvar():
            self.inp[self.superficie_selecionada][posi_i][posi_j][0] =  int(entrada_x.get())
            self.inp[self.superficie_selecionada][posi_i][posi_j][1] =  int(entrada_y.get())
            self.inp[self.superficie_selecionada][posi_i][posi_j][2] =  int(entrada_z.get())
           

            janela.destroy()                      
            # Calcula a superfície B-Spline
            self.canvas.delete("all") 
           
            self.outp = {}
            all_faces = []
            visibilidade = {}
            for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces , visibilidade[superfice]  = control.main()
                    
                    all_faces.append(faces)
            if (self.sobreamento):
                for superfice in range(self.quantidadeSuperfice):
                    
                    control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
            else:
                faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=4)
        

    def cor_frente(self):        
        cor = colorchooser.askcolor(title="Escolha a cor da aresta da frente")[1]
        if cor:  
            self.cor_aresta_frente[self.superficie_selecionada] = cor  
            
            self.canvas.delete("all") 
            self.outp = {}
            all_faces = []
            visibilidade = {}
            for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
            if (self.sobreamento):
                for superfice in range(self.quantidadeSuperfice):
                    
                    control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
            else:
                faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)         

    def cor_fundo(self):        
        cor = colorchooser.askcolor(title="Escolha a cor da aresta do fundo")[1]
        if cor:
            self.cor_aresta_fundo[self.superficie_selecionada] = cor  
               
            self.canvas.delete("all") 
            self.outp = {}
            all_faces = []
            visibilidade = {}
            for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
            
            if (self.sobreamento):
                for superfice in range(self.quantidadeSuperfice):
                    
                    control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
            else:
                faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
                    
        
    def sobra_aplicar(self):
        
        self.sobreamento = True
        self.outp = {}
        all_faces = []
        visibilidade = {}
        self.canvas.delete("all") 
        for superfice in range(self.quantidadeSuperfice):                    
                control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                            self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                _, self.inp_Axo[superfice], self.outp[superfice], faces,visibilidade[superfice] = control.main()
                all_faces.append(faces)
                
        if (self.sobreamento):
            
            for superfice in range(self.quantidadeSuperfice):

                
                control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])


    def sobra_remover(self):
         
         self.sobreamento = False
         self.outp = {}
         all_faces = []
         visibilidade = {}
         self.canvas.delete("all") 
         for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()     
                    all_faces.append(faces)
         faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
         control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)           
    
    def sobra_parametros(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Novos Valores")
        

        # Configurar colunas para alinhamento uniforme
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_columnconfigure(1, weight=1)
        janela.grid_columnconfigure(2, weight=1)

        tk.Label(janela, text="Iluminação Ambiente Posição :").grid(row=0, column=0, columnspan=3)          

        tk.Label(janela, text="X:").grid(row=1, column=0, sticky="w")
        ambiente_x = tk.Entry(janela, width=10,)
        ambiente_x.grid(row=2, column=0)

        tk.Label(janela, text="Y:").grid(row=1, column=1, sticky="w")
        ambiente_y = tk.Entry(janela, width=10)
        ambiente_y.grid(row=2, column=1)

        tk.Label(janela, text="Z:").grid(row=1, column=2, sticky="w")
        ambiente_z = tk.Entry(janela, width=10)
        ambiente_z.grid(row=2, column=2)


        tk.Label(janela, text="Iluminação Ambiente Intensidade (IIa):").grid(row=3, column=0, columnspan=3)          

        tk.Label(janela, text="Red:").grid(row=4, column=0, sticky="w")
        IIa_r = tk.Entry(janela, width=10,)
        IIa_r.grid(row=5, column=0)

        tk.Label(janela, text="Green:").grid(row=4, column=1, sticky="w")
        IIa_g = tk.Entry(janela, width=10)
        IIa_g.grid(row=5, column=1)

        tk.Label(janela, text="Blue:").grid(row=4, column=2, sticky="w")
        IIa_b = tk.Entry(janela, width=10)
        IIa_b.grid(row=5, column=2)

        tk.Label(janela, text="Iluminação Luminosa (II) :").grid(row=6, column=0, columnspan=3)          

        tk.Label(janela, text="Red:").grid(row=7, column=0, sticky="w")
        II_r = tk.Entry(janela, width=10,)
        II_r.grid(row=8, column=0)

        tk.Label(janela, text="Green:").grid(row=7, column=1, sticky="w")
        II_g= tk.Entry(janela, width=10)
        II_g.grid(row=8, column=1)

        tk.Label(janela, text="Blue:").grid(row=7, column=2, sticky="w")
        II_b = tk.Entry(janela, width=10)
        II_b.grid(row=8, column=2)

        tk.Label(janela, text="Ka :").grid(row=9, column=0, columnspan=3)          

        tk.Label(janela, text="Red:").grid(row=10, column=0, sticky="w")
        ka_r = tk.Entry(janela, width=10,)
        ka_r.grid(row=11, column=0)

        tk.Label(janela, text="Green:").grid(row=10, column=1, sticky="w")
        ka_g= tk.Entry(janela, width=10)
        ka_g.grid(row=11, column=1)

        tk.Label(janela, text="Blue:").grid(row=10, column=2, sticky="w")
        ka_b = tk.Entry(janela, width=10)
        ka_b.grid(row=11, column=2)

        tk.Label(janela, text="Kd :").grid(row=12, column=0, columnspan=3)          

        tk.Label(janela, text="Red:").grid(row=13, column=0, sticky="w")
        kd_r = tk.Entry(janela, width=10,)
        kd_r.grid(row=14, column=0)

        tk.Label(janela, text="Green:").grid(row=13, column=1, sticky="w")
        kd_g= tk.Entry(janela, width=10)
        kd_g.grid(row=14, column=1)

        tk.Label(janela, text="Blue:").grid(row=13, column=2, sticky="w")
        kd_b = tk.Entry(janela, width=10)
        kd_b.grid(row=14, column=2)

        tk.Label(janela, text="Ks :").grid(row=15, column=0, columnspan=3)          

        tk.Label(janela, text="Red:").grid(row=16, column=0, sticky="w")
        ks_r = tk.Entry(janela, width=10,)
        ks_r.grid(row=17, column=0)

        tk.Label(janela, text="Green:").grid(row=16, column=1, sticky="w")
        ks_g= tk.Entry(janela, width=10)
        ks_g.grid(row=17, column=1)

        tk.Label(janela, text="Blue:").grid(row=16, column=2, sticky="w")
        ks_b = tk.Entry(janela, width=10)
        ks_b.grid(row=17, column=2)         

        tk.Label(janela, text="N:").grid(row=18, column=1, sticky="w")
        n = tk.Entry(janela, width=10,)
        n.grid(row=19, column=1)

        def Salvar():
            
                #Luz posi
                x = float(ambiente_x.get())
                y = float(ambiente_y.get())
                z = float(ambiente_z.get())
                self.Luz = []
                self.Luz =  [x, y , z]
                #IIa
                x = float(IIa_r.get())
                y = float(IIa_g.get())
                z = float(IIa_b.get())
                self.ila = []
                self.ila =  [x, y , z]
                #IL 
                x = float(II_r.get())
                y = float(II_g.get())
                z = float(II_b.get())
                self.il = []
                self.il =  [x, y , z]
                #Ka
                x = float(ka_r.get())
                y = float(ka_g.get())
                z = float(ka_b.get())
                self.ka[self.superficie_selecionada] = []  
                self.ka[self.superficie_selecionada] = [x, y , z]
                #Kd
                x = float(kd_r.get())
                y = float(kd_g.get())
                z = float(kd_b.get())
                self.kd[self.superficie_selecionada] = []  
                self.kd[self.superficie_selecionada] = [x, y , z]  
                #Ks
                x = float(ks_r.get())
                y = float(ks_g.get())
                z = float(ks_b.get())
                self.ks[self.superficie_selecionada] = []  
                self.ks[self.superficie_selecionada] = [x, y , z]
                #
                x = float(n.get())
                self.n[self.superficie_selecionada] = x
                

                self.canvas.delete("all") 
                self.outp = {}
                all_faces = []
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice):  
                                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    
                    all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                    faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                    control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
                    
        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=20, columnspan=3)


    def definir_nova_superfice(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Valores")

        # Configurar colunas para alinhamento uniforme
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_columnconfigure(1, weight=1)
        janela.grid_columnconfigure(2, weight=1)

        tk.Label(janela, text="Tamanho da Matrix:").grid(row=0, column=0, columnspan=3)          

        tk.Label(janela, text="Linhas (X):").grid(row=1, column=0, sticky="w")
        entrada_x = tk.Entry(janela, width=10)
        entrada_x.grid(row=2, column=0)

        tk.Label(janela, text="Colunas (Y):").grid(row=1, column=1, sticky="w")
        entrada_y = tk.Entry(janela, width=10)
        entrada_y.grid(row=2, column=1)


        tk.Label(janela, text="Resolução:").grid(row=3, column=0, columnspan=3)

        tk.Label(janela, text="Linhas:").grid(row=4, column=0, sticky="w")
        entrada_ResoI = tk.Entry(janela, width=10)
        entrada_ResoI.grid(row=5, column=0)

        tk.Label(janela, text="Colunas:").grid(row=4, column=1, sticky="w")
        entrada_ResoJ = tk.Entry(janela, width=10)
        entrada_ResoJ.grid(row=5, column=1)

        tk.Label(janela, text="Que ponto deseja iniciar a nova superfície:").grid(row=6, column=0, columnspan=3)

        tk.Label(janela, text="X:").grid(row=7, column=0, sticky="w")
        entrada_xponto = tk.Entry(janela, width=10)
        entrada_xponto.grid(row=8, column=0)

        tk.Label(janela, text="Y:").grid(row=7, column=1, sticky="w")
        entrada_yponto = tk.Entry(janela, width=10)
        entrada_yponto.grid(row=8, column=1)

        tk.Label(janela, text="Z:").grid(row=7, column=2, sticky="w")
        entrada_zponto = tk.Entry(janela, width=10)
        entrada_zponto.grid(row=8, column=2)

        tk.Label(janela, text="Numeros de linha interpoladas:").grid(row=9, column=0, columnspan=3)
        entrada_ti = tk.Entry(janela, width=10)
        entrada_ti.grid(row=11, column=0)

        def Salvar():
            if 4 <=  int(entrada_x.get()) <= 100 and 4 <= int(entrada_y.get()) <= 100:               
                
                self.quantidadeSuperfice += 1
                self.superficie_selecionada =  self.quantidadeSuperfice-1                
                    
                self.pontos_controleX[self.superficie_selecionada] = int(entrada_x.get())
                self.pontos_controleY[self.superficie_selecionada] = int(entrada_y.get())
                
                self.RESOLUTIONI[self.superficie_selecionada] = int(entrada_ResoI.get())
                self.RESOLUTIONJ[self.superficie_selecionada] = int(entrada_ResoJ.get())
                
                self.ponto_inicial[self.superficie_selecionada]= [int(entrada_xponto.get()),int(entrada_yponto.get()),int(entrada_zponto.get())]
                self.TI[self.superficie_selecionada] = int(entrada_ti.get())
                self.TJ[self.superficie_selecionada] = int(entrada_ti.get())
                self.cor_aresta_frente[self.superficie_selecionada] = "Green"
                self.cor_aresta_fundo[self.superficie_selecionada] = "Red"
                self.criar_pontos_controle() 

                janela.destroy()                      
                # Calcula a superfície B-Spline
                
                self.canvas.delete("all") 
                self.outp = {}                
                all_faces = []
                visibilidade = {}
                
                self.ka[self.superficie_selecionada] = (0.2,0.5,0.8)
                #self.kd = {}   
                self.kd[self.superficie_selecionada] = (0.1,0.2,0.5) 
                #self.ks = {} 
                self.ks[self.superficie_selecionada] = (0.3,0.1,0.8) 
                #self.n = {}
                self.n[self.superficie_selecionada] = 3    
                for superfice in range(self.quantidadeSuperfice):   
                             
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces) 

                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
        
                self.superficie_selecionada -= 1 
                self.atualizar_menu()
                
            else:
                
                 janela.destroy()
                 messagebox.showinfo("", "Valores inválidos ")
                 self.definir_nova_superfice()   
        tk.Button(janela, text="Salvar", command=Salvar).grid(row=12, column=0, columnspan=3)
        

    def ponto_focal(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Camera")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=1000, increment=1, width=10)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y:").grid(row=0, column=1)  # Adicionado dois pontos para consistência
        entrada_y = tk.Spinbox(janela, from_=0, to=1000, increment=1, width=10) # Spinbox para Y
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=0, column=2) # Adicionado dois pontos para consistência
        entrada_z = tk.Spinbox(janela, from_=0, to=1000, increment=1, width=10) # Spinbox para Z
        entrada_z.grid(row=1, column=2)

        def Salvar():
            try:  # Tratamento de erros para entradas inválidas
                x = float(entrada_x.get())
                y = float(entrada_y.get())
                z = float(entrada_z.get())
                self.P = []
                self.P =  [x, y , z, 1]

                self.canvas.delete("all") 
                self.outp = {}
                all_faces = []
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
                    
                   
               

            except ValueError:
                tk.messagebox.showerror("Erro", "Por favor, insira números válidos.")  # Mensagem de erro

        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=2, columnspan=3)


    def definir_windows(self):
        #windows = [-100, -100, 100, 100]
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Viewport")

        tk.Label(janela, text="X min:").grid(row=0, column=0)
        entrada_xMin = tk.Entry(janela)
        entrada_xMin.grid(row=1, column=0)

        tk.Label(janela, text="X max").grid(row=0, column=1)
        entrada_xMax = tk.Entry(janela)
        entrada_xMax.grid(row=1, column=1)

        tk.Label(janela, text="Y min:").grid(row=0, column=2)
        entrada_yMin = tk.Entry(janela)
        entrada_yMin.grid(row=1, column=2)

        tk.Label(janela, text="Y max:").grid(row=0, column=3)
        entrada_yMax = tk.Entry(janela)
        entrada_yMax.grid(row=1, column=3)
        
        def Salvar():
            x_min = float(entrada_xMin.get())
            x_max = float(entrada_xMax.get())
            y_min = float(entrada_yMin.get())
            y_max = float(entrada_yMax.get())
            self.windows = []
            self.windows =  [x_min, y_min, x_max, y_max] # u v u v
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            self.canvas.delete("all") 
            self.outp = {}
            all_faces = []
            visibilidade = {}
            for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
            if (self.sobreamento):
                for superfice in range(self.quantidadeSuperfice):
                    
                    control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
            else:
                faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)       
                   
            

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=4)


    def definir_viewport(self):
        
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Viewport")

        tk.Label(janela, text="U min:").grid(row=0, column=0)
        entrada_uMin = tk.Entry(janela)
        entrada_uMin.grid(row=1, column=0)

        tk.Label(janela, text="U max").grid(row=0, column=1)
        entrada_uMax = tk.Entry(janela)
        entrada_uMax.grid(row=1, column=1)

        tk.Label(janela, text="V min:").grid(row=0, column=2)
        entrada_vMin = tk.Entry(janela)
        entrada_vMin.grid(row=1, column=2)

        tk.Label(janela, text="V max:").grid(row=0, column=3)
        entrada_vMax = tk.Entry(janela)
        entrada_vMax.grid(row=1, column=3)
        
        def Salvar():
            u_min = float(entrada_uMin.get())
            u_max = float(entrada_uMax.get())
            v_min = float(entrada_vMin.get())
            v_max = float(entrada_vMax.get())
            self.viewport = []
            self.viewport =  [u_min, v_min, u_max, v_max]
            
            
            janela.destroy()                      
            # Calcula a superfície B-Spline
            self.canvas.delete("all") 
            self.outp = {}
            all_faces = []
            visibilidade = {}
            for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] , self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
            if (self.sobreamento):
                for superfice in range(self.quantidadeSuperfice):
                    
                    control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
            else:
                faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)        
                    
            

        tk.Button(janela, text="Salvar", command=Salvar).grid(row=2, columnspan=4)

    def definir_camera(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Definir Nova Camera")

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=100, increment=1, width=10)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y:").grid(row=0, column=1)  # Adicionado dois pontos para consistência
        entrada_y = tk.Spinbox(janela, from_=0, to=100, increment=1, width=10) # Spinbox para Y
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=0, column=2) # Adicionado dois pontos para consistência
        entrada_z = tk.Spinbox(janela, from_=0, to=100, increment=1, width=10) # Spinbox para Z
        entrada_z.grid(row=1, column=2)

        def Salvar():
            try:  
                x = float(entrada_x.get())
                y = float(entrada_y.get())
                z = float(entrada_z.get())
                self.VRP = [x, y, z, 1]

                self.canvas.delete("all")
                self.outp = {}
                all_faces = []
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice):                    
                    control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice], 
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                    _, self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                    all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)    
                    

                
            except ValueError:
                tk.messagebox.showerror("Erro", "Por favor, insira números válidos.")  # Mensagem de erro

        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=2, columnspan=4)

    

    def rotacao(self):
       
        janela = tk.Toplevel(self.tela)
        janela.title("Rotacao")       

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=-360, to=360, increment=1, width=10)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y:").grid(row=0, column=1)  # Adicionado dois pontos para consistência
        entrada_y = tk.Spinbox(janela, from_=-360, to=360, increment=1, width=10) # Spinbox para Y
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=0, column=2) # Adicionado dois pontos para consistência
        entrada_z = tk.Spinbox(janela, from_=-360, to=360, increment=1, width=10) # Spinbox para Z
        entrada_z.grid(row=1, column=2)

        def Salvar():
                x = int(entrada_x.get())
                y = int(entrada_y.get())
                z = int(entrada_z.get())
                valores_geo = []
                valores_geo.append((x,y,z))
                # Calcula a superfície B-Spline
                self.canvas.delete("all")
                self.outp = {}
                all_faces = [] 
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice):   
                    
                    if superfice == self.superficie_selecionada:             
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport, 2, valores_geo, self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice], self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces)
                        
                    else:
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                    self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport, 0, 0, self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice], self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)        
                            
              

        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=2, columnspan=3)

    def escala(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Escala")       

        tk.Label(janela, text="Escala em:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=500, increment=0.1, width=10)
        entrada_x.grid(row=1, column=0)

        def Salvar():
                x = float(entrada_x.get())
                # Calcula a superfície B-Spline
                self.canvas.delete("all")
                self.outp = {}
                all_faces = [] 
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice):   
                     
                    if superfice == self.superficie_selecionada:             
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                    self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,1,x,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice] , self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces)
                        
                    else:
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                    self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport, 0, 0, self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice], self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                        
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)       
                    
        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=2, columnspan=3)

    def translacao(self):
        janela = tk.Toplevel(self.tela)
        janela.title("Translacao")       

        tk.Label(janela, text="X:").grid(row=0, column=0)
        entrada_x = tk.Spinbox(janela, from_=0, to=600, increment=1, width=10)
        entrada_x.grid(row=1, column=0)

        tk.Label(janela, text="Y:").grid(row=0, column=1)  # Adicionado dois pontos para consistência
        entrada_y = tk.Spinbox(janela, from_=0, to=600, increment=1, width=10) # Spinbox para Y
        entrada_y.grid(row=1, column=1)

        tk.Label(janela, text="Z:").grid(row=0, column=2) # Adicionado dois pontos para consistência
        entrada_z = tk.Spinbox(janela, from_=0, to=600, increment=1, width=10) # Spinbox para Z
        entrada_z.grid(row=1, column=2)

        def Salvar():
                x = int(entrada_x.get())
                y = int(entrada_y.get())
                z = int(entrada_z.get())
                valores_geo = []
                valores_geo.append((x,y,z))
                # Calcula a superfície B-Spline
                self.canvas.delete("all")
                self.outp = {}
                all_faces = [] 
                visibilidade = {}
                for superfice in range(self.quantidadeSuperfice): 
                    if superfice == self.superficie_selecionada:                   
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                    self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,3,valores_geo,self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice] ,self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice] = control.main()
                        all_faces.append(faces)
                        
                    else:
                        control = Controle(self.canvas,self.pontos_controleX[superfice],self.pontos_controleY[superfice] ,  self.TI[superfice], self.TJ[superfice], self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice],
                                    self.inp[superfice], self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport, 0, 0, self.cor_aresta_frente[superfice], self.cor_aresta_fundo[superfice],self.sobreamento,superfice,self.ila,self.il,self.Luz,self.ka[superfice],self.kd[superfice],self.ks[superfice],self.n[superfice])
                        self.inp[superfice], self.inp_Axo[superfice], self.outp[superfice],faces,visibilidade[superfice]  = control.main()
                        all_faces.append(faces)
                if (self.sobreamento):
                    for superfice in range(self.quantidadeSuperfice):
                       
                        control.zbuffeConstante(self.outp[superfice],visibilidade[superfice],self.RESOLUTIONI[superfice], self.RESOLUTIONJ[superfice])
                else:
                        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
                        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)       
                   
               

        tk.Button(janela, text="Atualizar", command=Salvar).grid(row=2, columnspan=3)
    
      
    #------------------------------------------
    def criar_pontos_controle(self):
        
        self.inp[self.superficie_selecionada] = []        
        self.inp_Axo[self.superficie_selecionada] = []  

        for i in range(self.pontos_controleX[self.superficie_selecionada] + 1):
            linha = []
            for j in range(self.pontos_controleY[self.superficie_selecionada] + 1):
                #z =(random.randint(0, 9999) / 5000.0) - 1
                x = (self.ponto_inicial[self.superficie_selecionada][0] + i) * self.espacamento - (self.pontos_controleX[self.superficie_selecionada]* self.espacamento)/2
                y = random.uniform(-10, 10)  # Altura aleatória 
                z = (self.ponto_inicial[self.superficie_selecionada][2] + j) * self.espacamento - (self.pontos_controleY[self.superficie_selecionada]* self.espacamento)/2
                
                linha.append([x, y, z])

            self.inp[self.superficie_selecionada].append(linha)
            self.inp_Axo[self.superficie_selecionada].append(linha) 
        


    def desenhar_pontoControle(self):
        # Desenha os pontos de controle
        for i in range(self.pontos_controleX[self.superficie_selecionada] + 1):
            for j in range(self.pontos_controleY[self.superficie_selecionada] + 1):

                x = self.inp_Axo[self.superficie_selecionada][i][j][0]
                y = self.inp_Axo[self.superficie_selecionada][i][j][1] 
                
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
            
      
        
    def main(self):
        """Executa os cálculos e desenha a superfície."""
        self.quantidadeSuperfice = 1
        self.inp[self.superficie_selecionada] = []
        self.inp_Axo = {}
        self.inp_Axo[self.superficie_selecionada] = []  
        self.criar_pontos_controle()
        self.canvas.delete("all")
        self.outp = {}
        all_faces = []     
        visibilidade = {}
        visibilidade = {}              
        control = Controle(self.canvas, self.pontos_controleX[self.superficie_selecionada], self.pontos_controleY[self.superficie_selecionada], self.TI[self.superficie_selecionada], self.TJ[self.superficie_selecionada], self.RESOLUTIONI[self.superficie_selecionada], self.RESOLUTIONJ[self.superficie_selecionada], 
                          self.inp[self.superficie_selecionada],self.VRP, self.P, self.Y, self.dp, self.windows, self.viewport,0,0,self.cor_aresta_frente[self.superficie_selecionada], self.cor_aresta_fundo[self.superficie_selecionada],self.sobreamento,0,self.ila,self.il,self.Luz,self.ka[self.superficie_selecionada],self.kd[self.superficie_selecionada],self.ks[self.superficie_selecionada],self.n[self.superficie_selecionada])
        _ , self.inp_Axo[self.superficie_selecionada], self.outp[self.superficie_selecionada],faces,visibilidade[self.superficie_selecionada]  = control.main()
        all_faces.append(faces)
        faces_ordenadas = sorted(all_faces, key=lambda x: x[0], reverse=True)                
        control.pintor(faces_ordenadas, visibilidade, self.outp,self.cor_aresta_fundo, self.cor_aresta_frente)
        
   

if __name__ == "__main__":
    # Parâmetros da superfície
    pontos_controleX, pontos_controleY = 6,6
    TI, TJ = 6,6
    RESOLUTIONI, RESOLUTIONJ = 20, 20 
    espacamento = 15
    VRP = [100, 100, 100, 1]
    P = [0, 0, 0, 1]
    Y = [0, 1, 0]
    dp = 40
    windows = [-100, -100, 100, 100]
    viewport = [0, 0, 500, 500]

    root = tk.Tk()
    app = Interface(root, pontos_controleX, pontos_controleY, TI, TJ, RESOLUTIONI, RESOLUTIONJ, espacamento, VRP, P, Y, dp, windows, viewport)
    root.mainloop()
