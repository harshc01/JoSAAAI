from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import Browser
from scraper.parser import parse_table
from scraper.storage import save_to_csv


URL = "https://josaa.admissions.nic.in/Applicant/seatallotmentresult/currentorcr.aspx"


class SeleniumTraversal:

    def __init__(self):
        self.browser = Browser(URL)
        
    def run(self):
        self.browser.start()
        driver = self.browser.get_driver()

        wait = WebDriverWait(driver, 15)

        wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlRoundNo")))
        
        round_select = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlRoundNo"))
        
        results = []
        
        for i in range(1, len(round_select.options)):
            round_select.select_by_index(i)

            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlInstituteType")))
            
            inst_type = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlInstituteType"))
            
            for j in range(1, len(inst_type.options)):
                inst_type.select_by_index(j)
                
                wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlInstitute")))
                
                inst = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlInstitute"))
            
                for k in range(1, len(inst.options)):
                    inst.select_by_index(k)
                
                    wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlBranch")))
                    
                    branch = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlBranch"))
                
                    for l in range(1, len(branch.options)):
                        branch.select_by_index(l)
                        
                        wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlSeatType")))
                        
                        seat = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlSeatType"))
                        
                        for m in range(1, len(seat.options)):
                            seat.select_by_index(m)
                            
                            wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_ddlGender")))
                            
                            gender = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlGender"))
                            
                            for n in range(1, len(gender.options)):
                                gender.select_by_index(n)
                            
                                wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_GridView1")))
                            
                                html = driver.page_source
                                soup = BeautifulSoup(html, "lxml")
                                records = parse_table(soup)

                                results.extend(records)
                                print(f"Collected: {len(records)}")

save_to_csv(results, "data/output.csv")
self.browser.close()
