import requests
import time

# Configuration: Fill in your own values here
RADARR_URL = "http://YOUR_RADARR_IP:PORT"
API_KEY = "YOUR_RADARR_API_KEY"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_collections():
    """Retrieve all collections from Radarr."""
    url = f"{RADARR_URL}/api/v3/collection"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_movie(movie_id):
    """Retrieve a movie from Radarr using its internal ID."""
    url = f"{RADARR_URL}/api/v3/movie/{movie_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_movie_by_tmdb(tmdb_id):
    """Retrieve a movie from Radarr using its TMDB ID."""
    url = f"{RADARR_URL}/api/v3/movie?tmdbId={tmdb_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    movies = response.json()
    return movies[0] if movies else None

def get_default_quality_profile_id():
    """Get the default quality profile ID from Radarr."""
    url = f"{RADARR_URL}/api/v3/qualityprofile"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    profiles = response.json()
    if profiles:
        # Uses the first profile as default. Adjust logic if needed.
        return profiles[0]['id']
    else:
        raise Exception("No quality profiles found in Radarr!")

def get_default_root_folder_path():
    """Get the default root folder path from Radarr."""
    url = f"{RADARR_URL}/api/v3/rootfolder"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    folders = response.json()
    if folders:
        # Uses the first folder as default. Adjust logic if needed.
        return folders[0]['path']
    else:
        raise Exception("No root folders found in Radarr!")

def add_movie_to_radarr(tmdb_id, title, year, quality_profile_id, root_folder_path):
    """Add a new movie to Radarr and set it as monitored."""
    payload = {
        "tmdbId": tmdb_id,
        "title": title,
        "year": year,
        "qualityProfileId": quality_profile_id,
        "titleSlug": f"{title.replace(' ', '-').lower()}-{year}",
        "rootFolderPath": root_folder_path,
        "monitored": True,
        "addOptions": {
            "searchForMovie": True
        }
    }
    url = f"{RADARR_URL}/api/v3/movie"
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 400 and "already exists" in response.text:
        print(f"{title} ({year}) already exists.")
        return None
    else:
        print(f"Error adding {title} ({year}): {response.text}")
        return None

def update_movie(movie):
    """Update a movie in Radarr (set monitored or other changes)."""
    url = f"{RADARR_URL}/api/v3/movie/{movie['id']}"
    response = requests.put(url, json=movie, headers=headers)
    response.raise_for_status()
    return response.json()

def send_telegram_notification(message):
    """Send a notification message via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if not response.ok:
        print("Failed to send Telegram notification:", response.text)
    response.raise_for_status()

def main():
    print("Fetching default settings from Radarr...")
    quality_profile_id = get_default_quality_profile_id()
    root_folder_path = get_default_root_folder_path()
    print(f"Default quality profile id: {quality_profile_id}")
    print(f"Default root folder path: {root_folder_path}")

    collections = get_collections()
    total_monitored = 0
    total_added = 0
    notify_per_collection = []

    for collection in collections:
        # Use a safe key for the collection name (handles both 'name' and 'title')
        collection_name = collection.get('name') or collection.get('title') or 'Unknown Collection'
        info = f"*{collection_name}*\n"
        changes = False

        for movie in collection['movies']:
            movie_id = movie.get('movieId') or movie.get('id')
            movie_full = None

            if movie_id:
                try:
                    movie_full = get_movie(movie_id)
                except Exception as e:
                    print(f"Error retrieving movie with id {movie_id}: {e}")
                if movie_full and not movie_full.get('monitored', True):
                    movie_full['monitored'] = True
                    try:
                        update_movie(movie_full)
                        info += f"• [Set as monitored] {movie_full['title']} ({movie_full['year']})\n"
                        total_monitored += 1
                        changes = True
                    except Exception as e:
                        print(f"Error updating {movie_full['title']}: {e}")
            elif movie.get('tmdbId') and movie.get('title') and movie.get('year'):
                # Not yet in Radarr, add it!
                added = add_movie_to_radarr(
                    tmdb_id=movie['tmdbId'],
                    title=movie['title'],
                    year=movie['year'],
                    quality_profile_id=quality_profile_id,
                    root_folder_path=root_folder_path
                )
                if added:
                    info += f"• [Added & monitored] {movie['title']} ({movie['year']})\n"
                    total_added += 1
                    changes = True
                    # Wait a moment to prevent overloading Radarr
                    time.sleep(1)
            else:
                print(f"Cannot process movie: {movie.get('title')} ({movie.get('year')}) - missing data?")
                continue

        if changes:
            notify_per_collection.append(info)

    if total_monitored > 0 or total_added > 0:
        message = (
            f"🎬 *Radarr Collections updated!*\n\n"
            f"{total_monitored} existing movies set as monitored.\n"
            f"{total_added} movies added and monitored.\n\n"
            "Per collection overview:\n\n"
            + "\n".join(notify_per_collection)
        )
        send_telegram_notification(message)
        print("Telegram notification sent!")
    else:
        print("No changes needed; all movies were already monitored or previously added.")

if __name__ == "__main__":
    main()
