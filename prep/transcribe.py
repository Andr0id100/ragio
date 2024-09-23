import soundfile as sf
from faster_whisper import WhisperModel
import librosa
import numpy as np
from tqdm import tqdm
from silero_vad import load_silero_vad, get_speech_timestamps
import noisereduce as nr
import pandas as pd
import click

from prompts import asr_prompt

@click.command()
@click.option("--audio_path", required=True)
@click.option("--save_path", required=True)
@click.option("--whisper_model", default="medium.en")
@click.option("--noise_reduce", default=False)
def main(audio_path: str, save_path: str, whisper_model: str, noise_reduce: bool):
    print(f"{audio_path=}|{save_path=}|{whisper_model=}|{noise_reduce=}")

    whisper_model = WhisperModel(whisper_model)

    vad_model = load_silero_vad()

    audio, sr = sf.read(audio_path)
    audio = np.transpose(audio)
    if sr != 16_000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16_000)
        sr = 16_000

    audio = audio.mean(0)
    audio = np.float32(audio)

    speech_timestamps = get_speech_timestamps(
        audio, vad_model, min_silence_duration_ms=1000
    )

    
    data = []

    for speech_segment in tqdm(speech_timestamps):
        segment_audio = audio[speech_segment["start"] : speech_segment["end"]]

        if noise_reduce:
            segment_audio = nr.reduce_noise(y=segment_audio, sr=sr)

        segments, info = whisper_model.transcribe(
            segment_audio, beam_size=5, initial_prompt=asr_prompt
        )
        transcript = "".join(map(lambda x: x.text, segments)).strip()

        if len(transcript) == 0:
            transcript = "<NO_SPEECH_DETECTED>"

        print(transcript)

        data.append(
            (speech_segment["start"] / sr, speech_segment["end"] / sr, transcript)
        )

    df = pd.DataFrame(data, columns=["start", "end", "text"])
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
