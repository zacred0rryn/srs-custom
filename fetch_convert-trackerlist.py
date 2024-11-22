import urllib.request
import re
import json
import ipaddress

tracker_list_urls = [
    'https://cdn.jsdelivr.net/gh/DeSireFire/animeTrackerList/AT_all_http.txt',
    'https://cdn.jsdelivr.net/gh/DeSireFire/animeTrackerList/AT_all_https.txt',
    'https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all_http.txt',
    'https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/trackers_all_https.txt',
    'https://cf.trackerslist.com/http.txt',
]

domains = set()
ips = set()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

for url in tracker_list_urls:
    print(f"Fetching {url}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            lines = content.splitlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                line = re.sub(r'^https?://', '', line)
                line = re.sub(r'[/\?#].*', '', line)
                line = re.sub(r':\d+$', '', line)
                # Remove square brackets enclosing IPv6 addresses
                if line.startswith('[') and line.endswith(']'):
                    line = line[1:-1]
                try:
                    ip = ipaddress.ip_address(line)
                    if ip.version == 4:
                        ips.add(f"{line}/32")
                    elif ip.version == 6:
                        ips.add(f"{line}/128")
                except ValueError:
                    domains.add(line)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

output_data = {
    "version": 2,
    "rules": [
        {
            "domain": sorted(domains),
            "ip_cidr": sorted(ips)
        }
    ]
}

with open('bt_trackers.json', 'w') as f:
    json.dump(output_data, f, indent=4)