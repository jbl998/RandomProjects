import os
from PyPDF2 import PdfMerger

inputDir = "C:\\Users\\" + os.getlogin().lower() + "\\Documents\\Python\\Input\\"
outputDir = "C:\\Users\\" + os.getlogin().lower() + "\\Documents\\Python\\Output\\"
filename = "Eksamensopgaver"

def combinepdf(filename=filename, input=inputDir, output=outputDir):
    for dir in [input, output]:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    bl = filename.endswith('.pdf')
    merger = PdfMerger(strict=False)
    for file in os.listdir(input):
        if file.endswith('.pdf'):
            title = file[:-4]
            merger.append(input + "\\" + file, title)
    if bl:
        merger.write(output + "\\" + filename)
    else:
        merger.write(output + "\\" + filename + ".pdf")
    merger.close()
    if bl:
        print("The files has been merged. The output can be found at\n"
              +output + "\\" + filename)
    else:
            print("The files has been merged. The output can be found at\n"
              +output + "\\" + filename + ".pdf")


