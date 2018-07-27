from __future__ import generators
import plus
import Arenas
import Hazards
import math
#import Gooey

class BoxArena(Arenas.SuperArena):
    "Keznorg IGC. The Keznorg Intergalactic Center hosts some of the fiercest competition you will find. An electric fence guards the perimiter of the platform arena. Many amateurs are forbidden to compete here because the spectator fees are high and the crowd wants to see only the best."
    name = "Keznorg IGC (REAL)"
    preview = "RA1/Th3L3.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-12, 12, 12, -12)

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/RA1/keznorgIGC.gmf")
        plus.setBackColor(0,0,0)
        degrad = 0.01745
        self.sensors = {}
        self.zaptimer = 1
        self.zapsound = plus.createSound("Sounds/zap_loop.wav", False, (0,0,0))
        self.AddStaticCamera("Static 1", (-7, 8, 19), (30*degrad, 160*degrad), degrad*65)
        self.AddStaticCamera("Static 2", (0, 20, 0), (90*degrad, 90*degrad), degrad*75)
        self.AddStaticCamera("Driver's Seat", (0, 15, -31), (30*degrad, 0), degrad*62)

        self.AddWatchCamera("Watch Cam 1", (8, 15, -15), (20, 40, 50*degrad, 40*degrad))
        self.AddWatchCamera("Watch Cam 2", (-8, 8, 15), (12, 20, 50*degrad, 40*degrad))
        self.AddWatchCamera("Driver's Seat", (0, 15, 31), (25, 50, 50*degrad, 30*degrad))
        self.players = ()
        
        # self.plah = Gooey.Plain("blokus", 40, 90, 250, 120)
        # self.tbox0 = self.plah.addText("uno", 0, 0, 250, 15)
        # self.tbox0.setText("")

    def Activate(self, on):
        if on: self.players = plus.getPlayers()
        
        Arenas.SuperArena.Activate(self, on)
        
    def HazardsOn(self, on):
        if on:
            self.RegisterZone("zone", 1)
        #walls
        self.AddCollisionLine((-11.7, 11.7), (11.7, 11.7))
        self.AddCollisionLine((11.7, 11.7), (11.7, -11.7))
        self.AddCollisionLine((11.7, -11.7), (-11.7, -11.7))
        self.AddCollisionLine((-11.7, -11.7), (-11.7, 11.7))
            
        return Arenas.SuperArena.HazardsOn(self, on)
        
    def __del__(self):
        plus.removeSound(self.zapsound)
        Arenas.SuperArena.__del__(self)
        
    def Tick(self):
        #self.tbox0.setText("Bots in zone: " + str(self.sensors))
        # Electric fence
        if self.bHazardsOn:
            for bot, in_range in self.sensors.iteritems():
                if in_range:
                    plus.damage(bot, 0, self.zaptimer, plus.getLocation(bot))
                    plus.zap(bot, self.zaptimer, 0.25)
                    plus.loopSound(self.zapsound)
                    
            if self.NumBotsInRange()==0:
                plus.stopSound(self.zapsound)
                self.zaptimer = 1
            else:
                if self.zaptimer < 50:
                    self.zaptimer += 1
                
        #check to see if anyone has been "eliminated" by falling off the tabletop
        #why is "eliminated" in quotes?
        for each in self.players:
            if plus.getLocation(each)[1] < -200:
                plus.eliminatePlayer(each)
                    
        return Arenas.SuperArena.Tick(self)
        
    def NumBotsInRange(self):
        numBots = 0
        for bot, in_range in self.sensors.iteritems():
            if in_range: numBots += 1
                
        return numBots
        
    def ZoneEvent(self, direction, id, robot, chassis):
        r = robot - 1
        if r not in self.sensors: self.sensors[r] = 0
        
        if direction==1:
            self.sensors[r] += 1
        elif direction==-1:
            self.sensors[r] -= 1
            
        return True
        
Arenas.register(BoxArena)