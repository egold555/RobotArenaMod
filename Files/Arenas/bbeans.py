from __future__ import generators
import plus
import Arenas
import random
import Hazards
import math

class BoxArena(Arenas.SuperArena):
    "The official arena for BBEANS AI tournaments.  This arena features low boundary walls and a walled spinning blade in the center.  After 90 seconds, the walls around the blade will retract into the floor."
    name = "BBEANS Tournament Arena"
    preview = "bbeans/bbeans_preview.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-11, 11, 11, -11)

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/bbeans/bbeans.gmf")
        plus.setBackColor(0,0,0)
        degrad = 0.01745
        self.AddStaticCamera("                Overview", (0, 7.8, -17.5), (35*degrad,0), 68*degrad)
        self.AddStaticCamera("                Corner Cam 1", (4, 0, 4), (10*degrad,45*degrad),72*degrad)
        self.AddStaticCamera("                Corner Cam 2", (4, 0, -4), (10*degrad,135*degrad), 72*degrad)
        self.AddStaticCamera("                Corner Cam 3", (-4, 0, -4), (10*degrad,225*degrad), 72*degrad)
        self.AddStaticCamera("                Corner Cam 4", (-4, 0, 4), (10*degrad,315*degrad), 72*degrad)
        self.AddWatchCamera("                Watch Cam 1", (15, 7.8, -15), (6, 37, 40*degrad, 15*degrad))
        self.AddWatchCamera("                Watch Cam 2", (-15, 7.8, 15), (6, 37, 40*degrad, 15*degrad))
        self.AddWatchCamera("                Blade Cam", (0, 2, 0), (5, 25, 65*degrad, 45*degrad))
        self.AddWatchCamera("                Overhead Cam", (0, 7.8, 0), (10, 15, 68*degrad, 58*degrad))
        self.AddWatchCamera("                Audience Cam", (0, 3, -30), (19, 41, 30*degrad, 20*degrad))
        self.players = ()
        self.SetPinned ("bladewall", True)
        self.wallmaster = 0

    def Activate(self, on):
        if on: self.players = plus.getPlayers()
        
        Arenas.SuperArena.Activate(self, on)
        
    def Tick(self):
        self.wallmaster += 1

        for each in self.players:
            if plus.getLocation(each)[1] < -0.6 and (abs(plus.getLocation(each)[0]) > 11.3 or abs(plus.getLocation(each)[2]) > 11.3):
                plus.eliminatePlayer(each)
            if abs(plus.getLocation(each)[0]) < 1.8 and abs(plus.getLocation(each)[2]) < 1.8 and plus.getLocation(each)[1] < -0.5 and self.wallmaster < 370:
                self.wallmaster = 370

        if self.wallmaster == 370:
            self.retractsound = plus.createSound("Sounds/liftmotor.wav", False, (0, 0, 0))
            plus.playSound(self.retractsound)
        if self.wallmaster > 370 and self.wallmaster < 390:
            self.SetPinned ("bladewall", False)
            self.prism.Lock(False)
            self.prism.ApplyForce(50)
            
        return Arenas.SuperArena.Tick(self)

    def HazardsOn(self, on):
        self.spinner = self.GetHinge("Hinge01")
        self.spinner.SetAutoLocks(False, False)
        self.spinner.Lock(False)

        self.prism = self.AddPrismatic("floor", "bladewall", 0, -1, 0, 0, 3, 0)
        self.prism.SetAutoLock(False)

        if on:
            self.SetSubMaterialSound("blade", "metal", 1.0, "Sounds\\spinnerhit.wav")
            self.spinner.SetPowerSettings(250,68)
            self.spinner.SetDirection(100)
        else:
            self.wallmaster = 370

        #box off spinner
        self.AddCollisionLine((2.5, 2.5), (2.5, -2.5))
        self.AddCollisionLine((2.5, -2.5), (-2.5, -2.5))
        self.AddCollisionLine((-2.5, -2.5), (-2.5, 2.5))
        self.AddCollisionLine((-2.5, 2.5), (2.5, 2.5))
        #outer walls
        self.AddCollisionLine((10.5, 10.5), (10.5, -10.5))
        self.AddCollisionLine((10.5, -10.5), (-10.5, -10.5))
        self.AddCollisionLine((-10.5, -10.5), (-10.5, 10.5))
        self.AddCollisionLine((-10.5, 10.5), (10.5, 10.5))
        #spinner ai guide
        self.AddPOV(0, (4, 4), (0, 1))
        self.AddPOV(1, (4, -4), (1, 2))
        self.AddPOV(2, (-4, -4), (2, 3))
        self.AddPOV(3, (-4, 4), (3, 0))

        return Arenas.SuperArena.HazardsOn(self, on)
        
Arenas.register(BoxArena)
