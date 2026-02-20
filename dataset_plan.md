# YouTube Shorts Meme Comment Dataset Plan

## Overview

Build a multimodal AI training dataset by collecting YouTube Shorts videos and popular comments.
The goal is to train a model that generates high-engagement comments given a video as input.

## Target Scale

| Item               | Target                 |
| ------------------ | ---------------------- |
| Number of Shorts   | 10,000                 |
| Comments per Video | Top 50 (by popularity) |

## Data Schema

### 1. Video Metadata (`videos.csv`)

| Field           | Type   | Description                        |
| --------------- | ------ | ---------------------------------- |
| `video_id`      | string | YouTube video ID                   |
| `title`         | string | Video title                        |
| `description`   | string | Video description                  |
| `creator`       | string | Channel name                       |
| `creator_id`    | string | Channel ID                         |
| `view_count`    | int    | Total views                        |
| `like_count`    | int    | Video likes                        |
| `comment_count` | int    | Total comments                     |
| `duration`      | int    | Video length (seconds)             |
| `upload_date`   | string | Upload date                        |
| `tags`          | string | Tags (comma-separated)             |
| `category`      | string | YouTube category (yt-dlp provided) |
| `collected_at`  | string | Collection timestamp (ISO 8601)    |

### 2. Comments (`comments.csv`)

| Field              | Type   | Description                         |
| ------------------ | ------ | ----------------------------------- |
| `comment_id`       | string | Comment unique ID                   |
| `video_id`         | string | Video ID (FK)                       |
| `text`             | string | Comment text                        |
| `like_count`       | int    | Comment likes                       |
| `author`           | string | Comment author                      |
| `is_reply`         | bool   | Whether reply                       |
| `creator_heart`    | bool   | Creator heart status                |
| `time_text`        | string | Comment timestamp text              |
| `rank`             | int    | Like rank within video (1~50)       |
| `label`            | string | Engagement label (high / mid / low) |
| `normalized_score` | float  | Normalized score within video (0~1) |

## Labeling Strategy

### Engagement Label (Per-Comment)

Based on comment like_count percentile within video:

| Label  | Criterion  | Usage                               |
| ------ | ---------- | ----------------------------------- |
| `high` | Top 10%    | Positive sample (generation target) |
| `mid`  | Top 10~50% | Neutral                             |
| `low`  | Bottom 50% | Negative sample                     |

### Normalized Score

Since comment distribution varies by video, apply per-video normalization:

```
normalized_score = (comment_likes - min_likes) / (max_likes - min_likes + 1)
```

## Directory Structure

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

Git includes only scripts/ and CSV files. Add raw/ to .gitignore and share via Google Drive.

## Collection Pipeline

```
[1] Collect Shorts IDs (yt-dlp)
                ↓
[2] Extract video metadata (yt-dlp --dump-json)
                ↓
[3] Filter: duration <= 60s, views >= 10K, comments enabled
                ↓
[4] Download videos (480p) → raw/videos/
                ↓
[5] Scrape comments (top 50 by likes) → raw/comments/
                ↓
[6] Clean & label → videos.csv, comments.csv
```

## Filtering Criteria

- `duration` <= 60 seconds
- `view_count` >= 1,000,000
- Comments enabled
- Include only top 50 comments with `like_count` >= 1
- Language: English

## Estimated Collection Time

| Stage                          | Expected Time    |
| ------------------------------ | ---------------- |
| Collect Shorts IDs (1,000)     | 1~2 hours        |
| Extract metadata               | 30 minutes       |
| Download videos (480p, 10,000) | 3~5 hours        |
| Scrape comments (50K)          | 3~5 hours        |
| Clean & label                  | 1 hour           |
| **Total**                      | **~10~14 hours** |

## Notes

1. **Copyright**: Specify research purpose. No redistribution of data.
2. **Rate Limiting**: Apply 1~2 second sleep between requests to prevent IP blocking.
3. **Data Bias**: Large channels may skew comment styles. Ensure channel diversity.
4. **Collection Timestamp**: Comment likes change over time. Record collection time in `collected_at` field. Collecting mature videos ensures stable like counts.
5. **Language Mixing**: Consider adding language detection filter.
6. **Google Drive Sharing**: Share raw/ folder via Google Drive. Access in Colab with drive.mount().
