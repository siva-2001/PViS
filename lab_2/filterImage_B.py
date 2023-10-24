from PIL import Image
import logging
import time
import threading


class Task_B():
    def __init__(self, imageName):
        logging.basicConfig(level=logging.INFO, filename="logfile_task_B.log", filemode='w')
        self.image = Image.open(imageName)
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.matrix = [[0] * self.height for i in range(self.width)]
        self.resultMatrix = [[1] * self.height for i in range(self.width)]
        self.resultImage = Image.new("RGB", (self.width, self.height))
        self.resultPixels = self.resultImage.load()