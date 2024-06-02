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
            {"role": "system", "content": "You are an expert in political analysis and election predictions. Provide a detailed analysis and final Predicted Elected Member, Predicted Elected Party, Predicted Winning votes, Predicated Vote Share%. Calculate the predicted vote share percentage as the proportion of total votes received by the winning candidate compared to the overall votes cast in the election. Ensure that the difference in vote share percentage between the winner and the second-place candidate correctly maps to the predicted winning votes, which is the difference in the number of votes received by the winning candidate and the second-place candidate."},
            {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.2
    )
    return response.choices[0].message.content

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def preprocess_unstructured_data(files):
    # Process unstructured documents to create a structured context
    processed_docs = []
    model = None
    if os.path.exists('model.bin'):
        # Load model
        model = Word2Vec.load('model.bin')
    else:
        for file in files:
            print(f"Processing file: {file}")
            content = read_file(file)
        
            # Text Cleaning: This involves removing unnecessary and redundant data like HTML tags, URLs, emojis, and punctuation. It also includes converting all text to lower case to maintain uniformity.
            content = clean_text(content)

            # Tokenization: This is the process of breaking down the text into individual words or tokens. This can be done using the tokenize function from the nltk.tokenize module in Python.
            tokens = word_tokenize(content)

            # Stopword Removal: Stopwords are common words that do not add much meaning to a sentence (e.g., "the", "is", "in"). These can be removed to reduce the size of the data.
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words]

            # Stemming/Lemmatization: This is the process of reducing words to their root form. For example, "running" becomes "run". This can be done using the PorterStemmer or WordNetLemmatizer from the nltk.stem module.
            stemmer = PorterStemmer()
            tokens = [stemmer.stem(token) for token in tokens]

            print("Tokens:", tokens)
            processed_docs.append(tokens)


        # Vectorization: This involves converting text data into a numerical format that can be understood by the model. This can be done using techniques like Word Embeddings.
        # Train a Word2Vec model
        model = Word2Vec(processed_docs, min_count=1)

        # Save model
        model.save('model.bin')

    # Summarize the loaded model
    # print(model)
    
    return model

# Function to retrieve documents based on a query
def retrieve_documents(query, index, documents):
    query_words = query.split()
    relevant_docs = set()
    for word in query_words:
        if word in index:
            relevant_docs.update(index[word])
    return [documents[doc_id] for doc_id in relevant_docs]


def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # remove HTML tags
    text = re.sub(r'\n', ' ', text)  # remove newline characters
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    text = text.lower()  # convert to lower case
    return text

def get_most_similar_words(model, word):
    try:
        return model.wv[word]
    except KeyError:
        # print(f"The word '{word}' is not in the vocabulary.")
        return []

def MainRAG():
    # Load datasets
    candidates_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-candidates.csv')
    voter_turnout_2024  = pd.read_csv('../data/loksabha/2024/2024-kerala-voter-turnout.csv')
    data_2019   = pd.read_csv('../data/loksabha/2019/2019-kerala-constituency-wise-result.csv')
    data_2014  = pd.read_csv('../data/loksabha/2014/2014-kerala-constituency-wise-result.csv')
    data_2009  = pd.read_csv('../data/loksabha/2009/2009-kerala-constituency-wise-result.csv')
    poll_2024  = pd.read_csv('../data/loksabha/2024/polls.csv')

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

    # Process unstructured data
    unstructured_docs = [
        "./data/manorama-14Dec2023.txt", 
        "./data/mathrubhumi-21Mar2024.txt",
        "./data/new18-13Mar2024.txt",
        "./data/news-abplive-12Mar2024.txt"]  # Placeholder for actual unstructured data file paths
    
    unstructured_model = preprocess_unstructured_data(unstructured_docs)


    results = []
    print("# Election Predictions\n")
    for constituency in constituencies:
        constituency_number = constituency["#"]
        constituency_name = constituency["Constituency"]

        # Example query
        query = f"Predict the election result for constituency {constituency_name} in 2024."

        # Analyze the user's input
        relevant_words = get_most_similar_words(unstructured_model, constituency_name)
        # if relevant_words:
        #    print(f"Relevant words for query '{constituency_name}': {relevant_words}")

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
        turnout_context = "".join([str(doc) for doc in turnout_info.to_dict(orient='records')])
        context += f"{{2024 Voter Turnout: {turnout_context} }}"

        mp_info = data_mp[data_mp['Constituency'] == constituency_name]
        mp_info_context = "".join([str(doc) for doc in mp_info.to_dict(orient='records')])
        context += f"{{Current Elected Member Performance: {mp_info_context} }}"

        if relevant_words:
            context += f"{{Unstructured data: {relevant_words} }}"

        if not kerala_other_poll_data.empty:
            kerala_other_poll_data_context = "".join([str(doc) for doc in kerala_other_poll_data.to_dict(orient='records')])
            context += f"{{Kerala Opinion and Exit Poll Data: {kerala_other_poll_data_context} }}"

        if not allindia_other_poll_data.empty:
            allindia_other_poll_data_context = "".join([str(doc) for doc in allindia_other_poll_data.to_dict(orient='records')])
            context += f"{{All India Opinion and Exit Poll Data: {allindia_other_poll_data_context} }}"
        
        # Display context
        # print(f"Context for constituency {constituency_name}: {context}")

        # Generate response using OpenAI API
        response = generate_response(query, context)
        results.append({'Constituency': constituency_name, 'Prediction': response})
        print(f"## {constituency_name}\n")
        print(f"{response}\n")  
    
    # Printing in Markdown format
    # print("# Election Predictions\n")
    # for i, result in enumerate(results, start=1):
    #     print(f"## {result['Constituency']}\n")
    #     print(f"{result['Prediction']}\n")

# Run the main function
if __name__ == "__main__":
    # MainRandomForestClassifier()
    MainRAG()