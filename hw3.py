# Alec Rizzo
# Homework 3 - Python
# For this assignment create a class that represents the rainfall data we've been working with

class RainfallTable:

    def __init__(self, filename):
        file = open(filename, 'r')
        rain = {}
        for line in file:
            tokens = line.split()
            rain[int(tokens[0])] = [float(num) for num in tokens[1:]]

        self.table = rain
        file.close()

    def get_rainfall(self, year, month):
        """ Returns the rainfall associated with
            the given year and month.  Both values
            are assumed to be integers (month given
            as 1-12, year as a four digit year).
            Raises an exception if the year/month
            combination are not found
        """
        if year not in self.table or (month < 0 or month > 12):
            raise ValueError("Value does not appear in the table")

        for x in self.table:
            if x == year:
                months = self.table[year]
                return months[month-1]

    def get_average_rainfall_for_month(self, month):
        """ Returns the average rainfall associated with
            the given month across all years in the table.
            Month is assumed to be an integer (1-12.
            Raises an exception if the month is not valid.
        """
        sum = 0
        length = 0
        if month > 12 or month < 0:
            raise ValueError("Value is not a valid month")
        else:
            for x in self.table:
                months = self.table[x]
                sum += months[month-1]
                length += 1
            return round(sum / length, 2)

    def get_min_year(self):
        """ Returns the minimum year in the table """
        return list(self.table.keys())[0]

    def get_max_year(self):
        """ Returns the maximum year in the table """
        return list(self.table.keys())[len(self.table)-1]

    def get_median_rainfall_for_month(self, month):
        """ Returns the median* rainfall associated with
            the given month across all years in the table.
            Month is assumed to be an integer (1-12.
            Raises an exception if the month is not valid.
        """
        if month > 12 or month < 0:
            raise ValueError("Value is not a valid month")
        else:
            m = []
            for x in self.table:
                months = self.table[x]
                m.append(months[month-1])

            m.sort()
            if len(m) % 2 == 1:
                return m[round(len(m)/2)]

            elif len(m) % 2 == 0:
                return (m[int(len(m)/2)] + m[(int(len(m)/2) + 1)])



    def get_average_rainfall_for_year(self, year):
        """ Returns the average rainfall in
            the given year across all months.
            Raises exception if year is not
            in table
        """
        sum = 0
        if year in self.table:
            months = self.table[year]
            for month in months:
                sum += float(month)
            return round(sum / 12, 2)
        else:
            raise ValueError("Value does not exist in list")

    def get_all_by_year(self, year):
        """ Returns the rainfall values for each
            month in the given year.  Raise exception
            if year is not found
        """
        if year not in self.table:
            raise ValueError("Year not in table?")
        else:
            for x in self.table[year]:
                yield x

    def get_all_by_month(self, month):
        """ Returns the rainfall values for each
            year during the given month.  Raise exception
            if month is not valid
        """
        if month > 12 or month < 0:
            raise ValueError("Month not in table?")
        else:
            m = []
            for x in self.table:
                months = self.table[x]
                m.append(months[month-1])
            for x in m:
                yield x

    def get_median_rainfall_for_year(self, year):
        """ Returns the median rainfall in
            the given year across all months.
            Raises exception if year is not
            in table
        """
        if year not in self.table:
            raise ValueError("Year does not exist in table")
        else:
            months = self.table[year]
            months.sort()
            return round((months[5] + months[6]) / 2, 2)

    def get_droughts(self) :
        """ returns a list of strings, representing date (month/year) ranges
            where three or more months in a row had at least 5% less rainfall than
            their historical monthly medians
        """
        count = 0
        droughts = []
        result = []
        for x in self.table:
            months = self.table[x]
            month_count = 0
            for d in months:
                median = self.get_median_rainfall_for_month(month_count)
                if median * .95 > d:
                    if count == 0:
                        next_month = month_count + 1
                        date = (str(next_month) + "/" + str(x))
                        droughts.append(date)
                    count += 1
                elif count >= 3 and median * .95 < d:
                    if month_count != 0:
                        date = (str(month_count) + "/" + str(x))
                        droughts.append(date)
                        result.append(tuple(droughts))
                        count = 0
                        droughts.clear()
                    elif month_count == 0:
                        prev_year = int(x) - 1
                        date = "12" + "/" + str(prev_year)
                        droughts.append(date)
                        result.append(tuple(droughts))
                        count = 0
                        droughts.clear()
                else:
                    count = 0
                month_count += 1
        return result

#table = RainfallTable("njrainfall.txt") # used this line to test on my PC, original is below
table = RainfallTable("../../data/njrainfall.txt")
print(table.get_rainfall(1993, 6))
print(table.get_average_rainfall_for_month(6))

for year in range(table.get_min_year(), table.get_max_year()+1) :
    print("Average rainfall in ", year, "=", table.get_average_rainfall_for_year(year))
    print("Median rainfall in ", year, "=", table.get_median_rainfall_for_year(year))
    print("===========")
    for rain in table.get_all_by_year(year):
        print(rain, end='\t')
    print("\n===========")


for month in range(1, 13) :
    print("Average rainfall in month", month, "=", table.get_average_rainfall_for_month(month))
    print("Median rainfall in month", month, "=", table.get_median_rainfall_for_month(month))
    print("===========")
    for rain in table.get_all_by_month(month):
        print(rain, end='\t')
    print("\n===========")

for d in table.get_droughts() :
    print("Drought:  ", d)
