# Perylune
# by Tomek Mrugalski

# Source: https://stjarnhimlen.se/comp/ppcomp.html

def leap_year(y):
    if not y%400:
        return True
    if not y%100:
        return False
    if y%4:
        return False
    else:
        return True


def leap_years(min, max):
    """Returns number of leap years between year X and Y"""
    if min > max:
        min,max = max,min

    leap = 0
    for i in range(min,max):
        if leap_year(i):
            leap += 1

    return leap

def days(y, m, d, ut = 0.0):
    """Calculates number of days since 2000 Jan 1 0.0 UT"""
    # y - year, e.g. 2019
    # m - month (1-12), e.g. 9
    # d - day of the month (1-31), e.g. 22
    # ut - universal time, 0.0... 23.99999 - expressed in hours. Minutes and seconds expressed as a fraction of hour

    # Simple equation valid for March 1900 - Feb 2100.
    #days = 367*y - 7 * int(( y + int((m+9)/12) ) / 4) + int(275*m/9) + d - 730530

    # More complex formula valid over the entire Gregorian Calendar.
    days = 367*y - 7 * int(( y + int((m+9)/12) ) / 4) + int(275*m/9) - int(3 * ( int(( y + int((m-9)/7) ) / 100) + 1 ) / 4) + d - 730515

    days = days + ut/24.0

    return days



