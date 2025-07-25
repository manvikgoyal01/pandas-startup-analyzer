# Startup Funding Analysis Tool (CLI)

A command-line Python tool for analyzing Indian startup funding data using pandas. Users can filter by year, funding amount, startup name, sector, sub-sector, investment type, number of investors, and investor names. Provides clean tabular outputs, sorted views, and insights like top-funded startups and sector breakdowns. Includes a feature to export filtered data to a .csv file. Built for clarity, interactivity, and efficient terminal use — no GUI required.

## Features

- Filter by:
  - Startup name  
  - Funding amount (range)  
  - Year (range)  
  - Sector & Sub-sector  
  - Investment type  
  - Number of investors (range)  
  - Investor names (exact match)  

- View:
  - Filtered dataset in table form  
  - Top-funded startups  
  - Detailed anaylysis of various sorts, eg : city-wise, sector-wise, investor-wise, etc.
  - Get stats like mean, median, max, min, total startups of each type in that group, etc.

- Export:
  - Save filtered & sorted data to .csv on user's machine  

## How to Run

1. Clone the repo or download files  
2. Make sure Python 3 is installed  
3. Run from terminal:  
   python your_script_name.py  
4. Follow on-screen instructions  

## Requirements

- Python 3.x  
- pandas  

Install using:  
pip install pandas  

## Files

- startup_funding_tool.py – main script  
- startup_funding_data.csv – dataset (sample)  

## License

MIT License  

## Topics

python, pandas, data-analysis, command-line, startup, funding, csv, terminal-tool, filtering, investment
