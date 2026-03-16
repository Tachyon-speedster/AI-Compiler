import csv

def store_training_example(features, results):

    best = min(results, key=results.get)

    row = features + [best]

    with open("training_data.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
