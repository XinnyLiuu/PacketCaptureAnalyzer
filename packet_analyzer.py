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
from phases import FilterPackets


def main():
    """
    Instantiate the phase classes
    """

    # Filter all the given packets
    paths = [
        "captures/Node1.txt",
        "captures/Node2.txt",
        "captures/Node3.txt",
        "captures/Node4.txt"
    ]

    for path in paths:
        FilterPackets(path).filter()


if __name__ == "__main__":
    main()
