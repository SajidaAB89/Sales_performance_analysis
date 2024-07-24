
import pandas as pd
from typing import Union
from pydantic import BaseModel
import io

class SalesData(BaseModel):
    data: Union[str, bytes]  # to handle both string and file inputs
    file_type: str

def ingest_data(sales_data: SalesData) -> pd.DataFrame:
    if sales_data.file_type == 'csv':
        df = pd.read_csv(io.StringIO(sales_data.data.decode('utf-8')))
    elif sales_data.file_type == 'json':
        df = pd.read_json(io.StringIO(sales_data.data.decode('utf-8')))
    else:
        raise ValueError("Unsupported file type")
    return df