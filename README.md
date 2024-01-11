# Google Classroom File Downloader with Telegram Integration

## Project Overview

This Python project automates the download of files from Google Classroom, focusing on retrieving past year papers. The downloaded files are made accessible through a Telegram bot, providing users with an efficient and user-friendly interface.

## Key Tools and Techniques

- **Python:**
  - Primary programming language used for project development.

- **Chromedriver:**
  - Employed for web scraping automation, facilitating interactions with the Google Classroom web interface.

- **Google APIs (Classroom API and Drive API):**
  - Classroom API: Accesses information about courses and coursework programmatically.
  - Drive API: Manages and downloads files stored in Google Drive.

## Project Workflow

1. **Authentication:**
   - Authenticate the project with Google APIs using OAuth credentials.

2. **Web Scraping:**
   - Utilize Chromedriver to automate interactions with the Google Classroom web interface.
   - Automate navigation through courses, identification of past year papers, and initiation of file downloads.

3. **Error Handling:**
   - Implement robust error-handling mechanisms to manage potential issues during web scraping, API calls, or bot interactions.

## Getting Started

1. **Install Dependencies:**
   - Install the required Python packages using `pip install -r _req.txt`.

2. **Configure Credentials:**
   - Add the necessary credentials for Google APIs and Telegram in the designated configuration files.

3. **Run the Script:**
   - Execute the main Python script to initiate the web scraping, and  API calls.

## Expected Outcomes

- Extracting the links for drive files from the google classroom interface.
- Automated download of past year papers from Google Classroom.
- Seamless integration with Telegram.

## Notes and Considerations

- Ensure compliance with Google's policies and terms of service when interacting with Google Classroom and Drive.
- Respect intellectual property rights and privacy considerations.

## Contributors

- Chandan Sah
- Tharun Harish

---
