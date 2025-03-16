import numpy as np
import matplotlib.pyplot as plt
import math

class ZBuffer:
    def __init__(self, width, height, canvas):
        self.width = width
        self.height = height
        self.framebuffer = np.zeros((height, width, 3), dtype=np.uint8)
        self.zbuffer = np.full((height, width), np.inf)
        self.canvas = canvas

    def rgb_para_hex(self, rgb):
        return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
    
    def draw_scanline(self, y, x1, z1, x2, z2, color):
        limite_inferior = 0
        limite_superior = 250 
        red = max(limite_inferior, min(color[0], limite_superior))
        green = max(limite_inferior, min(color[1], limite_superior))
        blue = max(limite_inferior, min(color[2], limite_superior))
        cor_rgb = (red, green, blue)
        color_rgb  = self.rgb_para_hex(cor_rgb)
        

        if x1 > x2:
            x1, x2, z1, z2 = x2, x1, z2, z1
        
        dz = (z2 - z1) / (x2 - x1) if x2 != x1 else 0
        z = z1
        
        for x in range(int(x1), int(x2) + 1):
            if 0 <= x < self.width and 0 <= y < self.height and z < self.zbuffer[y, x]:
                self.zbuffer[y, x] = z
                self.framebuffer[y, x] = color
                self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill=color_rgb, outline=color_rgb )
            z += dz

    def render_triangle(self, p1, p2, p3, color):
        vertices = sorted([p1, p2, p3], key=lambda p: p[1])
        (y1, y2, y3) = vertices[0][1], vertices[1][1], vertices[2][1]
        
        
        if y1 == y2 == y3:
            return
        
        (x1, z1), (x2, z2), (x3, z3) = (vertices[0][0], vertices[0][2]), (vertices[1][0], vertices[1][2]), (vertices[2][0], vertices[2][2])

        y_start = math.ceil(y1)
        y_end = math.floor(y3)
        for y in range(y_start, y_end + 1):
            if y < y2:
                # Calcular xa/za (Aresta p1-p3)
                if y3 != y1:
                    xa = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
                    za = z1 + (z3 - z1) * (y - y1) / (y3 - y1)
                else:
                    xa, za = x1, z1
                
                # Calcular xb/zb (Aresta p1-p2)
                if y2 != y1:
                    xb = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                    zb = z1 + (z2 - z1) * (y - y1) / (y2 - y1)
                else:
                    xb, zb = x2, z2
            else:
                # Calcular xa/za (Aresta p1-p3)
                if y3 != y1:
                    xa = x1 + (x3 - x1) * (y - y1) / (y3 - y1)
                    za = z1 + (z3 - z1) * (y - y1) / (y3 - y1)
                else:
                    xa, za = x3, z3
                
                # Calcular xb/zb (Aresta p2-p3)
                if y3 != y2:
                    xb = x2 + (x3 - x2) * (y - y2) / (y3 - y2)
                    zb = z2 + (z3 - z2) * (y - y2) / (y3 - y2)
                else:
                    xb, zb = x3, z3
            
            self.draw_scanline(y, xa, za, xb, zb, color)

    def triangulate_and_render(self, vertices, color):
        if len(vertices) < 3:
            return
        
        p0 = vertices[0]
        for i in range(1, len(vertices) - 1):
            p1 = vertices[i]
            p2 = vertices[i + 1]
            self.render_triangle(p0, p1, p2, color)
        
        return 