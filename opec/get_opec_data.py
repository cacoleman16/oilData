import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
import datetime as dt
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
# pylint:disable=E1101

# I need to see about march 16, 2017 and there's a duplicate at the end
# Sets up a caldender to check if dates are holidays

dr = pd.date_range(start='2002-01-01', end='2020-12-12')
dates = pd.DataFrame()
dates['Date'] = dr
cal = calendar()
holidays = cal.holidays(start=dr.min(), end=dr.max())


# These were dates that didn't follow an easy rule in the search
missing_date1 = dt.datetime(2011, 6, 8)
missing_date2 = dt.datetime(2016, 12, 10)
missing_date3 = dt.datetime(2017, 11, 30)
delete_date = dt.datetime(2017, 3, 16)
PATH =
OUTPUT_PATH = 


class get_opec_data():

    def get_data_from_web(self):
        try:
            driver = webdriver.Chrome(PATH)
            time.sleep(1)
            driver.get('https://www.opec.org/opec_web/en/press_room/28.htm')
            time.sleep(1)
        # from random import randint
        # from time import sleep

        # sleep(randint(10,100))
            print(driver.title)
            time.sleep(1)
            df = []
            end_year = 2020
            start_year = 2002
            for year in range(0, end_year - start_year+2):
                select = Select(driver.find_element_by_xpath(
                    "//*[@id='aside']/div[3]/div/div/select"))
                select.options[year].click()
                print(driver.title)
                articles = (driver.find_elements_by_class_name("article"))
                for article in articles:
                    df.append(article.text)
                time.sleep(3)
                driver.get(
                    'https://www.opec.org/opec_web/en/press_room/28.htm')

        finally:
            driver.quit()
            # print(df)
            df = pd.DataFrame(df, columns=['PressReleaseText'])
            df.to_excel(
                OUTPUT_PATH + "opec_press_release_raw.xlsx", na_rep='NaN')

        return df
    # Reutrns an excel file with the date, titlte and text for each announcement

    def process_opec(self, df):
        first_split = df['PressReleaseText'].str.split("|", n=2, expand=True)
        second_split = first_split[0].str.split("\n", n=2, expand=True)
        df['title'] = second_split[0]
        df['date'] = second_split[1]
        df['text'] = first_split[1]
        df2 = df[['date', 'title', 'text']].copy()
        df2['date'] = pd.to_datetime(df.date)
        df2.to_excel(OUTPUT_PATH + "opec_press_release.xlsx",
                     na_rep='NaN', index=False)
        return df2

    def filter_dates(self, df):

        # Convoluted function that print date list for Matlab
        df['lower_title'] = df['title'].str.lower()
        df['lower_text'] = df['text'].str.lower()
        df = df.sort_values(by=['date'])
        # date2 removes holidays and weekends
        df['date2'] = df['date']
        df.loc[(df['date'].isin(holidays) == True),
               'date2'] = df['date'] + pd.Timedelta(days=1)
        df.loc[(df['date'].dt.weekday == 5),
               'date2'] = df['date'] + pd.Timedelta(days=2)
        df.loc[(df['date'].dt.weekday == 6),
               'date2'] = df['date'] + pd.Timedelta(days=1)
        df["meeting"] = df['lower_text'].str.extract(
            r'(\d+(rd|th|st|nd).*?meeting)')[0]
        df["sanity_check"] = df['lower_title'].str.extract(
            r'([0-9]+(rd|th|st|nd).*?meeting)')[0]
        df.loc[df.meeting.isnull(), ['meeting', 'sanity_check']
               ] = df['lower_text'].str.extract(r'(^.*?consultative.*?meeting)')[0]
# before I remove duplicates, let's try getting rid of extraordinary
        df.loc[(df['date'] == missing_date1), [
            'meeting', 'sanity_check']] = '159th meeting'
        df.loc[(df['date'] == missing_date2), ['meeting', 'sanity_check']
               ] = 'OPEC and non-OPEC ministerial meeting'
        df.loc[(df['date'] == missing_date3), [
            'meeting', 'sanity_check']] = '173rd meeting'
        # Doubles 1 and 2 get rid of extra words to compare them,
        # they're the same as meeting/sanity check
        df['doubles1'] = df.meeting
        df['doubles2'] = df.sanity_check
        df.doubles1 = df.doubles1.str.replace(
            " (extraordinary) ", " ", regex=False)
        df.doubles2 = df.doubles2.str.replace(
            " (extraordinary) ", " ", regex=False)
        df = df[~ (df.meeting.notnull() & df.sanity_check.isnull())]
        # more cleaning the data
        df = df[(~ df.doubles1.duplicated()) & (~ df.doubles2.duplicated()) | (
            df['meeting'].isnull()) | (df.doubles1.str.contains("consultative"))]
        df = df.dropna(subset=['doubles1'])
        df['Year'] = pd.DatetimeIndex(df['date2']).year
        df['Month'] = pd.DatetimeIndex(df['date2']).month
        df['Day'] = pd.DatetimeIndex(df['date2']).day
        new_df = df[['Day', 'Month', 'Year']].copy()
        # lazy way of dropping last row
        new_df.drop(new_df.tail(1).index, inplace=True)

        new_df.to_excel(
           OUTPUT_PATH + "opec_dates.xlsx", index=False)


# def breakup_dates(df):
#     df = df.copy()
#     df['Year'] = pd.DatetimeIndex(df['date2']).year
#     df['Month'] = pd.DatetimeIndex(df['date2']).month
#     df['Day'] = pd.DatetimeIndex(df['date2']).day
#     return df[['Day', 'Month', 'Year']]


def main():
    opec_data = get_opec_data()
    if os.path.isfile(OUTPUT_PATH + 'opec_press_release_raw.xlsx') == True:
        df = pd.read_excel(OUTPUT_PATH + 'opec_press_release_raw.xlsx', header=False))

    else:
        df = opec_data.get_data_from_web()

    df = opec_data.process_opec(df)
    opec_data.filter_dates(df)


if __name__ == "__main__":
    main()


