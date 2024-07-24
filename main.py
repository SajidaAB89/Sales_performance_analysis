from fastapi import FastAPI, UploadFile, File, Form
from data_ingestion import ingest_data, SalesData
from llm import generate_insights
import pandas as pd
import logging


app = FastAPI()
app.state.df = pd.DataFrame()  # Initialize an empty DataFrame

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/ingest_data/")
async def ingest_sales_data(
    file: UploadFile = File(...), file_type: str = Form(...)
) -> dict[str, str]:
    contents = await file.read()
    sales_data = SalesData(data=contents, file_type=file_type)
    df = ingest_data(sales_data)
    app.state.df = df  # Store the DataFrame in the app state
    logger.info("Data ingested successfully. DataFrame shape: %s", df.shape)
    return {"message": "Data ingested successfully"}

@app.get("/list_representatives/")
def list_representatives():
    try:
        # Sample DataFrame for testing
        df = pd.DataFrame({"sales_rep": ["Alice", "Bob", "Charlie"]})

        if df.empty:
            logger.warning("No data ingested")
            return {"message": "No data ingested"}

        sales_reps = df["sales_rep"].unique()
        logger.info("Unique sales representatives: %s", sales_reps)
        return {"sales_reps": sales_reps.tolist()}

    except Exception as e:
        logger.exception("Error listing representatives: %s", str(e))
        return {"error": "An error occurred while listing representatives"}

@app.get("/performance/{rep_id}")
def get_rep_performance(rep_id: str):  # Assuming rep_id is a string
    try:
        df = app.state.df
        if df.empty:
            logger.warning("No data ingested")
            return {"message": "No data ingested"}

        if rep_id not in df["sales_rep"].values:
            logger.warning("Representative ID %s not found", rep_id)
            return {"message": f"Representative ID {rep_id} not found"}

        prompt = f"Provide performance analysis for sales representative {rep_id}"
        insights = generate_insights(prompt)

        return {"representative_id": rep_id, "insights": insights}

    except Exception as e:
        logger.exception(
            "Error retrieving performance for representative %s: %s", rep_id, str(e)
        )
        return {
            "error": f"An error occurred while retrieving performance for representative {rep_id}"
        }


@app.get("/team_performance/")
def get_team_performance():
    prompt = "Provide overall team performance analysis"
    insights = generate_insights(prompt)
    return {"insights": insights}


@app.get("/performance_trends/")
def get_performance_trends():
    prompt = "Provide sales performance trends and forecast"
    insights = generate_insights(prompt)
    return {"insights": insights}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
