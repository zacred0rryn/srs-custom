import yaml
import json
import os

def convert_yaml_to_json(yaml_file, json_file):
  with open(yaml_file, 'r') as yf:
    yaml_data = yaml.safe_load(yf)

  json_data = {
    "version": 2,
    "rules": [
      {
        "domain": [item.split(',')[1] for item in yaml_data['payload'] if item.startswith('DOMAIN,')],
        "domain_suffix": [item.split(',')[1] for item in yaml_data['payload'] if item.startswith('DOMAIN-SUFFIX,')],
        "ip_cidr": [item.split(',')[1] for item in yaml_data['payload'] if item.startswith(('IP-CIDR,', 'IP-CIDR6,'))]
      }
    ]
  }

  with open(json_file, 'w') as jf:
    json.dump(json_data, jf, indent=4)

if __name__ == '__main__':
  for yaml_file in os.listdir('.'):
    if yaml_file.endswith('.yaml'):
      new_json_file = yaml_file.replace('.yaml', '.json')
      convert_yaml_to_json(yaml_file, new_json_file)
