#! File to run experiments

run_finished_experiments = False # Change to True to re-run everything

import subprocess
from common.experiments import generate_all_experiments
from common import Experiment
from Clients import Aggregator, Party, PowerCollector
import common.Configuration as Configuration
import time

batch_sizes = [16, 512]
rounds_and_epochs = [
    (3,4)
]
runs = 3
num_parties = len(Configuration.IP_CLIENTS)

experiments = generate_all_experiments(rounds_and_epochs=rounds_and_epochs, batch_sizes=batch_sizes, runs=runs, num_parties=num_parties)

def run_experiment(expt : Experiment):
    
    
    print(expt)
    time.sleep(3)

    # Setup all the clients, aggregators and power collectors
    
    aggregator : Aggregator = Aggregator(ip=Configuration.IP_AGGREGATOR, username=Configuration.getuser, flwrPort=Configuration.AGGREGATOR_FLOWER_SERVER_PORT, zmqPort=Configuration.AGGREGATOR_ZMQ_BROADCAST_PORT)
    parties : list[Party] = [Party(ip=ip, username=username) for username, ip in Configuration.IP_CLIENTS.items()]
    
    bluetooth_collectors : list[PowerCollector] = []
    
    for user, ip in Configuration.IP_POWER_COLLECTORS.items() :
        party = Configuration.POWER_COLLECTOR_CONNECTED_DEVICE[user]
        bt_addr = Configuration.UM25C_ADDR_FOR_POWER_COLLECTORS[user]
        bluetooth_collectors.append(PowerCollector(ip=ip, username=user, collection_party=party, bluetooth_address=bt_addr, experiment=expt))
    
    from Clients.Scripts.old_server import main as run_flwr_server
    
    # Setup SAR
    from common import sar
    all_ips = Configuration.IP_CLIENTS.copy()
    all_ips.update({Configuration.AGGREGATOR_USERNAME : Configuration.IP_AGGREGATOR})
    sar.initialize_sar(usernames_ips=all_ips)
    subprocess.run(["chmod u+x Clients/Scripts/sar_collector.sh"], shell=True)
    
    # Setup Bluetooth
    for collector in bluetooth_collectors:
        collector.pair_to_tester()
    
    # Ready to start the experiment
    
    # Start the Power Collections, SAR and then finally start the parties and the server
    
    for collector in bluetooth_collectors:
        collector.collect_power_data()
    
    sar_process = subprocess.Popen(["./Clients/Scripts/sar_collector.sh"], shell=True, stdin=subprocess.PIPE)
    
    for cid, party in enumerate(parties):
        party.start_client_server(agg_ip=Configuration.IP_AGGREGATOR, agg_port=Configuration.AGGREGATOR_FLOWER_SERVER_PORT, cid=cid, dataset=expt.dataset, num_parties=expt.num_participating_parties)
    
    args = {
        "rounds" : expt.rounds,
        "epochs" : expt.epochs,
        "run" : expt.run,
        "dataset" : expt.dataset,
        "batch_size" : expt.batch_size,
        "fusion" : expt.fusion,
        "model" : expt.model,
        "sample_fraction" : expt.sample_fraction,
        "proximal_mu" : expt.proximal_mu,
    }
    
    run_flwr_server(args=args)
    
    sar_process.communicate(b"\n")
    aggregator.ZMQStopPowerCollection()
    
    #! Done!
    

