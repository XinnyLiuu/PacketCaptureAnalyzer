class FilterPackets(object):
    """
    Each given *.pcap file and *.txt file contains 1300 - 1800 packets.

    FilterPackets will filter the raw text file so that only ICMP Echo Request and ICMP Echo Reply packets remain and are placed in a new filter output file - Node*_filtered.txt
    """

    def __init__(self, path):
        self.path = path
        self.file_name = path.split("/")[1].split(".")[0]
        self.icmp_lines = []

    def filter(self):
        """
        Parses each line in the text file and filters everything not related to ICMP protocols
        """
        print "Filtering {} ...".format(self.file_name)

        with open(self.path) as f:
            lines = f.readlines()

            # Iterate through each line to find the icmp related lines into an array
            for i, curr in enumerate(lines):
                if "No." in curr:
                    i += 1

                    info = lines[i]
                    if "Echo (ping)" in info:
                        self.icmp_lines.extend([curr, info])

                        i += 1
                        while "No." not in lines[i]:
                            self.icmp_lines.append(lines[i])
                            i += 1

        # Combine the filtered lines
        data = "".join(self.icmp_lines).strip()
        data += "\n"

        # Write to a file named <self.file_name>_filtered.txt
        with open("{}_filtered.txt".format(self.file_name), "w") as f:
            f.write(data)
            print "done."
