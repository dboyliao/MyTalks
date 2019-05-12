#!/usr/bin/env python
import argparse
from random import random, sample, seed
from string import ascii_letters, digits

import pandas as pd

_CHARSET = ascii_letters + digits
seed(1024)


def random_name(length=8):
    return "".join(sample(_CHARSET, length))


def generate_data(
    prob_have_child, n_first_generation=100000, output_fname="family.csv"
):
    gen1_data = []
    # first generation
    for _ in range(n_first_generation):
        parent = random_name()
        have_child = False
        while True:
            if random() <= prob_have_child:
                child = random_name()
                gen1_data.append((parent, child))
                have_child = True
            else:
                if not have_child:
                    gen1_data.append((parent, None))
                break
    gen2_data = []
    for parent, child in gen1_data:
        if child is None:
            continue
        have_child = False
        while True:
            if random() <= prob_have_child:
                grand_child = random_name()
                gen2_data.append((child, grand_child))
                have_child = True
            else:
                if not have_child:
                    gen2_data.append((child, None))
                break
    df = pd.DataFrame(gen1_data + gen2_data, columns=["parent", "child"])
    df.to_csv(output_fname, header=True, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--birth-prob",
        help="the probability of giving birth to a child [default: %(default)s]",
        type=float,
        default=0.5,
        dest="prob_have_child",
    )
    parser.add_argument(
        "-N",
        "--population-of-first-generation",
        help="the population of first generation [default: %(default)s]",
        type=int,
        default=100000,
        dest="n_first_generation",
    )
    parser.add_argument(
        "-o",
        "--output-fname",
        help="the output csv file name [default: %(default)s]",
        default="family.csv",
        dest="output_fname",
    )
    kwargs = vars(parser.parse_args())
    generate_data(**kwargs)
