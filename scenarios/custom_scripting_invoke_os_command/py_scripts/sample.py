import os, subprocess
import shlex

def get_credential():
  uri = os.environ.get('AWS_CONTAINER_CREDENTIALS_RELATIVE_URI')
  if uri is None :
    print('$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI is not defined')
    return

  cmd = 'curl 169.254.170.2{}'.format(uri)
  args = shlex.split(cmd)
  print(args)

  subprocess.Popen(args, shell=True)

def get_from_proc1():
  print('strings /proc/1/environ ... ')
  subprocess.run(['strings', '/proc/1/environ'])
  print('strings /proc/1/environ | grep AWS_CONTAINER_CREDENTIALS_RELATIVE_URI ...')
  subprocess.call('strings /proc/1/environ | grep AWS_CONTAINER_CREDENTIALS_RELATIVE_URI', shell=True)
  print('done')

def show_environ():
  for key, val in os.environ.items():
    print('{}: {}'.format(key, val))

def show_metadata():
  uri = os.environ.get('ECS_CONTAINER_METADATA_URI')
  subprocess.run(['curl', uri])

def run():
  get_credential()
  get_from_proc1()
  show_metadata()
  show_environ()