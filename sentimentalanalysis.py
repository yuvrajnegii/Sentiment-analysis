import csv

# Define the data to write to the CSV file
data = [
    {'title': 'Fox News', 'slug': 'fox-news', 'youtube_id': 'UCXIJgqnII2ZOINSWNOGFThA', 'playlist_id': 'UUXIJgqnII2ZOINSWNOGFThA', 'url': 'https://www.youtube.com/user/FoxNewsChannel', 'color': '#5975a4'},
    {'title': 'CNN', 'slug': 'cnn', 'youtube_id': 'UCupvZG-5ko_eiXAupbDfxWw', 'playlist_id': 'UUupvZG-5ko_eiXAupbDfxWw', 'url': 'https://www.youtube.com/user/CNN', 'color': '#b55d60'},
    {'title': 'MSNBC', 'slug': 'msnbc', 'youtube_id': 'UCaXkIU1QidjPwiAYu6GcHjg', 'playlist_id': 'UUaXkIU1QidjPwiAYu6GcHjg', 'url': 'https://www.youtube.com/user/msnbcleanforward', 'color': '#5f9e6e'},
    {'title': 'CBS News', 'slug': 'cbs-news', 'youtube_id': 'UC8p1vwvWtl6T73JiExfWs1g', 'playlist_id': 'UU8p1vwvWtl6T73JiExfWs1g', 'url': 'https://www.youtube.com/user/CBSNewsOnline', 'color': '#666666'},
]

# Specify the filename
filename = "channels.csv"

# Write data to CSV file
with open(filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "slug","youtube_id" ,"playlist_id" , "url", "color"])
    writer.writeheader()  # Write the header row
    writer.writerows(data)  # Write data rows

print(f"{filename} created")