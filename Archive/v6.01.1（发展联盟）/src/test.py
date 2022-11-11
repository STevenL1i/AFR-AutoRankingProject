import json
import xlsxwriter
workbook = xlsxwriter.Workbook("test.xlsx")
a = {}
with open("format/format.json") as gp:
    a = json.load(gp)
print(a)

testsheet = workbook.add_worksheet("test")
testsheet.write(0,0, "W%BGT$EF", workbook.add_format(a["driverlist"]["default"]))

workbook.close()
