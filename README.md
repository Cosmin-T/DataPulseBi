# DataPulse

DataPulse is a data visualization and exploration tool that allows users to connect to various data sources, including SQL databases, PostgreSQL, Microsoft SQL Server, DETA, and MongoDB. It provides a simple and intuitive interface for loading data, visualizing it, and gaining insights.

## Features

* Connect to various data sources, including SQL databases, PostgreSQL, Microsoft SQL Server, DETA, and MongoDB
* Load data from files (CSV, XLSX, XLS) or databases
* Visualize data using interactive dashboards
* Explore data using filtering, sorting, and grouping
* Support for multiple tables and databases

## Requirements

* Python 3.8+
* Streamlit
* pandas
* pygwalker
* streamlit-components
* mysql-connector-python
* psycopg2
* pytds
* deta
* pymongo

## Installation

1. Clone the repository: `git clone https://github.com/your-username/DataPulse.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the application: `streamlit run main.py`

## Usage

1. Launch the application by running `streamlit run main.py`
2. Select a data source from the sidebar
3. Enter the connection details for the selected data source
4. Load the data by clicking the "Login" button
5. Visualize the data using the interactive dashboard

## Troubleshooting

* Check the console output for error messages
* Verify the connection details for the selected data source
* Ensure that the required packages are installed

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed. See [LICENSE](LICENSE) for details.

## Acknowledgments

* Streamlit for providing a simple and intuitive way to build web applications
* pandas for providing a powerful data manipulation library
* pygwalker for providing a simple way to create interactive dashboards
* mysql-connector-python, psycopg2, pytds, deta, and pymongo for providing database connectors
