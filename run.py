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
    while True:
        print('Please enter sales data from the last market')
        print('The data should be six figures, seperated by commas')
        print('Example: 3,4,1,66,12,4\n')

        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data


def validate_data(values):
    """
    Checks if there are 6 values entered
    if so it converts strings into intergers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you entered {len(values)}"
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again')
        return False
    return True


def update_sales_worksheet(data):
    """
    Updates sales worksheet
    Adds new row with input data
    """
    print('updating sales worksheet...\n')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)


def calculate_surplus_data(sales_row):
    """
    compare the sales and the stock to caluclate surplus or waste
    """
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    print(surplus_data)
    update_surplus_worksheet(surplus_data)


def update_surplus_worksheet(surplus_data):
    """
    updates the surplus worksheet with the new surpluss data values
    """
    print('Updating surplus worksheet...\n')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(surplus_data)


def main():
    """
    main function calls
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print('Welcome to Love Sandwiches Data automation')
main()