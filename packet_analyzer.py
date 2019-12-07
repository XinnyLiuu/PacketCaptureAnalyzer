"""
Xin Liu
Mini Project 2 - Packet Capture Analysis Tool
12/9/2019

The packet analyzer program will consist of three main phases:

    - Packet Filtering: Keep only the packets we want to analyze
    - Packet Parsing: Read relevant packet fields into memory for processing
    - Compute Metrics: Using packet fields to compute metrics

Given ICMP packet captures containing ~8000 packets collected across 4 nodes, filter and compute 13 metrics from them.
"""

import os
from phases import *
from csv_output import CSVOutput


def main():
    """
    Packet Filtering 

    Grab the paths of the node texts to be filtered
    """
    paths = [
        "captures/Node1.txt",
        "captures/Node2.txt",
        "captures/Node3.txt",
        "captures/Node4.txt"
    ]

    for path in paths:
        FilterPackets(path).filter()

    """
    Packet Parsing
    
    Specify the paths and ip addresses of the filtered node texts for parsing 
    """
    paths = [
        {
            "path": "Node1_filtered.txt",
            "ip": "192.168.100.1"
        },
        {
            "path": "Node2_filtered.txt",
            "ip": "192.168.100.2"
        },
        {
            "path": "Node3_filtered.txt",
            "ip": "192.168.200.1"
        },
        {
            "path": "Node4_filtered.txt",
            "ip": "192.168.200.2"
        }
    ]

    # Stores all the metrics of each node
    all_metrics = []

    for p in paths:
        pp = PacketParser(p["path"])
        pp.parse()

        # Get all the packets from the parsing
        packets = pp.packets

        """
        Compute Metrics
        
        Compute the metrics for each node
        """
        cm = ComputeMetrics(packets, p["ip"])
        cm.compute()

        # Add metrics to list
        all_metrics.append(cm.metrics)

    """
    Output
    
    Write each metrics to a csv
    """
    CSVOutput(all_metrics).write()


if __name__ == "__main__":
    main()
