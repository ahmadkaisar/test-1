import datetime
import requests as req
import time
import yaml

def build_requests(config: dict):
  method = config.get('method', 'GET')
  url = config.get('url', None)
  name = config.get('name', None)
  headers = config.get('headers', None)
  body = config.get('body', None)
  resp = None

  if not url or not name or not method or method not in ['GET', 'POST']:
    return
  
  if method == 'GET':
    resp = req.get(url, headers=headers)
  elif method == 'POST':
    resp = req.post(url, headers=headers, json=body)

  if resp.status_code >= 400:
    print(f'[X][{config["last_fetched"]}] {name}, status code: {resp.status_code}')
  else:
    print(f'[V][{config["last_fetched"]}] {name}')

fetch_configs: list = []
with open('configs.yml', 'r') as f:
  configs = yaml.safe_load_all(f)
  
  for config in configs:
    config['last_fetched'] = datetime.datetime.utcnow()
    fetch_configs.append(config)

while True:
  now = datetime.datetime.utcnow()
  for config in fetch_configs:
    if (now - config['last_fetched']).seconds >= 15:
      config['last_fetched'] = datetime.datetime.utcnow()
      build_requests(config)

  time.sleep(1)