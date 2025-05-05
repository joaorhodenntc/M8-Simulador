from enum import Enum
import uuid

class EventType(Enum):
    ARRIVAL = "arrival"
    EXIT = "exit"
    PASS = "pass"

class Event:
    def __init__(self, time, event_type, queue_name, target_queue_name=None):
        self.time = time
        self.event_type = event_type
        self.queue_name = queue_name
        self.target_queue_name = target_queue_name

    def get_time(self):
        return self.time

    def get_type(self):
        return self.event_type

    def get_queue_name(self):
        return self.queue_name

    def get_target_queue_name(self):
        return self.target_queue_name

    def __lt__(self, other):
        return self.time < other.time

class Queue:
    def __init__(self, name, servers, capacity, min_arrival, max_arrival, min_service, max_service):
        self.name = name
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service
        self.customers = 0
        self.losses = 0
        self.connections = []
        self.times = [0.0] * (capacity + 1)

    def get_name(self):
        return self.name

    def get_servers(self):
        return self.servers

    def get_capacity(self):
        return self.capacity

    def get_min_arrival(self):
        return self.min_arrival

    def get_max_arrival(self):
        return self.max_arrival

    def get_min_service(self):
        return self.min_service

    def get_max_service(self):
        return self.max_service

    def get_customers(self):
        return self.customers

    def get_losses(self):
        return self.losses

    def get_connections(self):
        return self.connections

    def get_times(self):
        return self.times

    def in_(self):
        self.customers += 1

    def out(self):
        self.customers -= 1

    def loss(self):
        self.losses += 1

class NetworkConnection:
    def __init__(self, source, target, probability):
        self.source = source
        self.target = target
        self.probability = probability

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_probability(self):
        return self.probability

class Parameters:
    def __init__(self):
        self.events = []
        self.queues = {}
        self.network = []
        self.rndnumbers_per_seed = 0
        self.seeds = []
        self.rndnumbers = []
