class BaseStrategy:
    async def execute(self, query, manager, session_id):
        raise NotImplementedError
