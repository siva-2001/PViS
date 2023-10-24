from  imageProcessing import Task_A
from filterImage_B import Task_B
from task_C import Clusterizer, BaseExcelWorker, DannIndexCalculator
from speedCheck import checkSpeedOfFunc
import logging, threading, time
loggingPath = '/logs/'





if __name__ == '__main__':
    for name in ["image_1", "image_2", "image_3"]:
        task_a = Task_A(name+'.jpg')
        for i in range(2, 17, 2):
            checkSpeedOfFunc(task_a.processImage, thr_count=i)
            task_a.saveResultImage(name+"_result")





# if __name__ == '__main__':
#     worker = BaseExcelWorker()
#     worker.readFile("BD-Patients.csv")
#
#     data = {
#         "threads": [2, 4, 6, 8, 10, 12, 14, 16]
#     }
#     for i, row_num in enumerate([1000, 3000, 5000]):
#         clusterizer = Clusterizer(worker.readDataInFrame(("Creatinine_mean", "HCO3_mean"), rows_num=row_num))
#         dannCalculator = DannIndexCalculator()
#         for j, clusterCount in enumerate([3, 4, 5]):
#             logging.info(f"Объём данных:{row_num} ; Количество кластеров:{clusterCount}")
#             clusterizer.clusterization(clusterCount=clusterCount)
#             logging.info(f"Размерность кластеров: {[len(c) for c in clusterizer.clustersContent]}")
#
#             worker.writeInFile(fileName="clusters", data=clusterizer.getClusterOfPatientsInDictForExcel())
#
#             clustContent = clusterizer.getClustersContent()
#
#
#             data[f'vec{row_num}_clust{clusterCount}'] =\
#                 [checkSpeedOfFunc(dannCalculator.getDannIndex, thr_count=k, clustersContent=clustContent)
#                  for k in data["threads"]]
#
#             worker.writeInFile(fileName="result", data=data)
#
#
#
