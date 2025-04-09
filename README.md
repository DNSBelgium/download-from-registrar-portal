# Registrar Portal Automation Script

## Overview
This Python script automates the process of logging into the registrar portal and downloading an export file. It serves as a proof of concept to demonstrate that registrars can download files automatically.

## Prerequisites
- Python 3.13.2
- Virtual environment (`venv`)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/DNSBelgium/download-from-registrar-portal.git
    cd download-from-registrar-portal
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**
    - **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    - **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

1. **Run the script:**
    ```bash
    python3 download.py
    ```

2. The script will log into the registrar portal and download the export file to the specified directory.

## Configuration

- Ensure that the login credentials and portal URL are correctly set in the script.
- Modify the script as needed to match the specific requirements of your registrar portal.

