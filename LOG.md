# LOG

## Dataset collection

[1-1] collect Shorts IDs (yt-dlp)

    - use search Query
    - General Queries + Trending Queries (from trend.google.com)
    - Only IDs this time
    - Collect ID first and filter (view_count, duration) after because searching by view count is not available at Youtube API.

[1-2] collect Short IDs (Kaggle)

    - use kaggle datasets (trending videos)
        - https://www.kaggle.com/datasets/canerkonuk/youtube-trending-videos-global/data?select=youtube_trending_videos_global.csv
    - use only US + canada region (for english content filtering)

    - Trending Video count (data/ids/us_canada...)
        - US/Canada total : 55908 videos
        - US/Canada under 60s : 1163 videos
        - US/Canada under 90s : 2141 videos
        - US/Canada under 120s : 3288 videos
        - US/Canada over 60s : 54745 videos

[2] Extract video metadata (yt-dlp)

    - heads
        video_id,video_title,video_published_at,video_duration,video_view_count,channel_id,video_like_count,video_comment_count,video_category_id,channel_title,duration_sec
    - video_id
    - video_title
    - video_published_at
    - video_duration_sec
    - video_view_count
    - video_like_count
    - video_comment_count
    - video_category_id
    - channel_id
    - channel_title
    - comments enabled (more than 50 comments)

    - From [1-1],
        - data/ids/query_enriched_ids.csv

[3] Get video.mp4 by video_id

    - 480p
    - data/raw/videos/{video_id}.mp4

    - maybe slicing to jpg (~1 fps) could be needed

[4] Get comments by video_id

    - top 50 by likes (with 'like_count' >= 1)

## Target directory structure

```
data/
├── ids/                        # Video ids (not important)
├── videos.csv                  # Video metadata
├── comments.csv                # All comments (labeled)
├── raw/
│   ├── videos/
│   │   └── {video_id}.mp4      # 480p original
│   └── comments/
└──     └── {video_id}.json     # Raw comments per video
```
