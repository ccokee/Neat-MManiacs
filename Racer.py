import traceback
import time
import os.path
import sys
import pickle
import numpy as np
import os
from numpy.random import uniform, choice, random
from itertools import product
from PyBoy import PyBoy
from PyBoy.Logger import logger
from PyBoy.WindowEvent import WindowEvent
from PyBoy.GameWindow import SdlGameWindow as Window
import platform
if platform.system() != "Windows":
    from Debug import Debug

class Racer(object):
  
  actions_map = {'acelerar':0, 'turbo':1, 'inclinarAbajo':2, 'inclinarArriba':3 }

  
  
  def __init__(self, scale=1, radius=3, random_seed = 20):
    
    self.radius = radius
    self.bootROM = "ROMs/DMG_ROM.bin"
    self.ROMdir = "ROMs/"
    self.scale = scale
    self.caido = False
    self.random_seed = random_seed
    self.filename= "ROMs/MManiacs.rom"
    
    self._load_interface()
    
  
  def _load_interface(self):

	try:
        # Arrancar pyboy
    	    self.pyboy = PyBoy(Window(scale=self.scale), self.filename, self.bootROM)
            self.frame = 0
            self.view = self.pyboy.getTileView(False)	
	    self.view2 = self.pyboy.getTileView(True)
 	    self.xwraps = 0	
	    self.lastscreenposx = 0
	    self.posxChanged = False
	    self.pyboy.sendInput([WindowEvent.PressSpeedUp])

        except KeyboardInterrupt:
	    print ("Interrupted by keyboard")
        except Exception as ex:
            traceback.print_exc()

  def get_xy(self,screenposx,screenposy,dx,dy):
	
    dx+=screenposx
    if dx > 255 :
	dx-=255
    dy+=screenposy
    if dy > 255 :
	dy-=255   
    if screenposx != self.lastscreenposx :
	self.posxChanged = True
	self.lastscreenposx = screenposx
    else :
	self.posxChanged = False
    if dx == 255 and self.posxChanged:
	self.xwraps += 1

    return dx, dy, dx+(self.xwraps*255)

  def get_tilepos(self,dx,dy,plusx,plusy):

   dx=np.floor(dx/8)+plusx
   if dx > 31 :
	dx-=31
   dy=np.floor(dy/8)+plusy
   if dy > 31 :
	dy-=31

   return dx.astype(int), dy.astype(int)
  
  def get_sprites(self):
    sprites = []
    size = 0
    for n in range(40):
	sprite = self.pyboy.getSprite(n)
	if sprite.is_on_screen():
	   print "Sprite:", sprite.get_x(), sprite.get_y(), sprite.get_tile()
	if sprite.get_tile() != 127 :
	   size = 4
        else :
	   size = 1
	sprites.append({'sprite':sprite,'x': sprite.get_x(), 'y': sprite.get_y(), 'size': size })     
        
    return sprites
  
  def _within_limits(self, idx, ds1, ds2):
    maxlen = (self.radius*2+1)*(self.radius*2+1)
    return (idx%(2*self.radius + 1) + ds2 < 2*self.radius + 1) and (idx + ds1*(2*self.radius + 1) + ds2 < maxlen)
     
      
  def get_inputs(self):
    
    sprites = self.get_sprites()
    x,y,realx = self.get_xy(self.pyboy.getScreenPosition()[0],self.pyboy.getScreenPosition()[1],sprites[0]['x'],sprites[0]['y'])

    maxlen = (self.radius*2+1)*(self.radius*2+1)
    inputs = np.zeros(maxlen, dtype=int)

    ##window = (-self.radius*8, self.radius*8, 8)
    window = (32,32)
    j = 0

    if sprites[0]['sprite'].get_tile()==68:
	self.caido = True

    for dy, dx in product(range(*window), repeat=2):
	
	#tilex, tiley = self.get_tilepos(sprites[0]['sprite'].get_x(),sprites[0]['sprite'].get_y(),dx,dy)
	#tile = self.view.get_tile(tilex,tiley)	
	tile = self.view.get_tile(dx,dy)	

	for i in range(len(sprites)) :
	    distx = np.abs(sprites[i]['x'] - x - dx)
	    disty = np.abs(sprites[i]['y'] - y - dy)
	    size = sprites[i]['size']

	    if distx <= 8 and disty <= 8 :
		for s1, s2 in product(range(size), repeat=2):
		    if self._within_limits(j,s1,s2):
			inputs[j + s1*(self.radius*2 + 1) + s2] = -1
	j += 1

    return inputs, x, y, realx
    
  def reset(self):
    self.pyboy.mb.loadState(self.filename+".state")
    self.caido=False
    return self.get_inputs()
  
  def step(self, action):

    if action == 0:
      for it in range(8):
        self.pyboy.sendInput([WindowEvent.PressButtonA])
    elif action == 1:
      for it in range(4):
        self.pyboy.sendInput([WindowEvent.PressButtonB])
    elif action == 2:
      for it in range(2):
        self.pyboy.sendInput([WindowEvent.PressArrowRight])
    elif action == 3:
      for it in range(2):
        self.pyboy.sendInput([WindowEvent.PressArrowLeft])
    else:
      self.pyboy.sendInput([WindowEvent.PressButtonA])
    
    self.frame+=1  
    self.pyboy.tick()	
    inputs, x, y, realx = self.get_inputs()
    
    return inputs, x, y, realx, self.caido
