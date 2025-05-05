from queue import PriorityQueue
from models import Event, EventType, Queue
import random

class Simulator:
    def __init__(self):
        self.scheduler = PriorityQueue()
        self.global_time = 0.0
        self.x = 57406

    def next_random(self):
        self.x = (4212002 * self.x + 2224621) % 429496729
        return self.x / 429496729

    def start(self, queues, arrivals, rounds):
        for event in arrivals:
            self.scheduler.put(event)
        self.global_time = 0.0

        while rounds > 0 and not self.scheduler.empty():
            event = self.scheduler.get()
            event_queue = self.find_queue_by_name(queues, event.get_queue_name())

            if event.get_type() == EventType.ARRIVAL:
                self.arrival(event, queues, event_queue)
            elif event.get_type() == EventType.EXIT:
                self.exit(event, queues, event_queue)
            else:
                target_queue = self.find_queue_by_name(queues, event.get_target_queue_name())
                self.pass_(event, queues, event_queue, target_queue)
            rounds -= 1

        # Imprimir resultados
        for queue in queues:
            print(f"\n{queue.get_name()}")
            print("State   Time(min)              Probability")
            for i, time in enumerate(queue.get_times()):
                if time != 0.0:
                    probability = (time / self.global_time * 100) if self.global_time > 0 else 0
                    print(f"{i:<7} {time:<20.2f} {probability:.2f}%")
            print(f"\nNumber of losses: {queue.get_losses()}\n")
        print(f"Global time: {self.global_time:.2f}")

    def find_queue_by_name(self, queues, name):
        for queue in queues:
            if queue.get_name() == name:
                return queue
        return None

    def draw_probability(self, queue):
        prob = random.random()
        sum_prob = 0.0
        for conn in queue.get_connections():
            sum_prob += conn.get_probability()
            if prob < sum_prob:
                return conn.get_target()
        return None

    def arrival(self, event, queues, event_queue):
        self.acc_time(event, queues)
        if event_queue.get_customers() < event_queue.get_capacity():
            event_queue.in_()
            if event_queue.get_customers() <= event_queue.get_servers():
                name_target = self.draw_probability(event_queue)
                if name_target == "exit":
                    self.schedule_exit(event_queue)
                else:
                    target_queue = self.find_queue_by_name(queues, name_target)
                    self.schedule_pass(event_queue, target_queue)
        else:
            event_queue.loss()
        self.schedule_arrival(event_queue)

    def exit(self, event, queues, event_queue):
        self.acc_time(event, queues)
        event_queue.out()
        if event_queue.get_customers() >= event_queue.get_servers():
            name_target = self.draw_probability(event_queue)
            if name_target == "exit":
                self.schedule_exit(event_queue)
            else:
                target_queue = self.find_queue_by_name(queues, name_target)
                self.schedule_pass(event_queue, target_queue)

    def pass_(self, event, queues, event_queue, target_queue):
        self.acc_time(event, queues)
        event_queue.out()
        if event_queue.get_customers() >= event_queue.get_servers():
            name_target = self.draw_probability(event_queue)
            if name_target == "exit":
                self.schedule_exit(event_queue)
            else:
                target_queue_2 = self.find_queue_by_name(queues, name_target)
                self.schedule_pass(event_queue, target_queue_2)
        if target_queue.get_customers() < target_queue.get_capacity():
            target_queue.in_()
            if target_queue.get_customers() <= target_queue.get_servers():
                name_target = self.draw_probability(target_queue)
                if name_target == "exit":
                    self.schedule_exit(target_queue)
                else:
                    target_queue_2 = self.find_queue_by_name(queues, name_target)
                    self.schedule_pass(target_queue, target_queue_2)
        else:
            target_queue.loss()

    def acc_time(self, event, queues):
        for queue in queues:
            queue.get_times()[queue.get_customers()] += event.get_time() - self.global_time
        self.global_time = event.get_time()

    def schedule_arrival(self, event_queue):
        u = event_queue.get_min_arrival() + (
            (event_queue.get_max_arrival() - event_queue.get_min_arrival()) * self.next_random()
        )
        event = Event(self.global_time + u, EventType.ARRIVAL, event_queue.get_name())
        self.scheduler.put(event)

    def schedule_exit(self, event_queue):
        u = event_queue.get_min_service() + (
            (event_queue.get_max_service() - event_queue.get_min_service()) * self.next_random()
        )
        event = Event(self.global_time + u, EventType.EXIT, event_queue.get_name())
        self.scheduler.put(event)

    def schedule_pass(self, event_queue, target_queue):
        u = event_queue.get_min_service() + (
            (event_queue.get_max_service() - event_queue.get_min_service()) * self.next_random()
        )
        event = Event(self.global_time + u, EventType.PASS, event_queue.get_name(), target_queue.get_name())
        self.scheduler.put(event)
