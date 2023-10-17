# batchGPT

A Python script leveraging the OpenAI API, specifically the GPT-3.5-turbo-16k model, to process large text inputs. I wrote this script to post-processing (refining and translating) the transcription of some lectures I took using Google's Speech-to-Text API. You can define your own prompt for your text processing job.

The script efficiently breaks the input into manageable chunks, processes each chunk, and then invokes separate API calls and provides the joint output.

## My Prompts
- **Refine Text**: Improve the quality of transcriptions or any large text by refining grammar, maintaining tone, preserving humor, and improving readability.
- **Translate Text**: Convert English text into Chinese, providing high-quality, fluent translations with an emphasis on simplicity and clarity.

## Prerequisites
- Python 3.x
- `nltk` library (`pip install nltk`)
- OpenAI Python client (`pip install openai`)

## Setup & Installation

1. Clone this repository:

2. Download the required NLTK tokenizer:
   ```
   python -c "import nltk; nltk.download('punkt')"
   ```

3. Set up your OpenAI API key. Never hardcode this key in your scripts. Instead, set it as an environment variable:
   ```
   export OPENAI_API_KEY='your_openai_api_key'
   ```

## Usage

```
python batchGPT.py <path_to_input_file> [refine/translate]
```
- `<path_to_input_file>`: Path to the file containing the text you want to refine or translate.
- `refine`: For refining and improving the quality of the text.
- `translate`: For translating the text from English to Chinese.

For example:
```
python batchGPT.py myLectureTranscription.txt refine
```

## Customizing the Prompt

The prompts provided for refining and translating are generic. If you're working with a specific domain or need more customized results, you're encouraged to modify the `system_text` within the script. Create prompts that guide the model to deliver results in the manner you desire.

## License

This project is licensed under the MIT License.

## Disclaimer

This script uses the OpenAI API, which is a paid service. Ensure you're aware of the costs associated with your usage.
