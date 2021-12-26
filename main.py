from google.cloud import storage
import gzip
import io
import json
import pickle
import requests

client = storage.Client()
addons_json = client.bucket("wowless.dev").blob("addons.json")
picklefmt = "https://storage.googleapis.com/cursebreaker/{name}.pickle.gz"


def get_pickle(name):
    return pickle.load(
        gzip.open(
            io.BytesIO(requests.get(picklefmt.format(name=name)).content)
        )
    )


def get_depickled_json():
    return json.dumps(
        {
            "cf": [
                {"id": id, "slug": slug}
                for slug, id in get_pickle("cfid").items()
            ]
        },
        indent=2,
    )


def depickle():
    addons_json.upload_from_string(
        get_depickled_json(), content_type="application/json"
    )


if __name__ == "__main__":
    print(get_depickled_json())
