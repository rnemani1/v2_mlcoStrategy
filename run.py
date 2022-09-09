import v2Scraper

URL = input("Enter a sportsbook.fanduel.com game URL: ")
    
while '@' not in URL:
    URL = input("Enter a sportsbook.fanduel.com game URL: ")
        
letter = input("A or B: ")
v2Scraper.run(URL, letter)