import aiohttp
import asyncio
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

class AIEngine:
    """DeepSeek AI integration wrapper"""
    
    def __init__(self):
        # API key hardcoded (for deployment)
        self.api_key = "sk-51fb497ebdb9419b95db3eab9e61fb49"
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.model = "deepseek-chat"
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
    
    async def generate_response(
        self,
        query: str,
        system_prompt: str = "You are a helpful AI assistant.",
        wiki_context: Optional[str] = None,
        max_tokens: int = 300
    ) -> str:
        """
        Generate AI response using DeepSeek API
        
        Args:
            query: User's query
            system_prompt: System prompt for personality
            wiki_context: Optional Wikipedia context
            max_tokens: Maximum response tokens
            
        Returns:
            Generated response text
        """
        try:
            # Build messages
            user_message = query
            if wiki_context:
                user_message = f"{query}\n\n📚 Context:\n{wiki_context}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.95
            }
            
            # Make async request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        logger.error(f"API error: {response.status} - {error_text}")
                        return self._get_fallback_response(query)
        
        except asyncio.TimeoutError:
            logger.error("API request timeout")
            return self._get_fallback_response(query)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_fallback_response(query)
    
    def _get_fallback_response(self, query: str) -> str:
        """Fallback response when API fails"""
        return (
            f"<b>Response to: {query}</b>\n\n"
            "⚠️ I'm experiencing technical difficulties. "
            "Please try again later or contact the administrator."
        )