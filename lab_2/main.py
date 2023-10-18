# from  imageProcessing import Task_A
from filterImage_B import Task_B
from task_C import ThreadingClusterizer, BaseExcelWorker


if __name__ == '__main__':
    worker = BaseExcelWorker()
    worker.readFile("BD-Patients.csv")
    clusterizer = ThreadingClusterizer(worker.readDataInFrame(("Creatinine_mean", "HCO3_mean")))
    clusterizer.clusterization(thread_count=2, clusterCount=4)

    print(clusterizer.getClusterContent())
    worker.writeInFile()