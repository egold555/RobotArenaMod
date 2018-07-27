from __future__ import generators
import plus
import Arenas
import random
import Hazards
import math

class BoxArena(Arenas.SuperArena):
    "This arena is built underground, surrounded by concrete and one inch thick steel plating, made to contain any four bots, no matter how powerful.  The audience is safely shielded high above the arena floor, but the bots will be exposed to spikes, a vertical spinning blade, and a heavy hammer."
    name = "Containment Cube"
    preview = "cube/cube_preview.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-16, 16, 16, -16)

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/cube/cube.gmf")
        plus.setBackColor(0,0,0)
        degrad = 0.01745
        fmod = .015
        self.AddStaticCamera("                Corner 1", (15.5, 8, -15.5), (45*degrad,315*degrad), 70*degrad)
        self.AddStaticCamera("                Corner 2", (-15.5, 8, 15.5), (45*degrad,135*degrad), 70*degrad)
        self.AddStaticCamera("                Ceiling", (0, 27, 0), (90*degrad,0), 60*degrad)
        self.AddWatchCamera("                Overhead Cam", (0, 12, 0), (16, 20, 68*degrad, 64*degrad))
        self.AddWatchCamera("                Corner Cam 1", (15.5, 2, -15.5), (6, 37, 75*degrad, 25*degrad))
        self.AddWatchCamera("                Corner Cam 2", (-15.5, 2, 15.5), (6, 37, 75*degrad, 25*degrad))
        self.players = ()
        # Ironbot stuff
        # self.thirtyseconds = 0
        # plus.practice(1)
        # /Ironbot stuff
        self.AddXtra("Obstacle", "arenas\\cube\\cubefloorpanel.gmf", "metal")
        self.botinzone = 0
        self.hammertime = 12
        self.hamsound1 = plus.createSound("Sounds/hellraiser_trigger.wav", False, (0, 0, 0))
        self.hamsound2 = plus.createSound("Sounds/hzd_comp_fire.wav", False, (0, 0, 0))

    # def Activate(self, on):
        # if on:
            # self.AddXtra("Obstacle", "arenas\\cube\\cubefloorpanel.gmf", "metal")
        
        # Arenas.SuperArena.Activate(self, on)

    def HazardsOn(self, on):
        # Spikes
        self.AddCollisionLine((16, 16), (16, -16))
        self.AddCollisionLine((16, -16), (-16, -16))
        self.AddCollisionLine((-16, -16), (-16, 16))
        self.AddCollisionLine((-16, 16), (16, 16))
        # self.AddCollisionLine((15.5, 15.5), (15.5, 4))
        # self.AddCollisionLine((15.5, 14), (16, 4))
        # self.AddCollisionLine((16, 4), (16, -4))
        # self.AddCollisionLine((16, -4), (15.5, -4))
        # self.AddCollisionLine((15.5, -4), (15.5, -15.5))
        # self.AddCollisionLine((15.5, -15.5), (4, -15.5))
        # self.AddCollisionLine((4, -15.5), (4, -16))
        # self.AddCollisionLine((4, -16), (-4, -16))
        # self.AddCollisionLine((-4, -16), (-4, -15.5))
        # self.AddCollisionLine((-4, -15.5), (-15.5, -15.5))
        # self.AddCollisionLine((-15.5, -15.5), (-15.5, -4))
        # self.AddCollisionLine((-15.5, -4), (-16, -4))
        # self.AddCollisionLine((-16, -4), (-16, 4))
        # self.AddCollisionLine((-16, 4), (-15.5, 4))
        # self.AddCollisionLine((-15.5, 4), (-15.5, 15.5))
        # self.AddCollisionLine((-15.5, 15.5), (-4, 15.5))
        # self.AddCollisionLine((-4, 15.5), (-4, 16))
        # self.AddCollisionLine((-4, 16), (4, 16))
        # self.AddCollisionLine((4, 16), (4, 15.5))
        # self.AddCollisionLine((4, 15.5), (15.5, 15.5))
        
        self.spinner = self.GetHinge("Hinge01")
        self.spinner.SetAutoLocks(False, False)
        self.spinner.Lock(False)
        
        self.hammer = self.GetHinge("Hinge02")
        self.hammer.SetAutoLocks(False, False)
        self.hammer.Lock(True)

        if on:
            # Hammer
            self.AddCollisionLine((-16, 0.5), (-12, 0.5))
            self.AddCollisionLine((-12, 0.5), (-12, -0.5))
            self.AddCollisionLine((-12, -0.5), (-16, -0.5))
            
            self.AddPOV(0, (-14, 2.5), (0, 1))
            self.AddPOV(1, (-10, 2.5), (1, 2))
            self.AddPOV(2, (-10, -2.5), (2, 1))
            self.AddPOV(3, (-14, -2.5), (3, 2))
            
            # Blade
            self.AddCollisionLine((16, 0.125), (14, 0.125))
            self.AddCollisionLine((14, 0.125), (14, -0.125))
            self.AddCollisionLine((14, -0.125), (16, -0.125))
            
            self.AddPOV(4, (14, 2.5), (4, 5))
            self.AddPOV(5, (10, 2.5), (5, 6))
            self.AddPOV(6, (10, -2.5), (6, 5))
            self.AddPOV(7, (14, -2.5), (7, 6))
            
            self.SetSubMaterialSound("blade", "metal", 0.5, "Sounds\\bbeans\\spinnerhit.wav")
            self.SetSubMaterialSound("hammer", "metal", 1.3, "Sounds\\bbeans\\barrel_collision_loud.wav")
            self.spinner.SetPowerSettings(100,255)
            self.spinner.SetDirection(-100)
            self.RegisterZone("hammerzone", 1)
        else:
            self.SetPinned ("blade", True)
            self.SetPinned ("hammer", True)

        self.SetSubMaterialSound("spikes1", "metal", 2, "Sounds\\hzd_spike_hit.wav")
        self.SetSubMaterialSound("spikes2", "metal", 2, "Sounds\\hzd_spike_hit.wav")
        self.SetSubMaterialSound("spikes3", "metal", 2, "Sounds\\hzd_spike_hit.wav")
        self.SetSubMaterialSound("spikes4", "metal", 2, "Sounds\\hzd_spike_hit.wav")

        return Arenas.SuperArena.HazardsOn(self, on)
        
    # Ironbot stuff
    # def Introduction(self):
        # self.RemoveXtra("Obstacle")
        # self.LostComps0 = eval(open("Bot0_comps.txt").read())
        # for id in self.LostComps0:
            # plus.damage(0, id, 1000, plus.getLocation(0))
            # plus.damage(0, id, 1000, plus.getLocation(0))
        # self.LostComps1 = eval(open("Bot1_comps.txt").read())
        # for id in self.LostComps1:
            # plus.damage(1, id, 1000, plus.getLocation(1))
            # plus.damage(1, id, 1000, plus.getLocation(1))
        # self.LostComps2 = eval(open("Bot2_comps.txt").read())
        # for id in self.LostComps2:
            # plus.damage(2, id, 1000, plus.getLocation(2))
            # plus.damage(2, id, 1000, plus.getLocation(2))
        # self.LostComps3 = eval(open("Bot3_comps.txt").read())
        # for id in self.LostComps3:
            # plus.damage(3, id, 1000, plus.getLocation(3))
            # plus.damage(3, id, 1000, plus.getLocation(3))
        # yield 0
    # /Ironbot stuff
        
    def Tick(self):
        # Ironbot stuff
        # if self.thirtyseconds <= 123:
            # self.thirtyseconds += 0.25
        # # Activate immobility warnings after 2 minutes
        # if self.thirtyseconds == 123:
            # plus.practice(0)
        # Artificially end match after 30 seconds
        # if self.thirtyseconds == 33:
            # plus.disable(0, 1)
            # plus.disable(1, 1)
            # plus.playSound(plus.createSound("Sounds/announcers/End_MatchIsDone.wav", False, (0, 0, 0)))
            # # repair components so no more break after the end
            # for comp in xrange(0,plus.describe(0).count(" ")):
                # plus.damage(0, comp, -10000, plus.getLocation(0))
            # for comp in xrange(0,plus.describe(1).count(" ")):
                # plus.damage(1, comp, -10000, plus.getLocation(1))
            # file("bot0weight.txt", "w").write(str(plus.getWeight(0)))
            # file("bot1weight.txt", "w").write(str(plus.getWeight(1)))
        # /Ironbot stuff
        
        # HAMMER TIME
        if self.bHazardsOn:
            if self.hammertime < 12:
                self.hammertime += 1
            
            if self.botinzone == 1 and self.hammertime == 12:
                plus.playSound(self.hamsound1)
                self.hammer.Lock(False)
                self.hammer.SetPowerSettings(20,1000)
                self.hammer.SetDirection(-100)
                self.hammertime = 0
                
            # Retract sound effect
            if self.hammertime == 4:
                plus.playSound(self.hamsound2)
            
            # Retract hammer for 1/2 second
            if 4 <= self.hammertime < 12:
                self.hammer.Lock(False)
                self.hammer.SetPowerSettings(10,1000)
                self.hammer.SetDirection(100)
            
            # Lock hammer when not in use to reduce lag
            if self.botinzone == 0 and self.hammertime == 12:
                self.hammer.SetPowerSettings(0,0)
                self.hammer.Lock(True)
            
        return Arenas.SuperArena.Tick(self)
        
    def ZoneEvent(self, direction, id, robot, chassis):
        if id == 1 and robot > 0:
            if direction == 1:
                self.botinzone = 1
            elif direction == -1:
                self.botinzone = 0
        return True
        
Arenas.register(BoxArena)