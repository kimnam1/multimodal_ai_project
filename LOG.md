# LOG

## Dataset collection

[1] collect Shorts IDs (yt-dlp)

    - use search Query
    - General Queries + Trending Queries (from trend.google.com)
    - Only IDs this time
    - Collect ID first and filter (view_count, duration) after because searching by view count is not available at Youtube API.

[2] Extract video metadata (yt-dlp)

    - video_id
    - title
    - duration (<= 60)
    - view_count (>= 1_000_000)
    - comments enabled (more than 50 comments)

[3] Get video.mp4 by video_id

    - more than 10,000 videos
    - 480p
    - data/raw/videos

[4] Get comments by video_id

    - top 50 by likes (with 'like_count' >= 1)

## Target directory structure

```
youtube_shorts_meme_dataset/
├── videos.csv                  # Video metadata
├── comments.csv                # All comments (labeled)
├── raw/
│   ├── videos/
│   │   └── {video_id}.mp4      # 480p original
│   └── comments/
│       └── {video_id}.json     # Raw comments per video
└── scripts/
        ├── 01_collect_ids.py
        ├── 02_download_videos.py
        ├── 03_scrape_comments.py
        └── 04_label_and_clean.py
```
