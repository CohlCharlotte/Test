import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import json
import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client


def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)


with open("data/clean_data.json", "r") as f:
    data = json.load(f)
print(type(data))

df = pd.DataFrame(data['teams'])
df.to_csv("data/clean_data.csv")

print(df.head())


def upload_dataframe(df: pd.DataFrame, table_name: str, supabase: Client):
    """
    Uploads a Pandas DataFrame to a Supabase table.
    If the table does not exist, create it manually in the Supabase UI first.
    """
    # Convert DataFrame to list of dicts
    records = df.to_dict(orient="records")

    # Insert into Supabase
    response = supabase.table(table_name).insert(records).execute()

    if response.data:
        print(f"✅ Uploaded {len(response.data)} rows to '{table_name}'")
    else:
        print(f"⚠️ Upload failed: {response}")

def main():
    supabase = get_client()

    upload_dataframe(df, "models_upload", supabase)

    response = supabase.table("models_upload").select("*").execute()
    print("Rows in models_upload:")
    for row in response.data:
        print(row)

if __name__ == "__main__":
    main()
