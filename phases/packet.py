class Packet(object):
    """
    Object representation of the parsed data from the filtered text file
    """

    def __init__(self, ttl, total_length, frame_size, source, dest, type_request, data_length, summary):
        self.ttl = ttl
        self.total_length = total_length
        self.frame_size = frame_size
        self.source = source
        self.dest = dest
        self.type_request = type_request
        self.data_length = data_length
        self.summary = summary
