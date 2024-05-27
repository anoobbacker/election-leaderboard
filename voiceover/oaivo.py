from pathlib import Path
from openai import OpenAI
import warnings
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI()

# Define an array of sentences
sentences = [
    "Building a website is now super easy!",
    "Our friends love guessing football scores. This year, with all the election excitement, we decided to guess the Lok Sabha Election 2024 results for Kerala!",
    "I made this app from scratch using OpenAI, SvelteKit, Supabase, and Tailwind CSS.",
    "To start, open the website, click 'Get Started', and enter your email and password to log in!",
    "Each person can see the list of 20 constituencies in Kerala and their candidates. Then, click 'Predict' to submit your guesses!",
    "After the results are out on July 4th, the leaderboard will show the participants and their points based on their guesses!",
    "The entire source code and instructions are available on GitHub. Thanks for watching!",
    "Building a website is now super easy! Our friends love guessing football scores. This year, with all the election excitement, we decided to guess the Lok Sabha Election 2024 results for Kerala! I made this app from scratch using OpenAI, SvelteKit, Supabase, and Tailwind CSS. To start, open the website, click 'Get Started', and enter your email and password to log in. Each person can see the list of 20 constituencies in Kerala and their candidates. Then, click 'Predict' to submit your guesses! After the results are out on June 4th, the leaderboard will show the participants and their points based on their guesses! The entire source code and instructions are available on GitHub. Thanks for watching!"
]

# Create a directory to save the audio files
output_dir = Path(__file__).parent / "openai_speech_out"
output_dir.mkdir(parents=True, exist_ok=True)

# Temporary file to store the sentences from the last run
temp_file = os.path.join(output_dir, "last_sentences.txt")
# Read the last run's sentences from the temporary file
def read_last_sentences():
    if os.path.exists(temp_file):
        with open(temp_file, 'r') as file:
            return file.read().splitlines()
    return []

# Write the current run's sentences to the temporary file
def write_current_sentences(sentences):
    with open(temp_file, 'w') as file:
        file.write('\n'.join(sentences))

# Compare and synthesize speech for new or changed sentences
last_run_sentences = read_last_sentences()

# Iterate over sentences, generate audio for each, and save to separate files
for i, sentence in enumerate(sentences):
    # Generate speech only if the sentence is new or has changed
    if i >= len(last_run_sentences) or sentence != last_run_sentences[i]:
      speech_file_path = output_dir / f"speech_{i+1}.mp3"
      response = client.audio.speech.create(
          model="tts-1-hd",
          voice="alloy",
          input=sentence
      )
      response.stream_to_file(speech_file_path)
      print(f"Saved audio for sentence {i+1} to {speech_file_path}")
    else:
        print(f"Skipping synthesis for unchanged text [speech_{i+1}.mp3]")

# Update the temporary file with the current run's sentences
write_current_sentences(sentences)

print(f"All audio files saved to {output_dir}")
