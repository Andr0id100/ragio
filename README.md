# RAGio

A simple RAG based search interface for Formula 1 radio message transcripts.

**Tested on 2021 Formula 1 British Grand Prix**

Relevant Modules:
* get-data.sh: Download the onboard footage for all the drivers in the race. Also extracts and saved the audio file for the radio communications.
* prep/transcribe.py: Runs Voice Activity Detection (VAD) and ASR (Automatic Speech Recognition) on the audio files
* prep/embed.py: Converts the transcripts into embeddings to build a vector DB.
* rag.py: Based on the provided query, create samples that might be relevant for the query and extracts documents that could be useful to provide an answer.
* prompts.py: Prompts to provide specification for the task.
* utils.py: General utility code.

How to run:
Transcribe an audio file:
```bash
python -m prep.transcribe --audio_path temp.wav --save_path temp.csv
```

Embed an audio file:
```bash
python -m prep.embed --csv_path temp.csv --save_path temp.parquet
```

Run RAG CLI:
```bash
python rag.py
```

