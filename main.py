from bs4 import BeautifulSoup
import requests
import pandas
from time import sleep

# PART 1

# Send a GET request to the web page with a user-agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Connection': 'keep-alive'
}

data_dict = {
    'rank': [],
    'major': [],
    'degree': [],
    'early career pay': [],
    'mid career pay': [],
    'percent high meaning': [],
}

page = 0
while page < 33:
    sleep(5)
    page += 1
    response = requests.get(f'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{page}', headers=headers)
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    all_values = soup.find_all(name="span", class_='data-table__value')

    i = 0
    for value in all_values:
        print(value.get_text())
        i += 1
        if i == 1:
            data_dict['rank'].append(value.get_text())
        elif i ==2:
            data_dict['major'].append(value.get_text())
        elif i == 3:
            data_dict['degree'].append(value.get_text())
        elif i ==4:
            data_dict['early career pay'].append(int(value.get_text().replace('$', '').replace(',', '')))
        elif i ==5:
            data_dict['mid career pay'].append(int(value.get_text().replace('$', '').replace(',', '')))
        elif i ==6:
            try:
                  data_dict['percent high meaning'].append(int(value.get_text().strip('%')))
            except ValueError:
                  data_dict['percent high meaning'].append(0)

        if i == 6:
            i = 0

print(data_dict)
all_data = pandas.DataFrame(data_dict)
all_data.to_csv('all_data.csv')

# PART 2

# all_data = pandas.read_csv('all_data.csv')

# Make adjustments to the table - delete first column with redundant numbers and add 'spread' column
all_data = all_data.drop(all_data.columns[0], axis=1)
if 'spread' not in all_data.columns:
    spread_col = all_data['mid career pay'] - all_data['early career pay']
    all_data.insert(1, 'spread', spread_col)

# Show NaN data and delete it from the table
print(f'\nShow NaN data\n{all_data.isna()}')
all_data = all_data.dropna()

# Show all desired data results
print(f'\nFirst five rows\n{all_data.head()}')

print(f'\ntable size\n{all_data.shape}')

print(f'\nNames of columns\n{all_data.columns}')

print(f'\nLast five rows\n{all_data.tail()}')

print(f"\nShow Major with highest starting pay\n {all_data['major'].loc[all_data['early career pay'].idxmax()]} "
      f"Salary: ${all_data['early career pay'].max()}")

print(f"\nShow Major with highest mid-career pay\n {all_data['major'].loc[all_data['mid career pay'].idxmax()]} "
      f"Salary: ${all_data['mid career pay'].max()}")

print(f"\nShow Major with lowest starting pay\n {all_data['major'].loc[all_data['early career pay'].idxmin()]} "
      f"Salary: ${all_data['early career pay'].min()}")

print(f"\nShow Major with lowest mid-career pay\n {all_data['major'].loc[all_data['mid career pay'].idxmin()]} "
      f"Salary: ${all_data['mid career pay'].min()}")

low_increase = all_data.sort_values('spread')
print(f"\nTop five majors with lowest salary increase\n{low_increase[['major', 'spread']].head()}")

high_increase = all_data.sort_values('spread', ascending=False)
print(f"\nTop five majors with highest salary increase\n{high_increase[['major', 'spread']].head()}")

highest_salary_and_meaning = all_data.sort_values(['mid career pay','percent high meaning'], ascending=[False, False])
print(f"\nTop five majors with highest pay and meaning\n{highest_salary_and_meaning[['major', 'mid career pay', 'percent high meaning']].head()}")

