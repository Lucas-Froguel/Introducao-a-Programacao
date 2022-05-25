# -*- coding: utf-8 -*-
"""
Created on Fri May 14 18:03:50 2021

@author: Lucas
"""
import pyglet
import numpy as np
from pyglet import shapes

base_path = "C:\\Users\Lucas\Desktop\Anim"

window = pyglet.window.Window(800, 600)
#image = pyglet.resource.image('kitten.jpg')



label = pyglet.text.Label('Classical Gas',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')



class Points:
    def __init__(self, n = 10, radius = 5, m=0.01, g=0.1, v_max=50):
        self.p = 100*np.random.rand(n, 2) - [50, 50] + [window.width/2, window.height/2]
        self.cm = np.sum(self.p, axis=0)/n
        self.radius = radius
        self.velocity = v_max*np.random.rand(n, 2) - [v_max/2, v_max/2]
        self.n = n
        self.frame_number = 0
        self.mass = m
        self.k = 1.38*10**(-23)
        self.gravity = g
        
        self.gravity_text = pyglet.text.Label("g:{}".format(self.gravity), x=window.width-120, y=window.height-80, anchor_x='center', anchor_y='center')
        
        self.energy = 0
        self.total_momentum = 0
        self.temperature = 0
        
    
    
    def check_collision_border(self):
        r = self.radius
        for i in range(self.n):
            if self.p[i][0]-r < 0 or self.p[i][0]+r > window.width:
                self.velocity[i][0] = -self.velocity[i][0]
            if self.p[i][1]-r < 0 or self.p[i][1]+r > window.height:
                self.velocity[i][1] = -self.velocity[i][1]

    def check_collision_object(self, obj):
        left = obj.left
        right = obj.right
        bottom = obj.bottom
        top = obj.top
        r = self.radius
        
        '''moves = {1: "b", 3: "b", 5: "b", 7: "b",
                 0: "x", 4: "x",
                 2: "y", 6: "y"}
        
        r = self.radius
        for i in range(self.n):
            p = self.is_in_object(right, left, bottom, top, self.p[i])
            if not p:
                continue
            m = moves[p]
            if m == 'x':
                self.velocity[i][0] = - self.velocity[i][0]
                continue
            elif m == 'y':
                self.velocity[i][1] = - self.velocity[i][1]
                continue
            elif m == 'b':
                self.velocity[i] = - self.velocity[i]
                continue'''
        
        for i in range(self.n):
            is_in_height = self.p[i][1]+r > bottom and self.p[i][1]-r < top
            is_in_width = self.p[i][0]+r < right and self.p[i][0]-r > left
            
            if is_in_height and ((self.p[i][0]-r < left and self.p[i][0]+r > left) or (self.p[i][0]+r > right and self.p[i][0]-r < right)):
                self.velocity[i] = 0#-self.velocity[i][0]
            elif is_in_width and ((self.p[i][1]-r < bottom and self.p[i][1]+r > bottom) or (self.p[i][1]+r > top and self.p[i][1]-r < top)):
                self.velocity[i] = 0#-self.velocity[i][1]
    
    def check_collision(self, left, right, bottom, top):
        r = self.radius
        for i in range(self.n):
            is_in_height = self.p[i][1]+r > bottom and self.p[i][1]-r < top
            is_in_width = self.p[i][0]+r < right and self.p[i][0]-r > left
            
            if is_in_height and ((self.p[i][0]-r < left and self.p[i][0]+r > left) or (self.p[i][0]+r > right and self.p[i][0]-r < right)):
                self.velocity[i][0] = -self.velocity[i][0]
            elif is_in_width and ((self.p[i][1]-r < bottom and self.p[i][1]+r > bottom) or (self.p[i][1]+r > top and self.p[i][1]-r < top)):
                self.velocity[i][1] = -self.velocity[i][1]
    
    def is_in_object(self, right, left, bottom, top, p, k=8):

        Cx, Cy = p
        for i in [0, 2, 4, 6, 1, 3, 5, 7]:
            t = 0
            theta = (2*np.pi)/(k) * i
            x = Cx + self.radius * np.cos(theta)
            y = Cy + self.radius * np.sin(theta)
            px = window.width
            #py = window.height - y
            b_px = px > right
            esquerda_x = x < left
            direita_x = x > right
            pos_y = y >= bottom and y <= top
            if (b_px and esquerda_x) and pos_y:
                t = 2
            elif (b_px and direita_x) and pos_y:
                t = 0
            elif pos_y:
                t = 1
            if t%2 == 1:
                return i
        return False
        
    def is_center_in_object(self, right, left, bottom, top, p):
        Cx, Cy = p
        px = Cx + window.width
        b_px = px > right
        esquerda_x = Cx < left
        direita_x = Cx > right
        pos_y = Cy >= bottom and Cy <= top
        if (b_px and esquerda_x) and pos_y:
            t = 2
        elif (b_px and direita_x) and pos_y:
            t = 0
        elif pos_y:
            t = 1
        if t%2 == 1:
            return True
        return False
                
    def update(self, dt, obj=[]):
        self.check_collision_border()
        for o in obj:
            self.check_collision_object(o)
        self.velocity = self.velocity + [0, -self.gravity*dt]
        self.p += self.velocity * dt
        self.cm = np.sum(self.p, axis=0)/self.n
        
        
        self.calc_temperature()
        self.calc_total_momentum()
        self.calc_energy()
    
    #---PHYSICAL VALUES--------------------------------------------------
    
    def calc_temperature(self):
        avr_v = np.sum(np.sqrt(np.sum(self.velocity**2, axis=1)))/self.n
        self.temperature = (avr_v**2 * np.pi * self.mass)/(8*self.k)
    
    def calc_total_momentum(self):
        avr_v = np.sum(np.sqrt(np.sum(self.velocity**2, axis=1)))
        self.total_momentum = self.mass * avr_v
    
    def calc_energy(self):
        avr_v = np.sum(np.sum(self.velocity**2, axis=1))/self.n
        K = self.mass * avr_v/2
        U = np.sum(self.mass * self.gravity * self.p[:, 1])
        self.energy = K+U
    
    
     #---EXPORT --------------------------------------------------------

    def save_a_frame(self):
            file_num=str(self.frame_number)#.zfill(5)
            filename=base_path+"\_"+file_num+'.png'
            pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
            #print('image file writen : ',filename)

    def export_loop(self,dt):
        constant_interval=dt
        # update at a constant dt, regardless of real time
        # so that even if refresh is slow no frame should be missing
        # self.frame_draw(PicPS)
        self.update(constant_interval)
        self.save_a_frame()
        self.frame_number+=1
        

class Target:
    def __init__(self, y=window.height-100, x = window.width/2, w=10, h=10):
        self.y = y
        self.x = x
        self.height = h
        self.width = w
        self.obj = shapes.Rectangle(x=x, y=y, width=w, height=h, color=(55, 55, 255))

    def draw(self):
        self.obj.draw()

class Obstacle:
    def __init__(self, bottom=0, top=0, left=0, right=0, color=(55, 55, 255)):
        self.bottom = bottom
        self.top = top
        self.left = left
        self.right = right
        self.height = top-bottom
        self.width = right-left
        
        self.obj = shapes.Rectangle(x=left, y=bottom, width=self.width, height=self.height, color=color)
    
    def draw(self):
        self.obj.draw()
        

#---------------------------------------------------------------




points = Points(n=500, g=1)

# square = Obstacle(bottom=300, top=320, left=200, right=400)
# square_2 = Obstacle(bottom=500, top=515, left=400, right=500)




@window.event
def on_draw():
    window.clear()
    #image.blit(0, 0)
    label.draw()
    #square.draw()
    #square_2.draw()
    
    temperature_text = pyglet.text.Label("T:{}".format(round(points.temperature, 2)), x=window.width-120, y=window.height-20,
                             anchor_x='center', anchor_y='center').draw()
    momentum_text = pyglet.text.Label("P:{}".format(round(points.total_momentum, 2)), x=window.width-120, y=window.height-40, 
                             anchor_x='center', anchor_y='center').draw()
    energy_text = pyglet.text.Label("E:{}".format(round(points.energy, 2)), x=window.width-120, y=window.height-60, 
                             anchor_x='center', anchor_y='center').draw()
    points.gravity_text.draw()
    
    shapes.Circle(x=points.cm[0], y=points.cm[1], radius=points.radius, color=(255, 0, 55)).draw()
    for k in range(points.n):
        shapes.Circle(x=points.p[k][0], y=points.p[k][1], radius=points.radius, color=(105, 255, 0)).draw()
    
    
    #pyglet.graphics.draw(points.n, pyglet.gl.GL_POINTS, ('v2f', points.p))
    




def update(dt):
    points.update(dt)
    #points.export_loop(dt)



pyglet.clock.schedule_interval(update, 1/60.)

pyglet.app.run()








