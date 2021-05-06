#!/usr/bin/env python
import sys, os
import time
import random
import datetime

# Set date range (leave as int, datetime needs int)
_SYEAR = 2021
_EYEAR = 2021
_SMONTH = 7
_EMONTH = 7
_SDAY = 6
_EDAY = 7

_FAB = dict()
_FAB['AMER'] = ['Phoenix-FAB12', 'Austin-FAB3', 'Austin-FAB18']
_FAB['TAIW'] = ['TW-FAB25', 'TW-FAB3', 'TW-FAB8', 'TW-FAB42', 'TW-FAB11']
_FAB['ALL'] = _FAB['AMER'] + _FAB['TAIW']

##_FAB['ALL'] = ['Austin-FAB3']
_NUM_FABS = len(_FAB['ALL'])

_FAILURE_TYPE = ['Center', 'Donut', 'Edge-Loc', 'Edge-Ring', 'Loc', 'Random', 'Near-full', 'Scratch']

##_FAILURE_TYPE = ['Edge-Ring']
_NUM_FAILURES = len(_FAILURE_TYPE)

_MIN_WAFER_PER_LOT = 2
_MAX_WAFER_PER_LOT = 30

_MIN_TEMP = 10
_MAX_TEMP = 14

_MIN_DIES_PER_WAFER = 12
_MAX_DIES_PER_WAFER = 100

_WAFER_FAILURE_RATE_MIN = 0
_WAFER_FAILURE_RATE_MAX = 30

# this controls how much data is produced
_NUM_LOTS = 50


def get_failure_date(start_date=None, end_date=None):

    if start_date is None:
        start_date = (datetime.date(_SYEAR, _SMONTH, _SDAY))
        end_date = (datetime.date(_EYEAR, _EMONTH, _EDAY))
    time_date_between = end_date - start_date
    days_between = time_date_between.days
    random_days = random.randrange(days_between)
    failure_date = start_date + datetime.timedelta(days=random_days)

    return failure_date


def get_failure_time(start_time=None, end_time=None):

    if start_time is None:
        start_time = (datetime.datetime(1, 1, 1, 5, 00, 00))
        end_time = (datetime.datetime(1, 1, 1, 23, 59, 59))
    time_date_between = end_time - start_time
    time_between = time_date_between.seconds
    random_time = random.randrange(time_between)
    failure_time = start_time + datetime.timedelta(seconds=random_time)

    return failure_time.strftime("%H:%M:%S")


def get_fab():
    random_fab = random.randrange(_NUM_FABS)   ## Starts at 0
    for n,fab in enumerate(_FAB['ALL']):
        if random_fab == n:
            return fab


def get_fab_loc(fab):
    if fab in _FAB['AMER']:
        return 'AMER'
    if fab in _FAB['TAIW']:
        return 'TAIW'


def get_failure_type():
    random_failure = random.randrange(_NUM_FAILURES)
    return _FAILURE_TYPE[random_failure]


def get_total_wafer_num():
    random_wafer = random.randrange(_MIN_WAFER_PER_LOT,_MAX_WAFER_PER_LOT)
    return random_wafer


def get_temp():
    random_temp = random.randrange(_MIN_TEMP,_MAX_TEMP)
    return random_temp


def get_dies_per_wafer():
    random_dies = random.randrange(_MIN_DIES_PER_WAFER,_MAX_DIES_PER_WAFER)
    return random_dies


def get_failure_rate():
    random_failure_rate = random.randrange(_WAFER_FAILURE_RATE_MIN, _WAFER_FAILURE_RATE_MAX)
    return random_failure_rate/100


def get_failure_list(total_wafers, failure_rate):
    failure_list = list()
    total_num_failed_wafers = round(total_wafers * failure_rate)

    for n in range(0, total_num_failed_wafers):
        random_failed_wafer = random.randrange(1, total_wafers)
        if random_failed_wafer not in failure_list:
            failure_list.append(random_failed_wafer)

    return failure_list


def main():
    rc = 0

    header = ('Lot Date',
              'Failure Time',
              'Fab location',
              'Fab Name',
              'Lot Number',
              'Failure type',
              'Total Wafers',
              'Total Failed Wafers',
              'Wafer Number',
              'Equipment Temperature',
              'Expected Dies per Wafer',
              'Actual Dies per Wafer'
              )

    print(','.join(header))
    lot_number = 1
    while lot_number <= _NUM_LOTS:

        fab = get_fab()
        fab_loc = get_fab_loc(fab)

        wafer_count = 1
        expected_dies = int(get_dies_per_wafer())
        dies_failure_count_min = expected_dies - (.3 * expected_dies)
        dies_failure_count_max = expected_dies - (.05 * expected_dies)
        total_num_wafers = get_total_wafer_num()
        lot_date = get_failure_date()
        wafer_failure_list = get_failure_list(total_num_wafers, get_failure_rate())
        total_num_failed_wafers = len(wafer_failure_list)

        for bad_wafer_num in sorted(wafer_failure_list):
            actual_dies = random.randrange(int(dies_failure_count_min), int(dies_failure_count_max))
            print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}"
                  .format(lot_date,
                          get_failure_time(),
                          fab_loc,
                          fab,
                          lot_number,
                          get_failure_type(),
                          total_num_wafers,
                          total_num_failed_wafers,
                          bad_wafer_num,
                          get_temp(),
                          expected_dies,
                          actual_dies
                         )
                  )
            wafer_count += 1
        lot_number += 1
    return rc


if __name__ == "__main__":
    sys.exit(main())


