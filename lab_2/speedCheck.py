import logging, time

def checkSpeedOfFunc(func, iterations=1, *args, **kwargs):
    averageTime = time.time()
    for i in range(iterations): func(*args, **kwargs)
    averageTime = time.time() - averageTime

    logging.info(f"Среднее время: " + str(round(averageTime / iterations, 7)) +
                 f"; Количество потоков: {str(kwargs['thr_count'])}")

