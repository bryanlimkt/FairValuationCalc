import requests
import bs4
import math
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def get_eps(soup):
    try:
        return float(soup.select("td[data-test*='EPS_RATIO-value']")[0].text)
    except:
        return('Error retreiving EPS')
    
def get_growth_rate (soup):
    try:
        growth_estimate=float(analysis_soup.select('td')[141].text.replace('%',''))
        half_growth_estimate = math.ceil(growth_estimate/2)
        return {"actual":growth_estimate,"halved": half_growth_estimate}
    except:
        return({"actual":'Error retreiving growth rate',"halved": 'Error retreiving growth rate'})
    
def get_pe_ratio(soup, growth_rate):
    try:
        if 'N/A' in soup.select('td[data-test*="PE_RATIO-value"]')[0].text:
            try:
                return float(growth_rate*2)
            except:
                'Error retreiving PE ratio and growth rate'
        else:
            return float(soup.select('td[data-test*="PE_RATIO-value"]')[0].text.replace(',',''))
            
    except:
        return('Error retreiving PE ratio')

def get_price(soup):
    try:
        return float(soup.select("div span[data-reactid*='29']")[0].text.replace(',',''))
    except:
        return('Error retreiving stock price')

def get_stock_name(soup):
    try:
        return soup.select("title")[0].text.split("(")[0]
    except:
        return "Error - Name not Found"

is_on = True
while is_on:

    ticker_symbol = ''
    eps = 0
    growth_rate = 0
    min_rate_of_return = 15
    margin_of_safety = 50
    pe_ratio = 0
    eps_estimation = 0
    price_estimation = 0

    while ticker_symbol == '':
        clearConsole()
        ticker_symbol = input('What is the ticker Symbol? ')

    #YAHOO Finance Main Page (Summary)
    base_url = 'https://sg.finance.yahoo.com/quote/{}/'
    scrape_url = base_url.format(ticker_symbol)
    request_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    res = requests.get(scrape_url, headers=request_headers)
    soup = bs4.BeautifulSoup(res.text,'lxml')
    stock_name = get_stock_name(soup)

    #YAHOO Finance Analysis Page
    base_analysis_url = 'https://sg.finance.yahoo.com/quote/{}/analysis?p={}'
    scrape_analysis_url = base_analysis_url.format(ticker_symbol,ticker_symbol)
    analysis_res = requests.get(scrape_analysis_url, headers=request_headers)
    analysis_soup = bs4.BeautifulSoup(analysis_res.text,'lxml')

    eps = get_eps(soup)
    eps_estimation = eps
    growth_rate = get_growth_rate(soup)
    pe_ratio = get_pe_ratio(soup, growth_rate)
    print(f'Stock: {stock_name}')
    print(f'eps is {eps}')
    print(f'Growth rate estimate from year 1-5 is: {growth_rate["actual"]}')
    print(f'Growth rate estimate from year 6-10 is: {growth_rate["halved"]}')
    print(f'pe_ratio is {pe_ratio}')

    try:
        for i in range(0,4):
            eps_estimation *= (1+(growth_rate["actual"]/100))
        for i in range(0,4):
            eps_estimation *= (1+(growth_rate["halved"]/100))
        price_estimation = eps_estimation*pe_ratio

        for i in range (0,9):
            price_estimation /= (1+min_rate_of_return/100)
            
        print(f'Fair Valuation is {round(price_estimation,2)}')
        print(f'After Margin of Safety: {round(price_estimation*(margin_of_safety/100),2)}')
        print(f'Current Price is: {get_price(soup)}')
    except:
        print('Unable to get Valuation')
    
    yes_or_no = ''
    while yes_or_no.lower() != 'y' and yes_or_no.lower() != 'n':
        yes_or_no = input('Want to search another ticker symbol? Y/n ')
    
    if yes_or_no.lower() == 'n':
        is_on = False