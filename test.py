import requests


url = "http://127.0.0.1:8000/ingest_data/"
files = {
    "file": (
        "sales_performance_data.csv",
        open("sales_performance_data.csv", "rb"),
        "text/csv",
    )
}
data = {"file_type": "csv"}

response = requests.post(url, files=files, data=data)
print(response.json())


# Example function to read the data
def read_data():
    df = pd.read_csv("sales_performance_data.csv")  # Adjust path as needed
    return df

df = read_data()
print(df.head())
