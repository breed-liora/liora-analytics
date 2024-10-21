# Liora Analytics

This project contains scripts for downloading and analyzing reports from the EMA (Electronic Medical Assistant) system for Liora Dermatology & Aesthetics using Dagster.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-username/liora_analytics.git
   cd liora_analytics
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set the PYTHONPATH:
   ```
   export PYTHONPATH=/Users/reedbarric/dev/liora_analytics:$PYTHONPATH
   ```

## Project Structure

- `src/`: Main source code directory
  - `main.py`: Entry point of the application
  - `repository.py`: Dagster repository definition
  - `assets/`: Contains asset definitions
  - `ops/`: Contains operation definitions
  - `jobs/`: Contains job definitions
  - `resources/`: Contains resource definitions (e.g., IO managers)
  - `utils/`: Contains utility modules
    - `reports/`: Contains reporting-related modules
      - `config.py`: Configuration settings for the reports
      - `download_reports.py`: Main logic for downloading reports

## Running the Dagster Pipeline

To run the Dagster pipeline, use the following command:

```
dagster dev
```

This will start the Dagster UI, where you can view and execute the defined jobs.

## Notes

- Ensure you have the necessary permissions and credentials set up in `src/reporting/config.py`.
- The downloaded reports will be saved using the configured IO manager.

## Reports

The following reports are currently configured to be pulled:

1. Payments Posted by Date
2. Appointments by Date

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
