from google_play_scraper import reviews, Sort
import pandas as pd
import os
import time

apps = [
    {
        "bank": "Commercial Bank of Ethiopia",
        "app_id": "com.combanketh.mobilebanking"
    },
    {
        "bank": "Bank of Abyssinia",
        "app_id": "com.boa.boaMobileBanking"
    },
    {
        "bank": "Dashen Bank",
        "app_id": "com.dashen.dashensuperapp"
    }
]

os.makedirs("data/raw", exist_ok=True)

for app in apps:
    print(f"Scraping {app['bank']}")

    all_reviews = []
    token = None

    for _ in range(5):  # batches
        result, token = reviews(
            app['app_id'],
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=500,
            continuation_token=token
        )

        if not result:
            break

        for r in result:
            all_reviews.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"],
                "bank": app["bank"]
            })

        if token is None:
            break

        time.sleep(1)

    df = pd.DataFrame(all_reviews)

    filename = f"data/raw/{app['bank'].replace(' ', '_').lower()}_reviews.csv"
    df.to_csv(filename, index=False)

    print(f"Saved {len(df)} reviews to {filename}")