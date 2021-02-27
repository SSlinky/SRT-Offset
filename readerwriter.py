class Io():
    @staticmethod
    def read(filename: str):
        """Opens a text file and returns the data"""
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines

    @staticmethod
    def write(filename: str, data) -> None:
        """Writes data to a text file"""
        with open(filename, "w") as f:
            f.writelines(data)
