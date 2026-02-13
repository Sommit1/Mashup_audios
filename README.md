# Mashup_audios

# Mashup Generator (Program 1 & Program 2)

This repository contains my submission for the **Mashup Assignment**.

## Program 1 (CLI Program)
A command-line Python program that:
- Takes **Singer Name**, **Number of videos (n)**, **Duration from each video (y seconds)**, and **Output file name**
- Downloads top `n` YouTube audio results for the singer (via `yt-dlp`)
- Trims first `y` seconds from each audio
- Merges all clips into a single mashup file using **FFmpeg**
- Generates final output as `.mp3`

### Run (Program 1)
```bash
python 102303184.py "Sharry Maan" 20 30 102303184-output.mp3

