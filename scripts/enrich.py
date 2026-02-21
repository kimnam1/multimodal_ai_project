"""
youtube_shorts_dataset/video_ids.csv (query 수집본)에 있는 video_id들을
yt-dlp로 개별 조회하여 Kaggle 데이터셋과 동일한 스키마로 저장한다.
"""

import pandas as pd
import yt_dlp
import time
import os
from tqdm import tqdm

INPUT_PATH = "youtube_shorts_dataset/video_ids.csv"
OUTPUT_PATH = "data/ids/query_enriched_ids.csv"
SLEEP_SEC = 1.0

os.makedirs("data/ids", exist_ok=True)

if os.path.exists(OUTPUT_PATH):
    done_ids = set(pd.read_csv(OUTPUT_PATH)["video_id"].dropna().tolist())
    print(f"이미 처리된 ID: {len(done_ids)}개 스킵")
else:
    done_ids = set()

ids_df = pd.read_csv(INPUT_PATH)
todo = ids_df[~ids_df["video_id"].isin(done_ids)]["video_id"].tolist()
print(f"처리 대상: {len(todo)}개")

ydl_opts = {
    "quiet": True,
    "skip_download": True,
    "ignoreerrors": True,
    "no_warnings": True,
}

results = []
success = 0
failed = 0

pbar = tqdm(todo, desc="Enriching", unit="video", dynamic_ncols=True)

for i, vid in enumerate(pbar):
    url = f"https://www.youtube.com/watch?v={vid}"
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if info is None:
            failed += 1
            pbar.set_postfix(success=success, failed=failed)
            continue

        duration_sec = info.get("duration")

        raw_date = info.get("upload_date", "")
        published_at = (
            f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
            if len(raw_date) == 8
            else None
        )

        results.append(
            {
                "video_id": vid,
                "video_title": info.get("title"),
                "video_published_at": published_at,
                "video_trending_date": None,
                "video_trending_country": None,
                "video_duration": duration_sec,
                "video_view_count": info.get("view_count"),
                "channel_id": info.get("channel_id"),
                "video_like_count": info.get("like_count"),
                "video_comment_count": info.get("comment_count"),
                "video_category_id": info.get("category"),
                "channel_title": info.get("channel"),
                "duration_sec": duration_sec,
            }
        )
        success += 1

    except Exception as e:
        failed += 1

    pbar.set_postfix(success=success, failed=failed)

    if (i + 1) % 100 == 0 and results:
        df = pd.DataFrame(results)
        write_header = not os.path.exists(OUTPUT_PATH)
        df.to_csv(OUTPUT_PATH, mode="a", header=write_header, index=False)
        results = []

    time.sleep(SLEEP_SEC)

if results:
    df = pd.DataFrame(results)
    write_header = not os.path.exists(OUTPUT_PATH)
    df.to_csv(OUTPUT_PATH, mode="a", header=write_header, index=False)

total = pd.read_csv(OUTPUT_PATH)
print(
    f"\n완료. 성공: {success} / 실패: {failed} / 총 누적: {len(total)}개 → {OUTPUT_PATH}"
)
