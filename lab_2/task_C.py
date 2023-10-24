import pandas, math, logging, random, threading
import queue

class BaseExcelWorker():
    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="logfile_task_C.log", filemode='w')

    def readFile(self, filePath):
        if filePath.split(".")[-1] == "csv" : self.table_data = pandas.read_csv(filePath)
        elif filePath.split(".")[-1] in ["xlsx", "xls"] : self.table_data = pandas.read_excel(filePath)


    def readDataInFrame(self, cols, rows_num=None):
        if not rows_num: rows_num = len(self.table_data)
        self.dataList = list()
        for i in range(rows_num):
            record = {}
            for col in cols: record[col] = self.table_data.at[i, col]
            self.dataList.append(record)
        return self.dataList

    def writeInFile(self, data, fileName):
        self.new_table_data = pandas.DataFrame(data)
        self.new_table_data.to_excel(fileName+".xlsx", index=False)

class Clusterizer():
    def __init__(self, data):
        logging.basicConfig(level=logging.INFO, filename="logfile_task_C.log", filemode='w')
        self.data, self.dataSize, self.dataDimension, self.keys, = data, len(data), len(data[0]), list(data[0].keys())
        self.clustersContent = None

    def clusterization(self, clusterCount, thread_count=1):
        def createCluster():
            dictionary = dict()
            for key in self.keys: dictionary[key] = random.random()
            return dictionary

        while True:
            try:

                self.thread_count, self.clusterCount = thread_count, clusterCount
                self.clustersContent = [[] for k in range(self.clusterCount)]
                self.clusters = [createCluster() for k in range(self.clusterCount)]
                self.normalizeParams()
                while(not self.checkAccuracyAchieve()):
                    self.distributeClusterContent()
                    self.reCalculateClustersCenters()
                break
            except ZeroDivisionError: continue
        self.distributeClusterContent()

    def getClusterOfPatientsInDictForExcel(self):
        data = dict()
        colNamesList = [list(self.keys)[0]]
        for i in range(self.clusterCount): colNamesList.append(list(self.keys)[1]+f"(Кластер {i+1})")
        for i in range(self.clusterCount): colNamesList.append(list(self.keys)[1]+f"(Центр кластера {i+1})")
        for colName in colNamesList: data[colName] = ['' for i in range(self.dataSize + self.clusterCount)]

        row_ind = 0
        for i, content in enumerate(self.clustersContent):
            for item in content:
                data[self.keys[0]][row_ind] = item[self.keys[0]]
                data[self.keys[1]+f"(Кластер {i+1})"][row_ind] = item[self.keys[1]]
                row_ind+=1
        for i in range(self.clusterCount):
            data[list(self.keys)[0]][row_ind] = self.clusters[i][list(self.keys)[0]]
            data[list(self.keys)[1]+f"(Центр кластера {i+1})"][row_ind] = self.clusters[i][list(self.keys)[1]]
            row_ind += 1
        return data

    def getClustersContent(self):
        return self.clustersContent

    def checkAccuracyAchieve(self):
        try:
            for i in range(self.clusterCount):
                for key in self.keys:
                    if(abs(self.clusters[i][key] - self.previousCenters[i][key])) > 0.01: return False
            return True
        except: return False

    def getEuclideanDistance(self, point1, point2):
        key1 = self.keys[0]
        key2 = self.keys[1]
        # return pow(pow(point1[self.keys[0]] - point2[self.keys[0]], 2) +
        #            pow(point1[self.keys[1]] - point2[self.keys[1]], 2), 0.5)
        return pow(pow(point1[key1] - point2[key1], 2) +
                   pow(point1[key2] - point2[key2], 2), 0.5)
        # sumOfSquare = 0
        # for key in self.keys:
        #     sumOfSquare += pow(point1[key] - point2[key], 2)
        # return pow(sumOfSquare, 0.5)

    def distributeClusterContent(self):
        for item in self.data:
            distanceList = [self.getEuclideanDistance(item, center) for center in self.clusters]
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
            minMaxValuesOfParams[key] = {"min":0.0, "max":max(paramList)}
        for i in range(self.dataSize):
            for key in minMaxValuesOfParams.keys():
                try:
                    if math.isnan(self.data[i][key]): self.data[i] = None
                    else: self.data[i][key] = (minMaxValuesOfParams[key]["max"] - self.data[i][key]) / \
                                              (minMaxValuesOfParams[key]["max"] - (minMaxValuesOfParams[key]["min"]))
                except: continue
        self.data = [val for val in self.data if val is not None]
        self.dataSize = len(self.data)

class DannIndexCalculator():
    def getEuclideanDistance(self, point1, point2):
        return pow(pow(point1[self.keys[0]] - point2[self.keys[0]], 2) +
                   pow(point1[self.keys[1]] - point2[self.keys[1]], 2), 0.5)

    def getDannIndex(self, clustersContent, thr_count=4):
        self.keys = list(clustersContent[0][0].keys())
        self.maxDiam = 0
        self.minDist = self.getEuclideanDistance(clustersContent[0][0], clustersContent[0][1])


        diamTQueue = queue.Queue()
        distTQueue = queue.Queue()

        thread_list = list()
        for thr_i in range(int((thr_count+1)/2)):
            thread_list.append(
                threading.Thread(target=self.threadCalcMaxDiam, args=(diamTQueue,), name="diam-thr-" + str(thr_i)))
            thread_list.append(
                threading.Thread(target=self.threadCalcMinDistance, args=(distTQueue,), name="diam-thr-" + str(thr_i)))
        for thr in thread_list: thr.start()
        print(threading.enumerate())



        for cluster in clustersContent:
            for i in range(thr_count*3):
                diamTQueue.put(
                    (cluster[int(i * (len(cluster) / thr_count)):int((i + 1) * (len(cluster) / thr_count))], cluster)
                )
            for cluster2 in clustersContent:
                if cluster != cluster2:
                    distTQueue.put(
                        (cluster2[int(i * (len(cluster) / thr_count)):int((i + 1) * (len(cluster) / thr_count))], cluster)
                    )

        for thr in thread_list: thr.join()

        print(self.minDist / self.maxDiam)
        return self.minDist / self.maxDiam


    def threadCalcMaxDiam(self, dQueue):
        task = dQueue.get()
        for item1 in task[0]:
            for item2 in task[1]:
                diam = self.getEuclideanDistance(item1, item2)
                if diam > self.maxDiam: self.maxDiam = diam

    def threadCalcMinDistance(self, distQueue):
        task = distQueue.get()
        for item1 in task[0]:
            for item2 in task[1]:
                dist = self.getEuclideanDistance(item1, item2)
                if dist < self.minDist: self.minDist = dist




# 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