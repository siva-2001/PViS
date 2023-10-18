from PIL import Image
import logging
import time
import threading
from base_image_handler import BaseImageHandler

logging.basicConfig(level=logging.INFO, filename="logfile_task_A.log", filemode='w')


class Task_A(BaseImageHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO, filename="logfile_task_A.log", filemode='w')
    def getBinaryMatrixFromImageInThread(self, start, end):
        self.matrix = [[0] * self.height for i in range(self.width)]
        threshold = 100
        for i in range(start, end):
            for j in range(self.height):
                self.matrix[i][j] = 1 if int(sum(self.pixels[i, j]) / (3 * threshold)) else 0

    def squareErosionInThread(self, start, end, step=1):
        structElement = [i - step for i in range(step * 2 + 1)]
        self.resultMatrix = [[1] * self.height for i in range(self.width)]

        for i in range(start, end):
            for j in range(self.height):
                iList = [i + elem for elem in structElement if (i + elem < self.width or i + elem < 0)]
                jList = [j + elem for elem in structElement if (j + elem < self.height or j + elem < 0)]
                for iStr in iList:
                    for jStr in jList:
                        if self.matrix[iStr][jStr] == 0:
                            self.resultMatrix[i][j] = 0
                            break

    def binaryMatrixToImageInThread(self, start, end):
        for i in range(start, end):
            for j in range(self.height):
                self.resultPixels[i, j] = (255, 255, 255) if self.resultMatrix[i][j] else (0, 0, 0)

    def threadProcess(self, start, end):
        self.getBinaryMatrixFromImageInThread(start, end)
        self.squareErosionInThread(start, end)
        self.binaryMatrixToImageInThread(start, end)
        self.saveResultImage(name="result")
        print(f"{threading.current_thread().name} is finish\n", end="")
