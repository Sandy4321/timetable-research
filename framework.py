#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      William
#
# Created:     25/08/2012
# Copyright:   (c) William 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from xml.dom.minidom import parseString
import random

class timetableProblem:

    def __init__(self):
        self.courses = []
        self.teachers = []

    def setupXML(self, filename):
        file = open(filename, "r")
        data = file.read()
        file.close()
        self._setupXMLString(data)

    def _setupXMLString(self,data):
        self.dom = parseString(data)
        global teacherNum
        teacherNum = 0
        self.rows = 0
        self.periods = 0
        for elem in self.dom.getElementsByTagName("course"):
            self.courses.append(course(elem.attributes["id"].value, elem.attributes["name"].value, elem.attributes["periods"].value, \
            elem.attributes["semesters"].value, elem.attributes["grades"].value, elem.attributes["mutExcl"].value, elem.attributes["likelyIncl"].value, elem.attributes["priority"].value))

        for elem in self.dom.getElementsByTagName("teacher"):
            self.rows += 1
            self.teachers.append(teacher(elem.attributes["name"].value, elem.attributes["yrcourses"].value, \
            elem.attributes["sblocks"].value, elem.attributes["s1blocks"].value, elem.attributes["s2blocks"].value,\
            elem.attributes["sskinnies"].value, elem.attributes["s1skinnies"].value, elem.attributes["s2skinnies"].value, elem.attributes["earlyBird"].value, self))


class timetable:
    def __init__(self, problem):
        #Initialize Empty Matrix
        #matrix[row(teacher)][column(period)]
        self.periods = 8
        self.rows = problem.rows
        self.problem = problem


    def mutate(self):
        self.mutaterow(random.randrange(0,self.rows))

    def mutaterow(self, row):
        while self._swap(random.randrange(0,self.periods), random.randrange(0,self.periods), row) == False:
            pass

    def _swap(self, a, b, row):
        try:
            ca = self.matrix[row][a]
            cb = self.matrix[row][b]
            if ca == " " or cb == " ":
                return False
            if ca=="-" or cb == "-":
                return False
            if a==b:
                return False
            if (ca.semFix == True or cb.semFix == True) and ((a<=7 and b > 7) or (b<=7 and a>7)):
                return False
            if(ca.semesters == "2" and a >7) or (cb.semesters == "2" and b>7):
                return False
            if(a==7 and cb.semesters == "1") or (b==7 and ca.semesters == "1"):
                return False

            #Like swaps
            if(ca.semesters == "1" and ca.periods == "1" and cb.semesters == "1" and cb.periods == "1"):
                self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                return True
            if(ca.semesters == "1" and ca.periods == "2" and cb.semesters == "1" and cb.periods == "2"):
                self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                return True
            if(ca.semesters == "2" and ca.periods == "1" and cb.semesters == "2" and cb.periods == "1"):
                self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                self.matrix[row][self.periods + a], self.matrix[row][self.periods + b] = self.matrix[row][self.periods + b], self.matrix[row][self.periods + a]
                return True

            blockopts = [0,2,4,5,8,10,12,13]
            if(ca.semesters =="1" and ca.periods == "1" and cb.semesters== "1" and cb.periods == "2"):
                a, b = b, a
                ca, cb = cb, ca
            if(ca.periods == "2" and not b in blockopts):
                return False
            if(ca.semesters == "1" and ca.periods == "2" and cb.semesters== "1" and cb.periods == "1"):
                if b in blockopts:
                    if (self.matrix[row][b+1].periods == "1" and self.matrix[row][b+1].semesters == "1") \
                    and not (self.matrix[row][b+1].semFix == True and ((a<7 and b >= 7) or (b<7 and a>=7))):
                        self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                        self.matrix[row][a + 1], self.matrix[row][b + 1] = self.matrix[row][b+1], self.matrix[row][a+1]
                        return True
                    if (self.matrix[row][b+1].periods == "1" and self.matrix[row][b+1].semesters == "2") and (self.matrix[row][(b + self.periods) % 16].periods == "1") \
                        and ((self.matrix[row][(a+self.periods) % 16].periods == "2") or \
                        (self.matrix[row][(a+self.periods) % 16].periods == "1" and self.matrix[row][(a+self.periods) % 16 + 1].periods == "1")):
                            if a > 7:
                                a-=8
                            if b > 7:
                                b-=8
                            self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                            self.matrix[row][a+1], self.matrix[row][b+1] = self.matrix[row][b + 1], self.matrix[row][a + 1]
                            self.matrix[row][a+8], self.matrix[row][b+8] = self.matrix[row][b + 8], self.matrix[row][a + 8]
                            self.matrix[row][a+9], self.matrix[row][b+9] = self.matrix[row][b + 9], self.matrix[row][a + 9]
                            return True

                """if b-1 in blockopts:
                    if (self.matrix[row][b-1].periods == "1" and self.matrix[row][b-1].semesters == "1") \
                    and not (self.matrix[row][b-1].semFix == True and ((a<7 and b >= 7) or (b<7 and a>=7))):
                        self.matrix[row][a], self.matrix[row][b - 1] = self.matrix[row][b - 1], self.matrix[row][a]
                        self.matrix[row][a + 1], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a+1]
                        return True
                    if (self.matrix[row][b-1].periods == "1" and self.matrix[row][b-1].semesters == "2") and (self.matrix[row][(b + self.periods) % 16].periods == "1") \
                        and ((self.matrix[row][(a+self.periods) % 14].periods == "2") or \
                        (self.matrix[row][(a+self.periods) % 16].periods == "1" and self.matrix[row][(a+self.periods) % 16 + 1].periods == "1")):
                            if a > 7:
                                a-=8
                            if b > 7:
                                b-=8
                            self.matrix[row][a], self.matrix[row][b-1] = self.matrix[row][b-1], self.matrix[row][a]
                            self.matrix[row][a+1], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a + 1]
                            self.matrix[row][(a+self.periods) % (self.periods*2)], self.matrix[row][b+7] = self.matrix[row][b + 7], self.matrix[row][(a + self.periods) % (self.periods*2)]
                            self.matrix[row][(a+9) % 16], self.matrix[row][b+8] = self.matrix[row][b + 8], self.matrix[row][(a + 9) % 16]
                            return True"""

            if ca.semesters == "1" and cb.semesters == "2" and cb.periods == "1":
                a, b= b, a
                ca, cb= cb, ca

            if ca.semesters == "2" and cb.semesters == "1" and cb.periods == "1":
                if self.matrix[row][(b+self.periods) % (self.periods * 2)].periods == "1":
                    if b > 7:
                        b-=8
                    self.matrix[row][a], self.matrix[row][b] = self.matrix[row][b], self.matrix[row][a]
                    self.matrix[row][a + self.periods], self.matrix[row][b + self.periods] = self.matrix[row][b + self.periods], self.matrix[row][a + self.periods]
                    return True
            if ca.semesters == "2" and cb.periods == "2":
                a, b= b, a
                ca, cb= cb, ca
            if(ca.periods == "2" and not b in blockopts):
                return False
            if ca.periods == "2" and cb.semesters == "2":
                if not ((self.matrix[row][(a + self.periods) % (self.periods * 2)].periods == "2") or \
                (self.matrix[row][(a + self.periods) % (self.periods * 2)].periods == "1"  and self.matrix[row][(a + self.periods) % (self.periods*2) + 1].periods == "1")):
                    return False
                if b != self.periods - 2:
                    if(self.matrix[row][b+1].semesters == "2") or (self.matrix[row][b+1].semesters == "1" and self.matrix[row][b+1].periods == "1" \
                    and self.matrix[row][b+1 + self.periods].semesters == "1" and self.matrix[row][b+1+self.periods].periods == "1"):
                        self.matrix[row][a], self.matrix[row][b]  =self.matrix[row][b], self.matrix[row][a]
                        self.matrix[row][(a + self.periods) % (self.periods*2)], self.matrix[row][b + self.periods]  = self.matrix[row][b + self.periods], self.matrix[row][(a + self.periods) % (self.periods*2)]
                        self.matrix[row][a + 1], self.matrix[row][b + 1]  =self.matrix[row][b + 1], self.matrix[row][a + 1]
                        self.matrix[row][(a + self.periods) % (self.periods*2) + 1], self.matrix[row][b + self.periods + 1]  = self.matrix[row][b + self.periods + 1], self.matrix[row][(a + self.periods) % (self.periods*2) + 1]
                        return True
                if b != 0 and b-1 in blockopts:
                    if(self.matrix[row][b-1].semesters == "2") or (self.matrix[row][b-1].semesters == "1" and self.matrix[row][b-1].periods == "1" \
                    and self.matrix[row][b-1 + self.periods].semesters == "1" and self.matrix[row][b-1+self.periods].periods == "1"):
                        self.matrix[row][a], self.matrix[row][b - 1]  =self.matrix[row][b - 1], self.matrix[row][a]
                        self.matrix[row][(a + self.periods) % (self.periods*2)], self.matrix[row][b + self.periods - 1]  = self.matrix[row][b + self.periods - 1], self.matrix[row][(a + self.periods) % (self.periods*2)]
                        self.matrix[row][a + 1], self.matrix[row][b]  =self.matrix[row][b], self.matrix[row][a + 1]
                        self.matrix[row][(a + self.periods) % (self.periods*2) + 1], self.matrix[row][b + self.periods]  = self.matrix[row][b + self.periods], self.matrix[row][(a + self.periods) % (self.periods*2) + 1]
                        return True
        except AttributeError:
            return False

        return False

    def _countSections(self):
        self.sections = {}
        for row in self.matrix:
            i = 0
            for course in row:
                i+=1
                if course == "-":
                    continue
                if course == " ":
                    continue
                if course.semesters == "2" and i >8:
                    continue
                if course.course in self.sections:
                    self.sections[course.course] += 1
                else:
                    self.sections[course.course] = 0

    def setupRandom(self):
        problem = self.problem
        self.matrix = [[None for i in range(0, self.periods*2)] for x in range(0, self.rows)]

        i=0
        blockopts = [0,2,4,5]
        for t in problem.teachers:
            for course in t.s1blocks:
                for opt in blockopts:
                    if self.matrix[i][opt] == None and self.matrix[i][opt+1] == None:
                        self.matrix[i][opt] = timeslot(course, semFix = True)
                        self.matrix[i][opt+1] = " "
                        break
            i += 1

        i=0
        blockopts = [8,10,12,13]
        for t in problem.teachers:
            for course in t.s2blocks:
                for opt in blockopts:
                    if self.matrix[i][opt] == None and self.matrix[i][opt+1] == None:
                        self.matrix[i][opt] = timeslot(course, semFix = True)
                        self.matrix[i][opt+1] = " "
                        break
            i += 1

        i=0
        blockopts = [0,8,2,10,4,12,5,13]
        for t in problem.teachers:
            for course in t.sblocks:
                for opt in blockopts:
                    if self.matrix[i][opt] == None and self.matrix[i][opt+1] == None:
                        self.matrix[i][opt] = timeslot(course)
                        self.matrix[i][opt+1] = " "
                        break
            i += 1

        i=0
        yropts = range(0,7)

        for t in problem.teachers:
            if t.earlyBird == "true":
                self.matrix[i][7] = timeslot(t.yrcourses.pop(0))
                self.matrix[i][15] = self.matrix[i][7]
            else:
                self.matrix[i][7] = "-"
                self.matrix[i][15] = "-"
            for course in t.yrcourses:
                for opt in yropts:
                    if self.matrix[i][opt] == None and self.matrix[i][self.periods + opt] == None:
                        self.matrix[i][opt] = timeslot(course)
                        self.matrix[i][self.periods + opt] = timeslot(course)
                        break
            if t.earlyBird == "true":
                t.yrcourses.insert(0, self.matrix[i][7].course)
            i += 1
        i=0
        skinnyopts = range(0,7)
        for t in problem.teachers:
            for course in t.s1skinnies:
                for opt in skinnyopts:
                    if self.matrix[i][opt] == None:
                        self.matrix[i][opt] = timeslot(course, semFix=True)
                        break
            i += 1

        i=0
        skinnyopts = range(8,15)
        for t in problem.teachers:
            for course in t.s2skinnies:
                for opt in skinnyopts:
                    if self.matrix[i][opt] == None:
                        self.matrix[i][opt] = timeslot(course, semFix=True)
                        break
            i += 1

        i=0
        skinnyopts = range(0,15)
        skinnyopts.remove(7)
        for t in problem.teachers:
            for course in t.sskinnies:
                for opt in skinnyopts:
                    if self.matrix[i][opt] == None:
                        self.matrix[i][opt] = timeslot(course)
                        break
            i += 1

        self.shuffle()


    def printMatrix(self):
        string = ""
        i=0
        for row in self.matrix:
            if i > 9:
                string += str(i) + "."
            else:
                string += " " + str(i) + "."
            for c in row:
                if(c == " "):
                    string += "   --      "
                elif(c=="-"):
                    string += c + "          "

                elif(c == None):
                    string += "None       "
                else:
                    if len(c.id) < 10:
                        c.id += "".join([" " for j in range(0,10-len(c.id))])
                    string +=  " " + c.id
            string += "\n"
            i+=1
        return string

    def shuffle(self):
        rownum = 0
        for row in self.matrix:
            i = len(row) - 1
            for c in reversed(row):
                j = random.randrange(0, i + 1)
                self._swap(i,j,rownum)
                i-=1
            rownum += 1

    def objective(self):
        self._countSections()
        objValue = 0
        self.rowcosts = []
        for row in self.matrix:
            rowcost = self._costRow(row)
            self.rowcosts.append(rowcost)
            objValue += rowcost
        self.obj = objValue
        return objValue


    def _costRow(self, row):
        rowcost = 0
        i=0
        for c0 in row:
            if c0 != " " and c0 != "-":
                if c0.id !="P":
                    c0cost = 0

                    column = [r[i] for r in self.matrix]
                    j = 0
                    for ci in column:
                        if self.matrix[j] == row:
                            j += 1
                            continue
                        if ci == " ":
                            ci = self.matrix[j][i-1]
                        if ci == "-":
                            j+=1
                            continue
                        j+=1
                        try:
                            if ci.id != "P":
                                cicost = 0
                                if self.sections[ci.course] >=3:
                                    pass
                                elif ci.mutExcl == c0.mutExcl:
                                    pass
                                else:
                                    cicost = 4 - int(ci.priority)
                                    if self.sections[ci.course] == 1:
                                        if self.sections[c0.course] == 1:
                                            cicost *= 3
                                        else:
                                            cicost *= 2
                                    if ci.likelyIncl == c0.likelyIncl:
                                        cicost *= 2
                                    overlap = False
                                    for g in c0.grades:
                                        if g in ci.grades:
                                            overlap = True
                                    if not overlap:
                                        cicost = 0
                                c0cost += cicost
                        except AttributeError:
                            print str(j) + " " + str(i)
                            print ci
                            print self.matrix[j][i]
                            print self.matrix[j][i-1]
                            self.printMatrix()
                            raise AttributeError
                    rowcost += c0cost
            i+=1
        return rowcost

class teacher:

    def __init__(self, name, yrcourses, sblocks, s1blocks, s2blocks, sskinnies, s1skinnies, s2skinnies, earlyBird, problem):
        global teacherNum
        self.name = name
        self.problem = problem
        courseidarray = []
        self.yrcourses = []
        self.sblocks = []
        self.s1blocks = []
        self.s2blocks = []
        self.s1skinnies = []
        self.s2skinnies = []
        self.sskinnies = []
        self.earlyBird = earlyBird
        self.num = teacherNum
        teacherNum += 1
        clistarray = [self.yrcourses, self.sblocks, self.s1blocks, self.s2blocks, self.sskinnies, self.s1skinnies, self.s2skinnies]
        paramarray = [yrcourses, sblocks, s1blocks, s2blocks, sskinnies, s1skinnies, s2skinnies]
        for i in range(0, len(clistarray)):
            courseidarray = paramarray[i].split(",")
            for courseid in courseidarray:
                if courseid != "":
                    clistarray[i].append([x for x in self.problem.courses if x.id == courseid][0])

class course:
    def __init__(self, id, name, periods, semesters, grades, mutExcl, likelyIncl, priority):
        self.id = id
        self.name = name
        self.periods = periods
        self.semesters = semesters
        if self.id != "P":
            self.grades = [int(elem) for elem in grades.split("-")]
            if len(self.grades) == 1:
                self.grades.append(self.grades[0])
            self.grades = range(self.grades[0], self.grades[1] + 1)
        else:
            self.grades = []
        self.mutExcl = mutExcl
        self.likelyIncl = likelyIncl
        self.priority = priority
        self.sections = 0


class timeslot:
    def __init__(self, course, semFix = False):
        self.course = course
        self.id = course.id
        self.name = course.name
        self.periods = course.periods
        self.semesters = course.semesters
        self.grades = course.grades
        self.mutExcl = course.mutExcl
        self.likelyIncl  = course.likelyIncl
        self.semFix = semFix
        self.priority = course.priority
        self.sections = course.sections

def main():
    global a, k
    a = timetableProblem()
    a.setupXML("samplesets/Final Run/03.xml")
    k = timetable(a)
    k.setupRandom()
    print k.printMatrix()


if __name__ == '__main__':
    main()
    pass

