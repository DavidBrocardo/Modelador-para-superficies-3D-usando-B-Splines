import tkinter as tk
from tkinter import colorchooser
from math import ceil, floor

class FillPoly:
    lista_intersecoess = {}
    vertices_poliginos = []

    def __init__(self, poligino, tela, corPreenchimento, ymin, ymax):          
        self.tela = tela
        self.cor = corPreenchimento       
        self.y_min = int(ymin)
        self.y_max = int(ymax)   
        self.num_Scanlines = 0
        self.yP = []
        self.xP = []
        
        self.poligino = poligino       
        FillPoly.vertices_poliginos.append((self.poligino)) 
                   
        self.scanlines()
        self.calc_intersecoes()
        self.FillPoly_pinta()                
        return
            
    def scanlines(self):           
        for i in range(len(self.poligino)):
            x, y = self.poligino[i]             
            if y > self.y_max:
                self.y_max = y
            if y < self.y_min:
                self.y_min = y
        self.num_Scanlines = self.y_max - self.y_min 
        
        for i in range(int(self.num_Scanlines) + 1):

            FillPoly.lista_intersecoess[round(self.y_min) + i] = []                
        return                  

    def calc_intersecoes(self):
        for i in range(len(self.poligino)):             
            if i != len(self.poligino) - 1:
                x_ver1, y_ver1 = self.poligino[i]
                x_ver2, y_ver2 = self.poligino[i + 1]
                if y_ver1 <= y_ver2:
                    x_Ini, y_ini = self.poligino[i]
                    x_Fin, y_Fin = self.poligino[i + 1]
                else:
                    x_Ini, y_ini = self.poligino[i + 1]
                    x_Fin, y_Fin = self.poligino[i]
            else:
                x_ver1, y_ver1 = self.poligino[i]
                x_ver2, y_ver2 = self.poligino[0]
                if y_ver1 <= y_ver2:
                    x_Ini, y_ini = self.poligino[i]
                    x_Fin, y_Fin = self.poligino[0]
                else:
                    x_Ini, y_ini = self.poligino[0]
                    x_Fin, y_Fin = self.poligino[i]
                
            if y_ini != y_Fin:                    
                Tx = (x_Fin - x_Ini) / (y_Fin - y_ini)
                YInter  = y_ini
                XInter = x_Ini 
                FillPoly.lista_intersecoess[round(y_ini)].append(x_Ini)
                self.xP.append(x_Ini + Tx)
                
                while YInter < (y_Fin - 1):                        
                    YInter = YInter + 1
                    XInter = XInter + Tx
                    FillPoly.lista_intersecoess[round(YInter)].append(XInter)
        return    

    def FillPoly_pinta(self):
        i = len(self.poligino)     
        while i < self.y_max:
            pontos_Intersecoess = sorted(FillPoly.lista_intersecoess.get(i, []))
            if len(pontos_Intersecoess) > 1:
                j = 0
                while j < len(pontos_Intersecoess):
                    x_ini = ceil(pontos_Intersecoess[j])
                    x_fim = floor(pontos_Intersecoess[j + 1])
                    self.tela.create_line(x_ini, i, x_fim, i, fill=self.cor, width=1)
                    j += 2
            i += 1

        for vertice in range(len(self.poligino)):
            x, y = self.poligino[vertice]
            self.tela.create_oval(x, y, x + 2, y + 2, fill=self.cor)
        return
