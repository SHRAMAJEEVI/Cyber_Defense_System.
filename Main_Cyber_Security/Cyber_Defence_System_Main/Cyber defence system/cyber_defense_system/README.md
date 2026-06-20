# Cyber Threat Detection System

A Django-based web application that simulates a cyber defense monitoring platform with a built-in web honeypot to capture unauthorized login attempts.

## Features

- **Honeypot Login System**: Fake admin login that captures attacker data
- **Attack Logging**: Records IP, username, password, user agent, and timestamp
- **Real-time Dashboard**: Shows attack statistics and trends
- **Security Alerts**: Detects brute force attacks (>5 attempts from same IP)
- **Attack Timeline**: Visual chart of attacks over last 24 hours
- **Detailed Logs**: Searchable table of all attack attempts

## Installation

1. Clone or download the project
2. Navigate to project directory:
   ```bash
   cd cyber_defense_system
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
6. Start development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### Testing the Honeypot

1. Visit `http://127.0.0.1:8000/honeypot-login/`
2. Enter any username/password combination
3. The system will capture the attempt and show "Invalid credentials"
4. View captured data in the dashboard at `http://127.0.0.1:8000/dashboard/`

### Accessing Features

- **Home Page**: `http://127.0.0.1:8000/`
- **Honeypot Login**: `http://127.0.0.1:8000/honeypot-login/`
- **Dashboard**: `http://127.0.0.1:8000/dashboard/`
- **Attack Logs**: `http://127.0.0.1:8000/logs/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

## Project Structure

```
cyber_defense_system/
├── manage.py
├── requirements.txt
├── cyberdefense/          # Django project settings
├── honeypot/              # Main application
├── templates/             # HTML templates
├── static/               # CSS and JavaScript files
└── db.sqlite3           # SQLite database
```

## Security Features

- IP address capture using `request.META.get('REMOTE_ADDR')`
- User agent logging for browser fingerprinting
- Brute force detection algorithm
- Real-time monitoring dashboard
- Secure session management

## Technologies Used

- **Backend**: Django 4.2+, Python 3.8+
- **Frontend**: Bootstrap 4.5, HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Testing

To test the honeypot functionality:

1. Start the server
2. Navigate to the honeypot login page
3. Try various username/password combinations
4. Check the dashboard for captured attempts
5. Verify attack logs contain all captured data

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure proper `SECRET_KEY`
3. Set up production database (PostgreSQL recommended)
4. Configure web server (Nginx + Gunicorn)
5. Set up HTTPS/SSL certificates
6. Configure firewall rules
7. Set up monitoring and logging

## License

This project is for educational purposes only. Use responsibly and in compliance with applicable laws and regulations.
