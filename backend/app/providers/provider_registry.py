class ProviderRegistry:
    """
    Registry for external data providers.

    This gives AlphaSight one place to register, retrieve,
    and inspect providers as the platform grows.
    """

    def __init__(self):
        self._providers = {}

    def register(self, name: str, provider):
        self._providers[name] = provider

    def get(self, name: str):
        return self._providers.get(name)

    def all(self):
        return self._providers

    def names(self):
        return list(self._providers.keys())