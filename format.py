# This file will hold the openpyxl code.

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from transform import wellness_payroll, cei_payroll


# Instantiate workbook, and activate worksheet for wellness payroll
wb = Workbook()
ws_wellness = wb.active
ws_wellness.title = 'Wellness Payroll'

# create secondary worksheet for CEI payroll
ws_cei = wb.create_sheet('CEI Payroll')

# read in dataframes from transform.py
for r in dataframe_to_rows(wellness_payroll, index=False, header=True):
    ws_wellness.append(r)

for r in dataframe_to_rows(cei_payroll, index=False, header=True):
    ws_cei.append(r)

# insert row above row 1 for title
ws_wellness.insert_rows(0, amount=1)
ws_cei.insert_rows(0, amount=1)

# edit column widths
# ws_wellness.column_dimensions['A'] = 20
# ws_wellness.column_dimensions['B'] = 9
# ws_wellness.column_dimensions['C'] = 9
# ws_wellness.column_dimensions['D'] = 15
# ws_wellness.column_dimensions['E'] = 22

col_widths = [21, 10, 10, 16, 23]

for i, width in enumerate(col_widths):
    ws_wellness.column_dimensions[get_column_letter(i+1)].width = width

for i, width in enumerate(col_widths):
    ws_cei.column_dimensions[get_column_letter(i+1)].width = width

 
# change save location later on
wb.save('Test.xlsx')