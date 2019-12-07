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
    def __init__(self, packets, source_ip):
        self.packets = packets
        self.source_ip = source_ip
        self.metrics = {}

        # Set the 3 categories of metrics in the dictionary
        self.metrics["data_size"] = {}
        self.metrics["time"] = {}
        self.metrics["distance"] = {}

    def compute(self):
        """
        Computes metrics from all packets
        """
        self.set_requests_sent(self.packets["requests"])
        self.set_requests_received(self.packets["requests"])
        self.set_replies_sent(self.packets["replies"])
        self.set_replies_received(self.packets["replies"])
        self.set_request_bytes_sent(self.packets["requests"])
        self.set_request_bytes_received(self.packets["requests"])
        self.set_request_data_sent(self.packets["requests"])
        self.set_request_data_received(self.packets["requests"])

    def set_requests_sent(self, requests):
        """
        Computes the number of echo requests sent
        """
        sent = []

        for packet in requests:
            if packet.source == self.source_ip:
                sent.append(packet)

        self.metrics["data_size"]["requests_sent"] = len(sent)

    def set_requests_received(self, requests):
        """
        Computes the number of echo requests received
        """
        received = []

        for packet in requests:
            if packet.dest == self.source_ip:
                received.append(packet)

        self.metrics["data_size"]["requests_received"] = len(received)

    def set_replies_sent(self, replies):
        """
        Computes the number of echo replies sent
        """
        sent = []

        for packet in replies:
            if packet.source == self.source_ip:
                sent.append(packet)

        self.metrics["data_size"]["replies_sent"] = len(sent)

    def set_replies_received(self, replies):
        """
        Computes the number of echo replies received
        """
        received = []

        for packet in replies:
            if packet.dest == self.source_ip:
                received.append(packet)

        self.metrics["data_size"]["replies_received"] = len(received)

    def set_request_bytes_sent(self, requests):
        """
        Computes the total number of bytes sent by requests
        """
        total = 0

        for packet in requests:
            if packet.source == self.source_ip:
                total += packet.frame_size

        self.metrics["data_size"]["request_bytes_sent"] = total

    def set_request_bytes_received(self, requests):
        """
        Computes the total number of bytes received by requests
        """
        total = 0

        for packet in requests:
            if packet.dest == self.source_ip:
                total += packet.frame_size

        self.metrics["data_size"]["request_bytes_received"] = total

    def set_request_data_sent(self, requests):
        """
        Computes the total number of data sent by requests
        """
        total = 0

        for packet in requests:
            if packet.source == self.source_ip:
                total += packet.data_length

        self.metrics["data_size"]["request_data_sent"] = total

    def set_request_data_received(self, requests):
        """
        Computes the total number of data received by requests
        """
        total = 0

        for packet in requests:
            if packet.dest == self.source_ip:
                total += packet.data_length

        self.metrics["data_size"]["request_data_received"] = total
