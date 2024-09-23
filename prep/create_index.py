import click
from pathlib import Path
from tqdm import tqdm
import pandas as pd


@click.command()
@click.option("--data_root", required=True)
@click.option("--save_path", required=True)
def main(data_root: str, save_path: str):
    print(f"{data_root=}|{save_path=}")

    dfs = []
    for x in tqdm(list(Path(data_root).glob("*.parquet"))):
        df = pd.read_parquet(x)
        df["name"] = x.name.split("-")[-1][: -len(".parquet")]
        dfs.append(df)

    df_final = pd.concat(dfs, axis=0, ignore_index=True)
    df_final.to_parquet(
        save_path,
        engine="pyarrow",
        index=False,
    )


if __name__ == "__main__":
    main()
