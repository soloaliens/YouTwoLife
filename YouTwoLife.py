# %%
# docker buildx create --name mybuilder --use
# docker buildx build --platform linux/amd64 -t gcr.io/youtwolife/youtwolife . --push

# gcloud run deploy youtwolife --image gcr.io/youtwolife/youtwolife --platform managed --allow-unauthenticated --set-env-vars=GITHUB_PAT=[GITHUB],API_KEY=[API],API_KEY_NAME=[API KEY]  --port=8000


# curl -X POST "https://youtwolife-od3gon4pca-df.a.run.app/api/match" \
#      -H "Content-Type: application/json" \
#      -H "X-API-KEY: [API]" \
#      -d '{"birth_date1": "22-12-1982", "birth_date2": "01-10-1984", "gender1": "F", "gender2": "M"}'

# curl -X POST "https://youtwolife-od3gon4pca-df.a.run.app/api/list" \
#      -H "Content-Type: application/json" \
#      -H "X-API-KEY: [API]" \
#      -d '{"birth_date1": "22-12-1982", "gender1": "F"}'


# curl -X POST "http://0.0.0.0:8000/api/match" \
#      -H "Content-Type: application/json" \
#      -H "X-API-KEY: [API]" \
#      -d '{"birth_date1": "22-12-1982", "birth_date2": "01-10-1984", "gender1": "F", "gender2": "M", "email": "adrianstuart@gmail.com", "name_first": "adrian" , "name_second" : "stuart"}'

# curl -X POST "http://localhost:8000/api/list"  -H "Content-Type: application/json" -H "X-API-KEY: [API]" -d '{"birth_date1": "22-12-1982", "gender1": "M","email":"adrianstuart@gmail.com", "name_first" : "adrian", "name_second" : "stuart" }'     

# curl -X POST "http://localhost:8000/api/list"  -H "Content-Type: application/json" -H "X-API-KEY: [API]" -d '{"birth_date1": "22-12-1982", "gender1": "F"}'


# %%
import pandas as pd   
import datetime  
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field, validator
from typing import List, Dict
from datetime import date
from pydantic import BaseModel, Field, validator
from datetime import date
from dotenv import load_dotenv
import os 
from datetime import date
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field, validator
from typing import List
import os
from dotenv import load_dotenv
from fastapi.security.api_key import APIKeyHeader
from datetime import date
import uvicorn
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


no_years = 15
gmail_user = 'lifeyoutwo@gmail.com'
gmail_password = 'loro lcvg milu bpyv'
google_sheets_api_file = 'YouTwoLife_google_sheeets_key/youtwolife-od3gon4pca-df.json'

# %%
                                                                                                      
                                                                                                                                    
def calculate_zodiac_sign(day: int, month: int, type_zodiac: str) -> str:                                                                              
    # Load the Zodiac dates from the CSV file                                                                                        
    zodiac_dates_df = pd.read_csv("Dates of zodiac.csv", skiprows=2)                                                                 
                                                                                                                                    
    # Iterate through the DataFrame to find the correct Zodiac sign                                                                  
    for i, row in zodiac_dates_df.iterrows():                                                                                        
        start_month, start_day, end_month, end_day = row[0:4]  
        #convert all to float
        start_month = float(start_month)
        start_day = float(start_day)
        end_month = float(end_month)
        end_day = float(end_day)
        
                                                                              
        # Check if the date is within the range for this Zodiac sign                                                                 
        if ((month == start_month and day >= start_day) or                                                                           
            (month == end_month and day <= end_day)):                                                                                
            # Return the name of the Zodiac sign                                                                                     
            return row[type_zodiac]                                                                                                       
                                                                                                                                    
    # Fallback in case the date doesn't match any known Zodiac signs (should not happen with valid input)                            
    return f"Unknown {type_zodiac} Zodiac Sign"                                                                                                     
                                                                                                                               
# # Example test case                                                                                                                  
# test_month = 12 #3  # March                                                                                                              
# test_day = 22 #15  # 15th   
# type_zodiac= 'Sign'                                                                                                             
# print(f"The {type_zodiac} Zodiac sign for {test_month}/{test_day} is: {calculate_zodiac_sign(test_day, test_month,type_zodiac)}")  
# type_zodiac= 'Element'                                                                                                             
# print(f"The {type_zodiac} Zodiac sign for {test_month}/{test_day} is: {calculate_zodiac_sign(test_day, test_month,type_zodiac)}")  

# %%
# def get_zodiac_element(zodiac_sign: str) -> str:                                                                                     
#     # Load the Zodiac data from the CSV file, skipping the first two rows which are headers                                          
#     zodiac_data = pd.read_csv("Dates of zodiac.csv", skiprows=2)                                                                     
                                                                                                                                    
#     # Find the row in the DataFrame where the Sign matches the input zodiac_sign                                                     
#     element_row = zodiac_data[zodiac_data['Sign'].str.strip() == zodiac_sign.strip()]                                                
                                                                                                                                    
#     # If the sign is found, return the corresponding element                                                                         
#     if not element_row.empty:                                                                                                        
#         return element_row.iloc[0]['Element']                                                                                        
#     # Fallback if the zodiac sign is not found                                                                                       
#     return "Unknown Element"                                                                                                         
                                                                                                                                    
# # Example test case                                                                                                                  
# test_zodiac_sign = "Pisces"                                                                                                          
# print(f"The element for {test_zodiac_sign} is: {get_zodiac_element(test_zodiac_sign)}")                                              
                                                                                        

# %%
                                                                                                                                    
def calculate_zodiac_compatibility(sign1: str, sign2: str) -> str:                                                                   
    try:                                                                                                                             
        # Correctly load the DataFrame, setting the first row as column headers                and set the first column as the index                                      
        compatibility_df = pd.read_csv("Table of Zodiac compatibility.csv", header=1, index_col=0)
        

                                             
                                                                                                                                    
        # Ensure indices (Zodiac signs) and column names are correctly formatted                                                     
        compatibility_df.columns = compatibility_df.columns.str.strip()                                                              
        # compatibility_df.set_index("NaN", inplace=True)                                                                              
        compatibility_df.index.name = None  
                                                                                             
                                                                                                                                    
        # Strip spaces and ensure case matching with DataFrame for sign names                                                        
        sign1 = sign1.strip().title()  # Title case to match DataFrame                                                               
        sign2 = sign2.strip().title()                                                                                                
                                                                                                                                    
        # Access the compatibility score                                                                                             
        score = compatibility_df.loc[sign1, sign2]                                                                                   
        return score                                                    
    except KeyError as e:                                                                                                            
        # Return an informative error message indicating the issue                                                                   
        return f"Error finding compatibility score: The issue is with '{e}'. Please check the provided Zodiac signs."                
                                                                                                                                    
# # Test the function with a corrected approach                                                                                        
# sign1_test = "Gemini"                                                                                                                
# sign2_test = "Libra"                                                                                                                 
# result = calculate_zodiac_compatibility(sign1_test, sign2_test)                                                                      
# print(result)   

# %%
def calculate_feng_shui_energy(year_of_birth: int, gender: str) -> str:                                                                           
    # Load the "Energy by Years of Birth.csv", focusing on the years and elements                                                    
    # Note: Skipping initial rows to directly start from year-element mappings                                                       
    energy_by_years_df = pd.read_csv(f"Energy by Years of Birth_{gender}.csv", skiprows=2, usecols=[0, 3])                                     
                                                                                                                                    
    # Cleanup and prepare the DataFrame by removing any non-numeric year entries                                                     
    energy_by_years_df = energy_by_years_df[pd.to_numeric(energy_by_years_df.iloc[:, 0], errors='coerce').notnull()]  
    #convert the firt column to float
    energy_by_years_df.iloc[:, 0] = energy_by_years_df.iloc[:, 0].astype(float)
    #convert the firt column to int
    energy_by_years_df.iloc[:, 0] = energy_by_years_df.iloc[:, 0].astype(int)
             
                                                                                                                                    
    # Search for the row that matches the year_of_birth and retrieve the corresponding element                                       
    matched_row = energy_by_years_df[energy_by_years_df.iloc[:, 0] == year_of_birth]                                                 
                                                                                                                                    
    if not matched_row.empty:                                                                                                        
        # Return the element associated with the year_of_birth                                                                       
        return matched_row.iloc[0, 1]                                                                                                
    else:                                                                                                                            
        # Fallback if the year_of_birth was not found                                                                                
        return "Unknown Element"                                                                                                     
                                                                                                                                    
# Example test case                                                                                                                  
# test_year = 1984                                                                                                                     
# print(f"The Feng Shui energy type for {test_year} is: {calculate_feng_shui_energy(test_year,'M')}") 

# %%
def calculate_feng_shui_compatibility(energy1: str, energy2: str) -> int:                                                            
    # Load the Feng Shui compatibility data                                                                                          
    comp_df = pd.read_csv("Fung Shui energy compatibiltiy.csv", header=1, index_col=0, skiprows=1)                                            
                                                                                                                                    
    # Retrieve the compatibility score for the two energy types                                                                      
    # The DataFrame's first row and column [0, 0] is used for headers, so direct string match can be used.                           
    score = comp_df.loc[energy1, energy2]                                                                                            
                                                                                                                                    
    return int(score)                                                                                                                
                                                                                                                                    
# # Example test cases                                                                                                                 
# energy_type_1 = "Water"                                                                                                              
# energy_type_2 = "Metal"                                                                                                              
# print(f"Compatibility score between {energy_type_1} and {energy_type_2} is: {calculate_feng_shui_compatibility(energy_type_1,        energy_type_2)}")                                                                                                                    
                                                                                                                                    
# energy_type_3 = "Wood"                                                                                                               
# energy_type_4 = "Fire"                                                                                                               
# print(f"Compatibility score between {energy_type_3} and {energy_type_4} is: {calculate_feng_shui_compatibility(energy_type_3,        energy_type_4)}")   

# %%
def calculate_overall_compatibility(zodiac_compatibility_score: int, feng_shui_compatibility_score: int, zodiac_divisor: int = 1)    -> int:                                                                                                                              
    """                                                                                                                              
    Calculates an overall compatibility score based on Zodiac and Feng Shui compatibility scores,                                    
    with an optional divisor for the Zodiac score.                                                                                   
                                                                                                                                    
    :param zodiac_compatibility_score: The Zodiac compatibility score as an integer.                                                 
    :param feng_shui_compatibility_score: The Feng Shui compatibility score as an integer.                                           
    :param zodiac_divisor: Divisor for the Zodiac score, defaults to 1.                                                              
    :return: The overall compatibility percentage as an integer.                                                                     
    """                                                                                                                              
    # Apply the divisor to the Zodiac score before averaging, ensuring the divisor is at least 1                                     
    adjusted_zodiac_score = zodiac_compatibility_score // max(1, zodiac_divisor)                                                     
                                                                                                                                    
    # Calculate the average of the adjusted Zodiac score and the Feng Shui score                                                     
    overall_compatibility = (adjusted_zodiac_score + feng_shui_compatibility_score) // 2                                             
                                                                                                                                    
    return overall_compatibility                                                                                                     
                                                                                                                                    
# # Example test case with the zodiac_divisor set to 2                                                                                 
# test_zodiac_score = 80                                                                                                               
# test_feng_shui_score = 70                                                                                                            
# zodiac_divisor = 2                                                                                                                   
                                                                                                                                    
# overall_score = calculate_overall_compatibility(test_zodiac_score, test_feng_shui_score, zodiac_divisor)                             
# print(f"Overall Compatibility Score with Zodiac Divisor {zodiac_divisor}: {overall_score}%")  

# %%
def get_zodiac_compatibility_description(score):  
    #set score as int
    score = int(score)
    zodiac_compatibility_description_df = pd.read_csv("Zodiak comaptibility result tex.csv")                                                                                    
    # Dropping rows where the score is NaN and ensuring the DataFrame is correctly processed                                         
    filtered_df = zodiac_compatibility_description_df.dropna(subset=['0']).copy()                                                    
    filtered_df['0'] = filtered_df['0'].astype(float)  # Ensuring the score column is float for comparison                           
                                                                                                                                    
    # Finding the minimum score in the DataFrame that is greater than or equal to the input score                                    
    matching_scores = filtered_df[filtered_df['0'] >= score]['0']                                                                    
    if not matching_scores.empty:                                                                                                    
        closest_score = matching_scores.min()                                                                                        
    else:                                                                                                                            
        closest_score = filtered_df['0'].max()                                                                                       
                                                                                                                                    
    # Fetching the corresponding description for the closest score                                                                   
    description = filtered_df[filtered_df['0'] == closest_score].iloc[0, 1]                                                          
                                                                                                                                    
    return description                                                                                                               
                                                                                                                                    
# # Example Test                                                                                                                       
# score_example = 18  # Input score for which we need the description                                                                  
# description_output = get_zodiac_compatibility_description(score_example)                                                             
# print(f"For a score of {score_example}, the Zodiac compatibility description is: '{description_output}'")   

# %%
def get_feng_shui_compatibility_description(score):  
    fung_shui_compatibility_df = pd.read_csv("Fung Shui compatibiltiy text.csv")                                                                                  
    # Ensuring the score column is float for accurate comparison and processing                                                      
    fung_shui_compatibility_df['0'] = fung_shui_compatibility_df['0'].astype(float)                                                  
                                                                                                                                    
    # Finding the minimum score in the DataFrame that is greater than or equal to the input score                                    
    matching_scores = fung_shui_compatibility_df[fung_shui_compatibility_df['0'] >= score]['0']                                      
    if not matching_scores.empty:                                                                                                    
        closest_score = matching_scores.min()                                                                                        
    else:                                                                                                                            
        closest_score = fung_shui_compatibility_df['0'].max()                                                                        
                                                                                                                                    
    # Fetching the corresponding description for the closest score                                                                   
    description = fung_shui_compatibility_df[fung_shui_compatibility_df['0'] == closest_score].iloc[0, 1]                            
                                                                                                                                    
    return description                                                                                                               
                                                                                                                                    
# # Example Test                                                                                                                       
# score_example = 18  # Input score for which we need the description                                                                  
# description_output = get_feng_shui_compatibility_description(score_example)                                                          
# print(f"For a Feng Shui compatibility score of {score_example}, the description is: '{description_output}'") 

# %%





def convert_to_chinese_birthday(birth_date):
    gregorian_year = birth_date.year
    gregorian_month = birth_date.month
    gregorian_day = birth_date.day
 
    #load Chinese New Year consists of.csv file
    chinese_new_year_df = pd.read_csv("Chinese New Year consists of.csv", skiprows=2)
    #convert the first column to int
    chinese_new_year_df.iloc[:, 0] = chinese_new_year_df.iloc[:, 0].astype(int)
    #using the birth_year look for the corresponding year in the chinese_new_year_df and get the corresponding month and day
    chinese_new_year_df = chinese_new_year_df[chinese_new_year_df.iloc[:, 0] == gregorian_year]
    chinese_month = chinese_new_year_df.iloc[0, 2]
    chinese_day = chinese_new_year_df.iloc[0, 1]
    chinese_month = int(chinese_month)
    chinese_day = int(chinese_day)
    
    # #=IF(C4>=G4,IF(D4>=H4,E4,E4-1),IF(D4>H4,E4,E4-1))
    if gregorian_day >= chinese_day:
        if gregorian_month >= chinese_month:
            adjusted_year = gregorian_year
        else:
            adjusted_year = gregorian_year - 1
    else:
        if gregorian_month > chinese_month:
            adjusted_year = gregorian_year
        else:
            adjusted_year = gregorian_year - 1

    #convert to date
 
    return  chinese_day, chinese_month , adjusted_year
    
    
# # Example usage:

# birth_date = date(1982, 12, 22)    # Birthday
# adjusted_year = convert_to_chinese_birthday(birth_date)
# print(f"Adjusted Year: {adjusted_year}")


# %%

def years_around_birthday(dob_str,years):
    """
    Returns a list of years within a ±15-year range of the birth year,
    excluding years that would make someone under 18.
    
    :param dob_str: Date of birth as a string in "YYYY-MM-DD" format.
    :param years: The range of years to consider.
    :return: List of years.
    """
    # Convert the string to a datetime object
    dob = datetime.datetime.strptime(dob_str, "%d-%m-%Y")
    
    # Extract the birth year
    birth_year = dob.year
    
    # Calculate the current year
    current_year = datetime.datetime.now().year
    
    # Calculate the age
    age = current_year - birth_year
    
    # Initialize the list of years
    years_list = []
    
    # Calculate the start and end year for the ±15 range
    start_year = birth_year - years
    end_year = birth_year + years
    
    # Loop through each year in the range
    for year in range(start_year, end_year + 1):
        # Calculate the hypothetical age for someone born in this year
        hypothetical_age = current_year - year
        
        # Check if the hypothetical age is 18 or more
        if hypothetical_age >= 18:
            years_list.append(year)
    
    return years_list

def get_100_percent_compatibility(zodiac_sign1):
    # Load the Zodiac compatibility data
    comp_df = pd.read_csv("Table of Zodiac compatibility.csv", header=1, index_col=0)
    # Retrieve the compatibility score for the two energy types
    comp_df = comp_df[comp_df[zodiac_sign1] == 100]
    #get the index names in a list
    return comp_df.index.tolist()

def get_zodiac_date_range(zodiac_copatable_list):
    list_dates = []
    for zodiac_sign in zodiac_copatable_list:
        zodiac_dates_df = pd.read_csv("Dates of zodiac.csv", skiprows=2)
        dates_df = zodiac_dates_df[zodiac_dates_df['Sign'] == zodiac_sign]
        #convert to a date
        #change the column names to Month	Day	Month1	Day1	Element	Sign
        dates_df.columns = [ 'Month','Day'	,'Month1'	,'Day1',	'Element',	'Sign']

        start_date = (int(dates_df.Month.values[0]) , int(dates_df.Day.values[0]))
        end_date = (int(dates_df.Month1.values[0]) , int(dates_df.Day1.values[0]))
        list_dates.append( ( start_date, end_date ) )

    return list_dates

def get_100_percent_feng_shui_compatibility(energy1):
    comp_df = pd.read_csv("Fung Shui energy compatibiltiy.csv", header=1, index_col=0, skiprows=1)
    comp_df = comp_df[comp_df[energy1] == 100]
    #show the column name where the value is 100
    return comp_df.columns[comp_df.eq(100).any()].to_list()

def get_fung_shui_energy_years(feng_shui_energy_copatable_list, gender1):
    # energy_years_df = pd.read_csv(f"Energy by Years of Birth_{gender1}.csv", skiprows=2)
    energy_years_df = pd.read_csv(f"Energy by Years of Birth_{gender1}.csv", skiprows=3)
    energy_years_df = energy_years_df.rename(columns={energy_years_df.columns[0]: 'year'})
    all_years = energy_years_df[energy_years_df['Element'] ==feng_shui_energy_copatable_list[0] ]['year'].to_list()
    all_years = [int(year) for year in all_years ]
    return all_years


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def format_date_ranges(date_ranges):
    formatted_dates = []
    for start, end in date_ranges:
        formatted_start = f"{start[0]:02d}-{start[1]:02d}"
        formatted_end = f"{end[0]:02d}-{end[1]:02d}"
        formatted_dates.append(f"{formatted_start} to {formatted_end}")
    return ', '.join(formatted_dates)

def format_years(years):
    return ', '.join(sorted(map(str, years)))

def send_html_email(data,type):
    #if teh type is list then the data contains email, name_first, name_second, birth_date1, gender1, zodiac_sign1, zodiac_compatable_dates, energy1, fung_shui_energy_compatable_years
    
    #if the type is match then the data contains email, name_first, name_second, birth_date1, birth_date2, gender1, gender2, zodiac_sign1, zodiac_sign2, zodiac_compatibility_score,zodiac_description, energy1, energy2, feng_shui_compatibility_score, feng_shui_description, overall_score

    if data['gender1'] == 'M':
        data['gender1'] = 'Male'
    else:
        data['gender1'] = 'Female'
    # Create message container
    msg = MIMEMultipart('alternative')
    if type =='list':
        msg['Subject'] = "Your Compatibility List"
        # Format the date ranges and years for HTML
        formatted_date_ranges = format_date_ranges(data['zodiac_compatable_dates'])
        formatted_years = format_years(data['fung_shui_energy_compatable_years'])
    elif type == 'match':
        msg['Subject'] = "Your Compatibility Report"
        if data['gender2'] == 'M':
            data['gender2'] = 'Male'
        else:
            data['gender2'] = 'Female'

    msg['From'] = gmail_user
    msg['To'] = data['email']

    #capitolise the fist name 
    data['name_first'] = data['name_first'].capitalize()
    
    # Create the body of the message (HTML version).
    if type == 'list':
        html = f"""\
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                h1 {{
                    color: #444;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .highlight {{
                    color: #D35400;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Compatibility Report</h1>
                <div class="section">
                    <p>Hi {data['name_first']},</p>
                    <p>Here is your compatibility report for birth date of {data['birth_date1']} and {data['gender1']}.</p>
                </div>
                <div class="section">
                    <p>Your Zodiac sign is <span class="highlight">{data['zodiac_sign1']}</span>.</p>
                    <p>Compatible Zodiac date ranges:</p>
                    <p>{formatted_date_ranges},</p>
                </div>
                <div class="section">
                    <p>Your Feng Shui energy is <span class="highlight">{data['energy1']}</span>.</p>
                    <p>Compatible Feng Shui energy years:</p>
                    <p>{formatted_years}</p>
                </div>
                <div class="section">
                    <p>Thank you for using YouTwoLife!</p>
            
                </div>
            </div>
        </body>
        </html>
        """
    elif type == 'match':
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid;
                    border-radius: 5px;
                }}
                h1 {{
                    color: #444;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .highlight {{
                    color: #D35400;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Compatibility Report</h1>
                <div class="section">
                    <p>Hi {data['name_first']},</p>
                    <p>Here is your compatibility report.</p>
                </div>
                <div class="section">
                    <p>Your Zodiac sign is <span class="highlight">{data['zodiac_sign1']}</span>.</p>
                    <p>Your partner's Zodiac sign is <span class="highlight">{data['zodiac_sign2']}</span>.</p>
                    <p>Zodiac compatibility score: {data['zodiac_compatibility_score']}%</p>
                    <p>Zodiac compatibility description: {data['zodiac_description']}</p>
                </div>
                <div class="section">
                    <p>Your Feng Shui energy is <span class="highlight">{data['energy1']}</span>.</p>
                    <p>Your partner's Feng Shui energy is <span class="highlight">{data['energy2']}</span>.</p>
                    <p>Feng Shui compatibility score: {data['feng_shui_compatibility_score']}%</p>
                    <p>Feng Shui compatibility description: {data['feng_shui_description']}</p>
                </div>
                <div class="section">
                    <p>Overall compatibility score: {data['overall_score']}%</p>
                    <p>Thank you for using YouTwoLife!</p>
                </div>
            </div>
        </body>
        </html>
        """

                                                                                                            


        # Record the MIME types.
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    msg.attach(part2)
    
    # Send the message via local SMTP server.
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, data['email'], msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# def store_data(data):
#     #make sure that any fields in the data that are lists are tunred into string
#     data = {k: str(v) if isinstance(v, list) else v for k, v in data.items()}
#     #store the data in a csv
#     data = pd.DataFrame(data, index=[0])
#     #add a time stamp
#     data['time'] = pd.to_datetime('today').strftime("%Y-%m-%d %H:%M:%S")
#     #store the data in a csv
#     data.to_csv('data.csv', mode='a', header=False)
#     return "Data has been stored"
        

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

def store_data(data,sheet_type):
    # Make sure that any fields in the data that are lists are turned into strings
    data = {k: ', '.join(v) if isinstance(v, list) else v for k, v in data.items()}
    
    # Add a timestamp
    data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert data to DataFrame
    data_df = pd.DataFrame([data])
    
    # Authenticate with the Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(google_sheets_api_file, scope)
    client = gspread.authorize(creds)
    
    # Open the Google Sheet
    sheet = client.open("YouTwoLife_web").worksheet(sheet_type)  # Use the worksheet method
    
   
    
    # Convert DataFrame to a list of lists and append to the Google Sheet
    data_list = data_df.values.tolist()
    sheet.append_rows(data_list)
    
    return "Data has been stored in Google Sheets"


# %%


# %%


# %%


app = FastAPI()

#get the API_KEY from the .env file

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Placeholder for your actual API key

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security: API Key Verification
async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")



class MatchRequest(BaseModel):
    birth_date1: str = Field(..., example="22-12-1982", pattern=r"^\d{2}-\d{2}-\d{4}$")
    birth_date2: str = Field(..., example="01-10-1984", pattern=r"^\d{2}-\d{2}-\d{4}$")
    gender1: str = Field(..., pattern="^[FM]$", example="F")
    gender2: str = Field(..., pattern="^[FM]$", example="M")
    #check the name variable is safe
    name_first: str = Field(..., example="John", max_length=50)
    name_second: str = Field(..., example="Jane", max_length=50)
    #check email is valid
    email: str = Field(..., example="john@gmail.com", max_length=50)
    

    @validator('birth_date1', 'birth_date2')
    def validate_date(cls, v):
        try:
            day, month, year = map(int, v.split('-'))
            date(year, month, day)  # This will raise an error if the date is not valid
            return v
        except ValueError:
            raise ValueError('Invalid date format, should be DD-MM-YYYY')
        
    @validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('name_first', 'name_second')
    def validate_name(cls, v):
        if not v.isalpha():
            raise ValueError('Name should only contain alphabets')
        return v
        
class ListRequest(BaseModel):
    birth_date1: str = Field(..., example="22-12-1982", pattern=r"^\d{2}-\d{2}-\d{4}$")
    gender1: str = Field(..., pattern="^[FM]$", example="F")

    #check the name variable is safe
    name_first: str = Field(..., example="John", max_length=50)
    name_second: str = Field(..., example="Jane", max_length=50)
    #check email is valid
    email: str = Field(..., example="john@gmail.com", max_length=50)
    
    @validator('birth_date1')
    def validate_date(cls, v):
        try:
            day, month, year = map(int, v.split('-'))
            date(year, month, day)  # This will raise an error if the date is not valid
            return v
        except ValueError:
            raise ValueError('Invalid date format, should be DD-MM-YYYY')
        
    @validator('email')
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('name_first', 'name_second')
    def validate_name(cls, v):
        if not v.isalpha():
            raise ValueError('Name should only contain alphabets')
        return v



# API endpoint
@app.post("/api/match")
@limiter.limit("60/minute")  # Adjust the rate limit as needed
# async def compatibility_api(request: MatchRequest, api_key: str = Depends(get_api_key)):
async def compatibility_api(request: Request, match_request: MatchRequest, api_key: str = Depends(get_api_key)):


    # Extract day, month, and year from birth dates
    day1, month1, year1 = map(int, match_request.birth_date1.split('-'))
    day2, month2, year2 = map(int, match_request.birth_date2.split('-'))

    # Convert the Gregorian dates to Lunar dates
    lunar_day1, lunar_month1, lunar_year1 = convert_to_chinese_birthday(date(year1, month1, day1))
    lunar_day2, lunar_month2, lunar_year2 = convert_to_chinese_birthday(date(year2, month2, day2))

    # Calculate Zodiac signs and elements
    zodiac_sign1 = calculate_zodiac_sign(day1, month1, 'Sign')
    zodiac_sign2 = calculate_zodiac_sign(day2, month2, 'Sign')
    element1 = calculate_zodiac_sign(lunar_day1, lunar_month1, 'Element')
    element2 = calculate_zodiac_sign(lunar_day2, lunar_month2, 'Element')

    # Compute Feng Shui energies
    energy1 = calculate_feng_shui_energy(lunar_year1, match_request.gender1)
    energy2 = calculate_feng_shui_energy(lunar_year2, match_request.gender2)

    # Calculate compatibilities
    zodiac_compatibility_score = calculate_zodiac_compatibility(zodiac_sign1, zodiac_sign2)
    feng_shui_compatibility_score = calculate_feng_shui_compatibility(energy1, energy2)

    # Get descriptive texts
    zodiac_description = get_zodiac_compatibility_description(zodiac_compatibility_score)
    feng_shui_description = get_feng_shui_compatibility_description(feng_shui_compatibility_score)

    overall_score = calculate_overall_compatibility(zodiac_compatibility_score, feng_shui_compatibility_score)

    # Compile the report
    report = {
        "Zodiac_Signs": [zodiac_sign1, zodiac_sign2],
        "Zodiac_Elements": [element1, element2],
        "Feng_Shui_Energies": [energy1, energy2],
        "Zodiac_Compatibility_Score": zodiac_compatibility_score,
        "Zodiac_Description": zodiac_description,
        "Feng_Shui_Compatibility_Score": feng_shui_compatibility_score,
        "Feng_Shui_Description": feng_shui_description,
        "Overall_Compatibility_Score": overall_score,
    }
    #create a dict of all the data top be stored
    data = {"email": match_request.email, "name_first": match_request.name_first, "name_second": match_request.name_second, "birth_date1": match_request.birth_date1, "birth_date2": match_request.birth_date2, "gender1": match_request.gender1, "gender2": match_request.gender2, "zodiac_sign1": zodiac_sign1, "zodiac_sign2": zodiac_sign2, "zodiac_compatibility_score": zodiac_compatibility_score, "zodiac_description": zodiac_description, "energy1": energy1, "energy2": energy2, "feng_shui_compatibility_score": feng_shui_compatibility_score, "feng_shui_description": feng_shui_description, "overall_score": overall_score}
    # store_data(data)
    store_data(data,'match')
    send_html_email(data,'match')

    return report

# API endpoint
@app.post("/api/list")
@limiter.limit("60/minute")  # Adjust the rate limit as needed
# async def compatibility_api(request: ListRequest, api_key: str = Depends(get_api_key)):
async def list_api(request: Request, list_request: ListRequest, api_key: str = Depends(get_api_key)):

    # Extract day, month, and year from birth dates
    day1, month1, year1 = map(int, list_request.birth_date1.split('-'))
    # Convert the Gregorian dates to Lunar dates
    lunar_day1, lunar_month1, lunar_year1 = convert_to_chinese_birthday(date(year1, month1, day1))
    # Calculate Zodiac signs and elements
    zodiac_sign1 = calculate_zodiac_sign(day1, month1, 'Sign')
    # element1 = calculate_zodiac_sign(lunar_day1, lunar_month1, 'Element')
    energy1 = calculate_feng_shui_energy(lunar_year1, list_request.gender1)
    #crete a function thatl looks up the zodiac sign table and returns only other zodiac signs that have 100% compatibility
    zodiac_copatable_list = get_100_percent_compatibility(zodiac_sign1)
    #function to get the date range of each of the zodiac sign
    zodiac_compatable_dates = get_zodiac_date_range(zodiac_copatable_list)
    #crate a function that looks up the feng shui table and returns only other feng shui elements that have 100% compatibility
    feng_shui_energy_copatable_list = get_100_percent_feng_shui_compatibility(energy1)
    #functrion to get all the years that are the same energy
    fung_shui_energy_compatable_years = get_fung_shui_energy_years(feng_shui_energy_copatable_list, list_request.gender1)
    years_in = years_around_birthday(list_request.birth_date1,no_years)
    #only return years that are both in years_in_15 and fung_shui_energy_compatable_years
    years_in = set(years_in)
    fung_shui_energy_compatable_years = set(fung_shui_energy_compatable_years)
    years_in = years_in.intersection(fung_shui_energy_compatable_years)
    fung_shui_energy_compatable_years = list(years_in)
    #function to store the data in a csv. email should be the index

    #create a dict of all the data top be stored 
    data = {"email": list_request.email, "name_first": list_request.name_first, "name_second": list_request.name_second, "birth_date1": list_request.birth_date1, "gender1": list_request.gender1, "zodiac_sign1": zodiac_sign1, "zodiac_compatable_dates": zodiac_compatable_dates, "energy1": energy1, "fung_shui_energy_compatable_years": fung_shui_energy_compatable_years}
    store_data(data,'list')
    send_html_email(data,'list')
    return {"zodiac_compatable_dates": zodiac_compatable_dates, "fung_shui_energy_compatable_years": years_in}





# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




# def run_server():
#     uvicorn.run("your_app:app", host="0.0.0.0", port=8000, log_level="info")

# if __name__ == "__main__":
#     server_thread = Thread(target=run_server)
#     server_thread.start()

# %%


# %%


# %%



# %%


# %%


# %%



