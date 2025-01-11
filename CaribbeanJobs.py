from requests_html import HTMLSession
import csv
import psycopg2
from psycopg2 import sql
from datetime import datetime
import os
import logging
import time
import nest_asyncio


# Apply nested asyncio fix
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}
headers['Referer'] = 'https://www.caribbeanjobs.com/'


def scrape_jobs(url):
    """Scrape job listings from the given URL."""
    try:
        session = HTMLSession()
        job_data = []
        page_number = 1

        while True:
            # Add pagination to the URL
            paginated_url = f"{url}&Page={page_number}"
            logging.info(f"Scraping page {page_number}: {paginated_url}")

            # Send the GET request
            response = session.get(paginated_url)

            # Render JavaScript
            response.html.render(sleep=5)

            # Extract job blocks
            job_blocks = response.html.find('div.module.job-result')

            if not job_blocks:
                logging.info("No more job listings found. Ending pagination.")
                break

            # Store the current date for default posting date
            default_date_posted = datetime.now().strftime("%Y-%m-%d")

            for job_block in job_blocks:
                job_title_element = job_block.find('h2[itemprop="title"] a', first=True)
                job_title = job_title_element.text.strip() if job_title_element else 'Unknown Title'

                company_element = job_block.find('h3[itemprop="name"] a', first=True)
                company_name = company_element.text.strip() if company_element else 'Unknown Company'

                location_elements = job_block.find('li[itemprop="jobLocation"] a')
                job_locations = ', '.join([loc.text.strip() for loc in location_elements]) if location_elements else 'Unknown Location'

                job_link = f"https://www.caribbeanjobs.com{job_title_element.attrs['href']}" if job_title_element else 'Unknown Link'

                date_posted_element = job_block.find('li[itemprop="datePosted"]', first=True)
                date_posted = date_posted_element.text.strip() if date_posted_element else default_date_posted

                website = "CaribbeanJobs"  # Set the website identifier

                if job_title != 'Unknown Title':
                    job_data.append((job_title, date_posted, job_link, website, company_name, job_locations))

            # Add a delay between requests to avoid detection
            time.sleep(2)

            # Move to the next page
            page_number += 1

        return job_data

    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        return []

def save_to_csv(job_data, csv_filename):
    """Save job data to a CSV file, appending new rows if the file already exists."""
    if not job_data:
        logging.info("No job data to save to CSV.")
        return

    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

    try:
        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                # Include the "Website" column in the header
                writer.writerow(["Job Title", "Job Location(s)", "Date Posted", "Source Link", "Hiring Organization", "Website"])
            writer.writerows(job_data)

        logging.info(f"Job data saved to {csv_filename}")

    except Exception as e:
        logging.error(f"Error saving job data to CSV: {e}")


def connect_db():
    """Connect to the PostgreSQL database."""
    try:
        # Update database connection parameters
        conn = psycopg2.connect(
            host="localhost",          # Database server (localhost for local machine)
            database="joblist",        # New database name
            user="postgres",           # Database username
            password="Kriston50!"      # Password for the user
        )
        print("Connection successful")
        return conn
    except psycopg2.Error as e:
        print(f"Connection error: {e}")
        return None

def save_to_database(job_data):
    """Save job data to PostgreSQL database, avoiding duplicates by job link."""
    conn = psycopg2.connect(
        host="localhost",
        database="joblist",        # New database name
        user="postgres",           # Database username
        password="Kriston50!"      # Password for the user
    )
    if not conn:
        logging.error("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        # Insert new job data, skipping duplicates based on the 'link' field
        for job in job_data:
            try:
                cursor.execute('''
                    INSERT INTO caribbeanjobs (job_title, date_posted, link, website, company, location)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING
                ''', job)
            except psycopg2.Error as e:
                logging.error(f"Error inserting job into database: {e}")

        # Commit the transaction
        conn.commit()
        logging.info("Job data saved to PostgreSQL database.")

    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        # Close the database connection
        conn.close()

def main():
    url = "https://www.caribbeanjobs.com/ShowResults.aspx?Keywords=&autosuggestEndpoint=%2Fautosuggest&Location=124&Category=&Recruiter=Company&Recruiter=Agency"
    csv_filename = "/Users/justinharrilal/Desktop/JobData/caribbeanjobs.csv"

    # Scrape job data
    job_data = scrape_jobs(url)

    # Save data to CSV and PostgreSQL database
    save_to_csv(job_data, csv_filename)
    save_to_database(job_data)

if __name__ == "__main__":
    main()
