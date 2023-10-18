from PIL import Image
import time, logging, threading

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

    def processImage(self, thread_numbers=1, vector=(0,0)):
        thread_list = list()
        for t_num in range(thread_numbers):
            start, end = int(t_num * (self.width / thread_numbers)), int((1 + t_num) * (self.width / thread_numbers))
            thread_list.append(
                threading.Thread(target=self.threadProcess, args=(start, end, vector), name=f'thr-{str(t_num)}'))
        for t in thread_list: t.start()
        for t in thread_list: t.join()