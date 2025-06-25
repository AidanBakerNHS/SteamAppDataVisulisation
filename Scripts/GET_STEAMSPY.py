import os
import time
import requests
import pandas as pd
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

INPUT_CSV = "SteamExport.csv"
OUTPUT_CSV = "SteamSpyExport.csv"
STEAMSPY_URL = "https://steamspy.com/api.php"
SAVE_INTERVAL = 500  # save after every 500 app's in event of script crashing - dont want to lose progress.
REQUEST_PARAMS = {
    'request': 'appdetails',
}

# Read the original dataset
df = pd.read_csv(INPUT_CSV)
# Ensure appid is int
df['appid'] = df['appid'].astype(int)

# Read existing output - if app id already included, skip it.
if os.path.exists(OUTPUT_CSV):
    existing_df = pd.read_csv(OUTPUT_CSV)
    if 'appid' in existing_df.columns:
        existing_df['appid'] = existing_df['appid'].astype(int)
        existing_ids = set(existing_df['appid'])
    else:
        existing_ids = set() # convert to set. Any existing app id's are stored in existing_ids.
else:
    existing_df = pd.DataFrame()
    existing_ids = set()

steamspy_data = []

# Iterate over appids and fetch SteamSpy details
for idx, appid in enumerate(df['appid'], start=1):
    params = REQUEST_PARAMS.copy()
    params['appid'] = appid

    if appid in existing_ids:
        print(f"Skipping appid {appid} as already done.")
        row = existing_df.loc[existing_df['appid'] == appid].iloc[0]
        data = {k: v for k, v in row.to_dict().items() if k not in df.columns}
    else:
        print(f"Fetching details for appid {appid} (#{idx})...")
        # Attempt request, handling rate limits and invalid JSON (common errors that occured while running script.)
        while True:
            try:
                response = requests.get(
                    STEAMSPY_URL,
                    params=params,
                    timeout=10,
                    verify=False  # Disable SSL verification - Issues while performing this with verification on work laptop.
                )
                if response.status_code == 429:
                    print(f"Rate limited, waiting 60 seconds.")
                    time.sleep(60)
                    continue
                response.raise_for_status()
                try:
                    data = response.json()
                except ValueError:
                    print(f"Invalid JSON received for appid {appid}. Skipping this APP.")
                    data = {}
                # Steam spy allows 1 request per second:
                time.sleep(1)
                break
            except requests.RequestException as e: # For other errors:
                print(f"Error for appid {appid}: {e}")
                data = {}
                break

    steamspy_data.append(data)

    # Save intermediate results every 500 games
    if idx % SAVE_INTERVAL == 0:
        temp_df = pd.concat([
            df.iloc[:idx].reset_index(drop=True),
            pd.DataFrame(steamspy_data)
        ], axis=1)
        temp_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Saved after {idx} apps.")

# After loop, merge and save final output
final_df = pd.concat([df.reset_index(drop=True), pd.DataFrame(steamspy_data)], axis=1)
final_df.sort_values(by="release_date", ascending=False, inplace= True) # Sort by latest release date first.
final_df.to_csv(OUTPUT_CSV, index=False)
print(f"Done!")
