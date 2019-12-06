"""
Each given *.pcap file and *.txt file contains 1300 - 1800 packets.

FilterPackets will filter the raw text file so that only ICMP Echo Request and ICMP Echo Reply packets remain and are placed in a new filter output file - Node*_filtered.txt
"""


class FilterPackets:
    def __init__(self, path):
        self.path = path
        self.file_name = path.split("/")[1].split(".")[0]
        self.icmp_lines = list()

    def filter(self):
        """
        Parses each line in the text file and filters everything not related to ICMP protocols
        """
        f = open(self.path)
        lines = f.readlines()

        for i in range(len(lines)):
            curr = lines[i]
            if "No." in curr:
                i += 1

                info = lines[i]
                if("Echo (ping)" in info):
                    self.icmp_lines.extend([curr, info])

                    i += 1
                    while "No." not in lines[i]:
                        self.icmp_lines.append(lines[i])
                        i += 1

        # Close file after filtering is done
        f.close()

        # Combine the filtered lines
        data = "".join(self.icmp_lines).strip()
        data += "\n"

        # Write to a file named <self.file_name>_filtered.txt
        f = open("{}_filtered.txt".format(self.file_name), "w")
        f.write(data)
        print("{}_filtered.txt done.".format(self.file_name))
        f.close()
