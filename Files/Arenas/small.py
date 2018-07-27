from __future__ import generators
import plus
import Arenas
import random
import Hazards
import math
import smHazards

class Box(Arenas.SuperArena):
    "Finally, little bots can enjoy the 'comforts' of a smaller arena. This arena works well for AW, BW, and LW combat. Or you might want to do a crammed and tangled point-blank heavyweight brawl... Make sure to TURN HAZARDS OFF."
    name = "Small Arena"
    preview = "small/small_preview.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-8, 8, 8, -8)
    # You won't beable to getch there!
    # I dunno what that "You won't beable to getch there!" is for.

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/small/small.gmf")
        plus.setBackColor(.5, 1, 0)
        
        degrad = 0.01745
        fmod = .015
        self.AddStaticCamera("Battle Veiw", (8, 5, 8), (38*degrad,225*degrad), 55*degrad)
        self.AddStaticCamera("High Flipper View", (-8, 9.5, -8), (48*degrad,45*degrad), 84*degrad)
        self.AddStaticCamera("Birds Eye View", (0, 9.5, 0), (90*degrad,0), 75*degrad)
        self.AddStaticCamera("Dinosaur Bones", (6, 12.5, 15), (38*degrad,205*degrad), 70*degrad)
        self.AddWatchCamera("Combat Cam", (5, 4, 5), (12, 20, 65*degrad, 40*degrad))
        self.AddWatchCamera("Aerial Cam", (-0, 9, 0), (24, 32, 45*degrad, 60*degrad))
        self.AddWatchCamera("Ground Cam", (-7.9, 0, -7.9), (15, 40, 75*degrad, 45*degrad))
        self.AddWatchCamera("Hey man, what's a ramblin' raggamuffin like you doin' standin' out there on the concrete where you're not s'posed to getch to? You're all actin' like a 'spectator' and stuff, standin' there wich yer Sony Digital Camcorder doohickey watchin' this fight an' all. Just scram, scram like the flamin' bear-meat-eatin' rascal of an upside-down clown you are! Ain't no spectators allowed here! This is the grungy concrete warehouse of doom! Only for the bots n' boots, ya hear? Now get out, SPECTATOR. You're so full of rotten catnip, you fool of a salted excrement sample. Clamber the walls and getch ye selfeth outta here, you moldy speck of a tater. Tater Daze is ashamed of you. Samwise Gamgee and Smeagol are ashamed of you. You're such a puny Runt (c)Wonka Candy Company of a PO-TA-TO that your granny stood on the roof of her shambly thatched-roofed cottage and fell asleep with a toad in her right palm! Take this rusty toothbrush and beat your way OUT with it! You foul-breathed un-offroad oyster mutton, you'll work through blood sweat and tears to the bitter end without rest or I'll get the whoopin' on you! SPECK TATERS ARE ILLEGAL!!!!!!!!!!111111111111111one111one1eleven1!!122two2!two hundred twenty-one21121!!!11r0flwaffle11pwndx0rz111253948!361246!8743251!!!!", (-9.2, -1, 2), (10, 18, 45*degrad, 30*degrad))
        
        self.players = ()
        self.grunk = 0
        self.butTheKitty = 0

    def Introduction(self):
        degrad = 0.01745
        sounds = self.intro_sounds
        
        # set initial camera & fade from black
        plus.setCameraPosition(-10,5,-10)
        plus.setCameraRotation(30*degrad ,45*degrad)
        plus.setCameraFOV(45*degrad)
        plus.fadeFromBlack(.25)

        #start playing music loop
        self.intro_music = plus.createSound("Sounds/crowd/angry_loop.wav", False, (0,0,0))
        plus.setVolume(self.intro_music, 0, 0)
        plus.loopSound(self.intro_music)
        yield .25
        
        #load all sounds now to decrease lag later
        sounds['crowd'] = plus.createSound("Sounds/crowd/boo.wav", False, (0,0,0))
        
        arenaOpt = ("Sounds/announcers/Arena_Small_Welcome.wav", "Sounds/announcers/Arena_Small_Welcome.wav")
        sounds['arena'] = plus.createSound(random.choice(arenaOpt), False, (0,0,0))
        genericOpt = ("Arena_Combat_CageOfSteel.wav", "Arena_NowhereToHide.wav", "Intro_TheFansAreReady.wav", "Intro_GreatMatchComingYourWay.wav", "Intro_FansAreRestless.wav", "Intro_PerfectEveningForDestruction.wav", "Intro_HoldOnToYourSeats.wav", "Misc_CrowdOnEdge.wav")
        sounds['generic'] = plus.createSound("Sounds/announcers/"+random.choice(genericOpt), False, (0,0,0))
        hazardOpt = ("Misc_TheSkyIsFalling.wav", "Intro_Compressor_OneStopWeightLoss.wav")
        sounds['hazards'] = plus.createSound("Sounds/announcers/"+random.choice(hazardOpt), False, (0,0,0))
        botOpt = ("Bots_YouCanFeelTension.wav", "Bots_ColdChill.wav", "Bots_FansLoveTheseBots.wav", "Bots_SeeingInterestingDesigns.wav", "Bots_CrowdPoisedBotsArmed.wav", "Bots_YouCanFeelTension.wav", "Bots_ColdChill.wav", "Bots_FansLoveTheseBots.wav", "Bots_SeeingInterestingDesigns.wav", "Bots_CrowdPoisedBotsArmed.wav", "Misc_BotPancakesAnyone.wav")
        sounds['bots'] = plus.createSound("Sounds/announcers/"+random.choice(botOpt), False, (0,0,0))
        sounds['burp'] = plus.createSound("Sounds/announcers/realburp_2.wav", False, (0,0,0))
        
        #intro cam, welcom comment
        plus.playSound(sounds['arena'])
        plus.fadeInToLoop(sounds['crowd'], -100, 800)
        plus.animateCamera((-10,5,-10), (30*degrad,45*degrad), 45*degrad, (10,5,-10), (30*degrad,-45*degrad), 45*degrad, 0, 1.5)
        plus.animateCamera((10,5,-10), (30*degrad,315*degrad), 45*degrad, (10,5,10), (30*degrad,225*degrad), 45*degrad, 1.5, 3)
        plus.animateCamera((10,5,10), (30*degrad,225*degrad), 45*degrad, (-10,5,10), (30*degrad,135*degrad), 45*degrad, 3, 4.5)
        plus.animateCamera((-10,5,10), (30*degrad,135*degrad), 45*degrad, (-10,5,-10), (30*degrad,45*degrad), 45*degrad, 4.5, 6)
        yield 6
        plus.fadeOutLoop(sounds['crowd'], 8000)
        yield 0.1
        
        #play a generic (or specific) secondary comment
        plus.playSound(sounds['burp'])
        plus.animateCamera((0,9.5,0), (90*degrad,0*degrad), 5*degrad, (0,9.5,0), (90*degrad,720*degrad), 160*degrad, 0, 2)
        yield 2
        
        #hazard cams
        if self.bHazardsOn:
            plus.playSound(sounds['hazards'])
            plus.animateCamera((0,12.1,0), (-90*degrad,180*degrad), 150*degrad, (0,12.1,0), (-90*degrad,180*degrad), 130*degrad, 0, 3)
            yield 4

        players = plus.getPlayers()
        pcount = len(players)
        if pcount>0: plus.playSound(sounds['bots'])
        delaytime = 4*(pcount**(-1))
        
        if 0 in players:
            #bot 1 cam
            plus.animateCamera((-6,30,0), (0,90*degrad), 75*degrad, (-6,30,0), (0,90*degrad), 68*degrad, 0, delaytime)
            yield delaytime

        if 1 in players:
            #bot 2 cam
            plus.animateCamera((6,30,0), (0,270*degrad), 75*degrad, (6,30,0), (0,270*degrad), 68*degrad, 0, delaytime)
            yield delaytime

        if 2 in players:
            #bot 3 cam
            plus.animateCamera((0,30,-6), (0,0*degrad), 75*degrad, (0,30,-6), (0,0*degrad), 68*degrad, 0, delaytime)
            yield delaytime

        if 3 in players:
            #bot 4 cam
            plus.animateCamera((0,30,6), (0,180*degrad), 75*degrad, (0,30,6), (0,180*degrad), 68*degrad, 0, delaytime)
            yield delaytime
        
        #fade out music
        plus.fadeOutLoop(self.intro_music, 2000)
        yield 2
        
        # done
        yield 0
        
        
    def HazardsOn(self, on):
        #walls
        self.AddCollisionLine((8, 8), (8, -8))
        self.AddCollisionLine((8, -8), (-8, -8))
        self.AddCollisionLine((-8, -8), (-8, 8))
        self.AddCollisionLine((-8, 8), (8, 8))
        if on:
            prism = self.AddPrismatic("concrete", "crusher", 0, -1, 0, 0, 17, 0)
            self.crush = smHazards.Spikes(prism, 6400000, (0, 15, 0))
            
            self.AddHazard(self.crush)
            
            self.SetSubMaterialSound("crusher", "metal", 3, "Sounds\\bbham.wav")
            
        else:
            # hazards should be in their "hidden" position
            self.SetPinned ("crusher", True)
            
        return Arenas.SuperArena.HazardsOn(self, on)
        
    def Tick(self):
        if not self.bDoingIntro:
            if self.grunk < 15:
                self.grunk += 1
            if self.grunk >= 15:
                if self.bHazardsOn:
                    self.butTheKitty = 1
        if self.butTheKitty == 1:
            self.crush.Tick()
        return Arenas.SuperArena.Tick(self)
        
Arenas.register(Box)
