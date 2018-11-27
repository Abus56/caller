#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv
import glob

import asterisk_api
import voice_api


DIGIT = re.compile(r'\d+')


def exlude_numbers(table_csv, exlude_csv):

    res = []
    for row in table_csv:
        duble = False

        for ex_row in exlude_csv:
            if row[0] == ex_row[0]:
                duble = True
                break

        if not duble:
            res.append(row)

    return res


def generate_call(table, reportpath):
    for row in table:
        if len(row) >= 2:
            print(row)
            number = ''.join(DIGIT.findall(row[0]))
            voices = [voice_api.get_voice(cel) for cel in row[1:]]
            reportpath = reportpath
            asterisk_api.call(number, '&'.join(voices))


def find_files(folder, mask='call*.csv'):
    return glob.glob(os.path.join(folder, mask))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(1)
    elif len(sys.argv) == 3:
        folder_files = sys.argv[1]
        folder_report = sys.argv[2]

        for filepath in find_files(folder_files):
            filereport = os.path.join(folder_report,
                                      'report_%s' % os.path.basename(filepath))
            try:
                csv_table = csv.reader(open(filepath, 'rb'), delimiter=';')
            except IOError:
                exit(1)

            try:
                csv_exclude = csv.reader(open(filereport, 'rb'), delimiter=';')
            except IOError:
                csv_exclude = []

            table = exlude_numbers(csv_table, csv_exclude)
            generate_call(table, filereport)
