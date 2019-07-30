import os
import random
import csv
import gridSolver
import math as m

def main():
    path = os.getcwd() + "/"
    #generate mock data of robot with random walk
    beacons = [1,2,3,4]
    #inital position
    beacon1 = [13.637, 6.9202, 2.335]
    beacon2 = [12.584, 2.0644, 2.095]
    beacon3 = [0.7796, 3.8653, 2.899]
    beacon4 = [5.104, 6.6205, 2.123]
    phone_pos = [random.uniform(3,10), random.uniform(3,10), 1.35]
    #calculate the range of the phone from each beacon
    pos = [dist(beacon1, phone_pos)+random.uniform(-0.1,0.1), dist(beacon2, phone_pos)+random.uniform(-0.1,0.1), dist(beacon3, phone_pos)+random.uniform(-0.1,0.1), dist(beacon4, phone_pos)+random.uniform(-0.1,0.1)]
    time = 0.3
    walk = [[0, pos[0], 0],[1, pos[1], 0.1],[2, pos[2], 0.2],[3, pos[3], 0.3]]


    for x in range(100): #simulate 100 readings from each beacon
        for y in range(4):
            time+=random.uniform(0.08,0.12) #simuatled time between readings
            phone_pos = [phone_pos[0]+random.uniform(-.5,.5), phone_pos[1]+random.uniform(-.5,.5), 1.35] #random phone position walk
            pos = [dist(beacon1, phone_pos)+random.uniform(-0.1,0.1), dist(beacon2, phone_pos)+random.uniform(-0.1,0.1), dist(beacon3, phone_pos)+random.uniform(-0.1,0.1), dist(beacon4, phone_pos)+random.uniform(-0.1,0.1)]
            skip = random.randrange(100) #1% chance to generate bad reading
            if skip == 1:
                pos[y] += random.randrange(10)
            skip = random.randrange(20)
            if skip != 1: #skip 5% of readings to simulate missed reading
                if pos[y] < 0.0:
                    pos[y] = 0.0
                walkNew = [y, pos[y], time]
                walk.append(walkNew)
        
    with open(path + 'ranges.csv', 'w', newline="") as myfile: #export range data file
        wr = csv.writer(myfile)
        wr.writerows(walk)

def dist(beacon, phone): # calculate distance between phone and beacon
    out = m.sqrt(m.pow(beacon[0]-phone[0],2)+m.pow(beacon[1]-phone[1],2)+m.pow(beacon[2]-phone[2],2))
    return out

if __name__ == '__main__': #run gridSolver code
    main()
    path = os.getcwd() + "/"
    data = gridSolver.gridSolver(path)
    data.range_grid()
    data.localize(path)
