import yaml
import json
import os

def convert_yaml_to_json(yaml_file, json_file):
  with open(yaml_file, 'r') as yf:
    yaml_data = yaml.safe_load(yf)
  
  domains = []
  domain_suffixes = []
  ip_cidrs = []
  
  for item in yaml_data['payload']:
    parts = item.split(',')
    if item.startswith('DOMAIN,'):
      domains.append(parts[1])
    elif item.startswith('DOMAIN-SUFFIX,'):
      domain_suffixes.append(parts[1])
    elif item.startswith(('IP-CIDR,', 'IP-CIDR6,')):
      ip_cidrs.append(parts[1])
  
  json_data = {
    "version": 2,
    "rules": [
      {
        "domain": domains,
        "domain_suffix": domain_suffixes,
        "ip_cidr": ip_cidrs
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