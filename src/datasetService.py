from csv import reader
from os import getenv

def createDataset():
    return True


def getColumn(colNum: int, datasetPath: str):

    colData = []
    with open(datasetPath) as datasetFile:
        dataset = reader(datasetFile, delimiter=",")
        lineCount = 0

        for i in dataset:
            if (lineCount > 0):
                colData.append(i[colNum])

            lineCount += 1
    
    return colData
