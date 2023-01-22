import json, xlsxwriter

# format
formatf = open("settings/format.json", "r", encoding='utf-8')
format:dict = json.load(formatf)
formatf.close()

workbook = xlsxwriter.Workbook("z.xlsx")

f = workbook.add_format(format["pointsformat"]["P1"])
print(f)

workbook.close()
