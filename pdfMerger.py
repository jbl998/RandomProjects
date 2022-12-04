import os
from PyPDF2 import PdfFileMerger
inputDir = input('Where are the files located?\n')
outputDir = input('Where do you want the output?\n')
filename = input('What do you want the file to be called?')
bl = filename.endswith('.pdf')
merger = PdfFileMerger(strict=False)
for file in os.listdir(inputDir):
    if file.endswith('.pdf'):
        title = file[:-4]
        merger.append(inputDir + "\\" + file, title)
if bl:
    merger.write(outputDir + "\\" + filename)
else:
    merger.write(outputDir + "\\" + filename + ".pdf")
merger.close()
if bl:
    print("The files has been merged. The output can be found at\n"
          +outputDir + "\\" + filename)
else:
    print("The files has been merged. The output can be found at\n"
      +outputDir + "\\" + filename + ".pdf")
