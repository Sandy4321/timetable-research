#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      William
#
# Created:     02/12/2012
# Copyright:   (c) William 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import framework, GeneticAlgorithm, simulatedannealing, ASAGA
alg = [GeneticAlgorithm.Environment,simulatedannealing.model,ASAGA.Environment]
letter = ["A","B","C"]
probPath = "samplesets/Final Run/"
dataFile = "data/final.csv"
dataProgFile = "data/finalProg.csv"
dataMatrixFile = "data/finalMatrix.txt"

def main():
    file = open(dataFile, "w")
    file.write("\"Treatment\",\"Problem\",\"Outcome\",\"Real Time\",\"CPU Time\",\"#Generations\",\"Starting State\"\n")
    file.close()
    file = open(dataProgFile, "w")
    file.write("")
    file.close()
    file = open(dataMatrixFile, "w")
    file.write("")
    file.close()
    for i in range(1,31):
        problem = framework.timetableProblem()
        name = str(i)
        if len(name) == 1:
            name = "0" + name
        problem.setupXML(probPath + name + ".xml")
        for j in range(0,3):
            for k in range(0,30):
                print str(i) + letter[j] + str(k)
                mod = alg[j](problem)
                rundata = mod.run()
                file = open(dataFile, "a")
                file.write(letter[j] + "," + str(i) + "," + ",".join([str(dat) for dat in rundata[0:4] + rundata[5:6]]) + "\n")
                file.close()
                file = open(dataProgFile, "a")
                file.write(letter[j] + "," + str(i) + "," + ",".join(rundata[4]) + "\n")
                file.close()
                file = open(dataMatrixFile, "a")
                file.write(letter[j] + str(i) + "\n" + rundata[6] + "\n\n")
                file.close()


if __name__ == '__main__':
    main()
