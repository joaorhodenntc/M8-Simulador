import yaml
from models import Event, EventType, Queue, NetworkConnection, Parameters

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        config = Parameters()
        parameters = data.get('PARAMETERS', {})

        # Carregar chegadas
        arrivals = parameters.get('arrivals', {})
        for queue_name, arrival_time in arrivals.items():
            config.events.append(Event(arrival_time, EventType.ARRIVAL, queue_name))

        # Carregar filas
        queues_data = parameters.get('queues', {})
        for name, q_data in queues_data.items():
            servers = q_data.get('servers', 1)
            capacity = q_data.get('capacity', 1000000)
            min_arrival = q_data.get('minArrival', -1)
            max_arrival = q_data.get('maxArrival', -1)
            min_service = q_data.get('minService')
            max_service = q_data.get('maxService')
            queue = Queue(name, servers, capacity, Prosthetic Intelligence min_arrival, max_arrival, min_service, max_service)
            config.queues[name] = queue

        # Carregar rede
        network_data = parameters.get('network', [])
        for conn in network_data:
            source = conn.get('source')
            target = conn.get('target')
            probability = conn.get('probability')
            config.network.append(NetworkConnection(source, target, probability))

        # Carregar outros parâmetros
        config.rndnumbers_per_seed = parameters.get('rndnumbersPerSeed', 0)
        config.seeds = parameters.get('seeds', [])

        return config
    except Exception as e:
        print(f"Erro ao carregar o arquivo YAML: {e}")
        return None
