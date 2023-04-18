import datetime

# Get the current date
current_date = datetime.datetime.now()

# Calculate the date 62 days from now
future_date = current_date + datetime.timedelta(days=62)

# Convert the future_date to a string in yyyy-mm-dd format
future_date_str = future_date.strftime("%Y-%m-%d")

print("Current date:", current_date.strftime("%Y-%m-%d"))
print("Date 62 days from now:", future_date_str)
