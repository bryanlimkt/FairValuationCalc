import requests
import bs4

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
        ticker_symbol = input('What is the ticker Symbol? ')

    #YAHOO Finance Main Page (Summary)
    base_url = 'https://sg.finance.yahoo.com/quote/{}/'

    scrape_url = base_url.format(ticker_symbol)

    res = requests.get(scrape_url)

    soup = bs4.BeautifulSoup(res.text,'lxml')

    #YAHOO Finance Analysis Page
    base_analysis_url = 'https://sg.finance.yahoo.com/quote/{}/analysis?p={}'

    scrape_analysis_url = base_analysis_url.format(ticker_symbol,ticker_symbol)

    analysis_res = requests.get(scrape_analysis_url)

    analysis_soup = bs4.BeautifulSoup(analysis_res.text,'lxml')

    def get_eps():
        try:
            return float(soup.select("td[data-test*='EPS_RATIO-value']")[0].text)
            
        except:
            return('Error retreiving EPS')
        
    def get_growth_rate ():
        try:
            return float(analysis_soup.select('td')[141].text.replace('%',''))
        except:
            return('Error retreiving growth rate')
        
    def get_pe_ratio():
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

    def get_price():
        try:
            return float(soup.select("div span[data-reactid*='32']")[0].text)
        except:
            return('Error retreiving stock price')

    eps = get_eps()
    eps_estimation = eps
    growth_rate = get_growth_rate()
    pe_ratio = get_pe_ratio()

    print(f'eps is {eps}')
    print(f'growth_rate is {growth_rate}')
    print(f'pe_ratio is {pe_ratio}')

    try:
        for i in range(0,9):
            eps_estimation *= (1+(growth_rate/100))
            price_estimation = eps_estimation*pe_ratio

        for i in range (0,9):
            price_estimation /= (1+min_rate_of_return/100)
            
        print(f'Fair Valuation is {price_estimation}')
        print(f'After Margin of Safety: {price_estimation*(margin_of_safety/100)}')
        print(f'Current Price is: {get_price()}')
    except:
        print('Unable to get Valuation')
    
    yes_or_no = ''

    while yes_or_no.lower() != 'y' and yes_or_no.lower() != 'n':

        yes_or_no = input('Want to search another ticker symbol? Y/n ')
    
    if yes_or_no.lower() == 'n':
        is_on = False
