# WebScraper for Job Listings - Indeed

This is the GUI based verison of the Indeed Scraper.

## Technologies Used

- **Python**: Main programming language.
- **Selenium**: Used to automate the web browser for scraping data.
- **Undetected-Chromedriver**: Helps to bypass detection and anti-scraping measures.
- **Pandas**: For handling and saving scraped data into CSV and Excel formats.
- **Tkinter**: Used to create the graphical user interface (GUI).

## Prerequisites

Before running the project, ensure you have the following dependencies installed:

1. **Python** (>= 3.6)
2. **pip** for installing Python packages

You can install the required packages by running:

```bash
pip install selenium undetected-chromedriver pandas openpyxl
```

## How to Use

### 1. Run the Script

- Clone or download the repository.
- Install the required dependencies using `pip`.
- Run the script in your terminal or IDE:


### 2. Input Search Parameters

The graphical user interface (GUI) will pop up where you can input:

- **Position**: Job title or keyword (e.g., "Controller").
- **Radius**: Search radius in kilometers
- **Page**: Page number of job results to scrape (Make sure to add this in increments of 10)

### 3. Click "Scrape" to Start the Process

Once you hit the "Scrape" button, the scraper will:

1. A minimized version of your browser will run (Headless driver wasn't used since Indeed blocks it)
2. Open indeed using the given URL (You can find it inside of the script and modify it to your liking)
3. Scrape the job listings along with the information required for the listings.
4. Save the results in CSV and Excel formats.

### 4. View Results

After the scraping process is complete, the script will output two files in the project folder:

- **CSV file**: `indeed_jobs_<timestamp>.csv`
- **Excel file**: `indeed_jobs_<timestamp>.xlsx`

These files contain the scraped data including job titles, companies, and locations.

## Areas Of Improvement

- As of right now, the scraper scrapes a maximum of 15 jobs per page and you can only scrape one page at a time
- This can be improved, allowing for multiple pages to be scraped at once.
