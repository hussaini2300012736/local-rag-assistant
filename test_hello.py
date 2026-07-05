from foundry_local_sdk import Configuration, FoundryLocalManager

print("Step 1: initializing config...")
config = Configuration(app_name="rag_project")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance
print("Step 2: manager ready")

print("Step 3: getting model from catalog...")
model = manager.catalog.get_model("phi-3.5-mini")
print("Step 4: got model, checking download...")

model.download()
print("Step 5: download check done, loading model...")

model.load()
print("Step 6: model loaded, sending chat request...")

client = model.get_chat_client()
response = client.complete_chat([
    {"role": "user", "content": "Say hello in one sentence."}
])
print("Step 7: got response")
print(response.choices[0].message.content)

model.unload()
