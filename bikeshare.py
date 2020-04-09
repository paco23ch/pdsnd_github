import time
import pandas as pd
import numpy as np

"""
Defining some global variables in order to easily validate user input.
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
DAY_OF_WEEK = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = None
    month = None
    day = None

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while city is None:
        city = input('Please type \'all\' or select a city to analyze: {}: '.format(CITY_DATA.keys())).lower()
        if city not in CITY_DATA.keys() and city != 'all':
            city = None
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while month is None:
        month = input('Please select a month to load {}: '.format(MONTHS)).lower()
        if month not in MONTHS:
            month = None
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while day is None:
        day = input('Please select a day of the week to load {}: '.format(DAY_OF_WEEK)).lower()
        if day not in DAY_OF_WEEK:
            day = None
        else:
            break

    print('-'*40)
    return city, month, day


def select_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('Loading data .... ')
    df = None
    load_df = {}

    for cities in CITY_DATA.keys():
        if city == cities or city == 'all':
            print('Loading {}...'.format(cities))
            load_df[cities] = pd.read_csv(CITY_DATA[cities])
            load_df[cities]['city'] = cities
            #print(load_df[cities].isnull().any())
    
    df = pd.concat(load_df.values(),sort=False)

    #Transform date/times to datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #add the month and day_of_week to be used as filters
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Applying month filters
    if month is not None and month != 'all':
        print('Filtering for month={}....'.format(month))
        df = df[df['month']==MONTHS.index(month)]

    #Applying day filters
    if day is not None and day != 'all':
        print('Filteromg fpr dahy={}....'.format(day))
        df = df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: {}'.format(df['month'].mode()[0]))

    # TO DO: display the most common day of week
    print('The most common day of week is: {}'.format(df['day_of_week'].mode()[0].title()))

    # TO DO: display the most common start hour
    print('The most common hour to start a trip is: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station is: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most commonly used end station is: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('The most commonly combination of stations is: {}'.format((df['Start Station']+' > '+df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is: {}'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('Average travel time is: {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.
        In this function we use the try-except block to identify when a column is missing and prevent calculation errors."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # TO DO: Display counts of user types
        print('The user type distribution: {}'.format(df.groupby('User Type')['User Type'].count()))

        # TO DO: Display counts of gender
        print('\nThe gender distribution: {}\n'.format(df.groupby('Gender')['Gender'].count()))

        # TO DO: Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is: {}'.format(df['Birth Year'].min()))
        print('The most recent year of birth is: {}'.format(df['Birth Year'].max()))
        print('The most common year of birth is: {}'.format(df['Birth Year'].mode()[0]))
    except:
        print('\n**ERROR: The data for Gender and Birth Year is not availble for this state.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    print('\nDataFrame size is {}'.format(df.size))
    print('DataFrame shape is {}'.format(df.shape))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print(df.shape[0])
    i=0
    see_raw = ''
    while see_raw != 'no' and i < df.shape[0]:
        try:
            to = i + 5 if i + 5 <= df.shape[0]-1 else df.shape[0]-1
            print(df[i:to])
            see_raw = input('Continue? (no to stop) ... ')
            if see_raw == 'no':
                return
            i += 5
        except:
            return

def main():
    while True:
        city, month, day = get_filters()
        df = select_data(city, month, day)

        #Based pm the filters selected, we may have an empty DataFrame.
        if df.size != 0:
            option = 1
            while option:
                try:                    
                    print('\n\nPlease select an option:')
                    print('1. Time stats')
                    print('2. Station stats')
                    print('3. Trip duration stats')
                    print('4. User Stats')
                    print('5. View raw data')
                    print('6. End analysis for this set')
                    option = int(input('===> '))
                    
                    if option == 1:
                        time_stats(df)
                    elif option == 2:
                        station_stats(df)
                    elif option == 3:
                        trip_duration_stats(df)
                    elif option == 4:
                        user_stats(df)
                    elif option == 5:
                        show_raw_data(df)
                    elif option == 6:
                        break

                    #input('Press enter to continue ... ')
                except:
                    option = 1
        else:
            print('Data not available for this combination of values')


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()