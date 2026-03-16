
import csv
import os

DATASET = "training_data.csv"

FEATURE_ORDER = [
    "num_instructions",
    "num_loops",
    "nested_loops",
    "max_loop_depth",
    "assignments",
    "add_assign",
    "prints",
    "vector_ops",
    "vector_add",
    "vector_scale",
    "operations",
    "memory_ops"
]


# ---------------------------------
# Initialize dataset file
# ---------------------------------

def init_dataset():

    if not os.path.exists(DATASET):

        with open(DATASET, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow(FEATURE_ORDER + ["label"])


# ---------------------------------
# Store training example
# ---------------------------------

def store_training_example(features, best):

    row = [features[f] for f in FEATURE_ORDER]

    with open(DATASET, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(row + [best])
