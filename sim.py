import ssl
import json
import csv
from datetime import datetime
import time
import smiputils
import config
import sys
import os 
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

sink = config.sim["sink"]
sm_utils = smiputils.utils(config.smip["authenticator"], config.smip["password"], config.smip["name"], config.smip["role"], config.smip["url"], config.smip["verbose"])
CNC_Num = sm_utils.smipgraphql.args.optional
dir_path = os.path.dirname(os.path.realpath(__file__))
data_file = os.path.join(dir_path, "cnc_values.csv")
hidden_parent_id = "449036" #CNC
shown_parent_id = "28221" #CESMII
instance_ids = ["448631", "488962", "489328"] #
sample_rate = config.sim["samplerate"]
simulation_data = []
ids = []
attr_names = []
labels = []

# Read File
def import_file():
    with open(data_file, newline='') as f:
      print("Adding attributes...")
      csv_reader = csv.reader(f)

      # Read the rows into memory, remembering labels and attributes
      count = 0
      for row in csv_reader:
        if count == 0:
            labels = row
        if row[0] == f'CNC {CNC_Num}':
            ids.append(row[1:])
        if row[0] == "Values" or row[0] == '':
            simulation_data.append(row[1:])
        count += 1
    return labels

def clear_data():
    ord = 0
    alias_mutates = ""
    for id in ids[0]:
        # Build Multi-Attr Mutation Query
        alias_mutates += sm_utils.build_alias_clear_ts_mutation(str(ord), id)
        ord +=1
    
    # Send Query
    print(alias_mutates)
    sm_utils.multi_tsmutate_aliases(alias_mutates)

def change_parent(parent_id):
    print("Updating parent. Start time: " + str(datetime.utcnow()))
    sm_utils.update_parent(parent_id, instance_ids[CNC_Num-1])
    print("Updating parent. End time: "  + str(datetime.utcnow()))

def run_sim():
    labels = import_file()
    if sink == "mqtt":
        labels.pop(0)
    print(json.dumps(labels))
    # the line below takes too long for a demo
    # change_parent(shown_parent_id)
    try:
        print()
        print("Starting CESMII Simulator...")
        j = 0

        while True:
            # TODO: Loop through the lines of the CSV file, restarting at end, and send values for each column
            if j >= len(simulation_data) - 1:
                j = 0
            else:
                j += 1

            print()
            print("Simulated values row " + str(j) + "...")
            curr_vals = list(simulation_data[j])
            print(f"using sink:", sink)

            if sink == "smip":
                ord = 0
                alias_mutates = ""
                for i,val in enumerate(curr_vals):

                    # Build Multi-Attr Mutation Query
                    if i == 0:
                        val = val + '-' + str(CNC_Num)
                    alias_mutates += sm_utils.build_alias_ts_mutation(str(ord), ids[0][i], val)
                    ord +=1
                
                # Send Query
                # print(alias_mutates)
                sm_utils.multi_tsmutate_aliases(alias_mutates)
            if sink == "mqtt":
                # Send to Broker
                data = dict(zip(labels, curr_vals))
                print(f"Publishing row: ", json.dumps(data))

                # Configure security
                if config.mqtt["tls"]:
                    sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)
                else:
                    sslSettings = None
                auth = {'username': config.mqtt["username"], 'password': config.mqtt["password"]}

                # Configure protocol
                if config.mqtt["protocol"] == "5":
                    useprotocol = paho.MQTTv5
                else:
                    useprotocol = paho.MQTTv311
                    
                # Publish message
                publish.single(topic=config.mqtt["topic"], payload=json.dumps(data), hostname=config.mqtt["broker"], port=config.mqtt["port"], auth=auth, tls=sslSettings, protocol=useprotocol)

                                
            time.sleep(sample_rate)
    finally:
        print("Cleaning up")

        # Delete Data 
        #clear_data()

        # Change Parent
        # change_parent(hidden_parent_id)

        print("CESMII Simulation Server Offline")


# Line is Values, start sending

run_sim()
