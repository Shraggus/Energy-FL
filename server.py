import argparse
from typing import List, Tuple

import flwr as fl
from flwr.common import Metrics

import sys
import os
import subprocess
import time

import zmq

# Constants
BEGIN_EVAL = 100
BEGIN_EVAL_POST_SYNC = 101
PARTY_STARTED = 200
EVAL_FINISHED = 201
EVAL_FINISHED_POST_SYNC = 202
PARTY_CLOSING = 404
STOP_POWER_COLLECTION = 300

ips = {
    "user": "10.8.1.46",
    "rpi1": "10.8.1.38",
    "rpi3": "10.8.1.192",
}

ports_listening = {
    "rpi1": 6012,
    "rpi3": 6013,
}

broadcast_port = 6011
aggregator_ip = ips.get("user")

# Data Generation
validDatasets = {"mnist", "cifar10"}
valid_fusion_algos = {
    fl.server.strategy.FedAvg,
    fl.server.strategy.FedProx,
    fl.server.strategy.FedAdagrad,
    fl.server.strategy.FedXgbNnAvg,
}

# Parameters
rounds = 3
epochs = 4

dataset = "mnist"
num_parties: int = 2
batch_size = 500
fusion = fl.server.strategy.FedAvg
run = "0"

sample_fraction = 1.0
min_num_clients = num_parties


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Thist function averages the `accuracy` metric sent by the clients in a `evaluate`
    stage (i.e. clients received the global model and evaluate it on their local
    validation sets)."""
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


def fit_config(server_round: int, *_, epochs: int = None, batch_size: int = None):
    """Return a configuration with static batch size and (local) epochs."""
    config = {
        "epochs": epochs if epochs else 4,  # Number of local epochs done by clients
        "batch_size": batch_size
        if batch_size
        else 16,  # Batch size to use by clients during fit()
    }
    return config


def main():

    print("\n" * 3)
    
    if num_parties != len(ips) - 1:
        print("""WARNING! Number of parties and number of provided IPs do not match.""")
        print("""Change the dictionary of IPs in this python script rfn""")
        input("Press Enter to Exit")
        sys.exit()

    print(
        f"""
      {'' if run is None else f'{run=}'}
      {dataset=}
      {num_parties=}
      {batch_size=}
      {fusion=}
      """
    )

    # Define strategy
    strategy = fl.server.strategy.FedAvg(
        fraction_fit=sample_fraction,
        fraction_evaluate=sample_fraction,
        min_fit_clients=min_num_clients,
        on_fit_config_fn=fit_config,
        evaluate_metrics_aggregation_fn=weighted_average,
    )

    # Start Flower server
    fl.server.start_server(
        server_address=args.server_address,
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=strategy,
    )


if __name__ == "__main__":
    main()
    sys.exit()


def main2(args):
    global dataset, num_parties, datapoints_per_party, model, fusion
    

    print("\n\n\n")
    time.sleep(3)

    

    if run is None:
        input(
            """
          Note : If you need SAR Timeseries data for multiple devices,
          specify that in the sar_timeseries_userlist at the end of the file
          Add each username as a string into the list
          Don't forget to change the following Scripts
          1.) pi_cache_port.sh [located in the Functions Directory]
          2.) sar_collector.sh [located in the Functions Directory]
          3.) The 'ips' dictionary of this python file. Leave only those IPs that are participating
          4.) The 'ports_listening' dictionary of this python file. Leave only the parties that are participating
          Edit the hosts and IPs list in these files if required and Press Enter to continue\n
          """
        )
        input("Are you absolutely sure you changed everything? Press Enter to continue")
        input(
            "Last chance to edit stuff. If you're done, press Enter to run the experiment"
        )
    # Run batch.sh manually first
    # Generate Data on Agg

    agg_context = zmq.Context()
    listeners = []
    try:
        for user, port in ports_listening.items():
            a = agg_context.socket(zmq.SUB)
            a.setsockopt(zmq.SUBSCRIBE, b"")
            a.connect(f"tcp://{ips.get(user)}:{port}")
            listeners.append(a)

        broadcast = agg_context.socket(zmq.PUB)
        broadcast.bind(f"tcp://{aggregator_ip}:{broadcast_port}")
    except OSError as e:
        print(f"OSError Occurred, Error {e}")

    party_id = 0
    for user, ip in ips.items():
        if user == "user":
            continue
        subp = subprocess.Popen(
            [
                "./Functions/pi_runner.sh",
                fusion,
                model,
                str(num_parties),
                dataset,
                aggregator_ip,
                ip,
                str(broadcast_port),
                str(ports_listening.get(user)),
                user,
                str(party_id),
                str(datapoints_per_party),
            ]
        )
        party_id += 1
        time.sleep(2)

    # We listen for the the parties to confirm they actually did stuff
    def wait_until_ready(value, msg=None) -> None:
        nonlocal listeners
        if msg is None:
            msg = f"Listening for value : {value}"
        print(msg)
        finished = [False] * len(listeners)
        finished_indicies = []
        while False in finished:
            for index, listener in enumerate(listeners):
                if index in finished_indicies:
                    continue
                try:
                    response = listener.recv_pyobj(flags=zmq.NOBLOCK)
                except zmq.ZMQError:
                    ...
                else:
                    if response == value:
                        finished_indicies.append(index)
                        finished[index] = True
            print(f"Parties that have responded :", *finished_indicies, sep=" ")
            if False not in finished:
                time.sleep(5)
            else:
                time.sleep(15)
        print("Finished Waiting")

    # Waits until all parties are ready for training

    wait_until_ready(PARTY_STARTED, msg="Waiting for all parties to start and register")

    # Starting Power collection
    power = subprocess.Popen(
        ["./Functions/power_collector.sh", "0.4"],
    )
    print("Power Collection Started")
    time.sleep(3)
    # Start Collecting SAR Data
    print("SAR STARTED, waiting 20 seconds to begin training")
    sar = subprocess.Popen(["./Functions/sar_collector.sh"], stdin=subprocess.PIPE)
    time.sleep(20)

    # Stop Collecting SAR Data
    sar.communicate(b"\n")
    sar.wait()
    print("SAR FINISHED")
    # Stopping power data
    broadcast.send_pyobj(STOP_POWER_COLLECTION)
    power.wait()
    print("POWER COLLECTION FINISHED")

    # Training is finished,  let's send the signal to begin evaluation
    broadcast.send_pyobj(BEGIN_EVAL)
    # Eval will take place and we have to sync, lets wait for parties to respond
    wait_until_ready(EVAL_FINISHED, msg="Waiting for parties to finish Evaluations")

    broadcast.send_pyobj(BEGIN_EVAL_POST_SYNC)
    wait_until_ready(
        EVAL_FINISHED_POST_SYNC,
        msg="Waiting for parties to finish Postsync Evaluations",
    )

    # Now that all the evals are done, we can shutdown the aggregator after parties are done
    wait_until_ready(PARTY_CLOSING, msg="Waiting for parties to close")

    print("\n\nStopping Aggregator\n\n")
    time.sleep(3)

    for user, ip in ips.items():
        if user != "user":
            subprocess.run(f"./Functions/files_copier.sh {user} {ip}", shell=True)

    # Shutdown all the sockets
    for listener in listeners:
        try:
            listener.close()
        except Exception:
            print("Close Failed")

    broadcast.close()
    agg_context.term()
    print("Done!")

    # Everything is now terminated
    # Now we can parse all the collected Data

    if run is None:
        fname = f"{fusion}_{model}_{datapoints_per_party}_{num_parties}_{dataset}"
    else:
        fname = f"{fusion}_{model}_{datapoints_per_party}_{num_parties}_{dataset}_{run}"

    print("Starting parsing of data")
    Parser.main(
        party_usernames=list(ips.keys()),
        name=fname,
        sar_timeseries_userlist=list(ips.keys()),
    )
    print("Parsing Complete")
    print("Exiting Now")
    return
