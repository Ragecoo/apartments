import requests
import json
import time
import random
import os
from tqdm import tqdm

NORTH = 51.2787
SOUTH = 51.0092
WEST = 71.2210
EAST = 71.6506
STEP = 0.05

def generate_grid():
    grid = []
    curr_north = NORTH
    while curr_north > SOUTH:
        curr_south = curr_north - STEP
        curr_west = WEST
        while curr_west < EAST:
            curr_east = curr_west + STEP
            grid.append(f"{curr_north:.5f},{curr_west:.5f},{curr_south:.5f},{curr_east:.5f}")
            curr_west += STEP
        curr_north -= STEP
    return grid


def get_all():
    output_dir = "squares_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    grid = generate_grid()
    print(f"squares: {len(grid)}\n")

    total_unique_count = 0
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "krishauid=019d0644-5d20-79ff-82f3-1205c6e97610; kraid=9438c1e8-2439-4c6f-b4c0-176c08f632e7; _gcl_au=1.1.75708887.1773926644; _ym_uid=1730864703217570918; _ym_d=1773926644; _tt_enable_cookie=1; _ttp=01KM34901T6ZZ6HQN4A1JGGBWB_.tt.1; krssid=kottc7ft4494m8hh9rfn7d36ev; _gid=GA1.2.1892970640.1776451480; _gat=1"
    }
    url = "https://krisha.kz/a/ajax-map-list/map/prodazha/kvartiry/astana/"

    with tqdm(total=len(grid), desc="get_all", unit="items") as pbar:
        for i, bounds in enumerate(grid):
            square_apartments = {}
            page = 1
            square_index = i + 1

            while True:
                params = {
                    "bounds": bounds,
                    "page": str(page)
                }

                try:
                    response = requests.get(url, headers=headers, params=params, timeout=15)
                    if response.status_code != 200:
                        tqdm.write(
                            f"\n! server error {response.status_code} on square {square_index}")
                        break
                    data = response.json()
                    adverts = data.get("adverts", {})
                    if not adverts:
                        break

                    square_apartments.update(adverts)
                    pbar.set_postfix(
                        items_in_square=len(square_apartments),
                        page=page,
                        square=square_index
                    )
                    if len(adverts) < 10:
                        break
                    page += 1
                    time.sleep(random.uniform(0.5, 1))
                except Exception as e:
                    tqdm.write(f"\n! server error: {e}")
                    break

            if square_apartments:
                file_name = f"square{square_index:02d}.json"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(square_apartments, f, ensure_ascii=False, indent=4)
                total_unique_count += len(square_apartments)
            pbar.update(1)
            time.sleep(random.uniform(1, 2))

    print(f"\ndone. total: {total_unique_count} items")
    print(f"> {output_dir}")

if __name__ == "__main__":
    get_all()