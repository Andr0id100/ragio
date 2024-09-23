import google.generativeai as genai

import click
from tqdm import tqdm

import pandas as pd
import numpy as np


@click.command()
@click.option("--csv_path", required=True)
@click.option("--save_path", required=True)
@click.option("--model", default="models/text-embedding-004")
def embed(csv_path: str, save_path: str, model: str):
    print(f"{csv_path=}|{save_path=}|{model=}")

    df = pd.read_csv(csv_path)

    embeddings = []
    for i in tqdm(range(len(df))):
        text = df.iloc[i].text

        result = genai.embed_content(
            model=model,
            content=text,
            task_type="retrieval_document",
        )
        embeddings.append(np.array(result["embedding"]))

    df["embedding"] = embeddings

    df.to_parquet(
        save_path,
        engine="pyarrow",
        index=False,
    )


if __name__ == "__main__":
    embed()


# 1 input > 1 vector output
