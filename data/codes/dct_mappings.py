""" This module processes the Short Description File to get the yearly variable names.
"""
import pandas as pd
import numpy as np
import shlex


def get_mappings():
    """ We process the mappings for two separate cases. (1) Variables that vary by year,
    and (2) variables where there are multiple realizations each year.
    """
    # Set up grid for survey years. Note that from 1996 we can only expect information every other
    # year. We start with 1978 as information about 1978 employment histories is collected with
    # the initial interview.
    years = range(1978, 2013)

    # time-constant variables
    dct_full = dict()

    dct_full.update(process_time_constant(years))

    dct_full.update(process_school_enrollment_monthly())
    dct_full.update(process_highest_degree_received())
    dct_full.update(process_multiple_each_year())
    dct_full.update(process_single_each_year())

    # Finishing
    return years, dct_full


def process_time_constant(years):
    """ We need to process some time-constant variables."""
    dct_constant = dict()

    dct_constant['RACE'] = dict()
    substrings = 'RACIAL/ETHNIC COHORT FROM SCREENER'
    for year in years:
        dct_constant['RACE'][year] = get_name(substrings)

    dct_constant['IDENTIFIER'] = dict()
    substrings = 'CASEID'
    for year in years:
        dct_constant['IDENTIFIER'][year] = get_name(substrings)

    dct_constant['SAMPLE_ID'] = dict()
    substrings = 'SAMPLE_ID'
    for year in years:
        dct_constant['SAMPLE_ID'][year] = get_name(substrings)

    dct_constant['GENDER'] = dict()
    substrings = 'SEX OF R'
    for year in years:
        dct_constant['GENDER'][year] = get_name(substrings)

    dct_constant['ROTTER_SCORE'] = dict()
    substrings = 'ROTTER SCALE SCORE'
    for year in years:
        dct_constant['ROTTER_SCORE'][year] = get_name(substrings)

    for i in range(1, 5):
        label = 'ROTTER_' + str(i)
        substrings = 'ROTTER-' + str(i) + 'A'
        dct_constant[label] = dict()
        for year in years:
            dct_constant[label][year] = get_name(substrings)

    dct_constant['ROSENBERG_SCORE'] = dict()
    substrings = 'SELF-ESTEEM SCORE'
    for year in years:
        dct_constant['ROSENBERG_SCORE'][year] = get_name(substrings)

    for i in range(1, 11):
        label = 'ROSENBERG_' + str(i)
        substrings = 'R030' + str(i + 34) + '.00'
        dct_constant[label] = dict()
        for year in years:
            dct_constant[label][year] = get_name(substrings)

    dct_constant['ASVAB_ARITHMETIC_REASONING'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 2-ARITHMETIC REASONING'
    for year in years:
        dct_constant['ASVAB_ARITHMETIC_REASONING'][year] = get_name(substrings)

    dct_constant['ASVAB_WORD_KNOWLEDGE'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 3-WORD KNOWLEDGE'
    for year in years:
        dct_constant['ASVAB_WORD_KNOWLEDGE'][year] = get_name(substrings)

    dct_constant['ASVAB_PARAGRAPH_COMPREHENSION'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 4-PARAGRAPH COMP'
    for year in years:
        dct_constant['ASVAB_PARAGRAPH_COMPREHENSION'][year] = get_name(substrings)

    dct_constant['ASVAB_NUMERICAL_OPERATIONS'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - SECTION 5-NUMERICAL OPERATIONS'
    for year in years:
        dct_constant['ASVAB_NUMERICAL_OPERATIONS'][year] = get_name(substrings)

    dct_constant['ASVAB_ALTERED_TESTING'] = dict()
    substrings = 'PROFILES, ASVAB VOCATIONAL TEST - NORMAL/ALTERED TESTING'
    for year in years:
        dct_constant['ASVAB_ALTERED_TESTING'][year] = get_name(substrings)

    dct_constant['AFQT_1'] = dict()
    substrings = 'PROFILES, ARMED FORCES QUALIFICATION TEST (AFQT) PERCENTILE SCORE - 1980'
    for year in years:
        dct_constant['AFQT_1'][year] = get_name(substrings)

    dct_constant['HIGHEST_GRADE_COMPLETED_FATHER'] = dict()
    substrings = 'HGC-FATHER'
    for year in years:
        dct_constant['HIGHEST_GRADE_COMPLETED_FATHER'][year] = get_name(substrings)

    dct_constant['HIGHEST_GRADE_COMPLETED_MOTHER'] = dict()
    substrings = 'HGC-MOTHER'
    for year in years:
        dct_constant['HIGHEST_GRADE_COMPLETED_MOTHER'][year] = get_name(substrings)

    # TODO: We need to reconstruct the Rosenberg and Rotter scores based on the individual items
    # as a test for the dataset.

    return dct_constant


def process_multiple_each_year():
    """ Employment Status for multiple weeks.
    """
    dct_multiple = dict()

    # The mapping between the continuous weeks counter and the calendar year is provided on the
    # NLSY website.
    mapping_continuous_week = pd.read_pickle('input/continuous_week_crosswalk_2012.pkl')
    years = mapping_continuous_week['Week Start: \nYear'].unique()

    # Prepare container
    year_weeks = dict()
    for year in years:
        year_weeks[year] = []

    for index, row in mapping_continuous_week.iterrows():
        year = row['Week Start: \nYear']
        year_weeks[year] += [row['Continuous \nWeek Number']]

    # We now process employment information for some selected weeks.
    weeks = [1, 7, 13, 14, 20, 26, 40, 46, 52]

    for type_ in ['STATUS', 'HOURS']:
        for week in weeks:
            label, idx = 'EMP_' + type_ + '_WK_' + str(week), week - 1
            dct_multiple[label] = dict()
            for year in years:
                substring = 'WEEK ' + str(year_weeks[year][idx])
                if type_ == 'STATUS':
                    substrings = ['LABOR FORCE STATUS', substring]
                elif type_ == 'HOURS':
                    substrings = ['HOURS AT ALL JOBS', substring]
                else:
                    raise AssertionError
                dct_multiple[label][year] = get_name(substrings)

    return dct_multiple


def process_single_each_year():
    """ We process variables that vary by year, i.e. one variables is available each year.
    """
    # Initialize containers
    dct = dict()

    ''' TOTAL INCOME FROM MILITARY SERVICE
    '''
    substrings = 'TOTAL INCOME FROM MILITARY SERVICE'
    dct['INCOME_MILITARY'] = get_year_name(substrings)

    ''' HOURLY RATE OF PAY JOB ##
    '''
    for i in range(1, 6):
        substrings = 'HOURLY RATE OF PAY JOB #0' + str(i)
        dct['WAGE_HOURLY_JOB_' + str(i)] = get_year_name(substrings)

    ''' ENROLLMENT STATUS AS OF MAY 1 SURVEY YEAR (REVISED)
    '''
    substrings = 'ENROLLMENT STATUS AS OF MAY 1 SURVEY YEAR (REVISED)'
    dct['ENROLLMENT_STATUS'] = get_year_name(substrings)

    ''' HIGHEST GRADE ATTENDED
    '''
    substrings = 'HIGHEST GRADE ATTENDED'
    dct['HIGHEST_GRADE_ATTENDED'] = get_year_name(substrings)

    ''' HIGHEST GRADE COMPLETED
    '''
    substrings = 'HIGHEST GRADE COMPLETED AS'
    dct['HIGHEST_GRADE_COMPLETED'] = get_year_name(substrings)

    ''' YEAR OF BIRTH
    '''
    substrings = 'DATE OF BIRTH - YEAR'
    dct['YEAR_OF_BIRTH'] = get_year_name(substrings)

    ''' MONTH OF BIRTH
    '''
    substrings = 'DATE OF BIRTH - MONTH'
    dct['MONTH_OF_BIRTH'] = get_year_name(substrings)

    ''' CPSOCC70
    '''
    substrings = 'OCCUPATION AT CURRENT JOB/MOST RECENT JOB (70 CENSUS 3 DIGIT)'
    dct['CPSOCC70'] = get_year_name(substrings)

    ''' OCCALL70
    '''
    for i in range(1, 6):
        substrings = ['OCCUPATION (CENSUS 3 DIGIT, 70 CODES)', 'JOB #0' + str(i)]
        dct['OCCALL70_JOB_' + str(i)] = get_year_name(substrings)

    # In the year 1993, the substring is changed for some reason and cannot be easily
    # distinguished from the CPSOCC70 variable.
    for i in range(2, 6):
        substrings = 'OCCUPATION (CENSUS 3 DIGIT) JOB #0' + str(i)
        dct['OCCALL70_JOB_' + str(i)].update(get_year_name(substrings))

    # In the year 1982, the substring for the fourth job contains a 0 instead of an O.
    substrings = ['OCCUPATION (CENSUS 3 DIGIT, 70 C0DES)', 'JOB #04']
    dct['OCCALL70_JOB_4'].update(get_year_name(substrings))

    ''' LINKING OCALLEMP70 and CPSOCC7
    '''
    for i in range(1, 6):
        substrings = ['IS JOB #0' + str(i) + ' SAME AS CURRENT JOB?']
        dct['CPS_JOB_INDICATOR_JOB_' + str(i)] = get_year_name(substrings)

    ''' REASONS FOR NON-INTERVIEW
    '''
    substrings = ['REASON FOR NONINTERVIEW']
    dct['REASON_NONINTERVIEW'] = get_year_name(substrings)

    return dct


def get_name(substrings):
    """ Search through the file by substrings
    """
    # We allow to pass in a string or a list of strings that are checked in the variable
    # descriptions.
    if type(substrings) == str:
        substrings = [substrings]

    with open('input/original.sdf', 'r') as infile:
        for line in infile.readlines():
            is_relevant = [substring in line for substring in substrings]
            is_relevant = np.all(is_relevant)
            if not is_relevant:
                continue
            # This special treatment is only required due to the string that identifiers RACE.
            line = line.replace("'", '')
            list_ = shlex.split(line)
            name = list_[0].replace('.', '')

            return name

    raise AssertionError('Substrings not found ...')


def get_year_name(substrings):
    """ Search through the file by substrings."""
    # We allow to pass in a string or a list of strings that are checked in the variable
    # descriptions.
    if type(substrings) == str:
        substrings = [substrings]

    container = dict()
    with open('input/original.sdf', 'r') as infile:
        for line in infile.readlines():
            is_relevant = [substring in line for substring in substrings]
            is_relevant = np.all(is_relevant)
            if is_relevant:
                list_ = shlex.split(line)
                name = list_[0].replace('.', '')
                year = int(list_[1])
                container[year] = name

    return container


def process_highest_degree_received():
    """ This function processes the information on the highest degree ever received. There are
    two different variable in some years with the same information.
    """
    def read_highest_degree_received():
        """ This method reads in the variable names for the highest grade received.
        """
        rslt = dict()
        with open('input/original.sdf', 'r') as infile:
            for line in infile.readlines():
                is_relevant = 'HIGHEST DEGREE EVER RECEIVED' in line

                if not is_relevant:
                    continue

                list_ = shlex.split(line)
                variable, year = list_[0].replace('.', ''), int(list_[1])
                if year not in rslt.keys():
                    rslt[year] = []

                rslt[year] += [variable]

        return rslt

    rslt = read_highest_degree_received()

    dct = dict()
    for year in rslt.keys():
        for val in rslt[year]:
            label = 'HIGHEST_DEGREE_RECEIVED_1'
            if label in dct.keys():
                if year in dct[label].keys():
                    label = 'HIGHEST_DEGREE_RECEIVED_2'
            if label not in dct.keys():
                dct[label] = dict()
            dct[label][year] = val

    return dct


def process_school_enrollment_monthly():
    """ This function processes the monthly school enrollment data. This is surprisingly
    difficult as, for example, information about March 1990 is asked in the surveys of 1990 and
    1991.
    """
    def read_school_enrollment_monthly():
        """ Search for the information in the short description file.
        """
        rslt = dict()
        with open('input/original.sdf', 'r') as infile:
            for line in infile.readlines():
                is_relevant = 'MONTHS ENROLLED IN SCHOOL SINCE LAST INT' in line
                is_relevant = np.all(is_relevant)

                if not is_relevant:
                    continue

                list_ = shlex.split(line)

                # Collect information
                variable, month = list_[0].replace('.', ''), list_[10]

                if 'R09052.00' in line:
                    month, year = list_[12], int(list_[13])
                # There are some typos in the variable descriptions
                elif 'INT-' in line:
                    month, year = list_[9], int(list_[10])
                else:
                    year = int(list_[11])

                # The labeling convention for the year are all over the place. For example 2012
                # does show up as 12 as well.
                if 0 <= year < 25:
                    year += 2000
                elif 70 < year < 100:
                    year += 1900
                else:
                    pass

                # The labeling convention for the month is not consistent.
                if 'JAN' in month:
                    month = 'JANUARY'
                elif 'FEB' in month:
                    month = 'FEBRUARY'
                elif 'MAR' in month:
                    month = 'MARCH'
                elif 'APR' in month:
                    month = 'APRIL'
                elif 'MAY' in month:
                    month = 'MAY'
                elif 'JUN' in month:
                    month = 'JUNE'
                elif 'JUL' in month:
                    month = 'JULY'
                elif 'AUG' in month:
                    month = 'AUGUST'
                elif 'SEP' in month:
                    month = 'SEPTEMBER'
                elif 'OCT' in month:
                    month = 'OCTOBER'
                elif 'NOV' in month:
                    month = 'NOVEMBER'
                elif 'DEC' in month:
                    month = 'DECEMBER'
                else:
                    raise AssertionError

                if year not in rslt.keys():
                    rslt[year] = dict()
                if month not in rslt[year].keys():
                    rslt[year][month] = []

                rslt[year][month] += [variable]

        return rslt

    rslt = read_school_enrollment_monthly()
    dct = dict()
    for year in rslt.keys():
        for month in rslt[year].keys():
            for val in rslt[year][month]:
                label = 'ENROLLED_SCHOOL_' + month + '_1'

                if label in dct.keys():
                    if year in dct[label].keys():
                        label = 'ENROLLED_SCHOOL_' + month + '_2'

                if label not in dct.keys():
                    dct[label] = dict()

                dct[label][year] = val

    return dct