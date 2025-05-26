# Auto Monitor & Add Radarr Collections

Automatically monitor all movies from your Radarr collections — and add any missing ones — with one script!  
Sends a summary notification via Telegram after every run.

---

## Features

- Checks all collections in your Radarr instance.
- Sets all movies in collections to **monitored** (if not already).
- **Automatically adds** any collection movies not yet in Radarr (based on TMDB ID).
- Uses your **Radarr defaults** for Quality Profile and Root Folder (no hardcoded values).
- Sends a Telegram notification with all changes (added or monitored) per collection.
- Fully Python 3 and cross-platform.
- Clean, well-commented code for easy editing.

---

## Requirements

- **Radarr** instance (tested with Radarr v3+)
- **Python 3.6+**
- Python package: `requests`  
  Install with:  
  ```bash
  pip install requests

    A Telegram bot and your chat ID (see below)

Setup

    Clone or download this repository.

    Create your Telegram bot (if you don’t have one):

        Open @BotFather on Telegram.

        Use /newbot and follow the steps. Save the token.

    Find your Telegram chat ID

        Start a chat with your bot.

        Go to: https://api.telegram.org/bot<YourBotToken>/getUpdates
        Send a test message to your bot and note your chat ID from the JSON.

    Edit the configuration section at the top of the script:

    RADARR_URL = "http://YOUR_RADARR_IP:PORT"
    API_KEY = "YOUR_RADARR_API_KEY"
    TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

    (Optional) For cronjobs, simply schedule this script as needed!

Usage

python3 AutoMonitorRadarrCollections.py

The script will:

    Fetch your Radarr collections

    Monitor all existing movies

    Add missing movies

    Send you a Telegram notification if anything changed

Example Telegram Notification

🎬 Radarr Collections updated!

3 existing movies set as monitored.
2 movies added and monitored.

Per collection overview:

*Spider-Man Collection*
• [Set as monitored] Spider-Man (2002)
• [Added & monitored] Spider-Man: No Way Home (2021)

*The Lord of the Rings*
• [Set as monitored] The Fellowship of the Ring (2001)

Notes & Tips

    The script will not add movies without TMDB ID, title, and year information.

    Quality profile and root folder are fetched dynamically from your Radarr setup (uses the first found as default).

    Uses a short delay between movie adds to avoid Radarr rate limiting.

    All output/errors are shown in the terminal for easy troubleshooting.

    The script is safe to run repeatedly; it won’t re-add or re-monitor anything already handled.

Troubleshooting

    If you get a KeyError on collection names, your Radarr API may use "title" instead of "name" — this script handles both.

    For network errors, check your API key, Radarr IP/port, and ensure the server is reachable from where the script runs.

    To debug Telegram, try sending a message manually via the Telegram API docs.

License

MIT License — free for personal and commercial use.
Feel free to submit improvements or open issues!
Credits

Script by MB053
Tested and improved with feedback from the community.


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MB053)

Happy automating! 🎬🤖
