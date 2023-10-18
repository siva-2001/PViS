import pandas, math, logging, random, threading


class BaseExcelWorker():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="logfile_task_B.log", filemode='w')

    def readFile(self, filePath):
        if filePath.split(".")[-1] == "csv" : self.table_data = pandas.read_csv(filePath)
        elif filePath.split(".")[-1] in ["xlsx", "xls"] : self.table_data = pandas.read_excel(filePath)



    def readDataInFrame(self, cols):
        self.dataList = list()
        for i in range(len(self.table_data)):
            record = {}
            for col in cols: record[col] = self.getValueFromFrame(i, col)
            self.dataList.append(record)
        return self.dataList

    def getValueFromFrame(self, row, col):
        # if row >= len(self.table_data): raise Exception
        # if col_name not in self.table_data.columns: raise Exception
        return self.table_data.at[row, col]

    def writeInFile(self, data, fileName):
        # input : {
        #     "first_col": [4, 5, 7, 3],
        #     "second_col": [4, 5, 7, 3],
        # }
        self.new_table_data = pandas.DataFrame()
        i = 0
        for key in data.keys():
            self.new_table_data.at[0, i] = key
            for j in range(len(data[key])): self.new_table_data.at[j+1, i] = data[key][j]
            i += 1
        # print(self.new_table_data)
        self.new_table_data.to_excel(fileName+".xlsx", index=False)




class ThreadingClusterizer():
    def __init__(self, data):
        self.data, self.dataSize, self.dataDimension, self.keys, = data, len(data), len(data[0]), data[0].keys()
        self.clustersContent = None

    def createCluster(self):
        dictionary = dict()
        for key in self.keys: dictionary[key] = random.random()
        return dictionary
    def clusterization(self, clusterCount, thread_count=1):
        self.thread_count, self.clusterCount = thread_count, clusterCount
        self.clustersContent = [[] for k in range(self.clusterCount)]
        self.clusters = [self.createCluster() for k in range(self.clusterCount)]
        self.normalizeParams()

        iteration = 0
        while(not self.checkAccuracyAchieve()):
            iteration += 1
            self.distributeClusterContent()
            self.reCalculateClustersCenters()
            # self.printData()
        # print(iteration)


    def getClusterContent(self):
        self.distributeClusterContent()
        item_count = 0
        for cont in self.clustersContent: item_count += len(cont)
        # print(item_count)

        return self.clustersContent



    def checkAccuracyAchieve(self):
        try:
            for i in range(self.clusterCount):
                for key in self.keys:
                    if(abs(self.clusters[i][key] - self.previousCenters[i][key])) > 0.01: return False
            return True
        except: return False

    def distributeClusterContent(self):
        def getEuclideanDistance(item, clusterCenter):
            sumOfSquare = 0
            for key in self.keys:
                sumOfSquare += pow(item[key] - clusterCenter[key], 2)
            return pow(sumOfSquare, 0.5)

        for item in self.data:
            distanceList = [getEuclideanDistance(item, center) for center in self.clusters]
            min_ind = distanceList.index(min(distanceList))
            self.clustersContent[min_ind].append(item)



    def reCalculateClustersCenters(self):
        self.previousCenters = self.clusters.copy()
        for clusterInd, clusterContent in enumerate(self.clustersContent):
            newClusterCenterDict = dict()
            for key in self.keys: newClusterCenterDict[key] = 0
            for item in clusterContent:
                for key in self.keys : newClusterCenterDict[key] += item[key]
            for key in self.keys : newClusterCenterDict[key] = newClusterCenterDict[key] / len(clusterContent)
            self.clusters[clusterInd] = newClusterCenterDict
        self.clustersContent = [[] for k in range(self.clusterCount)]


    def normalizeParams(self):
        minMaxValuesOfParams = {}
        for key in self.data[0].keys():
            paramList = [param[key] for param in self.data]
            minMaxValuesOfParams[key] = {"min":min(paramList), "max":max(paramList)}
        for i in range(self.dataSize):
            for key in minMaxValuesOfParams.keys():
                try:
                    if math.isnan(self.data[i][key]): self.data[i] = None
                    else: self.data[i][key] = (minMaxValuesOfParams[key]["max"] - self.data[i][key]) / \
                                              (minMaxValuesOfParams[key]["max"] - (minMaxValuesOfParams[key]["min"]))
                except: continue
        self.data = [val for val in self.data if val is not None]
        self.dataSize = len(self.data)

    def printData(self):
        print(self.clusters)
        print(self.previousCenters, end="\n\n")

# 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
# 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
# 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