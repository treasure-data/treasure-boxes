import os

print('Installing libs ...')
os.system("pip install --upgrade pip")
os.system("pip install pandas")

def generate_sample_df():
  import pandas as pd
  d = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Bonnie', 'Nicolle', 'Marlana', 'Bertha', 'Carlyn'],
        'city': ['New York','Chicago','Miami','New York','Miami'],
        'email': ['bonnie@example.com', 'nicolle@test.com', 'marlana@example.net', 'bertha@test.net', 'carlyn@example.org']
  }
  df = pd.DataFrame(data=d)
  return df

def add_col(df):
  print('Adding a new column ...')
  df['new_col'] = 'new data'
  print(df)

def drop_col(df):
  print('Dropping a column ...')
  df.drop(['new_col'], axis=1, inplace=True)
  print(df)

def edit_col(df):
  print('Editing a column ...')
  df['email'] = df['email'] = df['email'].str.split('@', expand=True)[0].replace('.','*',regex=True) + '@' + df['email'].str.split('@', expand=True)[1]
  print(df)

def filter_row(df):
  print('Filtering rows ...')
  print(df[df.city=='New York'])

def sample_row(df):
  print('Sampling rows ...')
  print(df.sample(frac=0.4))

def add_row(df):
  print('Adding a new row ...')
  print(df)

def output_csv(df):
  # Output file from DataFrame
  print('Outputting file as CSV into local ...')
  df.to_csv('file.csv', index=False)

def input_csv():
  import pandas as pd
  # Input file from local
  print('Inputting CSV file from local ...')
  df = pd.read_csv('file.csv', sep=',')
  print(df)
  return df

def output_json(df):
  # Output file from DataFrame
  print('Outputting file as JSON into local ...')
  df.to_json('file.json')

def input_json():
  import pandas as pd
  # Input file from local
  print('Inputting JSON file from local ...')
  df = pd.read_json('file.json')
  print(df)
  return df

def main():
  df = generate_sample_df()
  add_col(df)
  drop_col(df)
  edit_col(df)
  filter_row(df)
  sample_row(df)
  
  output_csv(df)
  input_csv()
  
  output_json(df)
  input_json()

