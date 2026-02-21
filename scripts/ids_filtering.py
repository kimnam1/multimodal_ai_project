# https://www.kaggle.com/datasets/canerkonuk/youtube-trending-videos-global/data
import pandas as pd
import isodate

IDS_DATA_PATH = "data/ids/youtube_trending_videos_global.csv"

COLS = [
    "video_id",
    "video_title",
    "video_published_at",
    "video_trending__date",
    "video_trending_country",
    "video_duration",
    "video_view_count",
    "channel_id",
    "video_like_count",
    "video_comment_count",
    "video_category_id",
    "channel_title",
]

chunks = []
for chunk in pd.read_csv(IDS_DATA_PATH, chunksize=100000, low_memory=False):
    us = chunk[
        chunk["video_trending_country"].isin(["United States", "Canada"])
    ][COLS]
    chunks.append(us)

df = pd.concat(chunks).drop_duplicates(subset="video_id")
df = df.rename(columns={"video_trending__date": "video_trending_date"})

# duration (ISO 8601) to seconds
df["duration_sec"] = df["video_duration"].apply(
    lambda x: (
        int(isodate.parse_duration(x).total_seconds()) if pd.notna(x) else None
    )
)

# shorts = df[df["duration_sec"] <= 120]
# print(f"US/Canada 고유 영상: {len(df)}개")
# print(f"US/Canada Shorts candidates(≤120s): {len(shorts)}개")
# shorts.to_csv("data/ids/us_canada_120s_candidates.csv", index=False)

normal = df[df["duration_sec"] > 60]

print(f"US/Canada Shorts candidates(≤120s): {len(normal)}개")
normal.to_csv("data/ids/us_canada_over60s_candidates.csv", index=False)

print(f"US/Canada Normal videos (>60s): {len(normal)}개")
normal.to_csv("data/ids/us_canada_over60s_videos.csv", index=False)

df.to_csv("data/ids/us_canada_videos.csv", index=False)
