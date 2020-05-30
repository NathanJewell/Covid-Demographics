import pandas as pd

def load_csv(filename, data_dir='../data/'):
    fp = "{}{}".format(data_dir, filename)
    with open(fp, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader: