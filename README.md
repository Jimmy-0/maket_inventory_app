# Inventory Management System

This is a simple Flask web application for managing inventory and placing orders. It utilizes Google Sheets as a backend to store and update inventory data.

## Getting Started

These instructions will help you set up and run the application on your local machine.

### Prerequisites

- [Python](https://www.python.org/) installed on your machine
- Google Sheets API credentials in JSON format (`cred_disco-nirvana.json`)
- [Gunicorn](https://gunicorn.org/) installed (for production deployment)

### Installing

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/inventory-management.git
   cd inventory-management
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Sheets API credentials:

   Place your `cred_disco-nirvana.json` file in the project root directory.

## Running the Application

### Development

To run the application in development mode, use the following command:

```bash
python app.py
```

### Production

For production deployment, it is recommended to use Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8080 --log-level debug app:app
```

The application will be accessible at [http://localhost:8080](http://localhost:8080).

## Usage

- Access the main page at [http://localhost:8080/](http://localhost:8080/)
- Navigate to specific routes for iOS and Android numpad interfaces.

## API Endpoints

- `/update_values` (POST): Update inventory values based on data from the frontend.
- `/get_values/<barcode>` (GET): Retrieve values for a specific barcode.
- `/place_order` (POST): Place an order and update the inventory.

## Contributing

Feel free to contribute by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Gspread: [https://gspread.readthedocs.io/](https://gspread.readthedocs.io/)

--- 

Adjust the content and structure based on your application's specific details and additional information you want to include.
