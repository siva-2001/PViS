import threading
import logging
import queue
from base_image_handler import BaseImageHandler



class Task_B(BaseImageHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO, filename="logfile_task_B.log", filemode='w')
        self.filterMatrix, self.div = [        # размерность матрицы должна быть равна в обоих направлениях
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 3, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ], 25
        self.filterMatrixSize = len(self.filterMatrix)

    def movePixelOnVectorInThread(self, lQueue, vector):
        while True:
            try: line = lQueue.get(block=False)
            except: break
            else:
                if (line + vector[0]) >= self.width or (line + vector[0]) < 0:
                    lQueue.task_done()
                    continue
                for j in range(self.height):
                    if (j + vector[1]) >= self.height or (j + vector[1]) < 0: continue
                    self.resultPixels[line + vector[0], j + vector[1]] = self.pixels[line, j]
                lQueue.task_done()
        print(f"{threading.current_thread().name} is finish\n", end="")

    def replaceUnchangedPixels(self, lQueue):
        while True:
            try: line = lQueue.get(block=False)
            except: break
            else:
                for j in range(self.height):
                    if self.pixels[line, j] == self.resultPixels[line, j]: self.resultPixels[line, j] = (187, 38, 73)
                lQueue.task_done()
        print(f"{threading.current_thread().name} is finish\n", end="")

    def applyFilter(self, lQueue):
        filterMatrixSize = len(self.filterMatrix)
        while True:
            try: line = lQueue.get(block=False)
            except: break
            else:
                if line + int(filterMatrixSize / 2) >= self.width or line - int(filterMatrixSize / 2) < 0:
                    lQueue.task_done()
                    continue
                for j in range(self.height):
                    if j + int(filterMatrixSize / 2) >= self.height or line - int(filterMatrixSize / 2) < 0: continue
                    redComponent, greenComponent, blueComponent = 0, 0, 0
                    for fi in range(filterMatrixSize):
                        for fj in range(filterMatrixSize):
                            checkPix = self.pixels[line + fi - int(filterMatrixSize / 2), j + fj - int(filterMatrixSize / 2)]
                            redComponent += checkPix[0] * self.filterMatrix[fi][fj]
                            greenComponent += checkPix[1] * self.filterMatrix[fi][fj]
                            blueComponent += checkPix[2] * self.filterMatrix[fi][fj]
                    self.resultPixels[line,j] = (int(redComponent/self.div), int(greenComponent/self.div), int(blueComponent/self.div))
                lQueue.task_done()
        print(f"{threading.current_thread().name} is finish\n", end="")


    def processImage(self, vector, thr_count=4):
        lineQueue = queue.Queue()

        thread_list = list()
        for thr_num in range(thr_count):
            thread_list.append(threading.Thread(target=self.movePixelOnVectorInThread, args=(lineQueue, vector,),
                                                name=f'movePix-thr-{str(thr_num)}'))
        for i in range(self.width): lineQueue.put(i)
        for t in thread_list: t.start()
        for t in thread_list: t.join()

        thread_list = list()
        for thr_num in range(thr_count):
            thread_list.append(threading.Thread(target=self.replaceUnchangedPixels, args=(lineQueue,),
                                                name=f'replace-thr-{str(thr_num)}'))
        for i in range(self.width): lineQueue.put(i)
        for t in thread_list: t.start()
        for t in thread_list: t.join()

        self.convertResultPixelsToBase()

        thread_list = list()
        for thr_num in range(thr_count):
            thread_list.append(threading.Thread(target=self.applyFilter, args=(lineQueue,),
                                                name=f'applyFilter-thr-{str(thr_num)}'))
        for i in range(self.width): lineQueue.put(i)
        for t in thread_list: t.start()
        for t in thread_list: t.join()

        self.saveResultImage("result_B")















