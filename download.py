import requests
import os
from crendentials import USER, PASSWORD


def download_month(
        data_type: str,
        year: int,
        month: int,
        out_dir: str
):
    """
    Downloads Stocktwits messages or activities for a given month. This requires partner-level API.
    :param data_type: Must be 'acitivy' or 'message'
    :param year: Four-digit year
    :param month: Starting from 1
    :param out_dir: The directory for saving the file
    :return: None
    """
    session = requests.Session()
    session.auth = (USER, PASSWORD)

    url = f"https://firestream.stocktwits.com/backups/{data_type}/{year}/{month}"
    try:
        response = session.get(url, stream=True)
    except requests.exceptions.HTTPError as e:
        print(e)
        return
    file_name = f"stocktwits_{data_type}_{year}_{month}.gz"
    out_path = os.path.join(out_dir, file_name)
    with open(out_path, "wb") as out_f:
        response.raise_for_status()
        for i, chunk in enumerate(response.iter_content(chunk_size=8192)):
            if chunk:
                out_f.write(chunk)
                if i % 100 == 0:
                    print("Chunks written:", (i + 1))


if __name__ == "__main__":
    out_dir = r"E:\stocktwits 2020"
    years = range(2009, 2020)
    months = range(1, 13)
    for year in years:
        for month in months:
            for data_type in ("message", "activity"):
                print(data_type, year, month)
                download_month(data_type, year, month, out_dir)


