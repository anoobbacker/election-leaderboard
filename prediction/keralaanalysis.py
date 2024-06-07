import os
import pandas as pd
from openai import OpenAI
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

client = OpenAI()

constituencies = [
    {"#": 1, "Constituency": "Kasaragod"},
    {"#": 2, "Constituency": "Kannur"},
    {"#": 3, "Constituency": "Vatakara"},
    {"#": 4, "Constituency": "Wayanad"},
    {"#": 5, "Constituency": "Kozhikode"},
    {"#": 6, "Constituency": "Malappuram"},
    {"#": 7, "Constituency": "Ponnani"},
    {"#": 8, "Constituency": "Palakkad"},
    {"#": 9, "Constituency": "Alathur (SC)"},
    {"#": 10, "Constituency": "Thrissur"},
    {"#": 11, "Constituency": "Chalakudy"},
    {"#": 12, "Constituency": "Ernakulam"},
    {"#": 13, "Constituency": "Idukki"},
    {"#": 14, "Constituency": "Kottayam"},
    {"#": 15, "Constituency": "Alappuzha"},
    {"#": 16, "Constituency": "Mavelikkara (SC)"},
    {"#": 17, "Constituency": "Pathanamthitta"},
    {"#": 18, "Constituency": "Kollam"},
    {"#": 19, "Constituency": "Attingal"},
    {"#": 20, "Constituency": "Thiruvananthapuram"}
]


def search_historical_data(historical_data, query, top_k=5):
    # Search for relevant rows based on constituency name
    matching_rows = historical_data[historical_data['#'] == query]
    
    # If there are more rows than top_k, truncate the results
    if len(matching_rows) > top_k:
        matching_rows = matching_rows.head(top_k)
    
    return matching_rows

def search_poll(data, statename, top_k=10):
    # Search for relevant rows    
    return data[(data['State'] == statename)]

# Define response generation function
def generate_response(query, context):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in political and election analysis. Provide a detailed analysis of Kerala Loksabha General Election 2024. Consider the trends, inflation, unemployment, fuel charges, LPG cooking gas price variations, increased taxes, and other factors that may affect the election results."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.2
    )
    return response.choices[0].message.content

def MainRAG():
    # Load datasets
    candidates_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-candidates.csv')
    voter_turnout_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-voter-turnout.csv')
    data_2009  = pd.read_csv('../data/loksabha/2009/2009-kerala-constituency-wise-result.csv')
    data_2014  = pd.read_csv('../data/loksabha/2014/2014-kerala-constituency-wise-result.csv')
    data_2019   = pd.read_csv('../data/loksabha/2019/2019-kerala-constituency-wise-result.csv')
    poll_2024  = pd.read_csv('../data/loksabha/2024/polls.csv')
    results_by_state_assembly  = pd.read_csv('../data/loksabha/2024/kerala-votes-by-state-assembly.csv')
    results_by_constituency  = pd.read_csv('../data/loksabha/2024/kerala-candidate-results-by-constituency.csv')

    # Check for leading/trailing spaces in column names
    poll_2024.columns = poll_2024.columns.str.strip()

    # Print the first few rows of the DataFrame to ensure it is loaded correctly
    # print("First few rows of the DataFrame:\n", poll_2024.head())

    # Add year columns
    data_2009['Year'] = 2009
    data_2014['Year'] = 2014
    data_2019['Year'] = 2019

    # Combine historical data
    historical_data = pd.concat([data_2009, data_2014, data_2019], ignore_index=True)

    # Preprocess data if necessary
    historical_data.fillna('', inplace=True)
    # print(historical_data)

    data_mp  = pd.read_csv('../data/loksabha/2024/mp-performance.csv')
    data_mp = data_mp[data_mp['State'] == 'Kerala']    

    # Search for poll data for Kerala
    kerala_other_poll_data = search_poll(poll_2024, 'Kerala')
    # print(f"Kerala other poll: \n{kerala_other_poll_data}")
    
    allindia_other_poll_data = search_poll(poll_2024, 'ALL INDIA')
    # print(f"All India other poll: \n{allindia_other_poll_data}")

    print("# Election Analysis\n")
    for constituency in constituencies:
        constituency_number = constituency["#"]
        constituency_name = constituency["Constituency"]

        # Example query
        query = f"Generate a comprehensive election analysis for Kerala constituency {constituency_name} in Kerala Loksabha Election 2024."

        # Retrieve 2024 candidate and voter turnout data
        candidate_info = candidates_2024[candidates_2024['#'] == constituency_number]
        turnout_info = voter_turnout_2024[voter_turnout_2024['#'] == constituency_number]
        results_by_state_assembly_info = results_by_state_assembly[results_by_state_assembly['#'] == constituency_number]
        results_by_constituency_info = results_by_constituency[results_by_constituency['#'] == constituency_number]
        
        # Extract 2024 candidate information by party
        udf_info = f"'UDF Party': '{candidate_info['UDF Party'].values[0]}', 'UDF Member': '{candidate_info['UDF Member'].values[0]}'"
        ldf_info = f"'LDF Party': '{candidate_info['LDF Party'].values[0]}', 'LDF Member': '{candidate_info['LDF Member'].values[0]}'"
        nda_info = f"'NDA Party': '{candidate_info['NDA Party'].values[0]}', 'NDA Member': '{candidate_info['NDA Member'].values[0]}'"

        context = f"{{'2024 Candidates': {{{udf_info} {ldf_info}{nda_info}}}}}"
        turnout_context = "".join([str(doc) for doc in turnout_info.to_dict(orient='records')])
        context += f"{{2024 Voter Turnout: {turnout_context} }}"

        mp_info = data_mp[data_mp['Constituency'] == constituency_name]
        mp_info_context = "".join([str(doc) for doc in mp_info.to_dict(orient='records')])
        context += f"{{Current Elected Member Performance: {mp_info_context} }}"

        if not results_by_state_assembly_info.empty:
            results_by_state_assembly_info_context = "".join([str(doc) for doc in results_by_state_assembly_info.to_dict(orient='records')])
            context += f"{{Votes by State Assembly: {results_by_state_assembly_info_context} }}"
        
        if not results_by_constituency_info.empty:
            results_by_constituency_info_context = "".join([str(doc) for doc in results_by_constituency_info.to_dict(orient='records')])
            context += f"{{Votes by Constituency: {results_by_constituency_info_context} }}"

        if not kerala_other_poll_data.empty:
            kerala_other_poll_data_context = "".join([str(doc) for doc in kerala_other_poll_data.to_dict(orient='records')])
            context += f"{{Kerala Opinion and Exit Poll Data: {kerala_other_poll_data_context} }}"

        if not allindia_other_poll_data.empty:
            allindia_other_poll_data_context = "".join([str(doc) for doc in allindia_other_poll_data.to_dict(orient='records')])
            context += f"{{All India Opinion and Exit Poll Data: {allindia_other_poll_data_context} }}"
        
        # Display context
        # print(f"Context for constituency {constituency_name}: {context}")

        # Generate response using OpenAI API
        print(f"## {constituency_name}\n")        
        response = generate_response(query, context)
        print(f"{response}\n")  


# Run the main function
if __name__ == "__main__":
    MainRAG()