from PIL import Image
import logging
import time, queue
import threading
from base_image_handler import BaseImageHandler

logging.basicConfig(level=logging.INFO, filename="logfile_task_A.log", filemode='w')

class Task_A(BaseImageHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO, filename="logfile_task_A.log", filemode='w')
        self.counter = 0
        self.threshold = 100
        self.matrix = [[0] * self.height for i in range(self.width)]
        self.resultMatrix = [[True] * self.height for i in range(self.width)]

    def getBinaryMatrixFromImageInThread(self, lineQueue):
        while True:
            try: line = lineQueue.get_nowait()
            except queue.Empty: break
            else:
                for j in range(self.height):
                    self.matrix[line][j] = 1 if int(sum(self.pixels[line, j]) / (3 * self.threshold)) else 0

    def squareErosionInThread(self, binQueue, postProcQueue):
        step = 1
        structElement = [i - step for i in range(step * 2 + 1)]
        while True:
            try: line = binQueue.get_nowait()
            except queue.Empty: break
            else:
                for j in range(self.height):
                    iList = [line + elem for elem in structElement if (line + elem < self.width or line + elem < 0)]
                    jList = [j + elem for elem in structElement if (j + elem < self.height or j + elem < 0)]
                    for iStr in iList:
                        for jStr in jList:
                            if self.matrix[iStr][jStr] == 0:
                                self.resultMatrix[line][j] = False
                                break
                postProcQueue.put(line)

    def binaryMatrixToImageInThread(self, postProcQueue, endEvent):
        while not endEvent.is_set():
            try:
                line = postProcQueue.get(block=False)
                for j in range(self.height):
                    self.resultPixels[line, j] = (255, 255, 255) if self.resultMatrix[line][j] else (0, 0, 0)
                postProcQueue.task_done()
            except: continue

    def processImage(self, thr_count=1):
        thread_list = list()
        lineQueue = queue.Queue()
        postProcQueue = queue.Queue()

        for thr_num in range(thr_count):
            thread_list.append(threading.Thread(target=self.getBinaryMatrixFromImageInThread, args=(lineQueue,),
                                                name=f'bin-thr-{str(thr_num)}'))
        for i in range(self.width): lineQueue.put(i)
        for t in thread_list: t.start()
        for t in thread_list: t.join()
        thread_list = list()

        for thr_num in range(thr_count):
            thread_list.append(threading.Thread(target=self.squareErosionInThread, args=(lineQueue, postProcQueue,),
                                                name=f'erosion-thr-{str(thr_num)}'))
        for i in range(self.width): lineQueue.put(i)
        for t in thread_list: t.start()

        stopEvent = threading.Event()
        thread_list_2 = list()
        for thr_num in range(thr_count):
            thread_list_2.append(threading.Thread(target=self.binaryMatrixToImageInThread, args=(postProcQueue, stopEvent,),
                                                  name=f'postProc-thr-{str(thr_num)}'))
        for thr in thread_list_2: thr.start()
        for thr in thread_list: thr.join()
        postProcQueue.join()
        stopEvent.set()
