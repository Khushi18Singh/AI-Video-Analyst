# import os
# import yt_dlp
# from pydub import AudioSegment

# DOWNLOAD_DIR = "downloads"
# os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# def download_youtube_audio(url: str) -> str:
#     """Download audio from a YouTube URL and return the .wav file path."""
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
#         "postprocessors": [
#             {"key": "FFmpegExtractAudio", "preferredcodec": "wav"}
#         ],
#         "quiet": True,
#         "noplaylist": True,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         return info["requested_downloads"][0]["filepath"]


# def convert_to_wav(input_path: str) -> str:
#     """Convert any audio/video file to 16kHz mono WAV."""
#     output_path = os.path.splitext(input_path)[0] + "_converted.wav"
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_channels(1).set_frame_rate(16000)  # 16 kHz
#     audio.export(output_path, format="wav")
#     return output_path


# if __name__ == "__main__":
#     path = download_youtube_audio("https://youtu.be/UdE-W30oOXo")
#     print("Saved to:", path)

#     converted = convert_to_wav(path)
#     print("Converted:", converted)


# def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
#     audio = AudioSegment.from_wav(wav_path)
#     chunk_ms = chunk_minutes * 60 * 1000 

#     chunks = []

#     for i, start in enumerate(range(0,len(audio),chunk_ms)):
#         chunk = audio[start : start + chunk_ms]
#         chunk_path = f"{wav_path}_chunk_{i}.wav"
#         chunk.export(chunk_path , format = "wav")

#         chunks.append(chunk_path)
    
#     return chunks




import yt_dlp
from pydub import AudioSegment
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloades')
os.makedirs(DOWNLOAD_DIR,exist_ok = True)

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename



def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks

if __name__ == "__main__":
    path = download_youtube_audio("https://youtu.be/UdE-W30oOXo")
    print("Downloaded:", path)

    converted = convert_to_wav(path)
    print("Converted:", converted)

    chunks = chunk_audio(converted)
    print("Chunks:", chunks)