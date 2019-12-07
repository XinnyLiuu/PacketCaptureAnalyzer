"""
Parse the filtered raw text files and read packet fields to be computed into metrics

Useful: https://hpd.gasmi.net/
"""
import socket
import struct
from packet import Packet


class PacketParser:
    def __init__(self, filename):
        self.file = filename
        self.node = filename.split(".")[0].split("_")[0]
        self.packets = {}
        self.packets["requests"] = []
        self.packets["replies"] = []

    def parse(self):
        """
        Parse through the lines of the filtered file and gather all the hex data of each packet
        """
        print("Parsing {} ...".format(self.node))

        with open(self.file) as f:
            lines = f.readlines()

            all_hex = []  # all_hex will contain arrays of complete hex data from the packets
            summaries = []  # Stores the summary of each packet

            # Search through each line to find hex data
            for i in range(len(lines)):
                if "No." in lines[i]:

                    # Grab the summary line for each packet
                    summaries.append(lines[i+1].strip())

                    if (i+3) < len(lines):
                        i += 3  # Jump to the first line containing the hex dump

                        # Add each section of hex data to an array called hex_data
                        hex_data = []
                        data = ""
                        while "No." not in lines[i]:
                            data += lines[i].strip()

                            if(i + 1) < len(lines):
                                i += 1
                            else:
                                break

                        hex_data.append(data)

                        # Append each complete hex data to all_hex
                        all_hex.append(hex_data)

        # For each complete hex data, clean the unnecessary data
        for i in range(len(all_hex)):
            hex_data = "".join(all_hex[i]).split()

            for hex_str in hex_data[:]:
                if len(hex_str) > 2:
                    hex_data.remove(hex_str)

            # Parse the data from the hex and prepare fields for Packet objects
            self.prepare_fields(hex_data, summaries[i])

        print("done.")

    def prepare_fields(self, hex_data, summary):
        """
        Given hex data of a packet and its corresponding summary, parse the fields from each and create a Packet object from each
        """
        # 0 - 14 represents the ethernet header (max size: 14 bytes)
        ethernet_header = hex_data[0:14]
        ethernet_header = " ".join(ethernet_header)

        # 14 - 34 represents the IP header (max size: 20 bytes)
        ip_header = hex_data[14:34]
        ip_header = " ".join(ip_header)

        # Get the TTL from the ip header
        ttl = ip_header.split(" ")[8]
        ttl = int("".join(ttl), 16)

        # Get the total length of everything after the ethernet header
        total_length = ip_header.split(" ")[2:4]
        total_length = int("".join(total_length), 16)

        # Frame size
        frame_size = total_length + 14

        # The parsing above is not entirely accurate and may have trailing elements, if the frame_size is less than the length of hex_data remove the offset from the array
        if frame_size < len(hex_data):
            offset = len(hex_data) - frame_size
            del hex_data[-offset:]

        # Get the source ip address based on the hex
        source = ip_header.split(" ")[12:16]
        source = int("".join(source), 16)
        source = socket.inet_ntoa(struct.pack("<L", source))
        source = source.split(".")[::-1]
        source = ".".join(source)

        # Get the dest ip address based on the hex
        dest = ip_header.split(" ")[16:20]
        dest = int("".join(dest), 16)
        dest = socket.inet_ntoa(struct.pack("<L", dest))
        dest = dest.split(".")[::-1]
        dest = ".".join(dest)

        # 34 - end represents the IP data (first 8 are related to the icmp message)
        ip_data = hex_data[34:]
        ip_data = " ".join(ip_data)

        # Get type of request
        type_request = int("".join(ip_data.split(" ")[0]), 16)

        # Get the data (after the first 8 metadata in the icmp message)
        data = ip_data.split(" ")[8:]
        data_length = total_length - 28

        # Create a Packet and add it to self.packets depending on the type of packet
        if type_request == 0:
            self.packets["replies"].append(
                Packet(ttl, total_length, frame_size,
                       source, dest, "reply", data_length, summary)
            )
        elif type_request == 8:
            self.packets["requests"].append(
                Packet(ttl, total_length, frame_size,
                       source, dest, "request", data_length, summary)
            )
