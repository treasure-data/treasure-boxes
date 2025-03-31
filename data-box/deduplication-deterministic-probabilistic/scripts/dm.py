import os

import pandas as pd
import hashlib
import pytd

def main(**kwargs):
  tdAPIkey = os.getenv("TD_API_KEY")
  tdAPIendpoint = os.getenv("TD_API_ENDPOINT")
  database = kwargs.get('db')
  src_table = kwargs.get('clean_tbl')
  out_table = kwargs.get('dm_tbl')

  td = pytd.Client(apikey=tdAPIkey, 
              endpoint=tdAPIendpoint, 
              database=database, 
              default_engine='presto')

  # Create a dataframe by importing data from Treasure Data database.
  res = td.query(f'SELECT cl_cc, cl_phone, cl_email, cl_customer_name, cl_full_address, cl_city, cl_vin FROM {database}.{src_table}')
  df = pd.DataFrame(**res)

  # Init
  dedup_list = []
  counts = []
  customer_code_col = 'cl_cc'
  phone_col = 'cl_phone'
  email_col = 'cl_email'
  name_col = 'cl_customer_name'
  address_col = 'cl_full_address'
  canonical_id_col = 'td_id'
  step_col = 'step'
  city_col = 'cl_city'
  vin_col = 'cl_vin'
  other_cc_col = 'cc_other'
  other_vin_col = 'vin_other'
  hash_cols = [customer_code_col, phone_col, email_col, name_col, address_col]

  # Unique, not null phones
  def check_phone_dup(phone):
      if pd.isna(phone):
          return True
      else:
          return len(df[df[phone_col] == phone]) > 1

  # Non-unique, not null phones; not null emails; phone isn't used in any other phone + email combination
  def check_phone_email_dup(phone, email):
      if pd.isna(email) or pd.isna(phone):
          return True
      else:
          if len(df[df[phone_col] == phone]) == 1:
              return True
          else:
              df_multi_ph_check = df[df[phone_col] == phone]
              df_multi_ph_em_check = df[(df[phone_col] == phone) & (df[email_col] == email)]
              if len(df_multi_ph_check) != len(df_multi_ph_em_check):
                  return True
              else:
                  return False

  # Non-unique, not null phones; not null names and addresses; emails don't matter
  def check_name_address_dup(phone, name, address):
      if pd.isna(name) or pd.isna(address) or pd.isna(phone):
          return True
      else:
          if len(df[df[phone_col] == phone]) == 1:
              return True
          else:
              df_multi_ph_check = df[df[phone_col] == phone]
              df_multi_ph_name_addr_check = df[(df[phone_col] == phone) & (df[address_col] == address) & (df[name_col] == name)]
              if len(df_multi_ph_check) != len(df_multi_ph_name_addr_check):
                  return True
              else:
                  return False

  # Function to generate unique identifier.
  # In: row of data; column names
  # Out: unique identifier
  def generate_canonical_id(row, columns):
      concatenated_values = ''.join(str(row[col]) for col in columns if pd.notna(row[col]))
      canonical_id = hashlib.sha256(concatenated_values.encode()).hexdigest()
      return canonical_id

  # Function to transform row, append unique identifier and step, delete processed rows in base dataframe.
  # In: row of data; step #; array of other customer codes; array of other vehicle identification numbers
  def store_row(row, step, occ, ov):
      dedup_list.append({
          step_col: step,
          canonical_id_col: generate_canonical_id(row, hash_cols),
          customer_code_col: row[customer_code_col],
          name_col: row[name_col],
          address_col: row[address_col],
          phone_col: row[phone_col],
          email_col: row[email_col],
          city_col: row[city_col],
          vin_col: row[vin_col],
          other_cc_col: occ,
          other_vin_col: ov
      })
      df.drop(df[df[customer_code_col] == row[customer_code_col]].index, inplace=True)
      if occ is not None:
          for oc in occ:
              df.drop(df[df[customer_code_col] == oc].index, inplace=True)

  # Function to create arrays of other customer codes in merged records.
  # In: temp dataframe; highest customer code
  # Out: array of other customer codes
  def collect_other_cc(t_df, max_cc):
      other_ccs = []
      for i, r in t_df.iterrows():
          if max_cc != r[customer_code_col]:
              other_ccs.append(r[customer_code_col])
      return other_ccs

  # Function to create arrays of other vehicle identification numbers in merged records.
  # In: temp dataframe; highest customer code
  # Out: array of other vehicle identification numbers
  def collect_other_vin(t_df, max_cc):
      other_vins = []
      for i, r in t_df.iterrows():
          if max_cc != r[customer_code_col]:
              other_vins.append(r[vin_col])
      return other_vins

  # Step 1 - Unique, not null phone rows
  s = 'S1'
  print('Start ', s)
  cnt_s1 = 0
  for index, row in df.iterrows():
      if not check_phone_dup(row[phone_col]):
          store_row(row, s, None, None)
          print(row.to_frame().T)
          cnt_s1 += 1
  df = df.reset_index(drop=True)
  counts.append({s: cnt_s1})

  # Step 2a - Duplicated phone rows, merge on phone + email
  s = 'S2a'
  print('Start ', s)
  cnt_s2a_bf = cnt_s2a_af = 0
  for index, row in df.iterrows():
      if not check_phone_email_dup(row[phone_col], row[email_col]) and index in df.index:
          df_ph_em = df[(df[phone_col] == row[phone_col]) & (df[email_col] == row[email_col])]
          cnt_s2a_bf += len(df_ph_em)
          max_cc = df_ph_em[customer_code_col].max()
          other_ccs = collect_other_cc(df_ph_em, max_cc)
          other_vins = collect_other_vin(df_ph_em, max_cc)
          print(df_ph_em[[customer_code_col, phone_col, email_col, name_col, address_col, vin_col]], other_ccs, other_vins)
          print(df_ph_em[df_ph_em[customer_code_col] == max_cc][[customer_code_col, phone_col, email_col, name_col, address_col, vin_col]], other_ccs, other_vins)
          store_row(df_ph_em[df_ph_em[customer_code_col] == max_cc].iloc[0], s, other_ccs, other_vins)
          cnt_s2a_af += 1
  df = df.reset_index(drop=True)
  counts.append({s: cnt_s2a_bf})
  counts.append({s: cnt_s2a_af})

  #Step 2b - Duplicated phone rows, merge on name + address, ignore email
  s = 'S2b'
  print('Start ', s)
  cnt_s2b_bf = cnt_s2b_af = 0
  for index, row in df.iterrows():
      if not check_name_address_dup(row[phone_col], row[name_col], row[address_col]) and index in df.index:
          df_ph_em = df[(df[phone_col] == row[phone_col]) & (df[name_col] == row[name_col]) & (df[address_col] == row[address_col])]
          cnt_s2b_bf += len(df_ph_em)
          max_cc = df_ph_em[customer_code_col].max()
          other_ccs = collect_other_cc(df_ph_em, max_cc)
          other_vins = collect_other_vin(df_ph_em, max_cc)
          print(df_ph_em[[customer_code_col, phone_col, email_col, name_col, address_col, vin_col]])
          print(df_ph_em[df_ph_em[customer_code_col] == max_cc][[customer_code_col, phone_col, email_col, name_col, address_col, vin_col]])
          store_row(df_ph_em[df_ph_em[customer_code_col] == max_cc].iloc[0], s, other_ccs, other_vins)
          cnt_s2b_af += 1
  df = df.reset_index(drop=True)
  counts.append({s: cnt_s2b_bf})
  counts.append({s: cnt_s2b_af})

  #Step 3 - Phone is null, email isn't null
  s = 'S3'
  print('Start ', s)
  cnt_s3 = 0
  for index, row in df.iterrows():
      if pd.isna(row[phone_col]) and not pd.isna(row[email_col]) and index in df.index:
          store_row(row, s, None, None)
          print(row.to_frame().T)
          cnt_s3 += 1
  df = df.reset_index(drop=True)
  counts.append({s: cnt_s3})

  #Step 4 - Phone and email are null
  s = 'S4'
  print('Start ', s)
  cnt_s4 = 0
  for index, row in df.iterrows():
      if pd.isna(row[phone_col]) and pd.isna(row[email_col]) and index in df.index:
          store_row(row, s, None, None)
          print(row.to_frame().T)
          cnt_s4 += 1
  df = df.reset_index(drop=True)
  counts.append({s: cnt_s4})

  #Step 2c - Duplicated phone rows, no PII to merge on
  s = 'S2c'
  print('Start ', s)
  cnt_s2c = 0
  for index, row in df.iterrows():
      if index in df.index:
          store_row(row, s, None, None)
          print(row.to_frame().T)
          cnt_s2c += 1
  counts.append({s: cnt_s2c})

  # Write results to TD table.
  result_df = pd.DataFrame(dedup_list)
  print(result_df)
  td.load_table_from_dataframe(result_df,f'{database}.{out_table}',writer='bulk_import',if_exists='overwrite')

  # Counts
  print(counts)
  print('Fin')

# Main
if __name__ == "__main__":
    main()
