from __future__ import generators
import plus
import Arenas
import random
import Hazards
import math
import Elec2haz

class ElectricArena(Arenas.SuperArena):
    "The grass is NOT greener on the other side of this fence!  Bots fight on a platform surrounded by an electric fence and suspended over a death pit that will turn your bot to slag.  Start points are adjusted for team battles."
    name = "Electric Arena 2T"
    preview = "electric2/dm_electric_preview2.bmp"
    game_types = ['TEAM MATCH']
    extent = (-15, 15, 15, -15)
    #FOR EVENT>>>Most fans don't come here to see the robots compete in neat, organized fights. They come to watch the dirty play and the fireworks and smell the smoke of cooking bots. All competitors are forewarned that their bot might not exist after fighting.

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/electric2/electric2team.gmf")
        #plus.Arena.__init__(self, "")
        plus.setBackColor(0, 0, 0)
        
        degrad = 0.01745
        self.AddStaticCamera("             Battle View", (19.5, 21, 19.5), (50*degrad,225*degrad), 55*degrad)
        self.AddStaticCamera("             Pit Cam", (23, -5, 23), (20*degrad, 225*degrad), 70*degrad)
	self.AddStaticCamera("             Birds Eye View", (0, 30, 0), (90*degrad,0), 75*degrad)
	self.AddWatchCamera("             Combat Cam", (-12, 14, 12), (16, 36, 65*degrad, 30*degrad))
	self.AddWatchCamera("             Aerial Cam", (-19.5, 30, -19.5), (50, 60, 45*degrad, 60*degrad))
	self.AddWatchCamera("             Ground Cam", (8, 1, -8), (15, 40, 75*degrad, 35*degrad))
	self.AddWatchCamera("             Spectator Cam", (39, 8, 12), (12, 36, 45*degrad, 30*degrad))
        
        self.SetSubMaterialSound("glowfloor", "metal", 10000000, "Sounds\\thunder.wav")
	
        self.players = ()
        
        self.lightningd = 0
        self.lightning0x = 0
        self.lightning0z = 0
        self.lightning1x = 0
        self.lightning1z = 0
        self.lightning2x = 0
        self.lightning2z = 0
        self.lightning3x = 0
        self.lightning3z = 0

        self.AddCollisionLine((-11.5, 11.5), (11.5, 11.5))
        self.AddCollisionLine((11.5, 11.5), (11.5, -11.5))
        self.AddCollisionLine((11.5, -11.5), (-11.5, -11.5))
        self.AddCollisionLine((-11.5, -11.5), (-11.5, 11.5))
        
        self.AddPOV(0, (11.5, 11.5), (1, 3))
        self.AddPOV(1, (11.5, -11.5), (0, 2))
        self.AddPOV(2, (-11.5, -11.5), (1, 3))
        self.AddPOV(3, (-11.5, 11.5), (2, 0))
        
    def __del__(self):
        if self.bHazardsOn:
            plus.removeSound(self.ambience)
        
        Arenas.SuperArena.__del__(self)

    def Activate(self, on):
        if on: self.players = plus.getPlayers()
        
        Arenas.SuperArena.Activate(self, on)
        
    def Introduction(self):
        degrad = 0.01745
        sounds = self.intro_sounds

        # set initial camera & fade from black
        plus.setCameraPosition(-15,14,-15)
        plus.setCameraRotation(45*degrad,45*degrad)
        plus.setCameraFOV(0.9)
        plus.fadeFromBlack(.25)
        
        #start playing music loop
        self.intro_music = plus.createSound("Sounds/intro_music/hybridloop1.wav", False, (0,0,0))
        plus.setVolume(self.intro_music, 0, 0)
        plus.loopSound(self.intro_music)
        yield .25
        
        #load all sounds now to decrease lag later
        sounds['crowd'] = plus.createSound("Sounds/crowd/LoudCheer_Loop.wav", False, (0,0,0))
        
        arenaOpt = ("Sounds/announcers/Arena_Electric_Welcome.wav", "Sounds/announcers/Arena_Electric_Enter.wav")
        sounds['arena'] = plus.createSound(random.choice(arenaOpt), False, (0,0,0))
        genericOpt = ("Hazard_Skull_CantSurviveDeathPit.wav", "Intro_Electric_PrepareToBeZapped.wav", "Hazard_Skull_PainDescribesDeathPit.wav", "Intro_HopeYoureReady.wav", "Intro_Electric_ShockingExperience.wav", "Intro_HoldOnToYourSeats.wav")
        sounds['generic'] = plus.createSound("Sounds/announcers/"+random.choice(genericOpt), False, (0,0,0))
        hazardOpt = ("Sounds/announcers/Hazard_Electric2_Equipment.wav", "Hazard_Electric2_WattsOfEnergy.wav",)
        # "Hazard_Electric2_HighVoltageAction.wav"
        sounds['hazards'] = plus.createSound("Sounds/announcers/"+random.choice(hazardOpt), False, (0,0,0))
        botOpt = ("Bots_YouCanFeelTension.wav", "Bots_ColdChill.wav", "Bots_FansLoveTheseBots.wav", "Bots_SeeingInterestingDesigns.wav", "Bots_CrowdPoisedBotsArmed.wav")
        sounds['bots'] = plus.createSound("Sounds/announcers/"+random.choice(botOpt), False, (0,0,0))
        
        #intro cam, welcom comment
        plus.playSound(sounds['arena'])
        plus.fadeInToLoop(sounds['crowd'], -100, 800)
        plus.animateCamera((-15,14,-15), (45*degrad,45*degrad), 0.9, (15,30,15), (55*degrad,225*degrad), 0.9, 0, 8)
        yield 2
        plus.fadeOutLoop(sounds['crowd'], 8000)
        yield 1
        
        #play a generic (or specific) secondary comment
        plus.playSound(sounds['generic'])
        yield 5
        
        #hazard cams
        if self.bHazardsOn:
            print "hazard vo"
            plus.playSound(sounds['hazards'])
            plus.animateCamera((5,-3.2,-5), (0,315*degrad), 0.675, (3,-3.2,3), (0,225*degrad), 0.675, 0, 2.5)
            plus.animateCamera((-13,-0.5,13), (10*degrad,80*degrad), 0.675, (-6,-0.5,13), (0*degrad,45*degrad), 0.675, 3, 6.5)
            yield 6.5

        players = plus.getPlayers()
        pcount = len(players)
        if pcount>0: plus.playSound(sounds['bots'])
        delaytime = 6 - pcount
        
        if 0 in players:
            #bot 1 cam
            plus.animateCamera((0,14,15), (30*degrad,180*degrad), 0.675, (0,-1,-7), (0*degrad,180*degrad), 0.675, 0, delaytime)
            yield delaytime

        if 1 in players:
            #bot 2 cam
            plus.animateCamera((0,14,-15), (30*degrad,0), 0.675, (0,-1,7), (0,0), 0.675, 0, delaytime)
            yield delaytime

        if 2 in players:
            #bot 3 cam
            plus.animateCamera((15,14,0), (30*degrad,270*degrad), 0.675, (-7,-1,0), (0,270*degrad), 0.675, 0, delaytime)
            yield delaytime

        if 3 in players:
            #bot 4 cam
            plus.animateCamera((-15,14,0), (30*degrad,90*degrad), 0.675, (7,-1,0), (0,90*degrad), 0.675, 0, delaytime)
            yield delaytime
        
        #fade out music
        plus.fadeOutLoop(self.intro_music, 2000)
        yield 2
        
        # done
        yield 0 
        
    def HazardsOn(self, on):
        if on:
            self.ambience = plus.createSound("Sounds/elec_ambience_loop.wav", False, (0, 0, 0))
            plus.loopSound(self.ambience)
            self.zrk = Elec2haz.Electricity((0, 0, 0))
            self.AddHazard(self.zrk)
            
            #lower south lightning
            
            self.CreateLightning(0, (-14.75, -1.5, -14.75), (0, -1.5, -14.75))
            self.SetLightningVisible(0, True)
            self.CreateLightning(1, (14.75, -1.5, -14.75), (0, -1.5, -14.75))
            self.SetLightningVisible(1, True)
            self.CreateLightning(2, (0, -1.5, -14.75), (-14.75, -1.5, -14.75))
            self.SetLightningVisible(2, True)
            self.CreateLightning(3, (0, -1.5, -14.75), (14.75, -1.5, -14.75))
            self.SetLightningVisible(3, True)
            
            #upper south lightning
            
            self.CreateLightning(4, (-14.75, -0.5, -14.75), (0, -0.5, -14.75))
            self.SetLightningVisible(4, True)
            self.CreateLightning(5, (14.75, -0.5, -14.75), (0, -0.5, -14.75))
            self.SetLightningVisible(5, True)
            self.CreateLightning(6, (0, -0.5, -14.75), (-14.75, -0.5, -14.75))
            self.SetLightningVisible(6, True)
            self.CreateLightning(7, (0, -0.5, -14.75), (14.75, -0.5, -14.75))
            self.SetLightningVisible(7, True)
            
            #lower west lightning
            
            self.CreateLightning(8, (-14.75, -1.5, -14.75), (-14.75, -1.5, 0))
            self.SetLightningVisible(8, True)
            self.CreateLightning(9, (-14.75, -1.5, 14.75), (-14.75, -1.5, 0))
            self.SetLightningVisible(9, True)
            self.CreateLightning(10, (-14.75, -1.5, 0), (-14.75, -1.5, -14.75))
            self.SetLightningVisible(10, True)
            self.CreateLightning(11, (-14.75, -1.5, 0), (-14.75, -1.5, 14.75))
            self.SetLightningVisible(11, True)
            
            #upper west lightning
            
            self.CreateLightning(12, (-14.75, -0.5, -14.75), (-14.75, -0.5, 0))
            self.SetLightningVisible(12, True)
            self.CreateLightning(13, (-14.75, -0.5, 14.75), (-14.75, -0.5, 0))
            self.SetLightningVisible(13, True)
            self.CreateLightning(14, (-14.75, -0.5, 0), (-14.75, -0.5, -14.75))
            self.SetLightningVisible(14, True)
            self.CreateLightning(15, (-14.75, -0.5, 0), (-14.75, -0.5, 14.75))
            self.SetLightningVisible(15, True)
            
            #lower north lightning
            
            self.CreateLightning(16, (-14.75, -1.5, 14.75), (0, -1.5, 14.75))
            self.SetLightningVisible(16, True)
            self.CreateLightning(17, (14.75, -1.5, 14.75), (0, -1.5, 14.75))
            self.SetLightningVisible(17, True)
            self.CreateLightning(18, (0, -1.5, 14.75), (-14.75, -1.5, 14.75))
            self.SetLightningVisible(18, True)
            self.CreateLightning(19, (0, -1.5, 14.75), (14.75, -1.5, 14.75))
            self.SetLightningVisible(19, True)
            
            #upper north lightning
            
            self.CreateLightning(20, (-14.75, -0.5, 14.75), (0, -0.5, 14.75))
            self.SetLightningVisible(20, True)
            self.CreateLightning(21, (14.75, -0.5, 14.75), (0, -0.5, 14.75))
            self.SetLightningVisible(21, True)
            self.CreateLightning(22, (0, -0.5, 14.75), (-14.75, -0.5, 14.75))
            self.SetLightningVisible(22, True)
            self.CreateLightning(23, (0, -0.5, 14.75), (14.75, -0.5, 14.75))
            self.SetLightningVisible(23, True)
            
            #lower east lightning
            
            self.CreateLightning(24, (14.75, -1.5, -14.75), (14.75, -1.5, 0))
            self.SetLightningVisible(24, True)
            self.CreateLightning(25, (14.75, -1.5, 14.75), (14.75, -1.5, 0))
            self.SetLightningVisible(25, True)
            self.CreateLightning(26, (14.75, -1.5, 0), (14.75, -1.5, -14.75))
            self.SetLightningVisible(26, True)
            self.CreateLightning(27, (14.75, -1.5, 0), (14.75, -1.5, 14.75))
            self.SetLightningVisible(27, True)
            
            #upper east lightning
            
            self.CreateLightning(28, (14.75, -0.5, -14.75), (14.75, -0.5, 0))
            self.SetLightningVisible(28, True)
            self.CreateLightning(29, (14.75, -0.5, 14.75), (14.75, -0.5, 0))
            self.SetLightningVisible(29, True)
            self.CreateLightning(30, (14.75, -0.5, 0), (14.75, -0.5, -14.75))
            self.SetLightningVisible(30, True)
            self.CreateLightning(31, (14.75, -0.5, 0), (14.75, -0.5, 14.75))
            self.SetLightningVisible(31, True)
            
            #rotary lightning
            
            self.CreateLightning(32, (0, -3.5, -0), (0, -3.5, 9))
            self.SetLightningVisible(32, True)
            self.CreateLightning(33, (0, -3.5, -0), (0, -3.5, 9))
            self.SetLightningVisible(33, True)
            self.CreateLightning(34, (0, -3.5, -0), (0, -3.5, -9))
            self.SetLightningVisible(34, True)
            self.CreateLightning(35, (0, -3.5, -0), (0, -3.5, -9))
            self.SetLightningVisible(35, True)
            self.CreateLightning(36, (0, -3.5, -0), (9, -3.5, 0))
            self.SetLightningVisible(36, True)
            self.CreateLightning(37, (0, -3.5, -0), (9, -3.5, 0))
            self.SetLightningVisible(37, True)
            self.CreateLightning(38, (0, -3.5, -0), (-9, -3.5, 0))
            self.SetLightningVisible(38, True)
            self.CreateLightning(39, (0, -3.5, -0), (-9, -3.5, 0))
            self.SetLightningVisible(39, True)
            
            self.RegisterZone("hazard", 1)
            self.RegisterZone("hazard1", 2)
            self.RegisterZone("hazard2", 3)
            self.RegisterZone("hazard3", 4)
            
	return Arenas.SuperArena.HazardsOn(self, on)
        
    def Tick(self):
        # "Eh, whadya say?" -Deaf Tick

        for each in self.players:
            if plus.getLocation(each)[1] < -22:
                plus.addPoints(each, -1024)

        if self.bHazardsOn:
            self.zrk.Tick()
            degrad = 0.01745
            
            self.lightning0x = 9.5*math.sin(self.lightningd*degrad)
            self.lightning0z = 9.5*math.cos(self.lightningd*degrad)
            self.lightning1x = 9.5*math.sin((self.lightningd+90)*degrad)
            self.lightning1z = 9.5*math.cos((self.lightningd+90)*degrad)
            self.lightning2x = 9.5*math.sin((self.lightningd+180)*degrad)
            self.lightning2z = 9.5*math.cos((self.lightningd+180)*degrad)
            self.lightning3x = 9.5*math.sin((self.lightningd+270)*degrad)
            self.lightning3z = 9.5*math.cos((self.lightningd+270)*degrad)
            
            self.SetLightningStartEnd(32, (0, -3.5, 0), (self.lightning0x, -3.5, self.lightning0z))
            self.SetLightningStartEnd(33, (0, -3.5, 0), (self.lightning0x, -3.5, self.lightning0z))
            self.SetLightningStartEnd(34, (0, -3.5, 0), (self.lightning1x, -3.5, self.lightning1z))
            self.SetLightningStartEnd(35, (0, -3.5, 0), (self.lightning1x, -3.5, self.lightning1z))
            self.SetLightningStartEnd(36, (0, -3.5, 0), (self.lightning2x, -3.5, self.lightning2z))
            self.SetLightningStartEnd(37, (0, -3.5, 0), (self.lightning2x, -3.5, self.lightning2z))
            self.SetLightningStartEnd(38, (0, -3.5, 0), (self.lightning3x, -3.5, self.lightning3z))
            self.SetLightningStartEnd(39, (0, -3.5, 0), (self.lightning3x, -3.5, self.lightning3z))
            
            self.lightningd += 2
            
            if self.lightningd >= 360:
                self.lightningd -= 360
                
        return Arenas.SuperArena.Tick(self)
        
    def ZoneEvent(self, direction, id, robot, chassis):
        if id>=0:
            self.zrk.ZoneEvent(direction, robot, chassis)
        return True

    def DistanceToEdge(self, location):
        min_dist = 999
        min_heading = 0
        
        dist = location[0] - -13.5
        if dist < min_dist:
            min_dist = dist
            min_heading = -math.pi / 2
        dist = 13.5 - location[0]
        if dist < min_dist:
            min_dist = dist
            min_heading = math.pi / 2
        dist = location[2] - -13.5
        if dist < min_dist:
            min_dist = dist
            min_heading = math.pi
        dist = 13.5 - location[2]
        if dist < min_dist:
            min_dist = dist
            min_heading = 0
        
        return (min_dist, min_dist <= 0, min_heading)

    def HeadingAwayFromEdge(self, location):
        dist, over, h = self.DistanceToEdge(location)
        
        return h + math.pi
        
Arenas.register(ElectricArena)
