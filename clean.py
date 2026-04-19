import os
import json
import pandas as pd
import re

INPUT_FOLDER = 'squares_data'
OUTPUT_MAIN_CSV = 'data01.csv'
OUTPUT_NO_FLOOR_CSV = 'data02.csv'

def parse_floor_info(title):
    floor_match = re.search(r'(\d+)(?:[/\s]+из[/\s]+|/)(\d+)\s+этаж', title)
    if floor_match:
        return int(floor_match.group(1)), int(floor_match.group(2))
    single_floor_match = re.search(r'(\d+)\s+этаж', title)
    if single_floor_match:
        return int(single_floor_match.group(1)), None
    return None, None

def process_files():
    main_list = []
    no_floor_list = []
    if not os.path.exists(INPUT_FOLDER):
        print(f"error: dir not found")
        return
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith('.json'):
            file_path = os.path.join(INPUT_FOLDER, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception as e:
                    print(f"error on reading {filename}: {e}")
                    continue
                for item_id, item in data.items():
                    if not isinstance(item, dict):
                        continue
                    title = item.get('title', '')
                    floor, total_floors = parse_floor_info(title)
                    record = {
                        'id': item.get('id'),
                        'isOnMap': item.get('isOnMap'),
                        'hasPrice': item.get('hasPrice'),
                        'price': item.get('price'),
                        'photos': json.dumps(item.get('photos', []), ensure_ascii=False),
                        'title': title,
                        'addressTitle': item.get('addressTitle'),
                        'square': item.get('square'),
                        'rooms': item.get('rooms'),
                        'ownerName': item.get('ownerName'),
                        'map_lat': item.get('map', {}).get('lat') if item.get('map') else None,
                        'map_lon': item.get('map', {}).get('lon') if item.get('map') else None,
                        'complexId': item.get('complexId'),
                        'floor': floor,
                        'total_floors': total_floors
                    }
                    if floor is not None and total_floors is not None:
                        record['is_first_floor'] = (floor == 1)
                        record['is_last_floor'] = (floor == total_floors)
                        record['relative_floor'] = round(floor / total_floors, 2)
                        main_list.append(record)
                    elif floor is None:
                        record['is_first_floor'] = None
                        record['is_last_floor'] = None
                        record['relative_floor'] = None
                        no_floor_list.append(record)
                    else:
                        continue

    if main_list:
        df_main = pd.DataFrame(main_list)
        df_main.to_csv(OUTPUT_MAIN_CSV, index=False, encoding='utf-8-sig')
        print(f"output: {OUTPUT_MAIN_CSV} ({len(main_list)} items)")
    if no_floor_list:
        df_no_floor = pd.DataFrame(no_floor_list)
        cols_to_drop = ['floor', 'total_floors', 'is_first_floor', 'is_last_floor', 'relative_floor']
        df_no_floor = df_no_floor.drop(columns=cols_to_drop)
        df_no_floor.to_csv(OUTPUT_NO_FLOOR_CSV, index=False, encoding='utf-8-sig')
        print(f"output: {OUTPUT_NO_FLOOR_CSV} ({len(no_floor_list)} items) (no floor data)")


if __name__ == "__main__":
    process_files()