sample_data_generation_prompt = """
Act as if you are a Formula 1 Driver and is in constant communication with the team regarding the state of the race and your car. 
Create some sentences that you might say that are relevant to the following query: {query}.

Guidelines:
* Keep the messages short brief and to the point.
* Respond in the form for a python list of strings
"""


query_prompt = """Please provide a concise yet informative response to the following question:
{query}
Guidelines:

* Aim for a balanced answer - neither overly lengthy nor excessively brief
* Focus on directly addressing the question without extensive justification
* Consider the context provided by the relevant radio transcript excerpts below
* Be aware that the transcripts may contain typos or errors - use your judgment to interpret similar words or phrases
* Mention the time for the transcript if needed for the query. Convert the seconds to a human readable format

Relevant transcript excerpts:
{transcripts}
"""

asr_prompt = """
This is an audio transcription of Formula 1 team radio communications. 
It may contain technical racing terms, driver and team names, and track-specific vocabulary. 
Background noise and accents may be present. 
Please transcribe accurately, paying attention to: Driver and engineer names, Car parts and setup terms, Racing strategy terminology, Track names and corner numbers, Tire compound names, Safety car and flag status updates.
Transcribe number values precisely and maintain original phrasing where possible. All sentences might not be grammatically accurate. 
Here are names of the drivers that might come up:

Lewis Hamilton
Valtteri Bottas
Max Verstappen
Sergio Pérez
Lando Norris
Daniel Ricciardo
Charles Leclerc
Carlos Sainz
Sebastian Vettel
Lance Stroll
Fernando Alonso
Esteban Ocon
Pierre Gasly
Yuki Tsunoda
Kimi Räikkönen
Antonio Giovinazzi
George Russell
Nicholas Latifi
Mick Schumacher
Nikita Mazepin

Some additional terms that can be present: turn, strat.
"""
