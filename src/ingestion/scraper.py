import logging
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class ScraperError(Exception):
    pass

class GrowwScraper:
    def __init__(self, headers: dict = None):
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException, ScraperError))
    )
    def fetch_page(self, url: str) -> str:
        """Fetches the HTML content of the page with retries."""
        logger.info(f"Fetching {url}")
        response = requests.get(url, headers=self.headers, timeout=10)
        
        if response.status_code != 200:
            logger.warning(f"Failed to fetch {url}. Status code: {response.status_code}")
            raise ScraperError(f"HTTP Error: {response.status_code}")
            
        return response.text

    def extract_factual_data(self, html_content: str, url: str) -> dict:
        """
        Parses the HTML and extracts factual data.
        Since the layout might change, this will extract raw text and some key metrics.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        import json
        json_ld_text = []
        next_data_text = []
        
        # Try to extract the rich __NEXT_DATA__ JSON payload which contains exact fund details
        try:
            next_data_script = soup.find("script", id="__NEXT_DATA__")
            if next_data_script and next_data_script.string:
                next_json = json.loads(next_data_script.string)
                mf_data = next_json.get("props", {}).get("pageProps", {}).get("mfServerSideData", {})
                
                if mf_data:
                    fund_name = mf_data.get("scheme_name", mf_data.get("fund_name", "The fund"))
                    
                    if mf_data.get("expense_ratio"):
                        next_data_text.append(f"The expense ratio of {fund_name} is {mf_data['expense_ratio']}%.")
                        
                    if mf_data.get("exit_load"):
                        next_data_text.append(f"The exit load of {fund_name} is {mf_data['exit_load']}")
                        
                    if mf_data.get("min_sip_investment"):
                        next_data_text.append(f"The minimum SIP investment for {fund_name} is ₹{mf_data['min_sip_investment']}.")
                        
                    lock_in = mf_data.get("lock_in", {})
                    if lock_in and lock_in.get("years"):
                        next_data_text.append(f"The lock-in period for {fund_name} is {lock_in['years']} years.")
                    else:
                        next_data_text.append(f"There is no lock-in period for {fund_name}.")
                        
                    risk = mf_data.get("risk_level", mf_data.get("nfo_risk"))
                    if risk:
                        next_data_text.append(f"The riskometer level for {fund_name} is {risk}.")
                        
                    if mf_data.get("benchmark_name"):
                        next_data_text.append(f"The benchmark for {fund_name} is the {mf_data['benchmark_name']}.")
                        
                    if mf_data.get("aum"):
                        next_data_text.append(f"The total AUM (Assets Under Management) for {fund_name} is ₹{mf_data['aum']} Cr.")
        except Exception as e:
            logger.debug(f"Failed to parse __NEXT_DATA__: {e}")

        for script in soup.find_all("script", type="application/ld+json"):
            if script.string:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get("@type") == "FAQPage":
                        for entity in data.get("mainEntity", []):
                            if entity.get("@type") == "Question":
                                q = entity.get("name", "")
                                a = entity.get("acceptedAnswer", {}).get("text", "")
                                # Remove HTML tags from the answer text
                                a_text = BeautifulSoup(a, "html.parser").get_text(separator=' ', strip=True)
                                json_ld_text.append(f"FAQ - Q: {q} A: {a_text}")
                except Exception as e:
                    logger.debug(f"Failed to parse JSON-LD: {e}")

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        # Extract plain text content
        raw_text = soup.get_text(separator=' ', strip=True)
        
        # Append the structured Next.js data to the raw text
        if next_data_text:
            raw_text += "\n\n" + "\n\n".join(next_data_text)
            
        # Append the structured FAQ data to the raw text
        if json_ld_text:
            raw_text += "\n\n" + "\n\n".join(json_ld_text)
        
        # Finding the title as the fund name
        fund_name = soup.title.string if soup.title else None
        
        return {
            "url": url,
            "fund_name": fund_name,
            "raw_text_content": raw_text
        }

    def scrape(self, url: str) -> dict:
        """Main method to scrape a single URL."""
        html = self.fetch_page(url)
        data = self.extract_factual_data(html, url)
        return data
