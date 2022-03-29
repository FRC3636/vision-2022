import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]


def connection_listener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()


class Network:
    __nt = 0

    def __init__(self):
        NetworkTables.initialize('10.36.36.2')
        NetworkTables.addConnectionListener(connection_listener, True)
        with cond:
            print("Waiting")
            if not notified[0]:
                cond.wait()

        print("Connected!")
        self.__nt = NetworkTables.getTable('Camera')

    def update(self, distance, angle):
        if not NetworkTables.isConnected():
            print("Disconnected")
        self.__nt.putNumber('Distance', distance)
        self.__nt.putNumber('Angle', angle)
