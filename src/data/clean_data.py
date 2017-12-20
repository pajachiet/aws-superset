#!/usr/bin/env python
# coding: utf-8

import os


def main():
    print("-- Cleaning csv files")
    for filename in os.listdir('data/raw'):
        if filename.endswith('.csv'):
            print(filename)
            clean(filename)


def clean(filename):
    with open('data/raw/' + filename, 'r') as f1, open('data/cleaned/' + filename, 'w') as f2:
        for line in f1:
            f2.write(line.replace('Ã‰/', 'É'))

if __name__ == '__main__':
    main()
