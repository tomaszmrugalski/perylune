#!/usr/bin/python

import os
import sys
import argparse

class ObstacleEditor:

    filename = ""
    obstacle_min = -1
    obstacle_max = -1
    obstacle_height = 0

    obs = []
    
    def printHelp(self):
        print("Obstacles editor for Trimble Planning")
        print("Author: Tomek Mrugalski")
        print("License: GNU GPL v3")
        print("")
        print("Usage:")
        print("python obstacles-editor.py filename.txt value1-value2,value3")
        print("filename.txt - file with obstacles. If not found, a new file with no obstacles will be generated.")
        print("value1-value2 - specifies beginning  and ending azimuth of an obstacle, expressed in degrees.")
        print("value3 - elevation of an obstacle, in degrees.")
        print("")
        print("Example: to add an obstacle that blocks 20 degrees in E direction and has height of 45 degrees, you can:")
        print("python obstacles-editor.py obstacles.txt 70-90,45")
    
    def checkParams(self):
        if len(sys.argv) < 3:
            print("ERROR: Invalid number of parameters. At least 2 (filename and obstacle definition) are needed")
            return False
        self.filename = sys.argv[1]
        tmp, self.obstacle_height = sys.argv[2].split(',')
        self.obstacle_min,self.obstacle_max = tmp.split('-')

        self.obstacle_min = int(self.obstacle_min)
        self.obstacle_max = int(self.obstacle_max)
        self.obstacle_height = int(self.obstacle_height)
        print("Filename %s, obstacle %d-%d, height %d\n" % (self.filename, self.obstacle_min, self.obstacle_max, self.obstacle_height))
        return True


    def createEmptyData(self):
        for i in range(0,360):
            self.obs.append([i, 0.0])
        pass

    def loadFile(self):
        try:
            f = open(self.filename, 'r')
        except IOError as x:
            print("File %s missing, creating empty file." % self.filename)
            return False
        for l in f.readlines():
            print ("Line len=%d [%s]" % (len(l), l))
            if l[0] == ';' or len(l) == 1:
                self.obs.append(l)
            else:
                a, b = l.split()
                self.obs.append([int(a),float(b)])
        print("Read %d lines from %s" % (len(self.obs), self.filename))
        return True

    def printData(self):
        for l in self.obs:
            print(l)

    def applyObstacles(self):
        for l in self.obs:
            if not isinstance(l, list):
                continue
            if l[0] >= self.obstacle_min and l[0] <= self.obstacle_max:
                l[1] = self.obstacle_height + 0.0
        pass

    def writeFile(self):

        backup = self.filename + '.old'
        print("Removing backup: %s" % backup)
        try:
            os.remove(self.filename + '.old')
        except IOError:
            pass

        print("Renaming %s to %s" % (self.filename, backup))
        try:
            os.rename(self.filename, self.filename + '.old')
        except IOError:
            pass

        print("Writing new data to %s" % self.filename)
        f = open(self.filename, 'w')
        print("Writing %d lines" % len(self.obs))
        for l in self.obs:
            if isinstance(l, str):
                f.write(l)
            else:
                f.write("%d %2.1f\n" % (l[0], l[1]))
        f.close()
    
    def editObstacles(self):
        if not self.checkParams():
            self.printHelp()
            sys.exit(1)

        if not self.loadFile():
            self.createEmptyData()

        self.applyObstacles()
        self.printData()
        self.writeFile()

if __name__ == "__main__":
    
    o = ObstacleEditor()
    o.editObstacles()

