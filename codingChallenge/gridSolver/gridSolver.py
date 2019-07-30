import numpy as np
import os
import multiprocessing
import csv


class gridSolver:
    def __init__(self, path):
        # loading the data files from path
        self.grid = np.genfromtxt(path + "grid.csv", delimiter=',').astype(int)
        self.r = np.genfromtxt(path + "ranges.csv", delimiter=',').astype(float)
        self.beacons = np.genfromtxt(path + "beacons.csv", delimiter=',').astype(float)

        # setup distance grid indices
        self.dgrid = np.indices((self.grid.shape[0] - 1, self.grid.shape[1] - 1)) + 0.5
        self.dgridz = np.ones((self.grid.shape[0] - 1, self.grid.shape[1] - 1)) * 1.35

        # preallocate distance array
        self.d = np.zeros((self.dgrid.shape[1], self.dgrid.shape[2], self.beacons.shape[0]))

        for x in range(self.beacons.shape[0]):
            self.d[:, :, x] += np.array(np.sqrt(
                np.power(self.dgrid[0] - self.beacons[x][0], 2) + np.power(self.dgrid[1] - self.beacons[x][1],
                                                                           2) + np.power(
                    self.dgridz - self.beacons[x][2], 2)))

    def range_grid(self):
        # arrange range data into sets
        # initialize array first 4 readings
        self.rangeSets = np.empty((1, 4))
        self.timeCheck = np.empty((1, 4))
        for x in range(4):
            self.rangeSets[0][int(self.r[x][0])] = self.r[x][1]
            self.timeCheck[0][int(self.r[x][0])] = self.r[x][2]

        # create every possible set
        for x in range(4, self.r.shape[0]):
            self.rangeSets = np.append(self.rangeSets, [self.rangeSets[self.rangeSets.shape[0] - 1][:]], axis=0)
            self.timeCheck = np.append(self.timeCheck, [self.timeCheck[self.timeCheck.shape[0] - 1][:]], axis=0)
            self.timeCheck[self.timeCheck.shape[0] - 1, int(self.r[x][0])] = self.r[x][2]
            self.rangeSets[self.rangeSets.shape[0] - 1, int(self.r[x][0])] = self.r[x][1]

        # check for illegal sets (time difference >0.7)
        bad = np.argwhere(np.amax(self.timeCheck, axis=1) - np.amin(self.timeCheck, axis=1) > 0.7)

        # remove oldest value to see if a legal set can be made of three beacons
        for x in np.nditer(bad):
            test = self.timeCheck[int(x)][:]
            rangeTest = self.rangeSets[int(x)][:]
            rangeTest[np.nanargmin(test)] = None
            test[np.nanargmin(test)] = None
            if np.nanmax(test, axis=0) - np.nanmin(test, axis=0) < 0.7:
                self.timeCheck[int(x)][:] = test
                self.rangeSets[int(x)][:] = rangeTest

        # delete sets that are still illegal
        bad2 = np.argwhere(np.nanmax(self.timeCheck, axis=1) - np.nanmin(self.timeCheck, axis=1) > 0.7)
        bad2 = bad2.tolist()
        for x in reversed(bad2):
            self.rangeSets = np.delete(self.rangeSets, int(x[0]), 0)
            self.timeCheck = np.delete(self.timeCheck, int(x[0]), 0)

    def multi_process(self, z):
        # initialize dr matrix
        dr = np.zeros([self.d.shape[0], self.d.shape[1]])
        for x in range(self.d.shape[1]):
            for y in range(self.d.shape[0]):
                dr[y][x] = np.nansum(np.abs(self.d[y][x][:] - self.rangeSets[z][:])) / (
                    np.count_nonzero(~np.isnan(self.rangeSets[z][:])))
        if np.min(dr) < 0.5:
            ind = np.unravel_index(np.argmin(dr, axis=None), dr.shape)
            dataOut = [ind[0] + 0.5, ind[1] + 0.5, 1.35, np.nanmin(self.timeCheck[z])]
        else:
            dataOut = []
        return dataOut

    def localize(self): #uses multiprocessing to process grid localization
        pool = multiprocessing.Pool()
        dataOut = pool.map(self.multi_process, range(self.rangeSets.shape[0]))
        pool.close()

        dataOut2 = [x for x in dataOut if x != []]
        with open(path + 'outFile.csv', 'w', newline="") as myfile:
            wr = csv.writer(myfile)
            wr.writerows(dataOut2)


if __name__ == '__main__':
    path = os.getcwd() + "/"
    data = gridSolver(path)
    data.range_grid()
    data.localize()






