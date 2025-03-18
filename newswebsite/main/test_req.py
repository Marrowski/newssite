import requests
import json

def war_data():
    url = 'https://russianwarship.rip/api/v2/statistics/latest'
    response = requests.get(url)
    
    
    if response.status_code == 200:
        data_main = response.json()
        
        data = data_main['data']['stats']
        
        units = data['personnel_units']
        tanks = data['tanks']
        armoured_vehicles = data['armoured_fighting_vehicles']
        atillery = data['artillery_systems']
        mlrs = data['mlrs']
        planes = data['planes']
        helicopters = data['helicopters']
        fuel_tanks = data['vehicles_fuel_tanks']
        warships = data['warships_cutters']
        
        print(f'Особистий склад: {units}\n'
      f'Танки: {tanks}\n'
      f'Бронетранспортери: {armoured_vehicles}\n'
      f'Артилерія: {atillery}\n'
      f'РЗСВ: {mlrs}\n'
      f'Літаки: {planes}\n'
      f'Гелікоптери: {helicopters}\n'
      f'Цистерни з ПММ: {fuel_tanks}'
      f'Кораблі: {warships}'
      )
    else:
        print(f'{response.status_code}')

    


