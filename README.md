# YouTube News Sentiment & Topic Analysis

A data pipeline and analysis notebook that collects the latest 8,000 videos from four U.S. news channels on YouTube, tags each video title with political topics, scores title sentiment with VADER, and tests whether the channels differ in how negatively they word their Trump headlines.

**Headline finding:** MSNBC's Trump-related headlines score slightly more negative on VADER than CBS, CNN and Fox News combined (mean −0.151 vs −0.072; Mann-Whitney U, p < 0.001). The difference is statistically significant but small. It measures headline *wording*, not the channel's coverage or bias.

---

## What it does

1. **Collects** up to 2,000 recent videos per channel (Fox News, CNN, MSNBC, CBS News) using the YouTube Data API v3.
2. **Tags topics** by matching each video title against keyword patterns for 7 topics: Obama, Clinton, Trump, Democrats, Republicans, Liberals, Conservatives.
3. **Scores sentiment** of each title with NLTK's VADER (compound score from −1, very negative, to +1, very positive).
4. **Analyzes** topic coverage per channel and average sentiment per channel and topic.
5. **Tests** the Trump-headline sentiment difference between channels with Kruskal-Wallis and Mann-Whitney U.

## Pipeline

```
channels.csv  +  topics.csv
      │
      ▼
youtube_api.download_channels_videos()   YouTube Data API v3, playlistItems.list
      │                                  (50 per page, up to 2,000 per channel)
      ▼
youtube_api.merge_channel_videos()       → videos-MERGED.csv
      │
      ▼
utils.create_topic_columns()             regex per topic on the title
      │                                  → one True/False column per topic + "relevant"
      ▼                                  → videos.csv
language_api.download_sentiments()       VADER compound score per title
      │                                  → sentiments.csv
      ▼
Project.ipynb                            coverage charts, sentiment by channel × topic,
                                         Kruskal-Wallis + Mann-Whitney U
```

## Results

Dataset: 8,000 videos (exactly 2,000 per channel), collected Oct 17, 2026.

| | Videos matching a topic | Share of channel's videos |
|---|---|---|
| MSNBC | 1,006 | 50.3% |
| CBS News | 428 | 21.4% |
| Fox News | 406 | 20.3% |
| CNN | 398 | 19.9% |
| **Total** | **2,238** | **28.0%** |

Trump appears in 2,027 of the 2,238 matched videos (90.6%), so the channel comparison focuses on that topic. The other topics have too few videos to test (Obama 32, Clinton 5, Liberals 1, Conservatives 5).

**Mean VADER sentiment of Trump videos**

| Channel | Videos | Mean sentiment |
|---|---|---|
| MSNBC | 930 | −0.151 |
| CNN | 370 | −0.090 |
| Fox News | 359 | −0.067 |
| CBS News | 368 | −0.059 |

**Statistical tests (Trump videos)**

| Test | Result |
|---|---|
| Kruskal-Wallis, all 4 channels | H = 22.91, p = 4.21×10⁻⁵ |
| Mann-Whitney U, MSNBC vs the other 3 combined | U = 451,460, p = 4.70×10⁻⁶ |

How to read it:
- **Kruskal-Wallis** (rank-based ANOVA) says the four channels are not all the same.
- **Mann-Whitney U** says MSNBC is the one that differs. A random MSNBC video scores higher than a random video from the other channels only 44.3% of the time (50% would mean no difference), an effect size (rank-biserial r) of about −0.12, which is small.
- Rank-based tests are used because VADER scores are bounded and 36% of Trump-video scores are exactly 0.0, so they are not bell-shaped.

## Limitations

- **Headline wording, not coverage:** VADER scores the words in the title. Emphatic headline styles score more negative regardless of a channel's stance.
- **Keyword topic matching:** regex on titles only. It misses paraphrases ("the former president") and mentions that appear only in the description. Its accuracy has not been measured.
- **Different time windows:** each channel contributes its latest 2,000 videos, so the windows differ (MSNBC about 32 days, Fox 37, CNN 56, CBS 63). Restricting every channel to the common window gives the same overall result (MSNBC vs the others p ≈ 1.9×10⁻⁴), but MSNBC vs CNN alone is then not significant.
- **Per-channel comparisons:** the p < 0.001 result is for MSNBC versus the other three combined. MSNBC vs CNN alone gives p = 0.014 (0.042 after Bonferroni correction).
- **Not fully independent:** many videos cover the same news events, and 122 videos match more than one topic, so p-values are somewhat optimistic.
- **Snapshot data:** the API returns the *current* latest videos, so a fresh run gives different numbers. The provided `videos.csv` and `sentiments.csv` are the dataset behind the results above.

## Project structure

```
.
├── Project.ipynb            # main notebook: pipeline, analysis, statistical tests
├── my_code/
│   ├── youtube_api.py       # download and merge channel videos
│   ├── utils.py             # regex topic tagging
│   ├── language_api.py      # VADER sentiment scoring
│   └── plotting.py          # bar charts and time-series plots
├── channels.csv             # 4 channels, playlist IDs, plot colors
├── topics.csv               # 7 topics with keyword variants
├── sentimentalanalysis.py   # script that generates channels.csv
├── videos.csv               # generated: videos + topic columns (8,000 rows)
├── sentiments.csv           # generated: VADER score per video (8,000 rows)
└── google-api-key.txt       # YOUR API key (not committed, see below)
```

`csvmaker.py` is an unused leftover from an earlier attempt with the Google Cloud Natural Language API; the project uses VADER instead.

## Setup

**1. Install dependencies** (Python 3):

```bash
pip install pandas numpy matplotlib seaborn nltk scipy google-api-python-client jupyter
```

The VADER lexicon is downloaded automatically on first run.

**2. Get a YouTube Data API key**

Create a project in the [Google Cloud Console](https://console.cloud.google.com/), enable *YouTube Data API v3*, create an API key, and save it as `google-api-key.txt` in the project folder (the key only, on one line).

**Never commit this file.** Add it to `.gitignore`:

```
google-api-key.txt
```

**3. Run**

Open `Project.ipynb` from the project folder (the code reads `google-api-key.txt` and the CSVs by relative path) and run the cells top to bottom.

- To reuse the provided data, skip the first cell's download step and start from the cell that reads `videos.csv`.
- To collect fresh data, delete `sentiments.csv` first. The scoring step appends to the file, so re-running it on an existing file duplicates rows.

## Configuration

- **Channels:** edit `channels.csv` (title, slug, YouTube channel ID, uploads playlist ID, color).
- **Topics:** edit `topics.csv` (title, slug, up to two keyword variants per topic).
- **Videos per channel:** change `max_videos` in `download_channel_videos()` in `my_code/youtube_api.py` (default 2,000).

## Tech stack

Python · YouTube Data API v3 (`google-api-python-client`) · NLTK VADER · pandas · NumPy · SciPy (Kruskal-Wallis, Mann-Whitney U) · matplotlib · seaborn · Jupyter
