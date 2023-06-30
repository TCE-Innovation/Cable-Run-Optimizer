# This is the cable class to store each individual cable's set of information
class Cable:
    def __init__(self, pull_number, stationing_start, stationing_end, cable_size, is_express):
        self.pull_number = pull_number
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.cable_size = cable_size
        self.is_express = is_express
