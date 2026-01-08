# Python QR Web Launcher

This Python script starts a local web server, displays a QR code in the terminal, and allows a user to "cast" a URL to the host machine's browser from a mobile device (or any other device on the network).

## Features

- **Local Web Server**: Starts an HTTP server on port 8000.
- **QR Code Generation**: Automatically generates and prints a QR code to the terminal for easy access from mobile devices.
- **Remote URL Launching**: Accepts a URL via a simple web interface and opens it in Google Chrome on the host machine.
- **Auto-Shutdown**: The server automatically shuts down after a successful URL launch.

## Prerequisites

- Python 3.x
- Google Chrome (or a Chromium-based browser) installed.

## Installation

1.  Clone this repository or download the script.
2.  Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    (The only external dependency is `qrcode`).

## Usage

1.  Run the script:

    ```bash
    python app.py
    ```

2.  Scanning the QR Code:
    - A QR code will appear in your terminal.
    - Scan this code with your mobile phone's camera or QR scanner app.
    - Ensure your mobile device is on the same Wi-Fi network as the host computer.

3.  Sending a URL:
    - The QR code redirects you to a web page hosted on your computer.
    - Enter a URL (e.g., `youtube.com`) into the input field.
    - Tap **Send**.

4.  Result:
    - Google Chrome will open on the host computer with the URL you entered.
    - The Python script will terminate.

## Troubleshooting

- **Connection Refused/Timeout**: Make sure both devices are on the same local network. Check if your firewall is blocking incoming connections to Python on port 8000.
- **Browser Not Opening**: The script attempts to locate Google Chrome specifically. If it fails, it falls back to the system default browser. Ensure Chrome is installed in the standard location.
