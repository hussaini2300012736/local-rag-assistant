# F1 RAG Assistant

This is a chatbot I built that answers Formula 1 questions using only its own local documents. It doesn't use the internet or any cloud AI service. Everything runs on my own laptop, including the AI model itself.

## The idea

Normal AI chatbots answer from whatever they memorized during training, which means they can be outdated or just make things up confidently. This project fixes that by giving the model a specific set of documents to work from. When you ask it something, it first searches those documents for the relevant part, then hands that text to the AI model so it can answer using real information instead of guessing. If nothing in the documents matches your question, it says so instead of inventing an answer.

This technique is called RAG, short for Retrieval-Augmented Generation. Retrieve the right info, add it to the prompt, then generate an answer.

## How it actually works, step by step

I wrote 9 short documents about F1. The basics, like what F1 is, tyres, and teams, plus a bunch of detail on the 2026 season specifically, like new car rules, new teams, tyre changes, and qualifying format changes.

Each document gets chopped into smaller chunks. A chunk is roughly a paragraph.

Every chunk gets turned into a list of numbers, called an embedding, that represents its meaning.

All of this gets saved into a small local database using SQLite.

When you ask a question, it turns your question into numbers the same way, then checks which stored chunks are numerically closest to it.

It hands the closest few chunks to the AI model along with your question, and tells it to only answer using this, and to say it doesn't know if the answer isn't there.

You get one real answer back, with the source documents it used.

## What it's built with

Foundry Local is Microsoft's tool that lets an AI model run directly on my laptop instead of calling a cloud server somewhere. SQLite is a lightweight local database, just one file, no server needed. Python handles all the actual logic, like chunking, searching, and connecting everything together. Streamlit runs the dashboard you see in the browser.

## Project files

rag_project holds app.py, which is the dashboard you open in your browser, and main.py, which is a plain terminal version if you don't want the dashboard.

Inside src, foundry_client.py connects to the AI model running locally, db.py sets up and talks to the SQLite database, ingest.py takes the documents, chunks them, embeds them, and saves them, retrieve.py finds the closest matching chunks for a question, and qa.py combines retrieval and the AI model into one answer.

data/docs holds the actual 9 F1 documents. data/knowledge.db is the database itself, not stored in git, and can be rebuilt anytime.

tests/test_pipeline.py has a few automated test questions. assets/background.mp4 is the video used for the dashboard background. PROGRESS.md has my week by week notes while building this.

## How to run it

Get the environment ready by creating a virtual environment, activating it, and installing the requirements file.

Install Foundry Local itself, which is separate from the Python packages, using Homebrew, then start the service.

Build the database from the documents. This only needs to be done once, or again if you change the documents.

Then either open the dashboard with Streamlit, or use the plain terminal version instead.

To run the test questions, run the test pipeline module.

## Things worth trying

How many teams are on the 2026 grid.

How did qualifying change for 2026.

How do the tyre changes and the power unit changes both affect race strategy.

Who won the 2023 Monaco Grand Prix. It should say it doesn't know, since that's not in my documents. This is actually the important part to notice, not a bug.

## Things I know aren't perfect

It always pulls its closest matches even if nothing is actually relevant, so on questions it can't answer, it sometimes still lists a source document that doesn't really apply. A fix would be to just not show any sources if the similarity score is too low.

The first question in a new session takes a while, usually 20 to 40 seconds, because the AI model has to load into memory. After that it's normally faster. This is a real limit of running the model on my own laptop instead of a powerful cloud server, not something I can fully code my way out of.

It only knows what's in my 9 documents. If I want it to know more, I just have to add more documents and rebuild the database.

## What I'd do next if I kept working on this

Add a minimum similarity score so it stops citing irrelevant documents on I don't know answers. Split documents more carefully instead of just by paragraph. Show a confidence warning in the dashboard when none of the matches are very close.
