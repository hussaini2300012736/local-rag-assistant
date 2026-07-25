# My notes while building this

This is just my running log of what I did each week, mistakes I made, and things worth remembering. Not polished, just honest notes for me and my teammate.

## Week 1, getting everything installed

Spent most of this week just getting things to actually run. Installed Foundry Local through Homebrew, set up a Python virtual environment, installed the packages I needed. Ran into a bunch of small problems along the way. Files saving to the wrong folder because VS Code and my terminal were pointed at two different folders without me realizing, forgetting to activate my virtual environment in new terminal windows, stuff like that. All normal beginner stuff, just took longer than I expected.

By the end of the week I had a script that actually sent a message to a real AI model running on my own laptop and got a real answer back. That was the actual goal. Everything else was just plumbing to get there.

Thing to remember. The actual way to use the SDK is different from a lot of tutorials online, since Microsoft seems to have changed it. The real pattern is:
```python
from foundry_local_sdk import Configuration, FoundryLocalManager
config = Configuration(app_name="rag_project")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("phi-3.5-mini")
model.download()
model.load()
client = model.get_chat_client()
```

## Week 2, proving the smart search idea works

This week was about the core trick behind the whole project. Turning text into numbers so a computer can tell what's similar in meaning, not just similar words. I tested it with two similar sentences and one unrelated one and checked the similarity scores. The similar pair scored 0.75, the unrelated one scored 0.38. That gap is basically the whole reason this project works.

Also learned how to save that stuff into SQLite, which is just a single file database, nothing fancy.

Small annoying thing. The embedding model doesn't even show up when you list available models from the command line, seems to be a display bug, but it works completely fine once you call it from Python. Also the response comes back nested inside an object, response.data[0].embedding, not directly.

## Week 3, the actual pipeline

Wrote 9 real documents about F1. Some general basics, and a bunch of very specific stuff about the 2026 season like new car rules, new teams such as Audi and Cadillac joining, cost cap changes, tyre changes, and qualifying format changes. Then built the actual code that breaks each document into small chunks, turns each chunk into an embedding, saves it all in the database, and can take any question and find the closest matching chunks.

Tested it with a bunch of questions and it consistently found the right document, with a clear gap between the best match and the rest. This is the part that actually convinced me the whole idea works, not just in theory.

## Week 4, hooking up the AI model to give real answers

Before this, the assistant just showed raw chunks of text. This week I combined the retrieval part with an actual AI model, so it reads the chunks and gives one real, written answer, and mentions which document it used.

Tested it on both an answerable question and one that isn't in my documents, like asking who won a specific old race. It correctly refused to guess on the one it didn't know. That felt like the best proof the whole thing was working the way it's supposed to.

Small thing I noticed. Even on "I don't know" answers, it still shows source documents, since my retrieval code always returns its top matches no matter how weak they are. Not wrong, just a little misleading. Worth fixing later by adding a minimum score cutoff.

Also built a dashboard using Streamlit so I could actually interact with it in a browser instead of just the terminal, and gave it an F1 look. Dark background, red accents, a proper F1 font, a scrolling checkered flag stripe, circular gauges showing how confident each source match was, and an opening animation styled like the actual F1 five lights start sequence.

## Week 5, testing it properly

Wrote 6 test questions, 3 it should be able to answer and 3 it shouldn't, and ran them automatically instead of just testing by hand. First run showed 2 false failures, but that was actually a bug in my test script, not the assistant. I was checking for one exact phrase, "don't have that information," and the model phrased it slightly differently both times, "don't have information about." Fixed the test to check for a few different phrasings instead. After that, 6 out of 6 passed properly.

Also looked at response times. First question in a session takes a long time, around 20 to 25 seconds, because the model has to load into memory. After that, each question takes somewhere between 4 and 12 seconds depending on how long the answer is. I tried to fix this a couple different ways, mainly caching the client differently, but the timing stayed exactly the same either way, which told me it's a real hardware limit of running the model locally, not a bug in my code. Isolating it with a warm up step at the start at least means it doesn't surprise you mid conversation.

Later, while adding a background video to the dashboard, questions started taking 40 seconds every single time, not just the first one. Still figuring out exactly why. My best guess going in was the video being reprocessed on every interaction, but I ruled that out with caching and it didn't help either. Left this as an open problem for now since it's not blocking the actual project from working, just makes the dashboard slower than it should be.

## Week 6, writing it all up

Finished the README, cleaned up the notes here, and put together a plan for demoing this live. Ask a normal question, ask a complex one that needs combining two documents, then ask something it genuinely shouldn't know, like an old race result, so it can show it correctly refuses instead of making something up. That last one is honestly the most important moment in the whole demo, since it's the entire point of RAG.

## Things I'd still like to fix if I keep working on this

Add a minimum similarity score, so weak or irrelevant matches don't get shown at all instead of always showing "closest" results. Figure out why the dashboard got slow after adding the background video. Chunk documents a bit smarter than just splitting by paragraph.
