# from  imageProcessing import Task_A
from filterImage_B import Task_B
from task_C import ThreadingClusterizer, BaseExcelWorker


if __name__ == '__main__':
    worker = BaseExcelWorker()
    worker.readFile("BD-Patients.csv")
    clusterizer = ThreadingClusterizer(worker.readDataInFrame(("Creatinine_mean", "HCO3_mean")))
    clusterizer.clusterization(thread_count=2, clusterCount=4)



    # print(clusterizer.getClusterContent())
    data = {}
    for i, cluster in enumerate(clusterizer.getClusterContent()):


        for key in cluster[0].keys():
            data[key+"-"+str(i)] = []
        for item in cluster:
            for key in item.keys():
                data[key+"-"+str(i)].append(item)

    print(data.keys())
    worker.writeInFile(fileName="result", data=data)