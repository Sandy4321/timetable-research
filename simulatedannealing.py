#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      William
#
# Created:     15/10/2012
# Copyright:   (c) William 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random, framework, math, os, time

class model:
    def __init__(self, problem, coolingRate=0.9, maxSwaps = 40, maxSuccessSwaps = 30, initTemp=100.0):
        self.problem = problem
        self.coolingRate=coolingRate
        self.maxSwaps = maxSwaps
        self.maxSuccessSwaps = maxSuccessSwaps
        self.initTemp = initTemp

    def run(self):
        startTimeReal = time.time()
        startTimeUser = os.times()[0]
        startTimeSys = os.times()[1]
        self.longdata = ""

        self.T = self.initTemp
        self.iternum = 0
        self.state = framework.timetable(self.problem)
        self.state.setupRandom()
        self.state.objective()
        self.startState = self.state.obj
        self.bestvalue = 100000
        self.bestcount = 0
        while True:
            self.bestcount += 1
            self.iteration()
            if self.T > 1:
                self.bestcount = 0
            if self.bestcount > 10:
                return self.bestvalue, time.time() - startTimeReal, (os.times()[0] - startTimeUser) + (os.times()[1] - startTimeSys), self.iternum, self.longdata, self.startState, self.best.printMatrix()

    def iteration(self):
        swaps = 0
        successSwaps = 0
        while swaps < self.maxSwaps and successSwaps < self.maxSuccessSwaps:
            newstate = framework.timetable(self.problem)
            newstate.matrix = [x[:] for x in self.state.matrix]
            newstate.mutate()
            newstate.objective()
            if newstate.obj <= self.state.obj:
                self.state = newstate
                successSwaps += 1
            elif random.random() < math.exp(-(newstate.obj-self.state.obj) / self.T):
                self.state = newstate
                successSwaps += 1

            swaps += 1
        print "T=" + str(self.T)
        print "SuccessSwaps: " + str(successSwaps)
        print "Swaps: " + str(swaps)
        print self.state.obj
        self.longdata += str(self.state.obj) + ","
        if self.state.obj < self.bestvalue:
            self.bestvalue = self.state.obj
            self.best = self.state
            self.bestcount = 0
        self.iternum += 1
        self.cool()


    def cool(self):
        self.T *= self.coolingRate


def main():
    prob = framework.timetableProblem()
    prob.setupXML("samplesets/12.xml")
    m = model(prob)
    print m.run()

if __name__ == '__main__':
    main()
