import os, sys
os.system(f"{sys.executable} -m pip install --user datarobot")

import datarobot as dr

def upload(database, table, project_id, model_id, datasource_id):
  # SetUp
  DR_API_TOKEN  = os.environ['DR_API_TOKEN']
  TD_USERNAME   = os.environ['TD_USERNAME']
  TD_PASSWORD   = os.environ['TD_PASSWORD']
  TD_API_KEY    = os.environ['TD_API_KEY']
  TD_API_SERVER = os.environ['TD_API_SERVER']
  MAX_WAIT = 60 * 60  # Maximum number of seconds to wait for prediction job to finish
  
  dr.Client(endpoint='https://app.datarobot.com/api/v2', token=DR_API_TOKEN)
  project = dr.Project.get(project_id)
  model = dr.Model.get(project_id, model_id)
  dataset = project.upload_dataset_from_data_source(datasource_id, TD_USERNAME, TD_PASSWORD)
  
  # Predict
  pred_job = model.request_predictions(dataset.id)
  pred_df = pred_job.get_result_when_complete(max_wait=MAX_WAIT)
  
  # Upload
  from pytd import pandas_td as td
  con = td.connect(apikey=TD_API_KEY, endpoint=TD_API_SERVER)
  td.to_td(pred_df, '{}.{}'.format(database, table), con=con, if_exists='replace', index=False)
