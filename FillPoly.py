from math import ceil, floor

class FillPoly:
    lista_intersecoess = {}
    vertices_poliginos = []

    def __init__(self, poligino, tela, sobreamento,visivel):          
        self.tela = tela
        #print(sobreamento)
        limite_inferior = 0
        limite_superior = 250 
        if visivel:
            red = max(limite_inferior, min(sobreamento[0], limite_superior))
            green = max(limite_inferior, min(sobreamento[1], limite_superior))
            blue = max(limite_inferior, min(sobreamento[2], limite_superior))
            cor_rgb = (red, green, blue)
            self.cor  = self.rgb_para_hex(cor_rgb)
            #print("Aqui", self.cor)
        else:
            self.cor  = "white"
        self.y_min = 10000
        self.y_max = -1
        self.num_Scanlines = 0
        self.yP = []
        self.xP = []
        self.poligino = []
        self.poligino = poligino   
 
        FillPoly.vertices_poliginos.append((self.poligino)) 
                   
        self.scanlines()
        self.calc_intersecoes()
        self.FillPoly_pinta()                
        return
            
    def rgb_para_hex(self, rgb):
        return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def scanlines(self):           
        
        FillPoly.lista_intersecoess = {}
        
        for i in range(len(self.poligino)):
            x , y ,z= self.poligino[(i)]             
            if y > self.y_max :
                self.y_max = round(y)
            if y < self.y_min :
                self.y_min = round(y)
        self.num_Scanlines = int(self.y_max - self.y_min) 
        
        
        for i in range(self.num_Scanlines+1):
            FillPoly.lista_intersecoess[self.y_min + i] = []
            
        return                      

    def calc_intersecoes(self):
        for i in range(len(self.poligino)):             
            if i != len(self.poligino) - 1:
                x_Ini, y_ini ,z = self.poligino[i]
                x_Fin, y_Fin, z = self.poligino[i + 1]
            else:
                x_Ini, y_ini ,z = self.poligino[i]
                x_Fin, y_Fin ,z = self.poligino[0]
            
            if y_ini > y_Fin:
                x_Ini, x_Fin = x_Fin, x_Ini
                y_ini, y_Fin = y_Fin, y_ini

            y_ini = round(y_ini)  
            y_Fin = round(y_Fin)

            if y_ini != y_Fin:                    
                Tx = (x_Fin - x_Ini) / (y_Fin - y_ini)
                YInter = y_ini
                XInter = x_Ini

                if y_ini not in FillPoly.lista_intersecoess:   
                    FillPoly.lista_intersecoess[y_ini] = []

                FillPoly.lista_intersecoess[y_ini].append(XInter)

                while YInter < (y_Fin - 1):                        
                    YInter += 1
                    XInter += Tx

                    YInter = round(YInter)  
                    if YInter not in FillPoly.lista_intersecoess:
                        FillPoly.lista_intersecoess[YInter] = []
                        
                    FillPoly.lista_intersecoess[YInter].append(XInter)
        

    def FillPoly_pinta(self):

        i = len(self.poligino)     
        while (i < self.y_max):
            pontos_Intersecoess = sorted(FillPoly.lista_intersecoess.get(i, []))
            if len(pontos_Intersecoess) > 1 :
                j = 0
                while j < (len(pontos_Intersecoess)):
                    x_ini =  ceil(pontos_Intersecoess[(j)])
                    x_fim =  floor(pontos_Intersecoess[(j+1)])
                    self.tela.create_line(x_ini, i, x_fim, i, fill=self.cor, width=1)
                    j = j + 2
                    
            
            i+=1
        
        return   
