# PacketCaptureAnalyzer

Python program written to analyze data from many ICMP packets in a network and computes the metrics.

Output:
```
Filtering Node1 ...
done.
Filtering Node2 ...
done.
Filtering Node3 ...
done.
Filtering Node4 ...
done.
Parsing Node1 ...
done.
{'data_size': {'replies_received': 128,
               'replies_sent': 49,
               'request_bytes_received': 51904,
               'request_bytes_sent': 89452,
               'request_data_received': 49846,
               'request_data_sent': 84076,
               'requests_received': 49,
               'requests_sent': 128},
 'distance': {'avg_hops': 1.91},
 'time': {'avg_reply_delay': 55.51,
          'avg_rtt': 2.56,
          'goodput': 256.1,
          'throughput': 272.5}}
Parsing Node2 ...
done.
{'data_size': {'replies_received': 82,
               'replies_sent': 160,
               'request_bytes_received': 113816,
               'request_bytes_sent': 53040,
               'request_data_received': 107096,
               'request_data_sent': 49596,
               'requests_received': 160,
               'requests_sent': 82},
 'distance': {'avg_hops': 2.32},
 'time': {'avg_reply_delay': 55.65,
          'avg_rtt': 2.68,
          'goodput': 225.9,
          'throughput': 241.6}}
Parsing Node3 ...
done.
{'data_size': {'replies_received': 72,
               'replies_sent': 98,
               'request_bytes_received': 62908,
               'request_bytes_sent': 53070,
               'request_data_received': 58792,
               'request_data_sent': 50046,
               'requests_received': 98,
               'requests_sent': 72},
 'distance': {'avg_hops': 1.94},
 'time': {'avg_reply_delay': 54.86,
          'avg_rtt': 2.78,
          'goodput': 250.1,
          'throughput': 265.2}}
Parsing Node4 ...
done.
{'data_size': {'replies_received': 108,
               'replies_sent': 86,
               'request_bytes_received': 42388,
               'request_bytes_sent': 75232,
               'request_data_received': 38776,
               'request_data_sent': 70696,
               'requests_received': 86,
               'requests_sent': 108},
 'distance': {'avg_hops': 2.43},
 'time': {'avg_reply_delay': 53.31,
          'avg_rtt': 3.04,
          'goodput': 215.4,
          'throughput': 229.3}}
Writing to output.csv ...
done.

```