import sys
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from openai import OpenAI

nltk.download('punkt')

client = OpenAI()

# We use 2k token inputs for GPT-3.5-turbo-1106 model
# as it returns a maximum of 4096 tokens per completion
# You might want to make some adjustment
MAX_SIZE = 2048

# Split long texts into chunks of sentences
def split_into_chunks(text, max_size=MAX_SIZE):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    for sentence in sentences:
        if current_chunk_size + len(word_tokenize(sentence)) <= max_size:
            current_chunk_size += len(word_tokenize(sentence))
            current_chunk.append(sentence)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_chunk_size = len(word_tokenize(sentence))
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

def process(input_file, action):
    output_file = os.path.splitext(input_file)[0] + (".refined.md" if action == "refine" else ".translated.md")

    with open(input_file, 'r') as f:
        content = f.read()

    chunks = split_into_chunks(content)
    print(f"Split into {len(chunks)} chunks")

    if action == "refine":
        system_text = """
        As a Computer Science professor, your task is to proofread and correct a raw transcript of your course. 
        The text has been transcribed using Google's Speech-to-Text API, resulting in grammar mistakes and recognition errors. 
        Your goal is to recover the original lecture transcript and provide the entire corrected text.

        To successfully complete this task, please consider the following guidelines:

        1. Error correction: Carefully examine the transcript and correct any grammar mistakes and recognition errors. Ensure that the corrected text accurately reflects the content of the lecture.
        2. Maintain tone and voice: While correcting errors, it is important to preserve the original tone and voice of the lecture. Pay attention to the professor's style of delivery, ensuring that the corrected text captures the same essence.
        3. Preserve humor: Never remove or alter jokes made by the professor. It is important to maintain the humor and light-heartedness of the lecture, as humor often helps engage students and make the subject more enjoyable.
        4. Improve readability: Seperate the transcript into paragraphs of appropriate length to enhance the readability of the corrected text. 
        5. Use Markdown syntax: Use Markdown syntax to format the text.

        """
    elif action == "translate":
        system_text = """
        Translate the following text from English to Chinese. Do not add any response other than the translated text.
        The system should exhibit a strong understanding of the context and produce high-quality and fluent translations. 
        To successfully complete this task, please consider the following guidelines:

        1. Use Markdown syntax: Use Markdown syntax to format the text.
        2. Improve readability: Use appropriate paragraph breaks to enhance the readability of the translated text.
        3. Improve coherence: Ensure that the translated text is coherent and flows naturally.

        """
    else:
        raise ValueError(f"Unsupported action: {action}")

    print("Processing...")

    with open(output_file, 'w') as f:
        for chunk in chunks:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=[
                    {"role": "system", "content": system_text},
                    {"role": "user", "content": chunk}
                ]
            )
            edited_chunk = completion.choices[0].message.content
            print(edited_chunk)
            f.write(edited_chunk + '\n')

    print(f"Output file saved as {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input_file [refine/translate]")
    else:
        input_file = sys.argv[1]
        action = sys.argv[2]
        if action not in ["refine", "translate"]:
            print("Invalid action. Please choose either 'refine' or 'translate'.")
        else:
            process(input_file, action)