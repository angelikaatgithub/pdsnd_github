import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see data for Chicago, New York City or Washington?\n').lower()
    
    while True:
         if city in CITY_DATA:
                break
         else:
            city = input('\nPlease type in a valid city(\'Chicago\', \'New York City\' or \'Washington\'?\n').lower()
            continue
                 
    # get user input for month (all, january, february, ... , june)
    month = input('\nPlease type in a valid month (\'all\',\'january\'-\'june\')?\n').lower()
    
    while True:
        if month in MONTH_DATA or month == 'all':
            break
        else:
             month = input('\nPlease type in a valid month (\'all\' or \'january\'-\'june\')?\n').lower()
             continue
            

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWould you like to see all days or just one specific day(\'all\',\'monday\'-\'sunday\')?\n').lower()
    
    while True:
        if day in DAY_DATA or day == 'all':
            break
        else:
            day = input('\nPlease type in a valid day (\'all\',\'monday\'-\'sunday\')?\n').lower()
            continue

    print('-'*40)
    return city, month, day
                              
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

      
    # display the most common month
    popular_month = df['month'].mode()
    print('Most Frequent Month:', popular_month.to_string(index=False))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()
    print('Most Frequent Day:', popular_day.to_string(index=False))

    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()
    print('Most popular Start Station:', popular_start.to_string(index=False)) 

    # display most commonly used end station
    popular_end = df['End Station'].mode()
    print('Most popular End Station:', popular_end.to_string(index=False))

    #display most frequent combination of start station and end         station trip
    #df['trip'] = df[['Start Station', 'End Station']].agg('          '.join, axis=1)
    #popular_trip = df['trip'].mode()
    #print('Most popular trip:',                                     #popular_trip.to_string(index=False))
    
    popular_combi = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most popular trip:', popular_combi.to_string())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nTotal Travel Time:', total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\nMean Travel Time:', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print('\nCounts for each User Type:\n',user_types.to_string())

    # Display counts of gender
    if len(df.columns)== 12:
        gender_types = df['Gender'].value_counts()
        print('\nCounts for each Gender:\n', gender_types.to_string())
    else:
        print('\nGender data not available!')
        
    # Display earliest, most recent, and most common year of birth
    if len(df.columns)== 12:
        earliest_yob = df['Birth Year'].min()
        latest_yob = df['Birth Year'].max()
        popular_yob = df['Birth Year'].mode()
        print('\nEarliest Year of Birth:\n', earliest_yob)
        print('\nMost Recent Year of Birth:\n', latest_yob)
        print('\nMost popular Year of Birth:\n', popular_yob.to_string(index=False))
    else:
        print('\nYear of Birth data not available!')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of data at a time."""

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data != 'no'):
        if view_data != 'yes':
            print('\nThis is not a valid entry. Please try again!\n')
            view_data = input("Do you wish to continue?: ").lower()
        elif view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'no' and restart.lower() != 'yes':
            restart = input('\nPlease type in a valid entry! Would you like to restart? Enter yes or no.\n')
        elif restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
