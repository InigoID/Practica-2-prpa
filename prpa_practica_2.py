import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value


SOUTH = "south"
NORTH = "north"

NCARS = 10
NPEOPLE = 10


class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.people_waiting = Condition(self.mutex)
        self.people_in_bridge = Value('i', 0)
        self.cars_in_bridge = Value('i', 0)

    def wants_enter(self, direction, is_person=False):
        self.mutex.acquire()
        if is_person:
            while self.cars_in_bridge.value > 0 or self.people_in_bridge.value > 0:
                self.people_waiting.wait()
        else:
            while self.people_in_bridge.value > 0:
                self.people_waiting.wait()
        if is_person:
            self.people_in_bridge.value += 1
        else:
            self.cars_in_bridge.value += 1
        self.mutex.release()

    def leaves_bridge(self, direction, is_person=False):
        self.mutex.acquire()
        if is_person:
            self.people_in_bridge.value -= 1
        else:
            self.cars_in_bridge.value -= 1
        self.people_waiting.notify()
        self.mutex.release()


def delay(n=3):
    time.sleep(random.random()*n)


def car(cid, direction, monitor):
    print(f"car {cid} direction {direction} created")
    delay(6)
    print(f"car {cid} heading {direction} wants to enter")
    monitor.wants_enter(direction)
    print(f"car {cid} heading {direction} enters the bridge")
    delay(3)
    print(f"car {cid} heading {direction} leaving the bridge")
    monitor.leaves_bridge(direction)
    print(f"car {cid} heading {direction} out of the bridge")


def person(pid, monitor):
    print(f"person {pid} created")
    delay(6)
    print(f"person {pid} wants to enter")
    monitor.wants_enter(NORTH, is_person=True)
    print(f"person {pid} enters the bridge")
    monitor.leaves_bridge(NORTH, is_person=True)
    print(f"person {pid} out of the bridge")


def main():
    monitor = Monitor()
    processes = []
    for i in range(NCARS):
        direction = NORTH if random.randint(0, 1) == 1 else SOUTH
        p = Process(target=car, args=(i+1, direction, monitor))
        processes.append(p)
    for i in range(NPEOPLE):
        p = Process(target=person, args=(i+1, monitor))
        processes.append(p)
    random.shuffle(processes)
    for p in processes:
        p.start()
        time.sleep(random.expovariate(1/0.5))
    for p in processes:
        p.join()
    print("simulation ended")


if __name__ == '__main__':
    main()
