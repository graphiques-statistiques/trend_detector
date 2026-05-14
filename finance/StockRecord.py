# Define a class to hold one record
class StockRecord:
    def __init__(self, timestamp, volume, close):
        self.timestamp = timestamp
        self.volume = volume
        self.close = close

    def __repr__(self):
        return f"StockRecord(timestamp={self.timestamp}, volume={self.volume}, close={self.close})"