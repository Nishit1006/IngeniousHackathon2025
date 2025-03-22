#!/usr/bin/env python
import os
import sys
import subprocess
import getpass
from pathlib import Path

def main():
    """
    Setup script for the Farmer Credit Evaluation Tool.
    This script helps with the initial setup of the project.
    """
    print("\n=== Farmer Credit Evaluation Tool Setup ===\n")
    
    # Create virtual environment if it doesn't exist
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("Virtual environment created successfully.\n")
    else:
        print("Virtual environment already exists.\n")
    
    # Determine the activate script based on the OS
    if sys.platform == 'win32':
        activate_script = os.path.join("venv", "Scripts", "activate")
        activate_cmd = f"{activate_script}"
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        activate_cmd = f"source {activate_script}"
    
    # Install dependencies
    print("Installing dependencies...")
    if sys.platform == 'win32':
        subprocess.run(f"{os.path.join('venv', 'Scripts', 'python')} -m pip install -r requirements.txt", shell=True)
    else:
        subprocess.run(f"{os.path.join('venv', 'bin', 'python')} -m pip install -r requirements.txt", shell=True)
    print("Dependencies installed successfully.\n")
    
    # Create .env file
    if not os.path.exists(".env"):
        print("Creating .env file...")
        with open(".env", "w") as f:
            f.write("DEBUG=True\n")
            secret_key = os.urandom(32).hex()
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write("DATABASE_URL=sqlite:///db.sqlite3\n")
            # Add more environment variables as needed
        print(".env file created successfully.\n")
    else:
        print(".env file already exists.\n")
    
    # Run migrations
    print("Running migrations...")
    if sys.platform == 'win32':
        subprocess.run(f"{os.path.join('venv', 'Scripts', 'python')} manage.py migrate", shell=True)
    else:
        subprocess.run(f"{os.path.join('venv', 'bin', 'python')} manage.py migrate", shell=True)
    print("Migrations completed successfully.\n")
    
    # Create superuser
    create_superuser = input("Would you like to create a superuser? (y/n): ")
    if create_superuser.lower() == 'y':
        print("\nCreating superuser...")
        if sys.platform == 'win32':
            subprocess.run(f"{os.path.join('venv', 'Scripts', 'python')} manage.py createsuperuser", shell=True)
        else:
            subprocess.run(f"{os.path.join('venv', 'bin', 'python')} manage.py createsuperuser", shell=True)
        print("Superuser created successfully.\n")
    
    # Collect static files
    collect_static = input("Would you like to collect static files? (y/n): ")
    if collect_static.lower() == 'y':
        print("\nCollecting static files...")
        if sys.platform == 'win32':
            subprocess.run(f"{os.path.join('venv', 'Scripts', 'python')} manage.py collectstatic --noinput", shell=True)
        else:
            subprocess.run(f"{os.path.join('venv', 'bin', 'python')} manage.py collectstatic --noinput", shell=True)
        print("Static files collected successfully.\n")
    
    # Setup complete
    print("\n=== Setup Complete ===\n")
    print(f"To activate the virtual environment, run: {activate_cmd}")
    print("To start the development server, run: python manage.py runserver")
    print("Visit http://127.0.0.1:8000/ in your browser to access the application.")
    print("\nThank you for setting up the Farmer Credit Evaluation Tool!")

if __name__ == "__main__":
    main() 