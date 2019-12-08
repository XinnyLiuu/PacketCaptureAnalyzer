import pprint


class ComputeMetrics(object):
    """
    Computes the metrics of the node given the packets and ip address
    """

    def __init__(self, packets, source_ip):
        self.packets = packets
        self.source_ip = source_ip
        self.metrics = {}
        self.total_rtt = 0

        # Set the 3 categories of metrics in the dictionary
        self.metrics["data_size"] = {}
        self.metrics["time"] = {}
        self.metrics["distance"] = {}

    def compute(self):
        # Data Metrics
        self.set_requests_sent(self.packets["requests"])
        self.set_requests_received(self.packets["requests"])
        self.set_replies_sent(self.packets["replies"])
        self.set_replies_received(self.packets["replies"])
        self.set_request_bytes_sent(self.packets["requests"])
        self.set_request_bytes_received(self.packets["requests"])
        self.set_request_data_sent(self.packets["requests"])
        self.set_request_data_received(self.packets["requests"])

        # Time Metrics
        self.set_average_RTT(self.packets)
        self.set_throughput(self.packets["requests"])
        self.set_goodput(self.packets["requests"])
        self.set_average_reply_delay(self.packets)

        # Distance Metric
        self.set_average_hops(self.packets)

        # Print the result metrics dictionary
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(self.metrics)

    def get_sent_requests(self, requests):
        """
        Gets the list of requests sent by the node
        """
        sent = []

        for packet in requests:
            if packet.source == self.source_ip:
                sent.append(packet)

        return sent

    def get_received_requests(self, requests):
        """
        Get the list of requests received by the node
        """
        received = []

        for packet in requests:
            if packet.dest == self.source_ip:
                received.append(packet)

        return received

    def get_sent_replies(self, replies):
        sent = []

        for packet in replies:
            if packet.source == self.source_ip:
                sent.append(packet)

        return sent

    def get_received_replies(self, replies):
        """
        Gets the list of replies received by the node
        """
        received = []

        for packet in replies:
            if packet.dest == self.source_ip:
                received.append(packet)

        return received

    def set_requests_sent(self, requests):
        """
        Computes the number of echo requests sent
        """
        sent = self.get_sent_requests(requests)
        self.metrics["data_size"]["requests_sent"] = len(sent)

    def set_requests_received(self, requests):
        """
        Computes the number of echo requests received
        """
        received = self.get_received_requests(requests)
        self.metrics["data_size"]["requests_received"] = len(received)

    def set_replies_sent(self, replies):
        """
        Computes the number of echo replies sent
        """
        sent = self.get_sent_replies(replies)
        self.metrics["data_size"]["replies_sent"] = len(sent)

    def set_replies_received(self, replies):
        """
        Computes the number of echo replies received
        """
        received = self.get_received_replies(replies)
        self.metrics["data_size"]["replies_received"] = len(received)

    def set_request_bytes_sent(self, requests):
        """
        Computes the total number of bytes sent by requests
        """
        total = 0

        for packet in self.get_sent_requests(requests):
            total += packet.frame_size

        self.metrics["data_size"]["request_bytes_sent"] = total

    def set_request_bytes_received(self, requests):
        """
        Computes the total number of bytes received by requests
        """
        total = 0

        for packet in self.get_received_requests(requests):
            total += packet.frame_size

        self.metrics["data_size"]["request_bytes_received"] = total

    def set_request_data_sent(self, requests):
        """
        Computes the total number of data sent by requests
        """
        total = 0

        for packet in self.get_sent_requests(requests):
            total += packet.data_length

        self.metrics["data_size"]["request_data_sent"] = total

    def set_request_data_received(self, requests):
        """
        Computes the total number of data received by requests
        """
        total = 0

        for packet in self.get_received_requests(requests):
            total += packet.data_length

        self.metrics["data_size"]["request_data_received"] = total

    def set_average_RTT(self, packets):
        """
        Computes the average time it takes to send a request and receive a corresponding reply from the destination 
        """
        requests = packets["requests"]
        replies = packets["replies"]

        # Get the requests sent from this node's ip
        requests_sent = self.get_sent_requests(requests)

        # Get the replies received from this node's ip
        replies_received = self.get_received_replies(replies)

        # Iterate through all sent/received packets
        for i, request in enumerate(requests_sent):
            reply = replies_received[i]

            # Get sequence numbers
            seq_no_request = request.summary.split()[10]
            seq_no_reply = reply.summary.split()[10]

            # Get time (s) and calculate the difference then convert to ms
            request_time = float(request.summary.split()[1])
            reply_time = float(reply.summary.split()[1])
            difference = (reply_time - request_time) * 1000

            # Check for matching sequence numbers
            if seq_no_request == seq_no_reply:
                self.total_rtt += difference

        # Get the average
        avg = round(self.total_rtt / len(requests_sent), 2)
        self.metrics["time"]["avg_rtt"] = avg

    def set_throughput(self, requests):
        """
        Computes the echo request throughput (in kB/sec) defined as the sum of the frame sizes of all echo request packets sent by the node divided by the sum of all Ping RTTs
        """
        total_frame_size = 0

        # Get the requests sent from this node's ip
        requests_sent = self.get_sent_requests(requests)

        # Get te sum of all frame sizes
        for packet in requests_sent:
            total_frame_size += packet.frame_size

        # Set throughput
        self.metrics["time"]["throughput"] = round(
            total_frame_size / self.total_rtt, 1)

    def set_goodput(self, requests):
        """
        Computes the echo request goodput (in KB/sec) defined as the sum of the ICMP paylods of all echo requests sent by the node divided by the sum of all ping RTTs
        """
        total_data_length = 0

        # Get the requests sent from this node's ip
        requests_sent = self.get_sent_requests(requests)

        # Get te sum of all data length
        for packet in requests_sent:
            total_data_length += packet.data_length

        # Set goodput
        self.metrics["time"]["goodput"] = round(
            total_data_length / self.total_rtt, 1)

    def set_average_reply_delay(self, packets):
        """
        Computes the average time between a node receiving an echo request packet and sending an echo reply packet back to the source in ms
        """
        total_reply_delay = 0

        requests = packets["requests"]
        replies = packets["replies"]

        # Get the requests where the dest is the node's ip
        requests_received = self.get_received_requests(requests)

        # Get the replies where the source is the node's ip
        replies_sent = self.get_sent_replies(replies)

        # Iterate through the packets
        for i, request in enumerate(requests_received):
            reply = replies_sent[i]

            # Get sequence numbers
            seq_no_request = request.summary.split()[10]
            seq_no_reply = reply.summary.split()[10]

            # Get time (s) and calculate the difference then convert to us
            request_time = float(request.summary.split()[1])
            reply_time = float(reply.summary.split()[1])
            difference = (reply_time - request_time) * 1000000

            # Check for matching sequence numbers
            if seq_no_request == seq_no_reply:
                total_reply_delay += difference

        # Get the average
        avg = round(total_reply_delay / len(requests_received), 2)
        self.metrics["time"]["avg_reply_delay"] = avg

    def set_average_hops(self, packets):
        """
        Computes the average number of hops per echo request. The hop count of an echo request is defined as the number of networks than an echo rqeuest packet must traverse in order to reach its destination. 

        Hop count will be 1 if the destination is on a node's network or 3 if it has to go through routers to react its destination
        """
        total_ttl = 0.0

        requests = packets["requests"]
        replies = packets["replies"]

        # Get the requests sent from this node's ip
        requests_sent = self.get_sent_requests(requests)

        # Get the replies received from this node's ip
        replies_received = self.get_received_replies(replies)

        # Iterate through the packets
        for i, request in enumerate(requests_sent):
            request = requests_sent[i]
            reply = replies_received[i]

            # Get sequence numbers
            seq_no_request = request.summary.split()[10]
            seq_no_reply = reply.summary.split()[10]

            # Get the ttls
            ttl_request = int(request.summary.split()[11].split("=")[1])
            ttl_reply = int(reply.summary.split()[11].split("=")[1])

            # Check for matching sequence numbers
            if seq_no_request == seq_no_reply:
                total_ttl += (ttl_request - ttl_reply) + 1

        # Calculate average
        avg = round(total_ttl / len(requests_sent), 2)
        self.metrics["distance"]["avg_hops"] = avg
