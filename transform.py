# This file will hold of the pandas code from jupyter.

import pandas as pd
from payroll_amt import payroll


def transform_script():
    
    # First, user will be prompted to input the summary file name without file extension (.csv)
    # Later I will implement a simple Qt gui file browser to make this step more user friendly.
    summary_file = input('File name:')


    # read in input csv file.
    file_path = f'C:/Users/mcmco/Desktop/QuikMed/Payroll/Summary/{summary_file}.csv'
    timesheet_summary = pd.read_csv(file_path, header=2)


    # remove unwanted columns from df. 
    timesheet_summary.drop(columns=['Actual & Scheduled Diff', 'Scheduled Hours'], inplace=True)


    # Merge first and last name columns, and rearange columns.
    timesheet_summary['Employee'] = timesheet_summary['First Name'] + ' ' + timesheet_summary['Last Name']
    timesheet_summary.drop(columns=['First Name', 'Last Name'], inplace=True)
    timesheet_summary = timesheet_summary[['Employee', 'Role', 'Wage Rate', 'Actual Hours']]


    # Rename columns
    timesheet_summary.rename(columns={'Wage Rate':'Pay Rate', 'Actual Hours':'Hours'}, inplace=True)


    # Next, we will split the summary timesheet into two timesheets/payrolls, Wellness and CEI
    # First, Wellness payroll
    wellness_emp = [
        'Debra Russell', 
        'Jodie Ewing', 
        'Kristy Knight', 
        'Lucie Tatum', 
        'Cassidy Davis', 
        'Tricia Loomis', 
        'Rick Tontarski',
        'Carrie Guga',
        'Milly Smith'
        ]
    wellness_role = [
        'PA', 
        'Nurse'
        ]

    wellness_payroll = timesheet_summary.query('Employee in @wellness_emp or Role in @wellness_role')
    wellness_payroll.reset_index(drop=True, inplace=True)


    # Edit Milly's and Carrie's pay rate and hours
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Pay Rate'] = '$4900'
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Hours'] = 1

    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Pay Rate'] = '$6000'
    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Hours'] = 1


    # remove dollar signs.
    wellness_payroll['Pay Rate'] = wellness_payroll['Pay Rate'].str[1:]


    # convert pay rate values to floats
    wellness_payroll['Pay Rate'] = wellness_payroll['Pay Rate'].astype('float64')


    # apply payroll function for payroll amount column. 
    wellness_payroll['Payroll Amount'] = wellness_payroll.apply(lambda x: payroll(x['Pay Rate'], x['Hours']), axis=1)


    # add DOT column
    wellness_payroll['DOT'] = ''

    # add notes column and add Janney Montgomery for Carrie and Milly
    wellness_payroll['Notes'] = ''
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Notes'] = 'Janney Montgomery'
    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Notes'] = 'Janney Montgomery'


    # check for and add overtime note if needed. 
    wellness_payroll.loc[wellness_payroll['Hours'] > 80, 'Notes'] = 'Overtime'


    # Lastly, drop the role column. It is no longer needed. 
    wellness_payroll.drop(columns='Role', inplace=True)


    # sort employees by hours worked
    wellness_payroll = wellness_payroll.sort_values(by=['Hours'], ascending=False).reset_index(drop=True)


    # Next, CEI payroll
    cei_emp = [
        'Alaynah Bowman', 
        'Alyssa Bowman',
        'Rebecca Wisner',
        'Chelby Davis',
        'Mia Kelly', 
        'Carrie Lewandowski'
        ]
    cei_role = [
        'Receptionist',
        'COVID',
        'Office Admin'
        ]

    cei_payroll = timesheet_summary.query('Employee in @cei_emp or Role in @cei_role')
    cei_payroll.reset_index(drop=True, inplace=True)


    # Edit Carlos Smith's pay rate and hours. 
    cei_payroll.loc[cei_payroll['Employee']=='Carlos Smith', 'Pay Rate'] = '$2000'
    cei_payroll.loc[cei_payroll['Employee']=='Carlos Smith', 'Hours'] = 1


    # remove dollar signs.
    cei_payroll['Pay Rate'] = cei_payroll['Pay Rate'].str[1:]


    # convert pay rate values to floats
    cei_payroll['Pay Rate'] = cei_payroll['Pay Rate'].astype('float64')


    # drop role column, data no longer needed.
    cei_payroll.drop(columns='Role', inplace=True)


    # Add other salaried employees
    salary_employees = [
        {'Employee':'Cassidy Davis',
        'Pay Rate':18.0,
        'Hours':40},
        {'Employee':'Shannon Herbert',
        'Pay Rate':18.0,
        'Hours':20},
        {'Employee':'MaryJo Rogers',
        'Pay Rate':20.0,
        'Hours':28},
        {'Employee':'Estevan Smith',
        'Pay Rate':1200.0,
        'Hours':1},
        {'Employee':'Iliana Smith',
        'Pay Rate':1200.0,
        'Hours':1}
        ]

    for employee in salary_employees:
        cei_payroll = cei_payroll.append(employee, ignore_index=True)


    # sort employees
    cei_payroll = cei_payroll.sort_values(by=['Employee']).reset_index(drop=True)


    # calculate payroll amount for each employee. 
    cei_payroll['Payroll Amount'] = cei_payroll.apply(lambda x: payroll(x['Pay Rate'], x['Hours']), axis=1)


    # add notes column and check for and add overtime note if needed. 
    cei_payroll['Notes'] = ''
    cei_payroll.loc[cei_payroll['Hours'] > 80, 'Notes'] = 'Overtime'


    # sort employees by hours worked
    cei_payroll = cei_payroll.sort_values(by=['Hours'], ascending=False).reset_index(drop=True)


    # return both dataframes and payroll date
    return wellness_payroll, cei_payroll, file_path


# unpack returned tuple
wellness_payroll, cei_payroll, file_path = transform_script()