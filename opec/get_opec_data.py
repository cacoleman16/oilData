import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

PATH = "" #Driver path here
OUTPUT_PATH = "" #excel file path here


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
        df['text'] = first_split[0]
        df = df[['date', 'title', 'text']]
        df['date'] = pd.to_datetime(df.date)
        df.to_excel(OUTPUT_PATH + "opec_press_release.xlsx", na_rep='NaN')


def main():
    opec_data = get_opec_data()
    if os.path.isfile(OUTPUT_PATH + 'opec_press_release_raw.xlsx') == True:
        df = pd.read_excel(OUTPUT_PATH + 'opec_press_release_raw.xlsx')

    else:
        df = opec_data.get_data_from_web()
    opec_data.process_opec(df)


if __name__ == "__main__":
    main()


