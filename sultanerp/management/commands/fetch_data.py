# Getting vacation days in JSON format "https://get.api-feiertage.de/?states=by


import requests

def fetch_data_from_url():
    url = "https://get.api-feiertage.de/?states=by"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch holiday data. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    holidays_data = fetch_data_from_url()
    if holidays_data:
        bavaria_holidays = holidays_data['feiertage']
        for holiday in bavaria_holidays:
            if holiday['by'] == '1':
                print(holiday['date'], "-", holiday['fname'])
