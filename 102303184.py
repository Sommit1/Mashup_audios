import sys
import shutil
import tempfile
from pathlib import Path

import yt_dlp
from pydub import AudioSegment


def print_usage(prog_name: str) -> None:
    print("Usage:")
    print(f'  python {prog_name} "<SingerName>" <NumberOfVideos> <AudioDurationSec> <OutputFileName>')
    print("Example:")
    print(f'  python {prog_name} "Sharry Maan" 20 20 102303184-output.mp3')


def validate_args(argv):
    # argv = [program.py, singer, N, Y, output.mp3]
    if len(argv) != 5:
        print("Error: Incorrect number of parameters.")
        print_usage(Path(argv[0]).name)
        sys.exit(1)

    singer = argv[1].strip()
    if not singer:
        print("Error: SingerName cannot be empty.")
        sys.exit(1)

    try:
        n = int(argv[2])
    except ValueError:
        print("Error: NumberOfVideos must be an integer.")
        sys.exit(1)

    try:
        y = int(argv[3])
    except ValueError:
        print("Error: AudioDurationSec must be an integer.")
        sys.exit(1)

    out_file = argv[4].strip()
    if not out_file.lower().endswith(".mp3"):
        print("Error: OutputFileName must end with .mp3")
        sys.exit(1)

    # As per assignment statement
    if n <= 10:
        print("Error: NumberOfVideos (N) must be greater than 10.")
        sys.exit(1)

    if y <= 20:
        print("Error: AudioDurationSec (Y) must be greater than 20 seconds.")
        sys.exit(1)

    return singer, n, y, out_file


def check_ffmpeg():
    # pydub requires actual ffmpeg.exe installed on system
    if shutil.which("ffmpeg") is None:
        print("Error: FFmpeg not found in PATH.")
        print("Install FFmpeg and then verify using: ffmpeg -version")
        sys.exit(1)


def download_n_audios_from_youtube(query: str, n: int, download_dir: Path):
    """
    Uses yt-dlp to search YouTube and download best audio as mp3 for N results.
    """
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "default_search": "ytsearch",
        "outtmpl": str(download_dir / "%(title).200s.%(ext)s"),
        "format": "bestaudio/best",
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ytsearchN:query
        ydl.extract_info(f"ytsearch{n}:{query}", download=True)

    mp3_files = sorted(download_dir.glob("*.mp3"))
    return mp3_files


def trim_first_y_seconds(mp3_files, y_seconds: int, trimmed_dir: Path):
    """
    Cuts the first Y seconds from each mp3 and stores in trimmed_dir.
    """
    trimmed = []
    limit_ms = y_seconds * 1000

    for i, f in enumerate(mp3_files, start=1):
        try:
            audio = AudioSegment.from_file(f)
            clip = audio[:limit_ms]
            out_path = trimmed_dir / f"clip_{i:03d}.mp3"
            clip.export(out_path, format="mp3", bitrate="192k")
            trimmed.append(out_path)
        except Exception as e:
            print(f"Warning: Could not process {f.name}: {e}")

    return trimmed


def merge_all(trimmed_files, output_file: str):
    """
    Merges all clips into one mp3.
    """
    if not trimmed_files:
        print("Error: No trimmed clips available to merge.")
        sys.exit(1)

    combined = AudioSegment.empty()
    for f in trimmed_files:
        combined += AudioSegment.from_file(f)

    combined.export(output_file, format="mp3", bitrate="192k")


def main():
    singer, n, y, out_file = validate_args(sys.argv)
    check_ffmpeg()

    temp_dir = Path(tempfile.mkdtemp(prefix="mashup_"))
    download_dir = temp_dir / "downloads"
    trimmed_dir = temp_dir / "trimmed"

    download_dir.mkdir(parents=True, exist_ok=True)
    trimmed_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Downloading {n} YouTube audios for: {singer}")
        mp3_files = download_n_audios_from_youtube(singer, n, download_dir)

        if len(mp3_files) == 0:
            print("Error: No audio files were downloaded.")
            sys.exit(1)

        if len(mp3_files) < n:
            print(f"Note: Only {len(mp3_files)} files downloaded (some downloads may have failed).")

        print(f"Cutting first {y} seconds from each audio...")
        trimmed_files = trim_first_y_seconds(mp3_files, y, trimmed_dir)

        print("Merging all trimmed clips into one output file...")
        merge_all(trimmed_files, out_file)

        print(f"Done ✅ Output created: {out_file}")

    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    finally:
        # Cleanup temp files
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
