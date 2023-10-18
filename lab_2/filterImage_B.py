import threading
import logging
from base_image_handler import BaseImageHandler



class Task_B(BaseImageHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO, filename="logfile_task_B.log", filemode='w')

    def movePixelOnVectorInThread(self, start, end, vector):
        for i in range(start, end):
            if (i + vector[0]) >= self.width or (i + vector[0]) < 0: continue
            for j in range(self.height):
                if (j + vector[1]) >= self.height or (j + vector[1]) < 0: continue
                self.resultPixels[i + vector[0], j + vector[1]] = self.pixels[i, j]

    def replaceUnchangedPixels(self, start, end):
        for i in range(start, end):
            for j in range(self.height):
                if self.pixels[i, j] == self.resultPixels[i, j]: self.resultPixels[i, j] = (187, 38, 73)

    def applyFilter(self, start, end):
        filterMatrix, div = [        # размерность матрицы должна быть равна в обоих направлениях
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 3, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ], 25
        filterMatrixSize = len(filterMatrix)

        for i in range(start, end):
            if i + int(filterMatrixSize / 2) >= self.width or i - int(filterMatrixSize / 2) < 0: continue
            for j in range(self.height):
                if j + int(filterMatrixSize / 2) >= self.height or i - int(filterMatrixSize / 2) < 0: continue
                redComponent, greenComponent, blueComponent = 0, 0, 0
                for fi in range(filterMatrixSize):
                    for fj in range(filterMatrixSize):
                        checkPix = self.pixels[i + fi - int(filterMatrixSize / 2), j + fj - int(filterMatrixSize / 2)]
                        redComponent += checkPix[0] * filterMatrix[fi][fj]
                        greenComponent += checkPix[1] * filterMatrix[fi][fj]
                        blueComponent += checkPix[2] * filterMatrix[fi][fj]
                self.resultPixels[i,j] = (int(redComponent/div), int(greenComponent/div), int(blueComponent/div))


    def threadProcess(self, start, end, vector):
        self.movePixelOnVectorInThread(start, end, vector)
        self.replaceUnchangedPixels(start, end)
        self.convertResultPixelsToBase()
        self.applyFilter(start, end)
        self.saveResultImage("result_B")
        print(f"{threading.current_thread().name} is finish\n", end="")

