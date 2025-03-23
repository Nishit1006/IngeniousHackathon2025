# most required python interpreter
- must need python Anaconda
  
# Farmer Credit Evaluation Tool

An alternative credit scoring system for farmers that uses non-traditional data sources like GIS data, weather forecasts, soil health metrics, and past crop yields to provide a fair and comprehensive credit assessment.

## Features

- Alternative credit score calculation based on agricultural data
- GIS integration for farmland tracking and analysis
- Weather forecasting and its impact on farming operations
- Soil health monitoring and analysis
- Crop yield history tracking
- Loan application processing system
- Different user roles (Farmers, Financial Institutions, Admins)
- Dashboard for farmers and financial institutions

## Tech Stack

### Frontend
- HTML, CSS, JavaScript
- Tailwind CSS for responsive design
- Chart.js for data visualization
- Leaflet.js for GIS/mapping integration

### Backend
- Django & Django REST Framework
- PostgreSQL database (SQLite for development)
- Celery & Redis for background tasks and caching

### APIs & Data Sources
- OpenStreetMap for GIS data
- Open-Meteo API for weather forecasts
- AgroMonitoring API for satellite-based soil data
- MapMyCrop API for crop monitoring

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip
- virtualenv
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/farmer-credit-tool.git
   cd farmer-credit-tool
   ```

2. Create and activate virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Setup environment variables (create a .env file):
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///db.sqlite3  # For development
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser

## API Documentation

Once the server is running, you can access the API documentation at:
- http://127.0.0.1:8000/api/docs/

## User Roles

### Farmer
- Register and maintain profile
- Add and manage farmland details
- View credit score and factors affecting it
- Apply for loans from partnered financial institutions
- Track loan application status and repayment schedule

### Financial Institution
- Register as a financial institution
- Create loan products
- Review and approve/reject loan applications
- View detailed farmer credit reports
- Manage loan disbursements and repayments

### Admin
- Manage all users and profiles
- Configure credit score calculation parameters
- Monitor system usage and performance
- Verify farmland details
- Generate reports

## Project Structure

```
farmer_credit_tool/
├── accounts/            # User account management
├── credit_score/        # Credit scoring system
├── gis_data/            # GIS and land management
├── loan_application/    # Loan application processing
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── farmer_credit_evaluation/  # Main project directory
└── manage.py            # Django management script
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all the open-source projects and APIs that make this tool possible
- Special thanks to agricultural experts who contributed to the credit scoring model 
