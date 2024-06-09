import pandas as pd
from openai import OpenAI
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
            {"role": "system", "content": "You are an expert in political and election analysis. Provide a detailed analysis of the Kerala Loksabha Election 2024 results announced on 4th June 2024. Highlight the trends that are hard to observe! Mention factors such as inflation, unemployment, fuel charges, LPG cooking gas prices, increased taxes, religious issues, health, education, and road conditions only if they are found online to have influenced the election results."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.2
    )
    return response.choices[0].message.content

def MainRAG():
    # Load datasets
    results_by_state_assembly = pd.read_csv('../data/loksabha/2024/kerala-votes-by-state-assembly.csv')
    results_by_constituency = pd.read_csv('../data/loksabha/2024/kerala-candidate-results-by-constituency.csv')

    # Print the first few rows of the DataFrame to ensure it is loaded correctly
    # print("First few rows of the DataFrame:\n", results_by_state_assembly.head())

    data_mp  = pd.read_csv('../data/loksabha/2024/mp-performance.csv')
    data_mp = data_mp[data_mp['State'] == 'Kerala']

    print("# Election Analysis\n")
    for constituency in constituencies:
        constituency_number = constituency["#"]
        constituency_name = constituency["Constituency"]

        context = ""

        # Example query
        query = f"Generate a comprehensive election analysis for Kerala constituency {constituency_name} in Kerala Loksabha Election 2024."

        # Search for historical data
        results_by_state_assembly_info = results_by_state_assembly[results_by_state_assembly['#'] == constituency_number]

        # Specify the columns you want to drop
        state_assembly_columns_to_drop = ['#', 'Constituency', 'StateAssemblyNumber', 'Candidate Position'] 
        results_by_state_assembly_info = results_by_state_assembly_info.drop(columns=state_assembly_columns_to_drop)

        results_by_constituency_info = results_by_constituency[results_by_constituency['#'] == constituency_number]

        # Specify the columns you want to drop
        constituency_columns_to_drop = ['#', 'Constituency'] 
        results_by_constituency_info = results_by_constituency_info.drop(columns=constituency_columns_to_drop)
            

        mp_info = data_mp[data_mp['Constituency'] == constituency_name]
        mp_info_context = "".join([str(doc) for doc in mp_info.to_dict(orient='records')])
        context += f"{{Current Elected Member Performance: {mp_info_context} }}"
        
        if not results_by_constituency_info.empty:
            results_by_constituency_info_context = "".join([str(doc) for doc in results_by_constituency_info.to_dict(orient='records')])
            context += f"{{Votes by Constituency: {results_by_constituency_info_context} }}"
        
        
        if not results_by_state_assembly_info.empty:
            results_by_state_assembly_info_context = "".join([str(doc) for doc in results_by_state_assembly_info.to_dict(orient='records')])
            context += f"{{Votes by State Assembly: {results_by_state_assembly_info_context} }}"
            
        # Generate response using OpenAI API
        print(f"## {constituency_name}\n")        
        response = generate_response(query, context)
        print(f"{response}\n")
        
        # Display context
        # print(f"{context}")
        # print(f"Context for constituency {constituency_name}: {results_by_constituency_info}")
        # print(f"Context for constituency {constituency_name}: {results_by_state_assembly_info}")



# Run the main function
if __name__ == "__main__":
    MainRAG()