'''
Author: Ruthuparan Prasad
Date: 20/05/2025

This script: 
1. Reads the google sheets and merges them into a single dataframe
2. Cleans the merged dataframe
3. Saves the cleaned dataframe to a .db file

'''

from typing import Dict
import pandas as pd
import gspread
import json
import os
from google.oauth2.service_account import Credentials
import sqlite3

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = "creds.json"

def read_google_sheet(sheet_name: str, tab_name: str = "Sheet1") -> pd.DataFrame:

    '''
    Reads a google sheet and returns a pandas dataframe
    '''
    
    # authorise the client


    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)

    # open the sheet and read the data
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    '''
    Cleans the merged dataframe
    '''

    # clean the test_date, score and passed columns - currently there are repeated columns
    df.drop(columns=['test_date_y', 'score_y', 'passed_y'], inplace=True)
    df.rename(columns={'test_date_x': 'test_date', 'score_x': 'score', 'passed_x': 'passed'}, inplace=True)

    # convert all date columns to appropriate data type

    for col in ['nominated_date', 'onboarding_date', 'test_date', 'assigned_date']:
      df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # add custom KPIs to track the progress of the apprentices
    df['days_to_diagnostic'] = (df['test_date'] - df['nominated_date']).dt.days
    df['days_to_assignment'] = (df['assigned_date'] - df['test_date']).dt.days
    df['days_to_onboarding'] = (df['onboarding_date'] - df['assigned_date']).dt.days
    df['fulfilled'] = df['onboarding_status'].str.lower() == 'completed'

    # reorder the dataframe
    df = df[['apprentice_id', 'name', 'employer', 'nominated_date','test_date', 'score', 'passed', 'days_to_diagnostic','programme_name', 'coach_name', 'assigned_date', 'days_to_assignment', 'onboarding_date', 'days_to_onboarding', 'onboarding_status', 'fulfilled']]
    
    df["onboarding_status"] = df["onboarding_status"].fillna("Not Onboarding")
    df["programme_name"] = df["programme_name"].fillna("Not Applicable")

    return df

def save_to_db(db_path: str = "fulfilment_tracker.db", tables: Dict[str, pd.DataFrame] = {}):

    '''
    Saves the cleaned dataframe to a .db file
    '''

    # create a connection to the database
    conn = sqlite3.connect(db_path)

    try:
        for table_name, df in tables.items():
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Saved {len(tables)} tables to {db_path}")
    finally:
        conn.close()

def main():
    # read the sheets
    apprentices = read_google_sheet("apprentices")
    diagnostics = read_google_sheet("diagnostics")
    onboarding_status = read_google_sheet("onboarding_status")
    programme_assignments = read_google_sheet("programme_assignments")

    # merge the sheets
    df = apprentices.merge(diagnostics, on="apprentice_id", how="left") \
                    .merge(onboarding_status, on="apprentice_id", how="left") \
                    .merge(programme_assignments, on="apprentice_id", how="left")

    # clean the dataframe
    df = clean_dataframe(df)

    # Dictionary of tables to store
    tables_to_save = {
        "apprentices": apprentices,
        "diagnostics": diagnostics,
        "programme_assignments": programme_assignments,
        "onboarding_status": onboarding_status,
        "apprentice_fulfilment": df
    }

    # save the tables to the database
    save_to_db(db_path="fulfilment_tracker.db", tables=tables_to_save)

if __name__ == "__main__":
    main()
