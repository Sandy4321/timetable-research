#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      00821380
#
# Created:     16/10/2012
# Copyright:   (c) 00821380 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random, time, math, copy
import GeneticAlgorithm
print "Initializing."

class Environment(GeneticAlgorithm.Environment):
    def __init__(self,problem,initTemp=100,NReset = 6):
        self.initTemp = initTemp
        self.NReset = NReset
        GeneticAlgorithm.Environment.__init__(self, problem)
        super

    def run(self):
        self.T=self.initTemp
        return GeneticAlgorithm.Environment.run(self)

    def generation(self):
        GeneticAlgorithm.Environment.generation(self)
        self.T = self.T * 0.9 #Insert other Cooling Schedule Here
        print self.T
        if self.bestcount == self.NReset:
            self.T = self.initTemp

    def crossover(self,A,B):
        child = GeneticAlgorithm.Environment.crossover(self,A,B)
        child.objective()
        return child


    def mutWithProb(self, child):
        newChild = GeneticAlgorithm.timetable(self.problem)
        newChild.matrix = [x[:] for x in child.matrix]
        newChild.mutate()
        newChild.objective()
        if newChild.obj <= child.obj:
                child.matrix = newChild.matrix
                child.obj = newChild.obj
                child.rowcosts = newChild.rowcosts
        elif random.random() < math.exp(-(newChild.obj-child.obj) / self.T):
                child.matrix = newChild.matrix
                child.obj = newChild.obj

def main():
    global prob
    prob = GeneticAlgorithm.framework.timetableProblem()
    prob.setupXML("samplesets/12.xml")
    env = Environment(prob)
    iTime = time.time()

    print env.run()
    print time.time() - iTime


if __name__ == '__main__':
    main()
