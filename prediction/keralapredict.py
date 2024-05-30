import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from openai import OpenAI

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

def get_chatgpt_prediction(constituency_number, constituency_name, candidate_names, predicted_party, turnout):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in political analysis and election predictions."},
            {"role": "user", "content": f"Predict the election result for constituency {constituency_number} ({constituency_name}). The candidates are {candidate_names}. The voter turnout is {turnout}%. The initial prediction is {predicted_party}. Provide a detailed analysis and final Predicted Elected Member, Predicted Elected Party, Predicted Margin, Predicated Vote Share%."}
        ]
    )
    return response.choices[0].message


# Define response generation function
def generate_response(query, context):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in political analysis and election predictions. Provide a detailed analysis and final Predicted Elected Member, Predicted Elected Party, Predicted Margin, Predicated Vote Share%."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.2
    )
    return response.choices[0].message

def MainRAG():
    # Load datasets
    candidates_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-candidates.csv')
    voter_turnout_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-voter-turnout.csv')
    data_2019   = pd.read_csv('../data/loksabha/2019/2019-kerala-constituency-wise-result.csv')
    data_2014  = pd.read_csv('../data/loksabha/2014/2014-kerala-constituency-wise-result.csv')
    data_2009  = pd.read_csv('../data/loksabha/2009/2009-kerala-constituency-wise-result.csv')

    # Add year columns
    data_2009['Year'] = 2009
    data_2014['Year'] = 2014
    data_2019['Year'] = 2019

    # Combine historical data
    historical_data = pd.concat([data_2009, data_2014, data_2019], ignore_index=True)

    # Preprocess data if necessary
    historical_data.fillna('', inplace=True)
    # print(historical_data)

    results = []
    
    for constituency in constituencies:
        constituency_number = constituency["#"]
        constituency_name = constituency["Constituency"]

        # Example query
        query = f"Predict the election result for constituency {constituency_name} in 2024."

        # Retrieve relevant documents
        retrieved_docs = search_historical_data(historical_data, constituency_number)

        # Concatenate retrieved documents as context
        context = "".join([str(doc) for doc in retrieved_docs.to_dict(orient='records')])
        
        # Retrieve 2024 candidate and voter turnout data
        candidate_info = candidates_2024[candidates_2024['#'] == constituency_number]

        turnout_info = voter_turnout_2024[voter_turnout_2024['#'] == constituency_number]

        # Extract 2024 candidate information by party
        udf_info = f"'UDF Party': '{candidate_info['UDF Party'].values[0]}', 'UDF Member': '{candidate_info['UDF Member'].values[0]}'"
        ldf_info = f"'LDF Party': '{candidate_info['LDF Party'].values[0]}', 'LDF Member': '{candidate_info['LDF Member'].values[0]}'"
        nda_info = f"'NDA Party': '{candidate_info['NDA Party'].values[0]}', 'NDA Member': '{candidate_info['NDA Member'].values[0]}'"

        context += f"{{'2024 Candidates': {{{udf_info} {ldf_info}{nda_info}}}}}"
        # context += f"{{2024 Voter Turnout: {turnout_info.to_string(index=False)}}}"
        turnout_context = "".join([str(doc) for doc in turnout_info.to_dict(orient='records')])
        context += f"{{2024 Voter Turnout: {turnout_context} }}\n"
        
        # Generate response using GPT-3
        response = generate_response(query, context)
        results.append({'Constituency': constituency_name, 'Prediction': response})
    
    print(results)

def MainRandomForestClassifier():
    # Load datasets
    constituency_df = pd.read_csv('../data/loksabha/2024/kerala-constituency.csv')
    candidates_df = pd.read_csv('../data/loksabha/2024/2024-kerala-candidates.csv')
    voter_turnout_df = pd.read_csv('../data/loksabha/2024/2024-kerala-voter-turnout.csv')
    result_2019_df = pd.read_csv('../data/loksabha/2019/2019-kerala-constituency-wise-result.csv')
    result_2014_df = pd.read_csv('../data/loksabha/2014/2014-kerala-constituency-wise-result.csv')
    result_2009_df = pd.read_csv('../data/loksabha/2009/2009-kerala-constituency-wise-result.csv')

    # Add year columns
    result_2009_df['Year'] = 2009
    result_2014_df['Year'] = 2014
    result_2019_df['Year'] = 2019

    # Combine historical data
    historical_data = pd.concat([result_2009_df, result_2014_df, result_2019_df], ignore_index=True)

    # Preprocess data if necessary
    historical_data.fillna('', inplace=True)
    # Data Preprocessing
    # Convert the 'Turnout%' and 'Vote Share%' columns to string to avoid AttributeError
    historical_data['Turnout%'] = historical_data['Turnout%'].astype(str)
    historical_data['VoteShare%'] = historical_data['VoteShare%'].astype(str)

    # Remove '%' sign and convert to float
    historical_data['Turnout%'] = historical_data['Turnout%'].str.rstrip('%').astype(float)
    historical_data['VoteShare%'] = historical_data['VoteShare%'].str.rstrip('%').astype(float)

    # Encoding categorical variables
    party_encoder = LabelEncoder()
    member_encoder = LabelEncoder()

    historical_data['Elected Party Encoded'] = party_encoder.fit_transform(historical_data['Elected Party'])
    historical_data['Elected Member Encoded'] = member_encoder.fit_transform(historical_data['Elected Member'])

    print(historical_data)

    # Features and Labels
    X = historical_data[['Year', 'Turnout%', 'VoteShare%']]
    y = historical_data[['Elected Party Encoded', 'Elected Member Encoded']]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(X_train, y_train)

    # Model evaluation
    y_pred = model.predict(X_test)
    accuracy_party = accuracy_score(y_test['Elected Party Encoded'], y_pred[:, 0])
    accuracy_member = accuracy_score(y_test['Elected Member Encoded'], y_pred[:, 1])
    print(f'Model Accuracy for Party: {accuracy_party * 100:.2f}%')
    print(f'Model Accuracy for Member: {accuracy_member * 100:.2f}%')

    # Preparing 2024 data for prediction
    voter_turnout_df['Turnout%'] = voter_turnout_df['Turnout%'].astype(str)
    voter_turnout_df['Turnout%'] = voter_turnout_df['Turnout%'].str.rstrip('%').astype(float)
    voter_turnout_df['Year'] = 2024  # Add the Year column for 2024 data

    candidates_df = candidates_df.merge(constituency_df, on='#')
    prediction_data = voter_turnout_df.merge(candidates_df, on='#')
    prediction_data['VoteShare%'] = prediction_data['Turnout%']  # Simplified assumption

    # Prediction
    X_2024 = prediction_data[['Turnout%', 'VoteShare%', 'Year']]
    y_2024_pred = model.predict(X_2024)
    prediction_data['Predicted Party Encoded'] = y_2024_pred[:, 0]
    prediction_data['Predicted Member Encoded'] = y_2024_pred[:, 1]
    # prediction_data['Predicted Party', 'Predicted Member'] = model.predict(X_2024)

    prediction_data['Predicted Party'] = party_encoder.inverse_transform(prediction_data['Predicted Party Encoded'])
    prediction_data['Predicted Member'] = member_encoder.inverse_transform(prediction_data['Predicted Member Encoded'])

    # Apply ChatGPT predictions
    for index, row in prediction_data.iterrows():
        print(f"Start predicting {row['Constituency']}...")
        candidate_names = f"UDF: {row['UDF Member']}, LDF: {row['LDF Member']}, NDA: {row['NDA Member']}"
        analysis = get_chatgpt_prediction(row['#'], row['Constituency'], candidate_names, row['Predicted Party'], row['Turnout%'])
        prediction_data.loc[index, 'ChatGPT Analysis'] = analysis
        print(f"Completed predicting {row['Constituency']}: {analysis}")

    # Display predictions
    print(prediction_data[['#', 'Constituency', 'Predicted Party', 'Predicted Member', 'ChatGPT Analysis']])

# Run the main function
if __name__ == "__main__":
    # MainRandomForestClassifier()
    MainRAG()