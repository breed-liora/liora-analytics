from dagster import asset, Output, AssetIn, get_dagster_logger
from src.utils.reports.download_reports import download_report, setup_driver, login
from src.utils.reports.config import REPORTS
from src.utils.data_cleaning import standardize_column_names

logger = get_dagster_logger()

@asset(group_name="financials")
def payments_posted_by_date():
    driver = setup_driver()
    login(driver)
    logger.info("Successfully logged in")
    
    report = REPORTS['payments_posted_by_date']
    df = download_report(driver, report)
    logger.info(f"Report '{report['name']}' downloaded successfully")
    
    standardized_df = standardize_column_names(df)
    logger.info(f"Data standardized and saved. Number of rows: {len(standardized_df)}")
    
    return Output(standardized_df, metadata={"num_rows": len(standardized_df)})


if __name__ == "__main__":
    result = payments_posted_by_date()
    print(f"Asset executed successfully. Number of rows: {result.metadata['num_rows']}")
    print(result.value.head())  # Display the first few rows of the DataFrame