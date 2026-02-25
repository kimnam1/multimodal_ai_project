"""
combined_ids.csv의 video_id 목록으로 YouTube Shorts를 480p mp4로 다운로드.

Usage:
    python scripts/download_videos.py              # 기본 (workers=4)
    python scripts/download_videos.py --workers 8  # 병렬 수 지정
    python scripts/download_videos.py --limit 100  # 앞 100개만 테스트
"""

import pandas as pd
import yt_dlp
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ── 설정 ──────────────────────────────────────────────────────────
INPUT_PATH = "data/ids/combined_ids.csv"
OUTPUT_DIR = "data/raw/videos"
SLEEP_SEC = 0.5  # 스레드당 요청 후 sleep
# ──────────────────────────────────────────────────────────────────

os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_ydl_opts(output_dir: str) -> dict:
    return {
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]",
        "outtmpl": os.path.join(output_dir, "%(id)s.mp4"),
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "merge_output_format": "mp4",
    }


def download_one(video_id: str) -> tuple[str, bool, str]:
    """
    Returns: (video_id, success, message)
    """
    out_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    # 이미 존재하면 스킵
    if os.path.exists(out_path):
        return video_id, True, "skipped"

    url = f"https://www.youtube.com/shorts/{video_id}"
    try:
        with yt_dlp.YoutubeDL(build_ydl_opts(OUTPUT_DIR)) as ydl:
            ret = ydl.download([url])
        time.sleep(SLEEP_SEC)

        if os.path.exists(out_path):
            return video_id, True, "ok"
        else:
            return video_id, False, "file not found after download"

    except Exception as e:
        return video_id, False, str(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers", type=int, default=4, help="병렬 다운로드 수 (default: 4)"
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="앞 N개만 다운로드 (테스트용)"
    )
    args = parser.parse_args()

    df = pd.read_csv(INPUT_PATH)
    ids = df["video_id"].dropna().unique().tolist()

    if args.limit:
        ids = ids[: args.limit]

    # 이미 다운로드된 것 제외
    already = {
        f.replace(".mp4", "")
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".mp4")
    }
    todo = [vid for vid in ids if vid not in already]

    print(
        f"전체: {len(ids)}개 | 이미 완료: {len(already)}개 | 다운로드 대상: {len(todo)}개"
    )
    print(f"병렬 workers: {args.workers}")

    success = 0
    failed = 0
    failed_ids = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_one, vid): vid for vid in todo}
        pbar = tqdm(
            as_completed(futures),
            total=len(todo),
            unit="video",
            dynamic_ncols=True,
        )

        for future in pbar:
            vid, ok, msg = future.result()
            if ok:
                success += 1
            else:
                failed += 1
                failed_ids.append((vid, msg))

            pbar.set_postfix(success=success, failed=failed)

    print(f"\n완료 — 성공: {success} / 실패: {failed}")

    if failed_ids:
        fail_df = pd.DataFrame(failed_ids, columns=["video_id", "reason"])
        fail_df.to_csv("data/ids/download_failed.csv", index=False)
        print("실패 목록 → data/ids/download_failed.csv")


if __name__ == "__main__":
    main()
