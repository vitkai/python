import datetime

FROM_DATE = '2023-04-13'
# Define a function to calculate the date 62 days from a given date
def get_future_date(input_date=None):
    # If no input date is provided, use the current date
    if input_date is None:
        input_date = datetime.datetime.now().date()
    else:
        input_date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()

    # Calculate the date 62 days from the input date
    future_date = input_date + datetime.timedelta(days=62)

    # Convert the future_date to a string in yyyy-mm-dd format
    future_date_str = future_date.strftime("%Y-%m-%d")

    return future_date_str

# Test the function
print("Date 62 days from now:", get_future_date())
print(f"Date 62 days from {FROM_DATE}:", get_future_date(FROM_DATE))