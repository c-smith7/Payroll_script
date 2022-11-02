# This file will hold of the pandas code from jupyter.

import pandas as pd
from payroll_amt import payroll
#from GUI import MainWindow


def transform_script(file):

    # read in csv file from GUI.
    file_path = f'C:/Users/mcmco/Desktop/QuikMed/Payroll/Summary/{file}'
    timesheet_summary = pd.read_csv(file_path, header=2)


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
        'Milly Smith',
        'Andrea Florkey'
        ]
    wellness_role = [
        'PA', 
        'Nurse'
        ]

    wellness_payroll = timesheet_summary.query('Employee in @wellness_emp')
    wellness_payroll.reset_index(drop=True, inplace=True)


    # Edit Milly's and Carrie's pay rate and hours
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Pay Rate'] = '$5000'
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Hours'] = 1

    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Pay Rate'] = '$6000'
    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Hours'] = 1

    # wellness_payroll.loc[wellness_payroll['Employee']=='Jeffrey Smith', 'Pay Rate'] = '$2500'
    # wellness_payroll.loc[wellness_payroll['Employee']=='Jeffrey Smith', 'Hours'] = 1

    # Removed from salaried employment
    # wellness_payroll.loc[wellness_payroll['Employee']=='Cassidy Davis', 'Pay Rate'] = '$1600'
    # wellness_payroll.loc[wellness_payroll['Employee']=='Cassidy Davis', 'Hours'] = 1

    # remove dollar signs.
    wellness_payroll['Pay Rate'] = wellness_payroll['Pay Rate'].str[1:]


    # convert pay rate values to floats
    wellness_payroll['Pay Rate'] = wellness_payroll['Pay Rate'].astype('float64')

    # Loop to add any salaried employees to Wellness that are not on Homebase

    salary_employees_wellness = [
        {'Employee': 'Jeffrey Smith',
         'Pay Rate': 2500.0,
         'Hours': 1}
    ]

    for employee in salary_employees_wellness:
        wellness_payroll = wellness_payroll.append(employee, ignore_index=True)


    # apply payroll function for payroll amount column. 
    wellness_payroll['Payroll Amount'] = wellness_payroll.apply(lambda x: payroll(x['Pay Rate'], x['Hours']), axis=1)


    # add notes column and add Janney Montgomery for Carrie and Milly
    wellness_payroll['Notes'] = ''
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', 'Notes'] = 'Janney Montgomery'
    wellness_payroll.loc[wellness_payroll['Employee']=='Milly Smith', 'Notes'] = 'Janney Montgomery'


    # add blank column for Carrie's DOT visits.
    wellness_payroll[''] = ''
    wellness_payroll.loc[wellness_payroll['Employee']=='Carrie Guga', ''] = 'DOT'


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
        'Carrie Lewandowski',
        'Autumn Koons',
        'Carlos Smith',
        'Sydney Rodderick'
        ]
    cei_role = [
        'Receptionist',
        'COVID',
        'Office Admin',
        'Work From Home'
        ]

    cei_payroll = timesheet_summary.query('Employee in @cei_emp or Role in @cei_role')
    cei_payroll.reset_index(drop=True, inplace=True)


    # Edit Carlos Smith's pay rate and hours. 
    # cei_payroll.loc[cei_payroll['Employee']=='Carlos Smith', 'Pay Rate'] = '$2000'
    # cei_payroll.loc[cei_payroll['Employee']=='Carlos Smith', 'Hours'] = 1


    # remove dollar signs.
    cei_payroll['Pay Rate'] = cei_payroll['Pay Rate'].str[1:]


    # convert pay rate values to floats
    cei_payroll['Pay Rate'] = cei_payroll['Pay Rate'].astype('float64')


    # drop role column, data no longer needed.
    cei_payroll.drop(columns='Role', inplace=True)


    # Add other salaried employees
    salary_employees = [
        {'Employee':'Carlos Smith',
        'Pay Rate':2400.0,
        'Hours':1},
        {'Employee':'Shannon Herbert',
        'Pay Rate':18.0,
        'Hours':20},
        {'Employee':'MaryJo Rogers',
        'Pay Rate':20.0,
        'Hours':28},
        {'Employee':'Estevan Smith',
        'Pay Rate':1700.0,
        'Hours':1},
        {'Employee':'Iliana Smith',
        'Pay Rate':1700.0,
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


    # create function attributes for required variables in format.py
    transform_script.wellness = wellness_payroll
    transform_script.cei = cei_payroll
    transform_script.file_path = file_path
    #return wellness_payroll, cei_payroll, file_path


# unpack returned tuple
#wellness_payroll, cei_payroll, file_path = transform_script()