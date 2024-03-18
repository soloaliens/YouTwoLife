# %%
import pandas as pd                                                                                                           
                                                                                                                                    
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
from datetime import date




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
# import json
# # Function to integrate all components                                                                                               
# def get_compatibility_report(birth_date1, birth_date2, gender1, gender2):                                                            
#     # Extract day, month, and year from birth dates                                                                                  
#     day1, month1, year1 = map(int, birth_date1.split('-'))                                                                           
#     day2, month2, year2 = map(int, birth_date2.split('-')) 
#     #print them
#     print(day1, month1, year1)
#     print(day2, month2, year2)

#     #convert to int
#     year1 = int(year1)
#     year2 = int(year2)
#     day1 = int(day1)
#     day2 = int(day2) 
#     month1 = int(month1)
#     month2 = int(month2)

#     # Convert the Gregorian dates to Lunar dates
#     lunar_day1, lunar_month1, lunar_year1 = convert_to_chinese_birthday(date(year1, month1, day1))
#     lunar_day2, lunar_month2, lunar_year2 = convert_to_chinese_birthday(date(year2, month2, day2))

#     print(lunar_day1, lunar_month1, lunar_year1)
#     print(lunar_day2, lunar_month2, lunar_year2)
                                                                                                          
#     # Calculate Zodiac signs and elements            
#     print('Zodiac SIGN should be from westebn birthdate')                                                                                
#     zodiac_sign1  = calculate_zodiac_sign(day1, month1,'Sign')                                                                     
#     zodiac_sign2  = calculate_zodiac_sign(day2, month2, 'Sign')   

#     print('Zodiac ELEMENT should be from Chinese birthdate')      
#     element1 = calculate_zodiac_sign(lunar_day1, lunar_month1, 'Element')
#     element2 = calculate_zodiac_sign(lunar_day2, lunar_month2, 'Element')                                                
                                                                                                                                    
#     # Compute Feng Shui energies                                                                                                     
#     energy1 = calculate_feng_shui_energy(lunar_year1, gender1)                                                                                   
#     energy2 = calculate_feng_shui_energy(lunar_year2, gender2)                                                                              
                                                                                                                                    
#     # Calculate compatibilities (placeholders)                                                                                       
#     zodiac_compatibility_score =   calculate_zodiac_compatibility(zodiac_sign1, zodiac_sign2)
#     feng_shui_compatibility_score = calculate_feng_shui_compatibility(energy1, energy2)                                                      
                                                                                                                
#     # Get descriptive texts                                                                                                          
#     zodiac_description = get_zodiac_compatibility_description(zodiac_compatibility_score)                                            
#     feng_shui_description = get_feng_shui_compatibility_description(feng_shui_compatibility_score)  

#     overall_score = calculate_overall_compatibility(zodiac_compatibility_score, feng_shui_compatibility_score, zodiac_divisor = 2)  
                                                                                                                                    
#     # Compile the report                                                                                                             
#     report = {   
#         "Zodiac_Signs": [zodiac_sign1, zodiac_sign2],
#         "Zodiac_Elements": [element1, element2],
#         "Feng_Shui_Energies": [energy1 ,energy2], 
#         "Zodiac_Compatibility_Score": zodiac_compatibility_score,                                                                    
#         "Zodiac_Description": zodiac_description,                                                                                    
#         "Feng_Shuicompatibility_Score": feng_shui_compatibility_score,                                                               
#         "Feng_Shui_Description": feng_shui_description  ,
#         "Overall_Compatibility_Score": overall_score  ,

                                                                                   
#     }                                                                                                                                
                                                                                                                                    
#     return json.dumps(report, indent=4)                                                                                              
                                                                                                                                    
# # Example usage                                                                                                                      
# birth_date1 = "22-12-1982"  # DD-MM-YYYY                                                                                             
# birth_date2 = "01-10-1984"                                                                                                           
# gender1 = "F"                                                                                                                   
# gender2 = "M"                                                                                                                     
# compatibility_report = get_compatibility_report(birth_date1, birth_date2, gender1, gender2)                                          
# print(compatibility_report)             

# %%
# import secrets

# def generate_api_key():
#     return secrets.token_urlsafe(32)  # Generates a 32-byte (256-bit) secure URL-safe text string

# api_key = generate_api_key()
# print(api_key)

# import jwt
# import datetime

# def generate_jwt_token(secret_key):
#     payload = {
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),  # Set the expiry time
#         'iat': datetime.datetime.utcnow(),  # Issued at time
#         # 'sub': 'subject',  # Optional: Subject of the token
#         # Additional claims can be included here as needed
#     }
#     token = jwt.encode(payload, secret_key, algorithm='HS256')
#     return token

# # Usage
# secret_key = 'your_secret_key'  # This should be kept secret!
# access_token = generate_jwt_token(secret_key)
# print(access_token)



# %%
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field, validator
from typing import List, Dict
import json
from datetime import date
from pydantic import BaseModel, Field, validator
from datetime import date

app = FastAPI()

#get the API_KEY from the .env file
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Placeholder for your actual API key

API_KEY_NAME = os.getenv("API_KEY_NAME")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Security: API Key Verification
async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")



class CompatibilityRequest(BaseModel):
    birth_date1: str = Field(..., example="22-12-1982", pattern=r"^\d{2}-\d{2}-\d{4}$")
    birth_date2: str = Field(..., example="01-10-1984", pattern=r"^\d{2}-\d{2}-\d{4}$")
    gender1: str = Field(..., pattern="^[FM]$", example="F")
    gender2: str = Field(..., pattern="^[FM]$", example="M")

    @validator('birth_date1', 'birth_date2')
    def validate_date(cls, v):
        try:
            day, month, year = map(int, v.split('-'))
            date(year, month, day)  # This will raise an error if the date is not valid
            return v
        except ValueError:
            raise ValueError('Invalid date format, should be DD-MM-YYYY')



# API endpoint
@app.post("/api/compatibility")
async def compatibility_api(request: CompatibilityRequest, api_key: str = Depends(get_api_key)):
    # Extract day, month, and year from birth dates
    day1, month1, year1 = map(int, request.birth_date1.split('-'))
    day2, month2, year2 = map(int, request.birth_date2.split('-'))

    # Convert the Gregorian dates to Lunar dates
    lunar_day1, lunar_month1, lunar_year1 = convert_to_chinese_birthday(date(year1, month1, day1))
    lunar_day2, lunar_month2, lunar_year2 = convert_to_chinese_birthday(date(year2, month2, day2))

    # Calculate Zodiac signs and elements
    zodiac_sign1 = calculate_zodiac_sign(day1, month1, 'Sign')
    zodiac_sign2 = calculate_zodiac_sign(day2, month2, 'Sign')
    element1 = calculate_zodiac_sign(lunar_day1, lunar_month1, 'Element')
    element2 = calculate_zodiac_sign(lunar_day2, lunar_month2, 'Element')

    # Compute Feng Shui energies
    energy1 = calculate_feng_shui_energy(lunar_year1, request.gender1)
    energy2 = calculate_feng_shui_energy(lunar_year2, request.gender2)

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

    return report

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


import uvicorn
from threading import Thread

def run_server():
    uvicorn.run("your_app:app", host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()

# %%



