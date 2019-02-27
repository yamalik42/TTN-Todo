def sort_dates(dates_list):
    mapped_dates = []
    for date in dates_list:
        parsed = dt.datetime.strptime(date[4:], '%b %d')
        formatted = dt.datetime.strftime(parsed, '%m%d')
        mapped_dates.append(int(formatted))
    sorted_dates = sorted(mapped_dates)
    for date in sorted_dates:
        parsed = dt.datetime.strptime(date, '%m%d').replace(year=2019)