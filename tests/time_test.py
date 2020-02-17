from perylune import time

def test_leap_year():
    # Tests if certain years are properly detected as leap years.
    values = [ [2000, True], [2019, False], [2001, False], [2004, True], [1900, False], [2100, False]]

    for _, row in enumerate(values):
        assert time.leap_year(row[0]) == row[1]

def test_leap_years():
    values = [ [2000, 2000, 0], [2000, 2001, 1], [2000, 2010, 3], [2000, 2100, 25] ]

    for _, row in enumerate(values):
        assert time.leap_years(row[0], row[1]) == row[2]

def test_days_0():
    days = time.days(1999,12,31,0.0)
    assert days == 0.0

def test_days_2019_09_22():
    days = time.days(2019, 9, 22, 0)
    expected = 19*365 + 5 # 19 years, five leap years (2000, 2004, 2008, 2012, 2016)
    expected += 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 # Full months since beginning of the year.
    expected += 21 # 21 full days since beginning of the year.
    expected += 1 # Because 2000-Jan-1 was day number 1
    assert days == expected

def test_days_2019_09_22_15h55m():
    days = time.days(2019, 9, 22, 15 + (55/60))
    expected = 19*365 + 5 # 19 years, five leap years (2000, 2004, 2008, 2012, 2016)
    expected += 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 # Full months since beggining of the year.
    expected += 21 # 21 full days since beginning of the year.
    expected += 1 # Because 2000-Jan-1 was day number 1
    expected += 15/24 + 55/(24*60) # 15h 55mins
    assert days == expected
