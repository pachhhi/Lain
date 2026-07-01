class LLMClient:

    def __init__(self, provider):
        self.provider = provider

    def generate(self, messages):
        return self.provider.generate(messages)