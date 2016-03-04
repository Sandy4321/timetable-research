#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      00821380
#
# Created:     02/10/2012
# Copyright:   (c) 00821380 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from xml.dom.minidom import Document
import random
from string import ascii_letters, digits
from framework import timetableProblem, timetable

def randString(n):
    return "".join([random.choice(ascii_letters + digits) for x in range(0,n)])
def generate():
    doc = Document()
    prob = doc.createElement("timetableProblem")
    doc.appendChild(prob)

    courses = doc.createElement("courses")
    prob.appendChild(courses)
    courselist = []
    mutExclGroups = [randString(6) for i in range(0,10)]
    likelyInclGroups = [randString(6) for i in range(0,10)]

    for i in range(0,50):
        course = doc.createElement("course")
        course.setAttribute("id", randString(10))
        course.setAttribute("name", randString(30))
        course.setAttribute("priority", str(random.randrange(1,4)))

        if random.random() <= 0.63:
            sem = "1"
        else:
            sem = "2"
        course.setAttribute("semesters", sem)
        if random.random() <= 0.59 and not sem == "2":
            per = "2"
        else:
            per = "1"
        course.setAttribute("periods", per)

        if random.random() <0.6:
            grades = str(random.randrange(9,13))
        else:
            x = random.randrange(9,12)
            y = random.randrange(x+1, 13)
            grades = str(x) + "-" + str(y)
        course.setAttribute("grades", grades)

        if random.random() < 0.3:
            mutExcl = random.choice(mutExclGroups)
        else:
            mutExcl = ""
        course.setAttribute("mutExcl", mutExcl)

        if random.random() < 0.3:
            likelyIncl = random.choice(likelyInclGroups)
        else:
            likelyIncl = ""
        course.setAttribute("likelyIncl", likelyIncl)
        courselist.append(course)
        courses.appendChild(course)

    course = doc.createElement("course")
    course.setAttribute("id", "P")
    course.setAttribute("grades", "")
    course.setAttribute("name", "Planning Period")
    course.setAttribute("periods", "1")
    course.setAttribute("semesters", "1")
    course.setAttribute("mutExcl", "")
    course.setAttribute("likelyIncl", "")
    course.setAttribute("priority", "0")
    courses.appendChild(course)

    teachers = doc.createElement("teachers")
    prob.appendChild(teachers)
    z = 0
    while z < 25:
        teacher = doc.createElement("teacher")
        teacher.setAttribute("name", random.choice(["mr.", "ms."]) + randString(10))
        yrcourses = []
        if random.random() <= 0.08:
            earlyBird = True
            teacher.setAttribute("earlyBird", "true")
        else:
            earlyBird = False
            teacher.setAttribute("earlyBird", "false")
        n = int(round(random.normalvariate(2.58,2)))
        if n > 7:
            n=7
        if n<0:
            n=0
        if(earlyBird):
            n += 1
        for i in range(0,n):
            while(True):
                x = random.choice(courselist)
                if(x.attributes["semesters"].value == "2"):
                    break
            yrcourses.append(x)
        if len(yrcourses) != 0 :
            teacher.setAttribute("yrcourses", "".join([course.attributes["id"].value + "," for course in yrcourses]))
        else:
            teacher.setAttribute("yrcourses", "")
        if earlyBird:
            n -= 1
            yrcourses.pop(len(yrcourses) - 1)
        if n==0:
            j=3
        if n==1:
            j=2
        if n==2:
            j=2
        if n==3:
            j=1
        if n==4:
            j=1
        if n>4:
            j=0
        sblocks = []
        s1blocks = []
        s2blocks = []
        numblocks = int(random.normalvariate(2.59, 2))
        if numblocks < 0:
            numblocks = 0
        if numblocks > j:
            numblocks = j
        if(j !=0):
            for i in range(0,numblocks):
                while(True):
                    x=random.choice(courselist)
                    if(x.attributes["periods"].value == "2"):
                        break
                if(random.random()<0.7):
                    sblocks.append(x)
                elif(random.random()<0.5 and len(s1blocks)+ len(sblocks) < j):
                    s1blocks.append(x)
                elif(random.random()<0.5 and len(s2blocks)+ len(sblocks) < j):
                    s2blocks.append(x)
        sskinnies = []
        s1skinnies = []
        s2skinnies = []
        for i in range(0,20):
            while True:
                x=random.choice(courselist)
                if(x.attributes["periods"].value == "1" and x.attributes["semesters"].value == "1"):
                    break
            if(random.random()<0.7 and len(s1blocks)*2 + len(s2blocks)*2 + \
                len(sblocks)*2 + len(sskinnies) + len(s1skinnies) + len(s2skinnies) + len(yrcourses)*2 < 12):
                sskinnies.append(x)
            elif((len(s1blocks) * 2 +len(s1skinnies) + len(yrcourses) <6) and len(s1blocks)*2 + len(s2blocks)*2 + \
                len(sblocks)*2 + len(sskinnies) + len(s1skinnies) + len(s2skinnies) + len(yrcourses)*2 < 12):
                s1skinnies.append(x)
            elif((len(s2blocks) *2 + len(s2skinnies) + len(yrcourses) <6) and len(s1blocks)*2 + len(s2blocks)*2 + \
                len(sblocks)*2 + len(sskinnies) + len(s1skinnies) + len(s2skinnies) + len(yrcourses)*2 < 12):
                s2skinnies.append(x)

        teacher.setAttribute("sblocks", "".join([course.attributes["id"].value + "," for course in sblocks]))
        teacher.setAttribute("s1blocks", "".join([course.attributes["id"].value + "," for course in s1blocks]))
        teacher.setAttribute("s2blocks", "".join([course.attributes["id"].value + "," for course in s2blocks]))

        teacher.setAttribute("sskinnies", "".join([course.attributes["id"].value + "," for course in sskinnies]))
        teacher.setAttribute("s1skinnies", "".join([course.attributes["id"].value + "," for course in s1skinnies]) + "P")
        teacher.setAttribute("s2skinnies", "".join([course.attributes["id"].value + "," for course in s2skinnies]) + "P")


        z += 1
        teachers.appendChild(teacher)
        a = timetableProblem()
        a._setupXMLString(doc.toxml())
        k = timetable(a)
        k.setupRandom()
        for row in k.matrix:
            if None in row:
                z -= 1
                teachers.removeChild(teacher)
                break
    return doc


Filename = "samplesets/" + raw_input("Filename:") + ".xml"
doc = generate()
file = open(Filename, "w")
file.write(doc.toprettyxml())
file.close()
"""for i in range(0,30):
    doc = generate()
    Filename = str(i+1)
    if len(Filename) == 1:
        Filename = "0" + Filename
    Filename = "samplesets/Final Run/" + Filename + ".xml"
    file = open(Filename, "w")
    file.write(doc.toprettyxml())
    file.close()"""
