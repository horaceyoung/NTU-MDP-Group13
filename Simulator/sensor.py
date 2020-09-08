import map
import configurations

class Sensor:
    def __init__(self, lowerRange, upperRange, row, col, dir, id):
        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.sensorPosRow = row
        self.sensorPosCol = col
        self.sensorDir = dir
        self.id = id

    def setSensor(self,row,col,dir):
        self.sensorPosRow = row
        self.sensorPosCol = col
        self.sensorDir = dir

    def sense(self, exploredMap, realMap):
        if(self.sensorDir == configurations.Direction.NORTH):
            return self.getSensorVal(exploredMap, realMap, 1, 0)
        elif(self.sensorDir == configurations.Direction.EAST):
            return self.getSensorVal(exploredMap, realMap, 0, 1)
        elif(self.sensorDir == configurations.Direction.SOUTH):
            return self.getSensorVal(exploredMap, realMap, -1, 0)
        elif(self.sensorDir == configurations.Direction.WEST):
            return self.getSensorVal(exploredMap, realMap, 0, -1)

        return -1

    def getSensorVal(self,exploredMap,realMap, rowInc, colInc):
        if(self.lowerRange > 1):
            for i in range(self.lowerRange - 1):
                row = self.sensorPosRow + (rowInc*(i+1))
                col = self.sensorPosCol + (colInc*(i+1))

                if(not exploredMap.checkValidCoordinates(row,col)):
                    return i+1
                if(realMap.getCell(row,col).isObstacle):
                    return i+1

        for i in range(self.lowerRange, self.upperRange+1, 1):
            row = self.sensorPosRow + (rowInc * i)
            col = self.sensorPosCol + (colInc * i)

            if(not exploredMap.checkValidCoordinates(row,col)):
                return i

            exploredMap.getCell(row,col).setIsExplored(True)
            if(realMap.getCell(row,col).isObstacle):
                exploredMap.setObstacleCell(row,col, True)
                return i
        return -1


    def senseReal(self,exploredMap,sensorVal):
        if(self.sensorDir == configurations.Direction.NORTH):
            self.processSensorVal(exploredMap, sensorVal, 1,0)
        elif(self.sensorDir == configurations.Direction.EAST):
            self.processSensorVal(exploredMap, sensorVal, 0,1)
        elif(self.sensorDir == configurations.Direction.SOUTH):
            self.processSensorVal(exploredMap, sensorVal, -1,0)
        elif(self.sensorDir == configurations.Direction.WEST):
            self.processSensorVal(exploredMap, sensorVal, 0,-1)



    def processSensorVal(self,exploredMap,sensorVal,rowInc,colInc):
        if(sensorVal == 0):
            return None

        for i in range(1,self.lowerRange,1):
            row = self.sensorPosRow + (rowInc*i)
            col = self.sensorPosCol + (colInc*i)

            if(not exploredMap.checkValidCoordinates(row,col)):
                return None
            if(exploredMap.getCell(row,col).isObstacle):
                return None

        for i in range(self.lowerRange, self.upperRange+1, 1):
            row = self.sensorPosRow + (rowInc*i)
            col = self.sensorPosCol = (colInc*i)

            if(not exploredMap.checkValidCoordinates(row,col)):
                continue
            exploredMap.getCell(row,col).setIsExplored(True)
            if(sensorVal == i):
                exploredMap.setObstacleCell(row,col,True)
                break

            if(exploredMap.getCell(row,col).isObstacle):
                if(id=="SRFL" or id=="SRFC" or id=="SRFR"):
                    exploredMap.setObstacleCell(row,col,False)
                else:
                    break
