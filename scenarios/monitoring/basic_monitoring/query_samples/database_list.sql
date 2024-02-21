select 
  id, name, created_at, 'https://console.treasuredata.com/app/databases/' || id as console_url
from databases