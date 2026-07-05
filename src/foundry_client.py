from foundry_local_sdk import Configuration, FoundryLocalManager

_manager = None


def get_manager():
    global _manager
    if _manager is None:
        config = Configuration(app_name="rag_project")
        FoundryLocalManager.initialize(config)
        _manager = FoundryLocalManager.instance
    return _manager


def get_embedding_client(alias="qwen3-embedding-0.6b"):
    manager = get_manager()
    model = manager.catalog.get_model(alias)
    model.download()
    model.load()
    return model.get_embedding_client()


def get_chat_client(alias="phi-3.5-mini"):
    manager = get_manager()
    model = manager.catalog.get_model(alias)
    model.download()
    model.load()
    return model.get_chat_client()


def embed(client, text):
    response = client.generate_embedding(text)
    return response.data[0].embedding
