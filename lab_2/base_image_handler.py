from PIL import Image
import time, logging, threading
import queue

class BaseImageHandler():
    def __init__(self, imageName):
        self.image = Image.open(imageName)
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.resultImage = Image.new("RGB", (self.width, self.height))
        self.resultPixels = self.resultImage.load()

    def convertResultPixelsToBase(self): self.pixels = self.resultPixels

    def checkSpeedOfFunc(self, *args, **kwargs):
        iterations = 1
        averageTime = time.time()
        for i in range(iterations): self.processImage(*args, **kwargs)
        averageTime = time.time() - averageTime

        logging.info(f"Среднее время: " + str(round(averageTime / iterations, 4)))
        logging.info(f"Threads count: {str(kwargs['thread_numbers'])}")
        logging.info(f"Iterations count: {iterations}")
        logging.info(f"Размер: {self.height} Х {self.width} = {self.width * self.height}тыс. пикселей\n")

    def saveResultImage(self, name="result"):
        self.resultImage.save(name + ".jpg", "JPEG")