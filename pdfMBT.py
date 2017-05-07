#!/usr/bin/python3
'''pdfMBT - pdf Merge with Bookmarks & Text

This module can be used for merging multiple pdf-documents into single file
with bookmarks and additional texts

author =    Joni Partanen
version =   1.0
status =    Initial release
'''

from PyPDF2 import utils, PdfFileReader, PdfFileWriter
import os
import sys
import csv
import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def readPdfFiles(files):
    # Read pdf files to objects
    files_to_merge = []

    for f in files:
        try:
            next_pdf_file = PdfFileReader(open(f, "rb"))
        except(utils.PdfReadError):
            print >>sys.stderr, "%s is not a valid PDF file." % f
            sys.exit(1)
        else:
            files_to_merge.append(next_pdf_file)

    return files_to_merge


def createCsv(csvfilename, files, files_to_merge):
    ''' Create csv-file with initial pdf-data
    [path], [docfilename], [Bookmark],[docpage], [totpage],
    [text1_x], [text1_y], [text1], '[text2_x], [text2_y], [text2],
    , ..., [textn_x], [textn_y], [textn], '''

    VALUES_IN_CSV = 7

    # Create List of csv-rows with header
    lor = [['filename', 'Bookmark', 'docpage', 'mergepage', 'text1_x',
            'text1_x', 'text1']]

    default_text_x = 10
    default_text_y = 10
    default_text = "Test String!"

    with open(csvfilename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Create csv-values in lists witin list
        totpage = 0
        pdffile = 0
        for f in files_to_merge:
            # Append new row for each page
            for docpage in range(f.numPages):
                lor.append(['' for i in range(VALUES_IN_CSV)])
                if docpage == 0:  # Add file info and bookmark for doc 1st page
                    lor[totpage+1][0] = files[pdffile]
                    # Strip path name and file extension from file name
                    # Does this work in windows?
                    lor[totpage+1][1] = str(os.path.basename(files[pdffile])
                                            .replace('.pdf', ''))
                lor[totpage+1][2] = str(docpage+1)
                lor[totpage+1][3] = str(totpage+1)
                lor[totpage+1][4] = str(default_text_x)
                lor[totpage+1][5] = str(default_text_y)
                lor[totpage+1][6] = str(default_text)

                totpage += 1
            pdffile += 1

        csvwriter.writerows(lor)


def readCsv(filename):
    # This function reads csv-file containing pdf merge information

    lor = []

    with open(filename, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            lor.append(row)

    # return list of values without the header row
    return lor[1:]


def createMergePdf(lor, output):
    # This funcion creates a merged pdf using the settings found in csv-file

    # get files from lor
    files = [lor[i][0] for i in range(len(lor)) if lor[i][0] != '']

    files_to_merge = readPdfFiles(files)

    # Merge page by page
    output_pdf_stream = PdfFileWriter()
    totpage = 0
    pdffile = 0
    for f in files_to_merge:
        for i in range(f.numPages):
            page = f.getPage(i)

            # Create text pdf and merge it with original page
            textfile = addText2Pdf(lor[totpage])
            if textfile:
                page.mergePage(textfile.getPage(0))
            output_pdf_stream.addPage(page)

            # Bookmark definition
            bookmark = lor[totpage][1]
            if bookmark:
                output_pdf_stream.addBookmark(bookmark, totpage)

            totpage += 1
        pdffile += 1

    # Create output pdf file
    try:
        output_pdf_file = open(output, 'wb')
        output_pdf_stream.write(output_pdf_file)
    finally:
        output_pdf_file.close()

    print('output.pdf succesfully created')


def addText2Pdf(row):
    # This module creates a document with text
    i = 4
    # check if there are text strings defined in csv
    if bool(row[i]) & bool(row[i+1]) & bool(row[i+2]):

        # Virtual file
        packet = io.BytesIO()

        can = canvas.Canvas(packet)

        while i+3 <= len(row):
            can.drawString(int(row[i])*mm, int(row[i+1])*mm, row[i+2])
            i += 3
        can.save()
        packet.seek(0)
        return PdfFileReader(packet)
    else:
        return False


def main():
    print('This is only a function library. Use pdf-csv-pdfMerge instead')

if __name__ == '__main__':
    # Excecute only if run as a script
    main()
