# [Inventory Management System](https://disco-nirvana-403601.de.r.appspot.com)

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

"""
Project: Inventory Management System with Flask and Google Sheets Integration

 Description:
 Developed a web-based Inventory Management System using Flask, a Python web framework, to streamline inventory tracking and order placement.

 Key Contributions:
     Implemented a responsive front-end using Flask, HTML, and Jinja templating, providing user-friendly interfaces for both iOS and Android platforms.
     Integrated Google Sheets API for real-time storage and retrieval of inventory data, allowing for seamless updates and order placement.
     Utilized threading for concurrent access to the Google Sheets backend, ensuring data consistency and preventing race conditions.
     Created RESTful API endpoints for updating inventory values, retrieving product details by barcode, and placing orders.

 Technologies Used:
     Python (Flask)
     Google Sheets API
     Gunicorn (for production deployment)
     HTML, Jinja
     Threading for concurrency management

 Outcome:
 Successfully deployed the system, enhancing the efficiency of inventory management and order processing.

 Skills Demonstrated:
     Full-stack web development
     API integration
     Threading and concurrency management
     Problem-solving and error handling
     Collaboration and teamwork

"""
