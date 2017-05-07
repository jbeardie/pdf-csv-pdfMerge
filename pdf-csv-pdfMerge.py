#!/usr/bin/python3

'''
pdf-csv-pdfMerge can merge multiple pdf-files into a single pdf file with
bookmarks and custom text in selected pages. Merge configuration is made in
the csv-file.

author =    Joni Partanen
version =   1.0
status =    Initial release
'''

import argparse
import os
import pdfMBT


def main(args):

    # Check if path exists and get a list of pdf-files
    if os.path.isdir(args.path):
        path = os.path.abspath(args.path)
        files = sorted([os.path.join(path, x) for x in os.listdir(path)
                        if x.endswith('.pdf')])
        if not files:
            print('No pdf-files found from: ', path)
    else:
        print('Path: ', args.path, ' does not exist.')
        return

    # Check if output is defined
    if args.output:
        output = args.output
    else:
        output = 'output.pdf'

    # Check if csv is defined
    if args.csv:
        csv_file = args.csv
    else:
        csv_file = 'config.csv'

    # Check if csv already exists
    if os.path.isfile(csv_file):
        print('csv-file found. Merging..')
        lor = pdfMBT.readCsv(csv_file)
        pdfMBT.createMergePdf(lor, output)
        print('done!')
    else:
        print('Creating a csv-file')
        files_to_merge = pdfMBT.readPdfFiles(files)
        pdfMBT.createCsv(csv_file, files, files_to_merge)
        print('done!')


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Enter the path for pdf-files that are ' +
                        'going to be merged')
    parser.add_argument(
        '-c', '--csv', help='Default csv-file "config.csv" is ' +
        'used if not defined otherwise by this argument')
    parser.add_argument('-o', '--output', help='Define output file. Default: ' +
                        'output.pdf')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
