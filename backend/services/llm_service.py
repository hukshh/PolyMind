class LLMService:
    @staticmethod
    async def get_response(message: str) -> str:
        # Placeholder for LLM logic
        return f"This is a dummy response to: '{message}'"

llm_service = LLMService()
