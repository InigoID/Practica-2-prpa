import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 100
NPED = 10
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.north_cars = Value('i', 0)
        self.south_cars = Value('i', 0)
        self.waiting_north = Value('i', 0)
        self.waiting_south = Value('i', 0)
        self.pedestrians = Value('i', 0)
        self.waiting_pedestrians = Value('i', 0)
        self.bridge = Condition(self.mutex)

    def wants_enter_car(self, direction: int) -> None:
        with self.bridge:
            if direction == NORTH:
                self.waiting_north.value += 1
                self.bridge.wait_for(lambda: self.south_cars.value == 0 and self.pedestrians.value == 0)
                self.waiting_north.value -= 1
                self.north_cars.value += 1
            else:
                self.waiting_south.value += 1
                self.bridge.wait_for(lambda: self.north_cars.value == 0 and self.pedestrians.value == 0)
                self.waiting_south.value -= 1
                self.south_cars.value += 1

    def leaves_car(self, direction: int) -> None:
        with self.bridge:
            if direction == NORTH:
                self.north_cars.value -= 1
                if self.north_cars.value == 0:
                    self.bridge.notify_all()
            else:
                self.south_cars.value -= 1
                if self.south_cars.value == 0:
                    self.bridge.notify_all()

    def wants_enter_pedestrian(self) -> None:
        with self.bridge:
            self.waiting_pedestrians.value += 1
            self.bridge.wait_for(lambda: self.north_cars.value == 0 and self.south_cars.value == 0)
            self.waiting_pedestrians.value -= 1
            self.pedestrians.value += 1

    def leaves_pedestrian(self) -> None:
        with self.bridge:
            self.pedestrians.value -= 1
            self.bridge.notify_all()


def delay_car_north() -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1]))

def delay_car_south() -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_CARS[0], TIME_IN_BRIDGE_CARS[1]))

def delay_pedestrian() -> None:
    time.sleep(random.uniform(TIME_IN_BRIDGE_PEDESTRIAN[0], TIME_IN_BRIDGE_PEDESTRIAN[1]))

def car(cid: int, direction: int, monitor: Monitor) -> None:
    print(f"car {cid} heading {direction} wants to enter.")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge.")
    if direction == NORTH:
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge.")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge.")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter.")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge.")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge.")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge.")

def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1 / TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1 / time_cars))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()

if __name__ == '__main__':
    main()

