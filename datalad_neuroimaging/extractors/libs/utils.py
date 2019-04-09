
class File:
    def __init__(self):
        pass


class Parser:
    def __init__(self):
        pass

    # parse annex data into array of dictionaries.
    def read_annex_data(self, data):
        d = {}
        collection = []
        # loop line by line (the data).
        for line in data.splitlines():
            # strip whitespace and split string by '=' into array.
            arr = (line.strip()).split('=')
            if len(arr) == 1:
                if bool(d):
                    collection.append(d)
                    d = {}
                arr = (line.strip()).split(' ')
                if len(arr) == 2:
                    d[arr[0]] = arr[1]
            elif len(arr) == 2:
                d[arr[0]] = arr[1]
        return collection
