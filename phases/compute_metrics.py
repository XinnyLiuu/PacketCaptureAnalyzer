"""
Given the parsed packet fields, compute the 13 metrics per node:

    Data Size (8) 
        - # Echo Requests
        - # Echo Requests received
        - # Echo Replies sent
        - # Echo Replies received
        - Total Echo Request bytes sent (based on frame)
        - Total Echo Request bytes received (based on frame)
        - Total Echo Request data sent (based on ICMP payload)
        - Total Echo Request data received (based on ICMP payload)
        
    Time (4)
        - Average Ping Round Trip Time (RTT) 
            (time spent sending and receiving a packet from a destination)
        - Echo Request Throughput (in KB/sec) 
            (sum of frame sizes of all - Echo Request packets sent by the node divided by sum of all Ping RTTs)
        - Echo Request Goodput (in KB/sec) 
            (sum of ICMP payloads of all Echo Request packets sent by the node divided by the sum of all Ping RTTs)
        - Average Reply Delay (in microseconds) 
            (time between a node receiving an Echo request packet and sending an Echo reply packet back to the source)
        
    Distance (1)
        - Average number of hops per Echo Request
            (number of networks that an Echo Request packet must traverse in order to reach its destination)
"""


class ComputeMetrics:
    def __init__(self, requests):
        self.requests = requests
        self.metrics = {}

    def compute(self):
        """
        Computes metrics from the requests summary (request, reply)
        """
        for request in self.requests:
            # Get the request and reply summaries
            req = request[0]
            reply = request[1]

            # Split the values by whitespaces
            print(req.split())
            print(reply.split())
            req = req.split()
            reply = reply.split()

            # Assign each field accordingly
            time_req = req[1]
            time_reply = reply[1]

            source_req = req[2]
            source_reply = reply[2]

            dest_req = req[3]
            dest_reply = reply[3]

            bytes_req = req[5]
            bytes_reply = reply[5]

            break
