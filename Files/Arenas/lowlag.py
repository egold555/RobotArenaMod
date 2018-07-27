from __future__ import generators
import plus
import Arenas
import random
import Hazards
import math

class Box(Arenas.SuperArena):
    "Great for flippers and online fights!"
    name = "Low Lag Arena"
    preview = "lowlag/lowlag_preview.bmp"
    game_types = ['DEATHMATCH', 'BATTLE ROYAL', 'TEAM MATCH']
    extent = (-15, 15, 15, -15)

    def __init__(self):
        Arenas.SuperArena.__init__(self, "Arenas/lowlag/lowlag.gmf")
        #plus.Arena.__init__(self, "")
        plus.setBackColor(.36, .537, .788)
        
        degrad = 0.01745
        self.AddStaticCamera("Battle Veiw", (19.5, 15, 19.5), (50*degrad,225*degrad), 55*degrad)
	self.AddStaticCamera("High Flipper View", (-19.5, 45, -19.5), (48*degrad,45*degrad), 84*degrad)
	self.AddStaticCamera("Birds Eye View", (0, 45, 0), (90*degrad,0), 75*degrad)
	self.AddWatchCamera("Combat Cam", (-12, 8, 12), (16, 36, 65*degrad, 30*degrad))
	self.AddWatchCamera("Aerial Cam", (-19.5, 35, -19.5), (50, 60, 45*degrad, 60*degrad))
	self.AddWatchCamera("Ground Cam", (8, -5, -8), (15, 40, 75*degrad, 35*degrad))
	self.AddWatchCamera("Spectator Cam", (13, 15, 13), (6, 18, 45*degrad, 45*degrad))
	
        self.players = ()

    def AddShadowReceivers(self):
        self.SetShadowSource(5.897, 19.159, 5.899)
        
    def Activate(self, on):
        if on: self.players = plus.getPlayers()
        
        Arenas.SuperArena.Activate(self, on)
        
Arenas.register(Box)
