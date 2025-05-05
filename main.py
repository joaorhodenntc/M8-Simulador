from config_loader import load_config
from simulator import Simulator

def main():
    config = load_config("model.yml")
    if not config:
        return

    # Atribuir conexões às filas
    for queue in config.queues.values():
        for connection in config.network:
            if queue.get_name() == connection.get_source():
                queue.get_connections().append(connection)
        queue.get_connections().sort(key=lambda c: c.get_probability())

    queues = list(config.queues.values())
    arrivals = config.events
    rounds = config.rndnumbers_per_seed

    simulator = Simulator()
    simulator.start(queues, arrivals, rounds)

if __name__ == "__main__":
    main()
