"""
Multi-LLM Service for PhysicsAI.

This service provides a unified interface to multiple LLM providers,
allowing users to choose their preferred model and use their own API keys.
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum

# Import LLM providers
import openai
import anthropic

# LangChain imports for compatibility
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class LLMModel(str, Enum):
    """Supported models for each provider."""
    # OpenAI models
    GPT45_PREVIEW = "gpt-4.5-preview"
    GPT4_TURBO = "gpt-4-turbo"
    GPT4 = "gpt-4"
    GPT35_TURBO = "gpt-3.5-turbo"
    
    # Anthropic models
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"

class MultiLLMService:
    """Service for interacting with multiple LLM providers."""
    
    def __init__(self):
        """Initialize the Multi-LLM service."""
        self.active_provider = LLMProvider.OPENAI
        self.active_model = LLMModel.GPT4
        self.api_keys = {}
        self.clients = {}
        
        # Initialize with environment variables if available
        if os.getenv("OPENAI_API_KEY"):
            self.set_api_key(LLMProvider.OPENAI, os.getenv("OPENAI_API_KEY"))
        if os.getenv("ANTHROPIC_API_KEY"):
            self.set_api_key(LLMProvider.ANTHROPIC, os.getenv("ANTHROPIC_API_KEY"))

    
    def set_api_key(self, provider: LLMProvider, api_key: str) -> None:
        """Set the API key for a specific provider."""
        self.api_keys[provider] = api_key
        
        # Initialize the client for this provider
        if provider == LLMProvider.OPENAI:
            os.environ["OPENAI_API_KEY"] = api_key
            self.clients[provider] = openai.OpenAI(api_key=api_key)
        elif provider == LLMProvider.ANTHROPIC:
            os.environ["ANTHROPIC_API_KEY"] = api_key
            self.clients[provider] = anthropic.Anthropic(api_key=api_key)

    
    def set_active_provider(self, provider: LLMProvider) -> bool:
        """Set the active provider to use for generation."""
        if provider not in self.api_keys:
            logging.error(f"No API key set for provider: {provider}")
            return False
        
        self.active_provider = provider
        return True
    
    def set_active_model(self, model: LLMModel) -> bool:
        """Set the active model to use for generation."""
        # Check if the model is compatible with the active provider
        provider_models = {
            LLMProvider.OPENAI: [LLMModel.GPT45_PREVIEW, LLMModel.GPT4_TURBO, LLMModel.GPT4, LLMModel.GPT35_TURBO],
            LLMProvider.ANTHROPIC: [LLMModel.CLAUDE_3_OPUS, LLMModel.CLAUDE_3_SONNET, LLMModel.CLAUDE_3_HAIKU]
        }
        
        if model not in provider_models.get(self.active_provider, []):
            logging.error(f"Model {model} is not compatible with provider {self.active_provider}")
            return False
        
        self.active_model = model
        return True
    
    def get_available_providers(self) -> List[LLMProvider]:
        """Get a list of providers that have API keys set."""
        return list(self.api_keys.keys())
    
    def get_available_models(self, provider: Optional[LLMProvider] = None) -> List[LLMModel]:
        """Get a list of available models for a provider."""
        provider = provider or self.active_provider
        
        provider_models = {
            LLMProvider.OPENAI: [LLMModel.GPT4_TURBO, LLMModel.GPT4, LLMModel.GPT35_TURBO],
            LLMProvider.ANTHROPIC: [LLMModel.CLAUDE_3_OPUS, LLMModel.CLAUDE_3_SONNET, LLMModel.CLAUDE_3_HAIKU]
        }
        
        return provider_models.get(provider, [])
    
    async def generate_text(self, prompt: str, system_prompt: str = "", temperature: float = 0.7, messages: List[Dict[str, str]] = None) -> str:
        """Generate text using the active provider and model.
        
        Args:
            prompt: The prompt to generate text from. If messages is provided, this will be added as the last user message.
            system_prompt: The system prompt to use.
            temperature: The temperature to use for generation.
            messages: Optional list of message dictionaries with 'role' and 'content' keys. If provided, these will be used instead of creating a simple system+user message pair.
        
        Returns:
            The generated text.
        """
        if self.active_provider not in self.api_keys:
            raise ValueError(f"No API key set for provider: {self.active_provider}")
        
        try:
            # OpenAI
            if self.active_provider == LLMProvider.OPENAI:
                return await self._generate_openai(prompt, system_prompt, temperature, messages)
            
            # Anthropic
            elif self.active_provider == LLMProvider.ANTHROPIC:
                return await self._generate_anthropic(prompt, system_prompt, temperature, messages)
            
            else:
                raise ValueError(f"Unsupported provider: {self.active_provider}")
                
        except Exception as e:
            logging.error(f"Error generating text with {self.active_provider} ({self.active_model}): {str(e)}")
            # Try a fallback if available
            fallback_providers = [p for p in self.get_available_providers() if p != self.active_provider]
            if fallback_providers:
                fallback = fallback_providers[0]
                logging.info(f"Trying fallback provider: {fallback}")
                old_provider = self.active_provider
                self.active_provider = fallback
                self.active_model = self.get_available_models()[0]
                try:
                    result = await self.generate_text(prompt, system_prompt, temperature, messages)
                    return result
                finally:
                    # Restore original provider
                    self.active_provider = old_provider
            
            # If no fallback or fallback failed
            raise
    
    async def _generate_openai(self, prompt: str, system_prompt: str, temperature: float, messages: List[Dict[str, str]] = None) -> str:
        """Generate text using OpenAI."""
        client = self.clients[LLMProvider.OPENAI]
        
        # If messages are provided, use them directly
        if messages:
            # Make sure we have a system message
            if not any(msg.get("role") == "system" for msg in messages):
                messages.insert(0, {"role": "system", "content": system_prompt})
                
            # Log the messages for debugging
            logging.info(f"Using {len(messages)} messages for OpenAI generation")
        else:
            # Create a simple system + user message pair
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model=self.active_model,
                messages=messages,
                temperature=temperature
            )
        )
        
        return response.choices[0].message.content.strip()
    
    async def _generate_anthropic(self, prompt: str, system_prompt: str, temperature: float, messages: List[Dict[str, str]] = None) -> str:
        """Generate text using Anthropic."""
        client = self.clients[LLMProvider.ANTHROPIC]
        
        # Anthropic has a different message format than OpenAI
        # It separates the system prompt from the messages
        
        # If messages are provided, convert them to Anthropic format
        if messages:
            # Extract system message if present
            system_messages = [msg for msg in messages if msg.get("role") == "system"]
            if system_messages:
                # Use the first system message
                system_prompt = system_messages[0]["content"]
            
            # Filter out system messages for Anthropic
            anthropic_messages = [msg for msg in messages if msg.get("role") != "system"]
            logging.info(f"Using {len(anthropic_messages)} messages for Anthropic generation")
        else:
            # Create a simple user message
            anthropic_messages = [{"role": "user", "content": prompt}]
        
        response = await asyncio.to_thread(
            lambda: client.messages.create(
                model=self.active_model,
                system=system_prompt,
                messages=anthropic_messages,
                temperature=temperature,
                max_tokens=4000  # Adding required max_tokens parameter
            )
        )
        
        return response.content[0].text
    
    def get_langchain_model(self):
        """Get a LangChain model for the active provider and model."""
        if self.active_provider == LLMProvider.OPENAI:
            return ChatOpenAI(model_name=self.active_model, temperature=0.7)
        elif self.active_provider == LLMProvider.ANTHROPIC:
            return ChatAnthropic(model_name=self.active_model, temperature=0.7)
        else:
            # Default to OpenAI if provider doesn't have a LangChain integration
            return ChatOpenAI(model_name=LLMModel.GPT35_TURBO, temperature=0.7)
