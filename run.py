import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures from input by user
    """
    print('Please enter sales data from the last market')
    print('The data should be six figures, seperated by commas')
    print('Example: 3,4,1,66,12,4\n')

    data_str = input('Enter your data here: ')
    sales_data = data_str.split(',')
    print(f'The value of your data is {sales_data}')


get_sales_data()
