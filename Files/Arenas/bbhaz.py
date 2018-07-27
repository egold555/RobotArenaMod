from __future__ import generators
import plus
import Arenas
import random
from random import randint
import Hazards
import math
import Gooey
import AI
#import os

class Epic(Arenas.SuperArena):
    "On the tallest of towers, in the fiercest of storms, bots will clash in the ultimate confrontation between good and evil."
    name = "Epic Showdown"
    preview = "bbeans/maps/preview1.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-11, 11, 11, -11)
    #in_list = False

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/bbeans/yellowlights.gmf")
        plus.setBackColor(0, 0, 0)
        
        degrad = 0.01745
        self.AddStaticCamera("                Birds Eye View", (0, 20, 0), (90*degrad,0), 75*degrad)
        self.AddStaticCamera("                Epic View", (-9, 10, -9), (48*degrad,45*degrad), 84*degrad)
        self.AddWatchCamera("                Default Cam", (3.84, 5, -6.66), (4, 23, 84*degrad, 30*degrad))
        self.AddWatchCamera("                Overhead Cam", (0, 15, 0), (15, 22, 68*degrad, 58*degrad))
        self.AddWatchCamera("                Low Cam", (3.84, 0, -6.66), (2, 23, 120*degrad, 45*degrad))
        self.AddWatchCamera("                Cloud Cam", (3, 10.5, -20), (19, 42, 60*degrad, 55*degrad))
        
        self.players = ()
        self.thundercount = 0
        self.boom = randint(20, 120)
        self.thundersound = randint(1, 4)
        self.wind = plus.createSound("Sounds\\bbeans\\sound7.wav", False, (0,0,0))
        self.thunder1 = plus.createSound("Sounds\\bbeans\\tsound1.wav", False, (0,0,0))
        self.thunder2 = plus.createSound("Sounds\\bbeans\\tsound2.wav", False, (0,0,0))
        self.thunder3 = plus.createSound("Sounds\\bbeans\\tsound3.wav", False, (0,0,0))
        self.thunder4 = plus.createSound("Sounds\\bbeans\\tsound4.wav", False, (0,0,0))
        
        #Code for silencing the crowd that works, but IT WON'T COME BACK EVER NO MATTER WHAT I TRY >=(
        # if "audience" in os.listdir("Sounds"):
            # os.rename("Sounds\\crowd", "Sounds\\ravend")
            # os.rename("Sounds\\audience", "Sounds\\crowd")
        
    def Activate(self, on):
        if on: self.players = plus.getPlayers()
        plus.loopSound(self.wind)
        
        Arenas.SuperArena.Activate(self, on)
        
    def HazardsOn(self, on):
        self.spinner1 = self.GetHinge("Hinge01")
        self.spinner1.SetAutoLocks(False, False)
        self.spinner1.Lock(False)
        self.spinner1.SetPowerSettings(5.8,150000)
        self.spinner1.SetDirection(-100)
        self.spinner2 = self.GetHinge("Hinge02")
        self.spinner2.SetAutoLocks(False, False)
        self.spinner2.Lock(False)
        self.spinner2.SetPowerSettings(2.68,150000)
        self.spinner2.SetDirection(-100)
        self.spinner3 = self.GetHinge("Hinge03")
        self.spinner3.SetAutoLocks(False, False)
        self.spinner3.Lock(False)
        self.spinner3.SetPowerSettings(1.11,150000)
        self.spinner3.SetDirection(-100)
        #walls
        self.AddCollisionLine((-3.882, 14.489), (3.882, 14.489))
        self.AddCollisionLine((3.882, 14.489), (5.125, 8.88))
        self.AddCollisionLine((5.125, 8.88), (10.607, 10.607))
        self.AddCollisionLine((10.607, 10.607), (14.489, 3.882))
        self.AddCollisionLine((14.489, 3.882), (10.25, 0))
        self.AddCollisionLine((10.25, 0), (14.489, -3.882))
        self.AddCollisionLine((14.489, -3.882), (10.607, -10.607))
        self.AddCollisionLine((10.607, -10.607), (5.125, -8.88))
        self.AddCollisionLine((5.125, -8.88), (3.882, -14.489))
        self.AddCollisionLine((3.882, -14.489), (-3.882, -14.489))
        self.AddCollisionLine((-3.882, -14.489), (-5.125, -8.88))
        self.AddCollisionLine((-5.125, -8.88), (-10.607, -10.607))
        self.AddCollisionLine((-10.607, -10.607), (-14.489, -3.882))
        self.AddCollisionLine((-14.489, -3.882), (-14.489, 3.882))
        self.AddCollisionLine((-14.489, 3.882), (-5.125, 8.88))
        self.AddCollisionLine((-5.125, 8.88), (-10.607, 10.607))
        self.AddCollisionLine((-10.607, 10.607), (-3.882, 14.489))
        #torches
        plus.AddParticleEmitter((-10.25, 4, 0), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        plus.AddParticleEmitter((-5.125, 4, -8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        plus.AddParticleEmitter((5.125, 4, -8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        plus.AddParticleEmitter((10.25, 4, 0), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        plus.AddParticleEmitter((5.125, 4, 8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        plus.AddParticleEmitter((-5.125, 4, 8.88), (0, 3, 0), (2, 5, 2)).SetEmitting(True)
        if on:
            self.SetSubMaterialSound("damagezone1", "metal", 2, "Sounds\\cinderblock2.wav")
            self.SetSubMaterialSound("damagezone2", "metal", 2, "Sounds\\cinderblock2.wav")
            self.SetSubMaterialSound("damagezone3", "metal", 2, "Sounds\\cinderblock2.wav")
            self.SetSubMaterialSound("damagezone4", "metal", 2, "Sounds\\cinderblock2.wav")
            self.SetSubMaterialSound("damagezone5", "metal", 2, "Sounds\\cinderblock2.wav")
            self.SetSubMaterialSound("damagezone6", "metal", 2, "Sounds\\cinderblock2.wav")
            
        return Arenas.SuperArena.HazardsOn(self, on)
        
    def __del__(self):
        plus.stopAllSounds()
        Arenas.SuperArena.__del__(self)
        
    def Tick(self):
        #lightning and DUNDAAAAAAAAAAAAAAA!
        self.thundercount += 1
        if self.thundercount == self.boom:
            plus.setBackColor(1,1,1)
            self.thundersound = randint(1, 4)
            self.thundercount = 0
            self.boom = randint(20, 100)
            if self.thundersound == 1:
                plus.playSound(self.thunder1)
            if self.thundersound == 2:
                plus.playSound(self.thunder2)
            if self.thundersound == 3:
                plus.playSound(self.thunder3)
            if self.thundersound == 4:
                plus.playSound(self.thunder4)
        else:
            plus.setBackColor(0,0,0)
            
        #check to see if anyone has been "eliminated" by falling off the tabletop
        for each in self.players:
            if plus.getLocation(each)[1] < -5:
                plus.eliminatePlayer(each)
                
        return Arenas.SuperArena.Tick(self)
        
Arenas.register(Epic)