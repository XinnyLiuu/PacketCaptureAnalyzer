import csv


class CSVOutput(object):
    """
    Takes the metrics that are computed and writes them to a csv
    """

    def __init__(self, metrics):
        self.metrics = metrics

    def write(self):
        """
        Writes metrics to `output.csv` 
        """
        print "Writing to output.csv ..."

        with open("output.csv", mode="w") as output:

            # Prepare the csv writer
            writer = csv.writer(output, delimiter=",")

            # Iterate through each node's metrics and write the fields to csv
            for i, metrics in enumerate(self.metrics):

                # Identify the node
                writer.writerow(["Node {}".format(i+1)])
                writer.writerow([])

                # Get the echo requests / replies sent and received
                writer.writerow([
                    'Echo Requests Sent',
                    'Echo Requests Received',
                    'Echo Replies Sent',
                    'Echo Replies Received'
                ])
                writer.writerow([
                    metrics["data_size"]["requests_sent"],
                    metrics["data_size"]["requests_received"],
                    metrics["data_size"]["replies_sent"],
                    metrics["data_size"]["replies_received"]
                ])

                # Get the echo requests bytes and data sent
                writer.writerow([
                    'Echo Requests Bytes Sent (bytes)',
                    'Echo Requests Data Sent (bytes)'
                ])
                writer.writerow([
                    metrics["data_size"]["request_bytes_sent"],
                    metrics["data_size"]["request_data_sent"]
                ])

                # Get the echo request bytes and data received
                writer.writerow([
                    'Echo Requests Bytes Received (bytes)',
                    'Echo Requests Data Received (bytes)'
                ])
                writer.writerow([
                    metrics["data_size"]["request_bytes_received"],
                    metrics["data_size"]["request_data_received"]
                ])
                writer.writerow([])

                # Get the average rtt
                writer.writerow([
                    "Average RTT (milliseconds)",
                    metrics["time"]["avg_rtt"]
                ])

                # Get the throughput
                writer.writerow([
                    "Echo Request Throughput (kB/sec)",
                    metrics["time"]["throughput"]
                ])

                # Get the goodput
                writer.writerow([
                    "Echo Request Goodput (kB/sec)",
                    metrics["time"]["goodput"]
                ])

                # Get the average reply delay
                writer.writerow([
                    "Average Reply Delay (microseconds)",
                    metrics["time"]["avg_reply_delay"]
                ])

                # Get the average hops
                writer.writerow([
                    "Average Echo Request Hop Count",
                    metrics["distance"]["avg_hops"]
                ])
                writer.writerow([])

        print "done."
