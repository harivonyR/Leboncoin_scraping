# Leboncoin Scraping

Leboncoin_Scraping is a Python project designed to extract classified ads data from **Leboncoin** using the **Piloterr Search API**.  
It takes one or multiple category IDs as input, retrieves the results, and exports them into structured JSON files for further analysis.


## 🚀 Use Cases

- **Price Monitoring & Benchmarking** – Track how prices evolve for similar products.
- **Market Research** – Analyze regional or seasonal patterns of product listings.
- **Machine Learning & NLP Training** – Build datasets for predictive modeling or sentiment analysis.
- **Competitor Analysis** – Scrape multiple categories to compare seller strategies.


## Get Started

### 1. Clone the repository

```bash
git clone https://github.com/harivonyR/Leboncoin_scraping
cd Leboncoin_scraping
```

### 2. Install dependencies

> Only install the non-native packages required for this project.

```bash
pip install requests tqdm pandas
```

### 3. Configure your API key

Create your credential file:

```bash
cp credential.example.py credential.py
```

Then open `credential.py` and paste your **Piloterr API key** inside:

```python
x_api_key = "YOUR_API_KEY_HERE"
```

### 4. Run the script
in  `main.py` :
+ Check the list of `categories` to scrape
+ Edit the `search_param`
+ **then run main.py**

```bash
python main.py
```

> 💡 Categories are identified by numerical IDs.  
> You can find all category IDs here : [Leboncoin Categories IDs - csv](https://raw.githubusercontent.com/harivonyR/Leboncoin_scraping/d5c3052ddf510c3fff1c308bc6f9179fb552ab96/output/leboncoin_catagories_with_id.csv)


## Notes

- Data is exported automatically into the `output/` folder.  
- Each category generates its own timestamped JSON file.  
- You can extend the scraper by adding pagination, error handling, or automated daily jobs.


## License

This project is distributed under the MIT License.  
See the `LICENSE` file for details.

