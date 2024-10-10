---

# AutoPoint

AutoPoint is an automation script designed to interact with the Proofpoint Essentials email security platform. The script automates the process of logging into Proofpoint, navigating to the sender lists, and adding a specified domain to the blocklist. This tool streamlines the process of blocking unwanted email domains, saving time and reducing manual effort.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Docker Usage](#docker-usage)
- [Notes](#notes)
- [License](#license)

## Features

- Automates login and navigation within Proofpoint Essentials.
- Adds specified domains to the blocklist efficiently.
- Securely stores and encrypts user credentials.
- Operates in headless mode for seamless background execution.

## Prerequisites

- **Python 3.x**
- **Selenium** library
- **Firefox WebDriver (geckodriver)**
- **Cryptography** library
- **Docker** (optional, for running via Docker)
- Access to the **Proofpoint Essentials** platform.

## Installation

### Clone the Repository

```bash
git clone https://github.com/jonathancostin/AutoPoint
cd AutoPoint
```

### Install Dependencies

Create a `requirements.txt` file with the following contents:

```
selenium
cryptography
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Download geckodriver

Download the appropriate version of **geckodriver** for your operating system from the [geckodriver releases page](https://github.com/mozilla/geckodriver/releases). Ensure that `geckodriver` is in your system's PATH.

## Usage

### Run the Script

```bash
python autopoint.py
```

### Initial Setup

- On the first run, the script will generate a `secret.key` and `credentials.enc` file.
- You will be prompted to enter your Proofpoint username(s) and password(s).
  - Enter multiple credentials by repeating the prompts.
  - Type `'done'` when you have finished entering all credentials.
- Credentials are encrypted and stored securely.

### Blocking a Domain

- The script will prompt:

  ```
  Enter the domain to be blocked:
  ```

- Input the domain you wish to block in the format `<domain@example.com>`.
- The script will extract the domain and add it to the blocklist in Proofpoint Essentials.

## Configuration

### Managing Credentials

- **Adding/Updating Credentials**: Delete the `secret.key` and `credentials.enc` files to reset credentials. Rerun the script to enter new credentials.
- **Encryption**: Credentials are encrypted using the Fernet symmetric encryption.

### Headless Mode

- The script runs in headless mode by default.
- To view the browser during execution (useful for debugging), comment out the `--headless` option:

  ```python
  options = Options()
  # options.add_argument("--headless")
  ```

## Logging

- All activities are logged to `script_log.txt`.
- Logs include timestamps, activity details, and error messages.

## Docker Usage

You can run the script inside a Docker container for portability and consistency.

### Build the Docker Image

Create a `Dockerfile` with the necessary configurations, then build the image:

```bash
docker build -t autopoint .
```

### Run the Docker Container

Use the provided batch file (**Windows**) or create a similar shell script (**Linux/MacOS**) to run the container:

**run_autopoint.bat**

```batch
@echo off
docker run -it --rm --name autopoint -v autopoint_data:/app/data autopoint %*
```

- **Explanation**:
  - `-it`: Runs the container in interactive mode.
  - `--rm`: Automatically removes the container when it exits.
  - `--name autopoint`: Names the running container.
  - `-v autopoint_data:/app/data`: Mounts a Docker volume to persist data.

## Notes

- **Security**: Keep `secret.key` and `credentials.enc` secure. Do not commit them to version control.
- **Dependencies**: Ensure all dependencies are correctly installed, especially `geckodriver`.
- **UI Changes**: The script relies on the current structure of the Proofpoint Essentials website. UI changes may require script updates.
- **Disclaimer**: The script is provided as-is. Use at your own risk.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

