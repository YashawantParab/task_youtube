import openai
import sys
from youtube_transcript_api import YouTubeTranscriptApi

openai.api_key = 'APIKEY'
diagnostics = 0
include_mentions = 0

def get_video_id(video_id_or_url):
    if len(video_id_or_url) > 11:
        return video_id_or_url[-11:]
    else:
        return video_id_or_url

def get_chunks(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    chunks = []
    start_timestamp = 0.0
    current_timestamp_mins = 0.0

    current_chunk = []

    for entry in transcript:
        current_timestamp_mins = entry['start'] / 60.0
        if current_timestamp_mins - start_timestamp > 10:
            chunks.append(current_chunk)
            start_timestamp = current_timestamp_mins
            current_chunk = []

        current_chunk.append(entry['text'])

    if len(current_chunk) > 0:
        chunks.append(current_chunk)

    print(f"Found {len(chunks)} chunks")
    return chunks

def summarize_chunk(index, chunk):
    chunk_str = "\n".join(chunk)
    prompt = (f"""This section of the transcript of a youtube video. It is section #{index+1}:
    {chunk_str} Summarize this section of the transcript.""")

    if diagnostics:
        # print each line of the prompt with a leading # so we can see it in the output
        for line in prompt.split('\n'):
            print(f"# {line}")

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=500, 
        temperature=0.2,
        prompt=prompt,
        frequency_penalty=0
    )

    msg = completion.choices[0].text

    if diagnostics:
        print(f"# Response: {msg}")

    return msg

def summarize_the_summaries(summaries):

    summaries_str = ""
    for index, summary in enumerate(summaries):
        summaries_str += f"Summary of chunk {index+1}:\n{summary}\n\n"

    prompt = (f"""This section is summaries of a youtube video in 10 minute chunks:"
    {summaries_str} Summarize the summaries.""")

    if diagnostics:
        # print each line of the prompt with a leading # so we can see it in the output
        for line in prompt.split('\n'):
            print(f"# {line}")

    completion = openai.Completion.create(
        engine="text-davinci-003", 
        max_tokens=500, 
        temperature=0.2,
        prompt=prompt,
        frequency_penalty=0
    )

    msg = completion.choices[0].text

    if diagnostics:
        print(f"# Response: {msg}")

    return msg

def main():
    video_id_or_url = "https://www.youtube.com/watch?v=Nro6oFD3oHw"

    video_id = get_video_id(video_id_or_url)

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg == "--diagnostics":
                global diagnostics
                diagnostics = True

            if arg == "--mentions":
                global include_mentions
                include_mentions = True

    chunks = get_chunks(video_id)

    if len(chunks) == 0:
        print("No chunks found")
    elif len(chunks) == 1:
        summary = summarize_chunk(0, chunks[0])
        print(f"\nSummary: {summary}")
    else:
        summaries = []
        mentioneds = []
        for index, chunk in enumerate(chunks):
            summary = summarize_chunk(index, chunk)
            summaries.append(summary)
            print(f"\nSummary of chunk {index+1}: {summary}")
        summary_of_summaries = summarize_the_summaries(summaries)

        print(f"\nSummary of summaries: {summary_of_summaries}")

if __name__ == "__main__":
    main()
