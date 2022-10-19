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


def update_worksheet(data, worksheet):
    """
    updates the spreadsheet selected in by the user
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} update complete')


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

    return surplus_data 


def get_last_5_sales_data():
    """
    collects the last 5 enteries from the sheet
    returns data as lists
    """
    sales = SHEET.worksheet('sales')
    # print(column)
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    print(columns)


def caluclate_stock_average(data):
    """
    takes averge of each stock type, adds 10%
    """
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    main function calls
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')


print('Welcome to Love Sandwiches Data automation')
# main()
get_last_5_sales_data()