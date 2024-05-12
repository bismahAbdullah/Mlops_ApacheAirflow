import requests
from bs4 import BeautifulSoup
import csv

def scrape_bbc_links():
    # URL of the BBC homepage
    url = "https://www.bbc.com/"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags (<a>) that contain links
        links = soup.find_all("a")

        # Extract the href attribute from each anchor tag
        bbc_links = [link.get("href") for link in links if link.get("href")]

        # Filter out links that are not relevant (e.g., internal navigation links)
        bbc_links = [link for link in bbc_links if "http" in link]

        return bbc_links
    else:
        print("Failed to retrieve BBC homepage. Status code:", response.status_code)
        return []

def save_links_to_csv(links, filename):
    # Write links to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Links"])
        for link in links:
            writer.writerow([link])
    print(f"Links saved to {filename}")

# Example usage
if __name__ == "__main__":
    bbc_links = scrape_bbc_links()
    if bbc_links:
        save_links_to_csv(bbc_links, "bbc_links.csv")
