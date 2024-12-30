import os
import sys
os.system(f"{sys.executable} -m pip install fuzzywuzzy textdistance python-Levenshtein rapidfuzz")

import pandas as pd
from fuzzywuzzy import fuzz
import textdistance as tedi
import Levenshtein as lev
import rapidfuzz as rf
import pytd
import multiprocessing

def main(**kwargs):
  tdAPIkey = os.getenv("TD_API_KEY")
  tdAPIendpoint = os.getenv("TD_API_ENDPOINT")
  process_cnt = int(os.getenv("PROCESS_CNT"))
  parts = int(os.getenv("PARTS"))
  part = int(os.getenv("PART"))
  database = kwargs.get('db')
  src_table = kwargs.get('dm_tbl')
  out_table = kwargs.get('pm_tbl')
  name_weight = int(kwargs.get('name_weight'))
  address_weight = int(kwargs.get('address_weight'))
  positive_threshold = int(kwargs.get('positive_threshold'))

  td = pytd.Client(apikey=tdAPIkey, 
              endpoint=tdAPIendpoint, 
              database=database, 
              default_engine='presto')

  # Init
  customer_code_col = 'cl_cc'
  phone_col = 'cl_phone'
  email_col = 'cl_email'
  name_col = 'cl_customer_name'
  address_col = 'cl_full_address'
  canonical_id_col = 'td_id'
  vin_col = 'cl_vin'
  cc_other_col = 'cc_other'
  vin_other_col = 'vin_other'

  # Create a dataframe by importing data from Treasure Data database.
  res = td.query(f'WITH with_rn AS (SELECT {customer_code_col}, {phone_col}, {email_col}, {name_col}, {address_col}, {canonical_id_col}, {vin_col}, {cc_other_col}, {vin_other_col}, ROW_NUMBER() OVER (ORDER BY {canonical_id_col}) AS rn FROM {database}.{src_table}) SELECT * FROM with_rn WHERE rn % {parts} = {part}')
  base_df = pd.DataFrame(**res)
  print(base_df)

  # Number of processes (vCPUs)
  num_processes = process_cnt
  print(f"Starting data processing using {num_processes} processes...")
  
  # Function to process data and store the result in the shared list.
  # In: chunk of dataframe, full dataframe, process's name, result dataframe, result index
  def process_data(data_chunk, base_df, process_name, results, index):
      print(f"{process_name} is processing...")
      pm_results = []

      for i, row in data_chunk.iterrows():
          print(process_name, ':', i)
          pm_temp_results = []
          for j, candidate in base_df.iterrows():
              if pd.notna(row[name_col]) and pd.notna(row[address_col]) and row[name_col] != '' and row[address_col] != '' and pd.notna(candidate[name_col]) and pd.notna(candidate[address_col]) and candidate[name_col] != '' and candidate[address_col] != '' and row[customer_code_col] != candidate[customer_code_col]:
                  score_fuzz_name = fuzz.ratio(row[name_col], candidate[name_col])
                  score_textdist_jaccard_name = tedi.jaccard.normalized_similarity(row[name_col], candidate[name_col]) * 100
                  score_levenshtein_name = lev.ratio(row[name_col], candidate[name_col]) * 100
                  score_rapid_name = rf.fuzz.ratio(row[name_col], candidate[name_col])
                  
                  score_fuzz_address = fuzz.ratio(row[address_col], candidate[address_col])
                  score_textdist_jaccard_address = tedi.jaccard.normalized_similarity(row[address_col], candidate[address_col]) * 100
                  score_levenshtein_address = lev.ratio(row[address_col], candidate[address_col]) * 100
                  score_rapid_address = rf.fuzz.ratio(row[address_col], candidate[address_col])

                  average_score_name = (score_fuzz_name + score_textdist_jaccard_name + score_levenshtein_name + score_rapid_name) / 4
                  average_score_address = (score_fuzz_address + score_textdist_jaccard_address + score_levenshtein_address + score_rapid_address) / 4

                  average_score = (average_score_name * name_weight + average_score_address * address_weight) / (name_weight + address_weight)

                  if average_score == 100:
                      similar = 'Matched'
                  elif average_score >= positive_threshold:
                      similar = 'Positive'
                  else:
                      similar = 'Negative'

                  if similar != 'Negative':
                      pm_temp_results.append({
                          'td_id': row[canonical_id_col],
                          'candidate_td_id': candidate[canonical_id_col],
                          'customer_code': row[customer_code_col],
                          'candidate_customer_code': candidate[customer_code_col],
                          'name': row[name_col],
                          'candidate_name': candidate[name_col],
                          'address': row[address_col],
                          'candidate_address': candidate[address_col],
                          'phone': str(row[phone_col]),
                          'candidate_phone': str(candidate[phone_col]),
                          'email': row[email_col],
                          'candidate_email': candidate[email_col],
                          'vin': row[vin_col],
                          'candidate_vin': candidate[vin_col],
                          'cc_other': row[cc_other_col],
                          'candidate_cc_other': candidate[cc_other_col],
                          'vin_other': row[vin_other_col],
                          'candidate_vin_other': candidate[vin_other_col],
                          'similarity': similar,
                          'average_score': average_score,
                          'average_score_name': average_score_name,
                          'average_score_address': average_score_address,
                          'score_fuzz_name': score_fuzz_name,
                          'score_textdist_jaccard_name': score_textdist_jaccard_name,
                          'score_levenshtein_name': score_levenshtein_name,
                          'score_rapid_name': score_rapid_name,
                          'score_fuzz_address': score_fuzz_address,
                          'score_textdist_jaccard_address': score_textdist_jaccard_address,
                          'score_levenshtein_address': score_levenshtein_address,
                          'score_rapid_address': score_rapid_address
                      })
          df_group = pd.DataFrame(pm_temp_results)
          if len(df_group) > 0:
              df_eval = df_group.groupby('td_id').agg(
                  best_score=('average_score', 'max'),
                  best_c_td_id=('candidate_td_id', lambda x: x[df_group['average_score'].idxmax()]),
                  best_proba=('similarity', lambda x: x[df_group['average_score'].idxmax()]),
                  best_name_score=('average_score_name', lambda x: x[df_group['average_score'].idxmax()]),
                  best_addr_score=('average_score_address', lambda x: x[df_group['average_score'].idxmax()]),
                  phone=('phone', lambda x: str(x[df_group['average_score'].idxmax()])),
                  c_phone=('candidate_phone', lambda x: str(x[df_group['average_score'].idxmax()])),
                  email=('email', lambda x: x[df_group['average_score'].idxmax()]),
                  c_email=('candidate_email', lambda x: x[df_group['average_score'].idxmax()]),
                  cc=('customer_code', lambda x: x[df_group['average_score'].idxmax()]),
                  c_cc=('candidate_customer_code', lambda x: x[df_group['average_score'].idxmax()]),
                  customer_name=('name', lambda x: x[df_group['average_score'].idxmax()]),
                  c_customer_name=('candidate_name', lambda x: x[df_group['average_score'].idxmax()]),
                  address=('address', lambda x: x[df_group['average_score'].idxmax()]),
                  c_address=('candidate_address', lambda x: x[df_group['average_score'].idxmax()]),
                  vin=('vin', lambda x: x[df_group['average_score'].idxmax()]),
                  c_vin=('candidate_vin', lambda x: x[df_group['average_score'].idxmax()]),
                  cc_other=('cc_other', lambda x: x[df_group['average_score'].idxmax()]),
                  c_cc_other=('candidate_cc_other', lambda x: x[df_group['average_score'].idxmax()]),
                  vin_other=('vin_other', lambda x: x[df_group['average_score'].idxmax()]),
                  c_vin_other=('candidate_vin_other', lambda x: x[df_group['average_score'].idxmax()]),
                  all_proba=('similarity', lambda x: list(x.sort_values(ascending=False))),
                  all_score=('average_score', lambda x: list(x.sort_values(ascending=False))),
                  all_c_td_id=('candidate_td_id', lambda x: list(x.sort_values(ascending=False)))
              ).reset_index()
              pm_results.append(df_eval.iloc[0].tolist())

      print(f"{process_name} finished processing.")
      
      # Store result in the corresponding index of the results list
      results[index] = pm_results

  # Function to create and start processes
  # In: full dataframe, number of processes
  def run_in_processes(base_df, num_processes):
      def gen_chunks(df, column_name, num_subsets):
          # Sort the DataFrame by the specified column
          df = df.sort_values(by=column_name)
          # Split the DataFrame into the required number of subsets
          subsets = []
          subset_size = len(df) // num_subsets
          remainder = len(df) % num_subsets
          
          start_idx = 0
          for i in range(num_subsets):
              # Calculate the size of the current subset
              current_subset_size = subset_size + (1 if i < remainder else 0)
              end_idx = start_idx + current_subset_size
              # Get the current subset as a dataframe
              subset = df.iloc[start_idx:end_idx].copy()
              # Append the subset to the list
              subsets.append(subset)
              # Update the start index for the next iteration
              start_idx = end_idx
          return subsets

      print("Generating chunks...")
      list_df = gen_chunks(base_df, customer_code_col, num_processes)
      print("Finished generating chunks!")
      processes = []
      
      # Using Manager to create a shared list for collecting results
      with multiprocessing.Manager() as manager:
          results = manager.list([None] * num_processes)  # Shared list to collect results

          # Create processes and assign each one a chunk of the data
          for i in range(num_processes):
              data_chunk = list_df[i]
              print("data chunk ", i, " ", data_chunk)
              
              # Pass the shared results list and the index to store each process's result
              process = multiprocessing.Process(target=process_data, args=(data_chunk, base_df, f"Process-{i}", results, i))
              processes.append(process)
          
          # Start processes
          for process in processes:
              process.start()

          # Wait for all processes to complete
          for process in processes:
              process.join()

          # Combine results
          combined_results = [item for sublist in results for item in sublist]
          return combined_results

  # Run the multiprocessing computation.
  final_result = run_in_processes(base_df, num_processes)
  result_df = pd.DataFrame(final_result)
  result_df.columns = ['td_id', 'best_score', 'best_candidate_td_id', 'best_proba', 'best_name_score', 'best_addr_score', 'phone', 'best_candidate_phone', 'email', 'best_candidate_email', 'customer_code', 'best_candidate_customer_code', 'name', 'best_candidate_name', 'address', 'best_candidate_address', 'vin', 'best_candidate_vin', 'cc_other', 'best_candidate_cc_other', 'vin_other', 'best_candidate_vin_other', 'all_proba', 'all_score', 'all_candidate_td_id']
  print("All processes have finished processing.")
  
  # Write results to TD table.
  td.load_table_from_dataframe(result_df,f'{database}.{out_table}',writer='bulk_import',if_exists='append')
  print(f"Fin {part}")

# Main
if __name__ == "__main__":
    main()