import os
import csv
import time
import requests

def api_request(url, max_retries=3, delay_on_429=300):
    # Make a GET request to API. Need to include logic to handle re-tries, as steam API is strict on number of requests.
    # Will retry up  to max_retries if 429 (Too Many Requests) error occured.

    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            
            # If rate-limited (429), wait 300 secs and retry.
            if response.status_code == 429:
                print(f"Hit 429 error - waiting {delay_on_429} seconds before re-try")
                time.sleep(delay_on_429)
                continue
            
            # Raise exception if other error / response. 
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"Request error on attempt {attempt + 1}/{max_retries}: {e}")


def get_all_apps():
    # Get whole list of steam apps via steam API within a dictionary. Just the ID's. One single API call.
    url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = api_request(url)
    if not response:
        return [] # return blank if error / no response from url

    data = response.json()
    return data["applist"]["apps"]

def get_app_details(appid):
    # Take the list of APP id's now collected and get the details for the app.
    # Example API response:
    '''
    {
"570": {
    "success": true,
    "data": {
    "name": "Dota 2",
    "type": "game",
    "is_free": true,
    ...
    }
}
}
'''
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = api_request(url)
    if not response:
        return None # return blank if error / no response from url
    
    data = response.json() # parse as json - convert response form API as dictionary 
    if str(appid) in data and data[str(appid)].get("success"): # Checks that api response was succesfull before getting the app data. success = means steam was able to lookup that ID and find it's details.
        return data[str(appid)]["data"]
    else:
        return None

def get_app_reviews(appid):
    # API to fetch review details.
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
    response = api_request(url)
    if not response:
        return None
    
    reviews_data = response.json()
    if reviews_data.get("success") == 1: # If found matching app id details:
        # Hold aggregate review data. Steam response with reviews (list of individual reviews) and query_summary (summary of reviews aggregated)
        query_summary = reviews_data.get("query_summary", {}) # Take the returned aggregated review info.
        return { # Return the fields needed from query_summary. 
            "num_reviews": query_summary.get("num_reviews", 0),
            "review_score": query_summary.get("review_score", None),
            "positive_total": query_summary.get("total_positive", 0),
            "negative_total": query_summary.get("total_negative", 0),
            "total_reviews": query_summary.get("total_reviews", 0),
        }
    return None

def load_existing_appids(csv_filename, appid_col="appid"):
    # Read existing .csv if it exists, and return set of APP ID's already fetched for, to avoid requesting multiple times.
    # Also if script crashes wont have to start from 0.

    existing_appids = set()
    if os.path.exists(csv_filename) and os.path.getsize(csv_filename) > 0: # check if extists and not empty
        with open(csv_filename, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader: # for each row:
                try:
                    existing_appids.add(int(row[appid_col])) # extract and convert id to int within existing_appids.
                except:
                    pass  # skip any 'weird' app ids. (ones with unicode characters in name for example)
    return existing_appids

def main():
    # Get complete list of ID's from steam
    all_apps = get_all_apps()
    
    # Only get the first 200 apps, to test script works.
    # all_apps = all_apps[:200]

    csv_filename = "Steam_Export.csv" # Output path
    
    fieldnames = [
        "appid",
        "name",
        "type",
        "is_free",
        "price_initial",
        "price_final",
        "short_description",
        "release_date",
        "developers",
        "publishers",
        "genres",
        "categories",
        "metacritic_score",
        "dlc",
        "num_reviews",
        "review_score",
        "positive_total",
        "negative_total",
        "total_reviews",
    ]

    # Load and skip existing app id's we already have data for.
    existing_appids = load_existing_appids(csv_filename, appid_col="appid")
    print(f"Found {len(existing_appids)} apps already in CSV.")

    # Open CSV if already existing, otherwie create new one. Need to make csv now as will incrementally save it after X requests.
    file_exists = os.path.exists(csv_filename)
    file_empty = (os.path.getsize(csv_filename) == 0) if file_exists else True

    with open(csv_filename, mode="a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if file_empty:
            writer.writeheader()

        #Process each app
        processed_count = 0 # keep count 
        for i, app in enumerate(all_apps, start=1):
            appid = app["appid"]
            print(f"Getting appid: {appid}")

            # Skip if we already have this appid in CSV
            if appid in existing_appids:
                continue

            # Get store details
            game_data = get_app_details(appid)
            if not game_data:
                # skip if no details
                continue

            # Extract store fields - map variable name to steam api name.
            name = game_data.get("name", None)
            app_type = game_data.get("type", None)
            is_free = game_data.get("is_free", None)

            price_overview = game_data.get("price_overview", {})
            price_initial = price_overview.get("initial", None)
            price_final = price_overview.get("final", None)

            short_description = game_data.get("short_description", None)

            release_data = game_data.get("release_date", {})
            release_date = release_data.get("date", None)

            developers = game_data.get("developers", [])
            publishers = game_data.get("publishers", [])

            # genres - join descriptions
            genres_list = game_data.get("genres", [])
            genres_list = [g["description"] for g in genres_list if "description" in g]

            # categories - join descriptions
            categories_list = game_data.get("categories", [])
            categories_list = [c["description"] for c in categories_list if "description" in c]

            # metacritic
            metacritic_data = game_data.get("metacritic", {})
            metacritic_score = metacritic_data.get("score", None)

            # DLC
            dlc_list = game_data.get("dlc", None)

            # Get review info, seperate api call.
            review_data = get_app_reviews(appid)
            if review_data:
                num_reviews = review_data["num_reviews"]
                review_score = review_data["review_score"]
                positive_total = review_data["positive_total"]
                negative_total = review_data["negative_total"]
                total_reviews = review_data["total_reviews"]
            else:
                num_reviews = None
                review_score = None
                positive_total = None
                negative_total = None
                total_reviews = None

            # Prepare to export.
            row = {
                "appid": appid,
                "name": name,
                "type": app_type,
                "is_free": is_free,
                "price_initial": price_initial,
                "price_final": price_final,
                "short_description": short_description,
                "release_date": release_date,
                "developers": ", ".join(developers) if developers else None,
                "publishers": ", ".join(publishers) if publishers else None,
                "genres": ", ".join(genres_list) if genres_list else None,
                "categories": ", ".join(categories_list) if categories_list else None,
                "metacritic_score": metacritic_score,
                "dlc": dlc_list, 
                "num_reviews": num_reviews,
                "review_score": review_score,
                "positive_total": positive_total,
                "negative_total": negative_total,
                "total_reviews": total_reviews,
            }
            writer.writerow(row)
            processed_count += 1

            # Print progress every 100 apps.
            if processed_count % 100 == 0:
                print(f"Processed {processed_count} new apps...")


    print(f"Done!")

if __name__ == "__main__":
    main()
