import pandas as pd
import numpy as np

import google.generativeai as genai
import os

from utils import create_formatted_transcripts
from prompts import sample_data_generation_prompt, query_prompt

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# df = pd.read_parquet("bahrain-ver.parquet")
df = pd.read_parquet("index.parquet")
# df = pd.read_parquet("data/embedding/Formula 1 Race - 2021 British Grand Prix-ALO.parquet")
df.embedding = df.embedding.map(np.array)

embeddings = np.array(df.embedding.tolist())

model = genai.GenerativeModel("gemini-1.5-flash")

while True:
    query = input("State your query about the 2021 British Grand Prix: ")
    # query = "Were there any safety cars?"

    query_embedded = np.array(
        genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_document",
        )["embedding"]
    )

    response = model.generate_content(
        contents=[sample_data_generation_prompt.format(query=query)]
    )
    sentences = eval(
        response.text[response.text.index("[") : response.text.rfind("]") + 1]
    )

    sentences_embedded = np.array(
        genai.embed_content(
            model="models/text-embedding-004",
            content=sentences,
            task_type="retrieval_document",
        )["embedding"]
    )

    similarities = (embeddings @ sentences_embedded.T).max(-1)
    order = np.argsort(similarities)[::-1]

    df_relevant = df.iloc[order[:50]]
    transcripts = create_formatted_transcripts(df_relevant)

    response = model.generate_content(
        contents=[query_prompt.format(query=query, transcripts=transcripts)],
        stream=True,
    )
    for x in response:
        print(x.text, end="")

    print("=" * 40)
