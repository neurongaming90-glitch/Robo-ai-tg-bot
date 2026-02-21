import wikipedia
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WikiEngine:
    """Wikipedia integration wrapper"""
    
    def __init__(self, language: str = 'en'):
        """
        Initialize Wikipedia engine
        
        Args:
            language: Wikipedia language code (default: 'en')
        """
        wikipedia.set_lang(language)
    
    def get_summary(self, query: str, sentences: int = 3) -> Optional[str]:
        """
        Fetch Wikipedia summary for a query
        
        Args:
            query: Search query
            sentences: Number of sentences to return
            
        Returns:
            Wikipedia summary or None if not found
        """
        try:
            # Search and get summary
            summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
            return summary
        
        except wikipedia.exceptions.DisambiguationError as e:
            logger.info(f"Disambiguation error for '{query}': {e}")
            # Return first option if disambiguation
            if e.options:
                try:
                    summary = wikipedia.summary(e.options[0], sentences=sentences)
                    return f"(From: {e.options[0]})\n{summary}"
                except Exception as inner_e:
                    logger.error(f"Error getting summary for disambiguation option: {inner_e}")
                    return None
            return None
        
        except wikipedia.exceptions.PageError:
            logger.info(f"Page not found for '{query}'")
            return None
        
        except Exception as e:
            logger.error(f"Unexpected error fetching Wikipedia: {e}")
            return None
    
    def search(self, query: str, results: int = 5) -> list:
        """
        Search Wikipedia
        
        Args:
            query: Search query
            results: Number of results to return
            
        Returns:
            List of search results
        """
        try:
            return wikipedia.search(query, results=results)
        except Exception as e:
            logger.error(f"Error searching Wikipedia: {e}")
            return []