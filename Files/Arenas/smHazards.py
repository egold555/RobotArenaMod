import plus
import random
from AI import vector3
import Arenas

class Hazard(object):
    def __init__(self, location):
        self.location = location
        
class Spikes(Hazard):
    
    def __init__(self, a_prismatic, a_power, location = (0, 0, 0)):
        Hazard.__init__(self, location)
        self.prismatic = a_prismatic
        self.power = a_power
        self.prismatic.SetAutoLock(False)
        self.timer = 0
        self.refcount = 0
        self.firesound = plus.createSound("Sounds\\hzd_comp_fire.wav", True, self.location)
        self.announcer = (plus.createSound("Sounds/announcers/Misc_SinisterLaugh1.wav", True, self.location), plus.createSound("Sounds/announcers/Misc_SinisterLaugh2.wav", True, self.location), plus.createSound("Sounds/announcers/Misc_SinisterLaugh3.wav", True, self.location), plus.createSound("Sounds/announcers/Misc_SinisterLaugh4.wav", True, self.location), plus.createSound("Sounds/announcers/Misc_SinisterLaugh5.wav", True, self.location), plus.createSound("Sounds/announcers/Misc_SinisterLaugh6.wav", True, self.location))
        
    def __del__(self):
        plus.removeSound(self.firesound)
        
        for x in self.announcer:
            plus.removeSound(x)
        
        self.announcer = ()
        
    def Tick(self):
        self.timer += .5
        if self.timer == 1: self.FireTeeth()
        if self.timer == 2: self.Retract()
        if self.timer >= 3: self.timer = 0
        
    def FireTeeth(self):
        plus.playSound(self.firesound)
        plus.playSound(random.choice(self.announcer))
        self.prismatic.Lock(False)
        self.prismatic.ApplyForce(self.power*2)
        
    def Retract(self):
        plus.playSound(self.firesound)
        self.prismatic.Lock(False)
        self.prismatic.ApplyForce(-self.power*2)
        