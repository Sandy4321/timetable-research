#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      00821380
#
# Created:     11/10/2012
# Copyright:   (c) 00821380 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import random, framework, time, os

problemPath = "samplesets/Final Run/01.xml"

class timetable (framework.timetable):
    def calcFitness(self, env):
        maxObj, minObj = 0, 100000
        for individual in env.population:
            if individual.obj > maxObj:
                maxObj = individual.obj
            if individual.obj < minObj:
                minObj = individual.obj
        try:
            self.fit = float(env.MaxFit) - (float(env.MaxFit-env.MinFit)/float(maxObj-minObj)) * float(self.obj - minObj)
        except ZeroDivisionError:
            self.fit = 1.0
        return self.fit



class Environment:
    def __init__(self, problem, populationSize = 60, mutationRate = 0.1, crossoverRate=0.5, MinFit = 1, MaxFit=10, elitism = 4):
        self.problem = problem
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.MinFit = MinFit
        self.MaxFit = MaxFit
        self.elitism = elitism

    def run(self):

        startTimeReal = time.time()
        startTimeUser = os.times()[0]
        startTimeSys = os.times()[1]
        self.longdata = ""
        self.population = []
        for i in range(0,self.populationSize):
            self.population.append(timetable(self.problem))
            self.population[i].setupRandom()
            self.population[i].objective()

        self.bestValue = 10000
        self.best = None
        self.bestcount = 0
        self.genNum = 0
        self.STOPCRIT = False
        print "Running"
        while not self.STOPCRIT:
            self.bestcount += 1
            self.generation()
            if self.genNum == 1:
                self.startState = self.bestValue
            if self.bestcount > 10:
                return self.bestValue, time.time() - startTimeReal, (os.times()[0] - startTimeUser) + (os.times()[1] - startTimeSys), self.genNum, self.longdata, self.startState, self.best.printMatrix()


    def crossover(self, A, B):
        sortList = zip(A.rowcosts,[x[:] for x in A.matrix],[x[:] for x in B.matrix], self.problem.teachers)
        sortList.sort()
        z= zip(*sortList)
        sortedA, sortedB, sortedTeachers = z[1], z[2], z[3]
        k = random.randrange(0, len(sortedA))
        sortedchild = sortedA[0:k] +  sortedB[k:len(sortedB)]
        unsortchild = zip([teacher.num for teacher in sortedTeachers], sortedchild)
        unsortchild.sort()
        child = timetable(self.problem)
        child.matrix = list(zip(*unsortchild)[1])
        return child


    def generation(self):
        genBest = 100000
        self.flagCrossover = False
        for individual in self.population:
            if individual.obj < self.bestValue:
                self.bestValue = individual.obj
                self.best = individual
                self.bestcount = 0
            if individual.obj < genBest:
                genBest = individual.obj
        totalFitness = 0
        for individual in self.population:
                    individual.calcFitness(self)
                    totalFitness += individual.fit

        boundries = [0]
        for individual in self.population:
            probability = individual.fit/totalFitness
            boundries.append(boundries[len(boundries) - 1] + probability)


        sortpopulation = zip([indv.obj for indv in self.population], self.population)
        sortpopulation.sort()
        newpopulation = list(zip(*sortpopulation)[1])[0:self.elitism]
        for i in range(0, self.populationSize/2 - self.elitism):
            r = random.random()
            j=0
            for boundry in boundries:
                if r <= boundry:
                    parentA = self.population[j-1]
                    break
                j+=1
            j=0
            r = random.random()
            for boundry in boundries:
                if r <= boundry:
                    parentB = self.population[j-1]
                    break
                j+=1
            if random.random() < self.crossoverRate:
                childA = self.crossover(parentA, parentB)
                childB = self.crossover(parentB, parentA)
                self.flagCrossover = True
            else:
                childA = timetable(self.problem)
                childA.matrix = [x[:] for x in parentA.matrix]
                childA.obj = parentA.obj
                childA.rowcosts= parentA.rowcosts
                childB = timetable(self.problem)
                childB.matrix = [x[:] for x in parentB.matrix]
                childB.obj = parentB.obj
                childB.rowcosts= parentB.rowcosts

            self.mutWithProb(childA)
            self.mutWithProb(childB)

            newpopulation.append(childA)
            newpopulation.append(childB)
            self.flagCrossover = False

        self.population = newpopulation

        self.genNum += 1
        print "Generation " + str(self.genNum) + "  " + str(genBest)
        self.longdata += str(genBest) + ","

    def mutWithProb(self,child):
        if random.random() < self.mutationRate:
            child.mutate()
            child.objective()
        elif self.flagCrossover:
            child.objective()

def main():
    global prob
    prob = framework.timetableProblem()
    prob.setupXML(problemPath)
    env = Environment(prob)
    print env.run()


if __name__ == '__main__':
    main()
