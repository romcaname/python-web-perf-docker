#!/usr/bin/env python3
import csv
import sys
import random
import string

# static seed to generate the same data all the time
rng = random.Random(0)


with open('data.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["a", "b"])

    for i in range(1_000_000):
        short_random_string = "".join(
            rng.choice(string.ascii_letters) for _ in range(20))
        csv_writer.writerow([i, short_random_string])
