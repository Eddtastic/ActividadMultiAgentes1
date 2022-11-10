from CleanerModel import CleanerModel
import time

def cleanerbots():
    model = CleanerModel(20, 6, 6, 0.30)
    maxTime = 40
    model.startTime = time.time()

    for i in range(maxTime):
        model.step()
        print("limpieza: ", str(round(model.dirtyCellRatio() * 100, 2)) + "%")
    print(model.counter())
    model.endTime = time.time()
    print("Tiempo de corrido: ")
    print(model.programTime())
