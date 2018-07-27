import plus
import random
from AI import vector3

import Arenas

class Hazard(object):
    def __init__(self, location):
        self.location = location
        
class Electricity(Hazard):

    def __init__(self, location = (0, 0, 0)):
        Hazard.__init__(self, location)
        self.sensors = {}
        self.zapping = []
        self.zapsound = plus.createSound("Sounds/zap_loop.wav", True, self.location)
        p = 0
        x = 0
        y = 0
        z = 0
        
    def __del__(self):
        plus.removeSound(self.zapsound)
        
    def Tick(self):
        for each in plus.getPlayers():
            if plus.getLocation(each)[1] < -5 or abs(plus.getLocation(each)[0]) > 18 or abs(plus.getLocation(each)[2]) > 18:
                p = 1
            else:
                p = 0

        if self.NumBotsInRange()>0:
            self.Zap()
            if not plus.isMatchPaused() and not plus.isMatchOver():
                for bot, in_range in self.sensors.iteritems():
                    x = abs(plus.getLocation(bot)[0])
                    y = plus.getLocation(bot)[1]
                    z = abs(plus.getLocation(bot)[2])
                    if in_range and p==0 and y<3 and y>-5 and ((x>11.5 and x<18) or (z>11.5 and z<18)):
                        plus.damage(bot, 0, 16, plus.getLocation(bot))
                        plus.addPoints(bot, -16)
        
        if self.NumBotsInRange()==0:
            self.zapping = []
            plus.stopSound(self.zapsound)
        
    def Zap(self):
        if not plus.isMatchPaused() and not plus.isMatchOver():
            for bot, in_range in self.sensors.iteritems():
                x = abs(plus.getLocation(bot)[0])
                y = plus.getLocation(bot)[1]
                z = abs(plus.getLocation(bot)[2])
                if in_range and y<3 and y>-5 and ((x>11.5 and x<18) or (z>11.5 and z<18)):
                    plus.zap(bot, 10, 3.0)
                    self.zapping.append(bot)
                    plus.playSound(self.zapsound)
        
    def NumBotsInRange(self):
        numBots = 0
        for bot, in_range in self.sensors.iteritems():
            if in_range: numBots += 1
        
        return numBots
        
    def ZoneEvent(self, direction, robot, chassis):
        if robot>0:
            r = robot - 1
            if r not in self.sensors: self.sensors[r] = 0
            
            if direction==1:
                self.sensors[r] += 1
            elif direction==-1:
                self.sensors[r] -= 1
        
