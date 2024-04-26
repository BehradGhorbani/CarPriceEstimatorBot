from csv import reader, writer
from os import getenv
from utils.requestService import getResponse

def createDataset(datasetPath):
    currentPage = 1
    pageCount = int(getenv('CRAWL_PAGE_COUNT'))
    endpoint = getenv('DATA_SOURCE_ENDPOINT') + '/car_listing?page='

    with open (datasetPath, 'w') as datasetFile:
        dataset = writer(datasetFile, delimiter=',')
        dataset.writerow(['type', 'date', 'price'])

        for i in range(1, pageCount):
            response = getResponse(f'{endpoint}{currentPage}')

            for data in response['results']:
                carType = data['car_properties']['brand']['title_en'] + ' ' + data['car_properties']['model']['title_en']
                carDate = data['car_properties']['year']
                carPrice = data['price']

                dataset.writerow([carType, carDate, carPrice])

            currentPage += 1
            print(f'{endpoint}{currentPage}')

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
