# improting the necessary libraries make sure you have installed  selenium in python in advance
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
import os
import datetime
from datetime import datetime
import numpy as np
import os.path
import csv
# scheduler
import sched, time





'''

Jason Beattie 2020

It works, could be better

Make sure to install chromedriver into the working directory

'''


def State_Parser(t):
    """states contains the Australian states values"""
    states=["VIC1","QLD1","NSW1","SA1","TAS1"]

    """staes_filename is mapping the states value to your desired name, baically you can map or modify your file name"""
    states_filename={"VIC1":'VIC',"QLD1":'QLD',"NSW1":'NSW',"SA1":'SA',"TAS1":'TAS'}

    """this is to map time periods and add to file naming whxih you can change"""
    Time_period_dic={'5MIN':"5MIN",'30MIN':"30MIN"}

    ### Here we need to create a chrome driver to use for scrapping the data

    select = Select(driver.find_element_by_id('period'))#first we select the time period on the page
    select.select_by_value(t) #inserting the time values into the select_by_value fucntion (t)
    for s in states: #Here we make a loop to insert all the states and scrap their data
        select = Select(driver.find_element_by_id('region-id')) 
        select.select_by_value(s)

        value=[]
        title=[]
        

        all_value = driver.find_elements_by_xpath("//div[@class='summary-column-value']")  # select and get all the values related to summary-column-value calss which are the price numbers
        all_title = driver.find_elements_by_xpath("//div[@class='summary-column-title']")  # select and get all the values related to summary-column-value calss which are the price Titles
        for i in all_title: # now we add them to the data frame
            print (i.text)
            title.append(i.text)

        for j in all_value: # now we add them to the data frame
            print (j.text)
            value.append(j.text)
        #create date and time and format it 
        now = datetime.now()
        timestamp = now.strftime("%Y/%m/%d  %H:%M")
        
        
        df=pd.DataFrame({"Title":title}) # here we write from memory  into dataframe files df (title data)
        df2=pd.DataFrame({"Value":value}) # here we write from memory  into dataframe files df (Price values data)

        df=df.T   # do the Transpose so we can insert it as rows
        df2=df2.T # do the Transpose so we can insert it as rows
       
        result = df.append(df2, ignore_index=True) # Now we need to merge title+Value+timestamp data
        
        # We need to add timestamp to the A1 and A2 cells as they are not  dataframe and we create them seperrately
        result.at[0, 'Timestamp'] = 'Timestamp' #changing the the cell title 
        result.at[1, 'Timestamp'] = timestamp   #changing the cell value
        col_name="Timestamp"
        first_col = result.pop('Timestamp') # remove the timestamp column form the right and 
        result.insert(0, col_name, first_col) # and shift it to first column

        print(result) # just to test the results you can remove or keep it
        
        Time_f=Time_period_dic[t]  # we get  each time period from the list and put in the Time variable to use it in our naming convention
        State_f=states_filename[s]  # we get  each filename  from the list and put in the Time variable to use it in our naming convention
        Filename=Time_f +"_"+ State_f+".csv" #making the file name as dynamic naming which changes by states names
        
        
        # to append the data to the data base we add if cluse to check the existance of the files and if = yes then it remove the header form the dataframe and append tot he old csv file
        file_exist=os.path.isfile(Filename)
        
        if file_exist==False:
            result.to_csv (Filename, index = False, header=False)
        else:
            new_header = result.iloc[0]
            result = result[1:]
            result.columns = new_header
            result.to_csv (Filename, index = False, header=False ,mode='a') # finally writing the data frame to the CSV file'''
    
    return print('Web Scrapping is done Successfully, Please check your files')

#######################################################################################################################################################################################


def scrape(time_p):
    
    global driver
    #below codes are to open the browser in headless mode and more efficient
    chrome_options = Options()  
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(".\chromedriver.exe",options=chrome_options)  # we create a webdriver from chrome driver, so first make sure you download the driver related to your installed chrome veriosn by going to 
    #this website: https://chromedriver.chromium.org/downloads and copy it into the folder which script existed
    
    #Time_period=["5MIN","30MIN"] # availabel tim eperiods
    Time_period=[time_p] # availabel tim eperiods
    driver.minimize_window() # to minimize the browser window
    driver.get("https://aemo.com.au/aemo/apps/visualisation/index.html#/electricity/nem/price-and-demand?Elec_enabled=Yes&Gas_enabled=No&Elec_location=NSW,QLD,SA&Gas_location=TAS,VIC,WA") # this is the target webpage for data scrapping
    for period in Time_period: # now this is the main loop to run our function by giving the time periods 
        State_Parser(period)
    driver.close() # closing the webbrowser
    
####################################################################################################################################################################################

def scrape_all():
    
    global driver
    #below codes are to open the browser in headless mode and more efficient
    chrome_options = Options()  
    chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(".\chromedriver.exe",options=chrome_options)  # we create a webdriver from chrome driver, so first make sure you download the driver related to your installed chrome veriosn by going to 
    #this website: https://chromedriver.chromium.org/downloads and copy it into the folder which script existed
    
    Time_period=["5MIN","30MIN"] # availabel tim eperiods
    #Time_period=[time_p] # availabel tim eperiods
    driver.minimize_window() # to minimize the browser window
    driver.get("https://aemo.com.au/aemo/apps/visualisation/index.html#/electricity/nem/price-and-demand?Elec_enabled=Yes&Gas_enabled=No&Elec_location=NSW,QLD,SA&Gas_location=TAS,VIC,WA") # this is the target webpage for data scrapping
    for period in Time_period: # now this is the main loop to run our function by giving the time periods 
        State_Parser(period)
    driver.close() # closing the webbrowser
    
####################################################################################################################################################################################

'''
Counts up to 6
Runs 5X 5Min scrape, then every 6 time (30min), runs the 30mins scrapper


'''

counter = 0
def counter_block():
    global counter
    if counter < 5:
        print('\n','\n','\n','\n','#####################','\n' )
        print("5 Min Run")
        scrape("5MIN")
        counter += 1
      
        
    else:
        print('\n','\n','\n','\n','#####################','\n' )
        print("30min")
        scrape_all()
        counter = 0
        

#------------------------------------------------------------------------------------------------------

        
# 5 Min Timer
        
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    counter_block()
    
    s.enter(300, 1, do_something, (sc,))
s.enter(300, 1, do_something, (s,))


#------------------------------------------------------------------------------------------------------


#Run Block

def run():
    print('runing...')
    scrape_all() # Scrape on script first launch
    s.run()         # Keeps script running every 5 mins    


#------------------------------------------------------------------------------------------------------

#error handling

def error_handling_run():
    

    while True:
        try:          
            run()
        except:
            driver.close() # without this, the code would look in the Run block
            with open('./error_log.csv', mode='a', newline='') as error_csv: #a for append
                error_file = csv.writer(error_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                print('Writing CSV...', '\n')
                error_file.writerow([time.strftime('%Y-%m-%d %H:%M', time.localtime()) , 'global run error' ])
            print("********************* Error ***********************")
            time.sleep(30)

#------------------------------------------------------------------------------------------------------
            
print("Wait until first run completes before leaving")

error_handling_run()


