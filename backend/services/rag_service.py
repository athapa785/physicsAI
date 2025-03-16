"""
RAG (Retrieval Augmented Generation) service for physics content retrieval and lesson generation.
"""

from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
import json
from typing import List, Dict, Tuple
from openai import OpenAI
import asyncio
import numpy as np
import faiss
import hashlib
import pickle
from typing import Dict, List, Tuple, Any

# Load environment variables
load_dotenv()

class PhysicsRAG:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI client with better error handling
        self.openai_client = None
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key.startswith("sk-"):
            try:
                self.openai_client = OpenAI(api_key=api_key)
                print("Successfully initialized OpenAI client with API key")
            except Exception as e:
                print(f"Error initializing OpenAI client: {str(e)}")
                self.openai_client = None
        else:
            print("Warning: No valid OpenAI API key found. RAG functionality will be limited.")
            
        # Load book structure
        self.book_structure = self.load_book_structure()
        
        # Initialize vector store
        self.vector_store_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'vector_store')
        os.makedirs(self.vector_store_dir, exist_ok=True)
        
        # Content directory
        self.content_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'physics_content')
        
        # Initialize vector store
        self.index = None
        self.documents = []
        self.document_embeddings = []
        
        # Load or create vector store
        try:
            self.load_or_create_vector_store()
        except Exception as e:
            import logging
            logging.error(f"Error initializing vector store: {str(e)}")
            
    def compute_content_hash(self) -> str:
        """Compute a hash of all content files to detect changes."""
        import logging
        
        if not os.path.exists(self.content_dir):
            logging.warning(f"Content directory not found: {self.content_dir}")
            return ""
        
        hash_md5 = hashlib.md5()
        
        # Get all files and sort them for consistent hashing
        all_files = []
        for chapter_dir in os.listdir(self.content_dir):
            chapter_path = os.path.join(self.content_dir, chapter_dir)
            if os.path.isdir(chapter_path):
                for file in os.listdir(chapter_path):
                    if file.endswith('.txt'):
                        all_files.append(os.path.join(chapter_path, file))
        
        all_files.sort()
        
        # Compute hash of all file contents
        for file_path in all_files:
            try:
                with open(file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
            except Exception as e:
                logging.error(f"Error hashing file {file_path}: {str(e)}")
        
        return hash_md5.hexdigest()
    
    def load_or_create_vector_store(self):
        """Load the vector store from disk or create it if it doesn't exist or content has changed."""
        import logging
        
        # Compute content hash
        content_hash = self.compute_content_hash()
        if not content_hash:
            logging.warning("Could not compute content hash, will create new vector store")
        
        # Check if vector store exists and has the same content hash
        hash_file = os.path.join(self.vector_store_dir, 'content_hash.txt')
        index_file = os.path.join(self.vector_store_dir, 'faiss_index.bin')
        docs_file = os.path.join(self.vector_store_dir, 'documents.pkl')
        
        if os.path.exists(hash_file) and os.path.exists(index_file) and os.path.exists(docs_file):
            try:
                with open(hash_file, 'r') as f:
                    stored_hash = f.read().strip()
                
                if stored_hash == content_hash:
                    logging.info("Content unchanged, loading vector store from disk")
                    # Load index
                    self.index = faiss.read_index(index_file)
                    # Load documents
                    with open(docs_file, 'rb') as f:
                        self.documents = pickle.load(f)
                    
                    logging.info(f"Loaded vector store with {len(self.documents)} documents")
                    return
                else:
                    logging.info("Content changed, creating new vector store")
            except Exception as e:
                logging.error(f"Error loading vector store: {str(e)}")
        else:
            logging.info("Vector store not found, creating new one")
        
        # Create new vector store
        self.create_vector_store()
        
        # Save content hash
        with open(hash_file, 'w') as f:
            f.write(content_hash)
        
        logging.info("Vector store created and saved successfully")
    
    def create_vector_store(self):
        """Create a new vector store from the physics content."""
        import logging
        
        if not os.path.exists(self.content_dir):
            logging.error(f"Content directory not found: {self.content_dir}")
            return
        
        # Clear existing data
        self.documents = []
        self.document_embeddings = []
        
        # Process all files
        for chapter_dir in os.listdir(self.content_dir):
            chapter_path = os.path.join(self.content_dir, chapter_dir)
            if os.path.isdir(chapter_path):
                chapter_name = chapter_dir.replace('_', ' ')
                
                for file in os.listdir(chapter_path):
                    if file.endswith('.txt'):
                        file_path = os.path.join(chapter_path, file)
                        topic_name = file.replace('.txt', '').replace('_', ' ')
                        
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                
                                # Store document with metadata
                                doc = {
                                    'content': content,
                                    'chapter': chapter_name,
                                    'topic': topic_name,
                                    'path': file_path
                                }
                                
                                self.documents.append(doc)
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {str(e)}")
        
        if not self.documents:
            logging.warning("No documents found to index")
            return
        
        # Generate embeddings
        logging.info(f"Generating embeddings for {len(self.documents)} documents")
        self.document_embeddings = self.generate_embeddings([doc['content'] for doc in self.documents])
        
        # Create FAISS index
        dimension = len(self.document_embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        embeddings_array = np.array(self.document_embeddings).astype('float32')
        self.index.add(embeddings_array)
        
        # Save index and documents
        faiss.write_index(self.index, os.path.join(self.vector_store_dir, 'faiss_index.bin'))
        with open(os.path.join(self.vector_store_dir, 'documents.pkl'), 'wb') as f:
            pickle.dump(self.documents, f)
        
    def load_book_structure(self) -> Dict:
        """Load the book structure from the physics content directory."""
        if not hasattr(self, 'book_structure'):
            chapters = []
            chapter_mapping = {
                'mechanics': {'number': 1, 'title': 'Mechanics'},
                'thermodynamics': {'number': 2, 'title': 'Thermodynamics'},
                'waves_oscillations': {'number': 3, 'title': 'Waves and Oscillations'},
                'electromagnetism': {'number': 4, 'title': 'Electromagnetism'}
            }
            
            content_dir = os.path.join(os.path.dirname(__file__), "..", "data", "physics_content")
            
            # Get chapters from directory structure
            for chapter_dir in sorted(os.listdir(content_dir)):
                if os.path.isdir(os.path.join(content_dir, chapter_dir)) and chapter_dir in chapter_mapping:
                    chapter_info = chapter_mapping[chapter_dir]
                    topics = []
                    
                    # Get topics from files in chapter directory
                    for file in os.listdir(os.path.join(content_dir, chapter_dir)):
                        if file.endswith('.txt'):
                            topic_name = ' '.join(file.replace('.txt', '').split('_')).title()
                            topics.append(topic_name)
                    
                    chapters.append({
                        'number': chapter_info['number'],
                        'title': chapter_info['title'],
                        'topics': sorted(topics)
                    })
            
            self.book_structure = {'chapters': sorted(chapters, key=lambda x: x['number'])}
        
        return self.book_structure
    
    def get_chapters(self) -> List[Dict]:
        """Get all chapters from the book."""
        structure = self.load_book_structure()
        return structure['chapters']
    
    def get_topics(self, chapter_number: int) -> List[str]:
        """Get topics for a specific chapter."""
        structure = self.load_book_structure()
        for chapter in structure['chapters']:
            if chapter['number'] == chapter_number:
                return chapter['topics']
        return []
    
    async def generate_lesson(self, topic: str) -> str:
        """Generate a concise lesson for a specific topic asynchronously."""
        # Check if OpenAI client is available
        if not self.openai_client:
            # Try to initialize with the current environment variable
            if os.getenv("OPENAI_API_KEY"):
                self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            else:
                return "I'm sorry, I need an OpenAI API key to generate lessons. Please provide one in the settings."
        
        prompt = f"Create a brief physics lesson about {topic}. Include:\n1. One key concept\n2. One important formula with LaTeX formatting\n3. A simple example\nKeep it under 200 words."
        
        try:
            response = await asyncio.to_thread(
                lambda: self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "You are a knowledgeable physics professor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
            )
            lesson = response.choices[0].message.content.strip()
            return lesson
        except Exception as e:
            import logging
            logging.error(f"Error generating lesson with RAG: {str(e)}")
            return f"I'm sorry, I encountered an error while generating a lesson about {topic}. Please try again later."
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using OpenAI's embeddings API."""
        import logging
        
        if not self.openai_client:
            logging.error("OpenAI client not initialized")
            return [[0.0] * 1536] * len(texts)  # Return dummy embeddings
        
        embeddings = []
        
        # Process in batches to avoid rate limits
        batch_size = 10
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                logging.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
            except Exception as e:
                logging.error(f"Error generating embeddings: {str(e)}")
                # Add dummy embeddings for this batch
                embeddings.extend([[0.0] * 1536] * len(batch))
        
        return embeddings
    
    def get_content_for_topic(self, topic: str) -> str:
        """Retrieve the content for a specific topic using the FAISS vector store."""
        import logging
        logging.info(f"Retrieving content for topic: {topic}")
        
        # Check if vector store is initialized
        if self.index is None or not self.documents:
            logging.warning("Vector store not initialized, falling back to direct search")
            return self.get_content_for_topic_direct(topic)
        
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embeddings([topic])[0]
            query_embedding_array = np.array([query_embedding]).astype('float32')
            
            # Search the index
            k = min(3, len(self.documents))  # Get top 3 matches or all if less than 3
            distances, indices = self.index.search(query_embedding_array, k)
            
            # Check if we got any results
            if len(indices[0]) == 0:
                logging.warning(f"No matches found in vector store for topic: {topic}")
                return self.get_content_for_topic_direct(topic)
            
            # Get the best matching document
            best_index = indices[0][0]
            best_doc = self.documents[best_index]
            
            logging.info(f"Best vector match: {best_doc['path']} (distance: {distances[0][0]})")
            
            # If the match is too distant, fall back to direct search
            if distances[0][0] > 0.8:
                logging.warning(f"Vector match too distant ({distances[0][0]}), falling back to direct search")
                direct_content = self.get_content_for_topic_direct(topic)
                if direct_content:
                    return direct_content
            
            # Combine top results if they're from the same chapter
            combined_content = best_doc['content']
            chapter = best_doc['chapter']
            
            for i in range(1, len(indices[0])):
                idx = indices[0][i]
                doc = self.documents[idx]
                if doc['chapter'] == chapter and distances[0][i] < 0.7:  # Only include if reasonably close
                    combined_content += "\n\n" + doc['content']
                    logging.info(f"Adding related content from: {doc['path']}")
            
            return combined_content
            
        except Exception as e:
            logging.error(f"Error searching vector store: {str(e)}")
            return self.get_content_for_topic_direct(topic)
    
    def get_content_for_topic_direct(self, topic: str) -> str:
        """Fallback method to retrieve content directly from files."""
        import logging
        logging.info(f"Using direct search for topic: {topic}")
        
        # Normalize topic for matching
        topic_lower = topic.lower().strip()
        topic_words = set(topic_lower.split())
        
        if not os.path.exists(self.content_dir):
            logging.error(f"Physics content directory not found: {self.content_dir}")
            return ""
        
        # Track best matches with scores
        best_matches = []
        
        # Special case for pendulum questions
        pendulum_related = False
        if 'pendulum' in topic_lower or 'oscillation' in topic_lower or 'harmonic motion' in topic_lower:
            pendulum_related = True
            logging.info("Detected pendulum-related topic, will prioritize pendulum content")
        
        # Look for matches in filenames
        for chapter_dir in os.listdir(self.content_dir):
            chapter_path = os.path.join(self.content_dir, chapter_dir)
            if os.path.isdir(chapter_path):
                chapter_name = chapter_dir.replace('_', ' ').lower()
                
                for file in os.listdir(chapter_path):
                    if file.endswith('.txt'):
                        file_path = os.path.join(chapter_path, file)
                        file_topic = file.replace('.txt', '').replace('_', ' ').lower()
                        
                        # Calculate match score
                        score = 0
                        
                        # Boost pendulum content for pendulum-related questions
                        if pendulum_related and ('pendulum' in file_topic):
                            score += 50  # Significant boost for pendulum files
                        
                        # Direct topic matches
                        if topic_lower == file_topic:
                            score = 100  # Exact match
                        elif topic_lower in file_topic:
                            score = 80   # Topic is substring of filename
                        elif file_topic in topic_lower:
                            score = 70   # Filename is substring of topic
                        
                        # Word-level matches
                        file_words = set(file_topic.split())
                        common_words = topic_words.intersection(file_words)
                        if common_words:
                            score = max(score, len(common_words) * 20)
                        
                        # Chapter relevance
                        if any(word in chapter_name for word in topic_words):
                            score += 15
                        
                        if score > 0:
                            try:
                                with open(file_path, 'r') as f:
                                    content = f.read()
                                    # Check content for topic mentions
                                    if topic_lower in content.lower():
                                        score += 25
                                    
                                    best_matches.append((score, content, file_path))
                            except Exception as e:
                                logging.error(f"Error reading file {file_path}: {str(e)}")
        
        # Sort matches by score (highest first)
        best_matches.sort(reverse=True, key=lambda x: x[0])
        
        # Return best match if we have one
        if best_matches and best_matches[0][0] >= 20:
            logging.info(f"Best direct match: {best_matches[0][2]} with score {best_matches[0][0]}")
            return best_matches[0][1]
        
        # If no good matches, try content-based search
        content_matches = []
        
        for chapter_dir in os.listdir(self.content_dir):
            chapter_path = os.path.join(self.content_dir, chapter_dir)
            if os.path.isdir(chapter_path):
                for file in os.listdir(chapter_path):
                    if file.endswith('.txt'):
                        file_path = os.path.join(chapter_path, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read().lower()
                                content_score = 0
                                
                                # Check for topic words in content
                                for word in topic_words:
                                    if len(word) > 3 and word in content:
                                        content_score += 10
                                
                                if content_score > 0:
                                    content_matches.append((content_score, content.replace(content.lower(), content), file_path))
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {str(e)}")
        
        # Sort content matches
        content_matches.sort(reverse=True, key=lambda x: x[0])
        
        # Return best content match if we have one
        if content_matches:
            logging.info(f"Best content match: {content_matches[0][2]} with score {content_matches[0][0]}")
            return content_matches[0][1]
        
        logging.warning(f"No content found for topic: {topic}")
        return ""
    
    async def answer_question(self, question: str, topic: str, chat_history: List[Tuple[str, str]], provider=None, model=None) -> str:
        """Answer a question about a specific topic using RAG.
        
        Args:
            question: The question to answer
            topic: The topic the question is about
            chat_history: Previous conversation history
            provider: Optional provider to use for generating the answer
            model: Optional model to use for generating the answer
            
        Returns:
            The answer to the question
        """
        import logging
        logging.info(f"RAG service answering question: '{question}' about topic: '{topic}'")
        
        try:
            # Check if any API key is available for the specified provider
            if provider is None:
                return "⚠️ Error: No LLM provider specified. Please select a provider in the sidebar."
            
            # For embeddings, we still need OpenAI API key, but for answering we can use any provider
            api_key = os.getenv("OPENAI_API_KEY")
            
            # Initialize OpenAI client for embeddings if not already initialized
            if not self.openai_client and api_key and api_key.startswith("sk-"):
                try:
                    print(f"Initializing OpenAI client with API key: {api_key[:5]}...")
                    self.openai_client = OpenAI(api_key=api_key)
                except Exception as e:
                    print(f"Error initializing OpenAI client: {str(e)}")
                    # We'll continue anyway since we might be able to use direct content retrieval
            
            # Get relevant content for the topic
            context = self.get_content_for_topic(topic)
            
            if not context:
                logging.warning(f"No context found for topic: {topic}. Using general knowledge.")
                # Fallback if no context is found
                prompt = f"""Answer this physics question about {topic}: {question}
                
                Provide a clear and educational explanation, using LaTeX for any mathematical formulas.
                If you need to include equations, use proper LaTeX notation with $ for inline equations and $$ for display equations.
                """
                system_prompt = "You are a knowledgeable physics professor helping a student understand concepts."
            else:
                logging.info(f"Found context for topic: {topic}. Using RAG approach.")
                
                # Check if the question is referring to a specific problem or example in the lesson
                import re
                
                # Check for problem references
                problem_reference = re.search(r'problem\s*(\d+)', question.lower())
                example_reference = re.search(r'example\s*(\d+)', question.lower())
                
                reference_type = None
                reference_num = None
                
                if problem_reference:
                    reference_type = "Problem"
                    reference_num = problem_reference.group(1)
                    print(f"Detected reference to Problem {reference_num}")
                elif example_reference:
                    reference_type = "Example"
                    reference_num = example_reference.group(1)
                    print(f"Detected reference to Example {reference_num}")
                
                # Special case for pendulum example
                pendulum_example = False
                if reference_type == "Example" and reference_num == "2" and "pendulum" in context.lower():
                    pendulum_example = True
                    print("Detected reference to pendulum example")
                
                if reference_type and reference_num:
                    # Try different patterns to extract the specific problem/example and its solution
                    patterns = [
                        # Standard format with explicit Solution marker
                        rf"{reference_type}\s*{reference_num}[\s\S]*?Solution:[\s\S]*?(?={reference_type}\s*\d+|$)",
                        # Format with Example instead of Problem
                        rf"Example\s*{reference_num}[\s\S]*?Solution:[\s\S]*?(?=Example\s*\d+|Problem\s*\d+|$)",
                        # Without explicit Solution marker
                        rf"{reference_type}\s*{reference_num}[\s\S]*?(?={reference_type}\s*\d+|Example\s*\d+|Problem\s*\d+|$)",
                        # With optional colon
                        rf"{reference_type}\s*{reference_num}:?[\s\S]*?(?={reference_type}\s*\d+|Example\s*\d+|Problem\s*\d+|$)"
                    ]
                    
                    # Special pattern for pendulum example
                    if pendulum_example:
                        patterns.insert(0, r"A pendulum swings with an amplitude[\s\S]*?maximum displacement in the opposite direction\.")
                    
                    problem_match = None
                    for pattern in patterns:
                        match = re.search(pattern, context, re.IGNORECASE)
                        if match:
                            problem_match = match
                            print(f"Found {reference_type} {reference_num} using pattern: {pattern}")
                            break
                    
                    if problem_match:
                        specific_context = problem_match.group(0)
                        print(f"Found specific {reference_type} {reference_num} in the context")
                        
                        # Construct a prompt specifically for explaining a problem or example
                        prompt = f"""The student is asking about {reference_type} {reference_num} from the lesson on {topic}.
                        
                        Here is the {reference_type.lower()} and solution from the reference material:
                        {specific_context}
                        
                        Student question: {question}
                        
                        Explain this {reference_type.lower()} and its solution in detail, making sure to:
                        1. Break down each step of the solution
                        2. Explain the physics concepts involved
                        3. Clarify any formulas used and what each variable represents
                        4. Use LaTeX for all mathematical formulas
                        
                        Base your answer strictly on the reference material provided.
                        """
                        system_prompt = f"You are a knowledgeable physics professor helping a student understand specific {reference_type.lower()}s. Focus on explaining the {reference_type.lower()} and solution in detail."
                    else:
                        print(f"Could not find specific {reference_type} {reference_num}, using full context")
                        # Use the regular RAG approach with full context
                        prompt = f"""Answer this physics question about {topic}: {question}
                        
                        Use the following reference material to help formulate your answer:
                        
                        {context}
                        
                        The student is asking about {reference_type} {reference_num}, so try to identify this {reference_type.lower()} in the reference material.
                        Provide a clear and educational explanation, using LaTeX for any mathematical formulas.
                        If you need to include equations, use proper LaTeX notation with $ for inline equations and $$ for display equations.
                        Base your answer on the reference material provided, but feel free to expand if needed.
                        """
                        system_prompt = "You are a knowledgeable physics professor helping a student understand concepts. Always provide accurate information based on the reference material."
                else:
                    # Regular question not referring to a specific problem
                    prompt = f"""Answer this physics question about {topic}: {question}
                    
                    Use the following reference material to help formulate your answer:
                    
                    {context}
                    
                    Provide a clear and educational explanation, using LaTeX for any mathematical formulas.
                    If you need to include equations, use proper LaTeX notation with $ for inline equations and $$ for display equations.
                    Base your answer on the reference material provided, but feel free to expand if needed.
                    """
                    system_prompt = "You are a knowledgeable physics professor helping a student understand concepts. Always provide accurate information based on the reference material."
            
            # Prepare messages for the chat API
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add chat history if available
            if chat_history and len(chat_history) > 0:
                logging.info(f"Including {len(chat_history)} previous exchanges in chat history")
                for user_msg, assistant_msg in chat_history:
                    # Add the raw user message without the context
                    messages.append({"role": "user", "content": user_msg})
                    messages.append({"role": "assistant", "content": assistant_msg})
            
            # Add the current question with context as a separate message
            # This ensures the LLM sees both the raw chat history and the current question with context
            messages.append({"role": "user", "content": prompt})
            
            # Use the multi_llm_service to generate the answer with the provided provider and model
            from backend.services.multi_llm_service import MultiLLMService, LLMProvider
            
            logging.info(f"Using {provider} provider for question answering")
            
            try:
                # Initialize the multi LLM service
                llm_service = MultiLLMService()
                
                # Generate the answer using the specified provider and model
                if provider and model:
                    # Set the active provider and model
                    llm_service.set_active_provider(provider)
                    llm_service.set_active_model(model)
                    
                    # Pass the full messages array to the LLM service
                    # This ensures all chat history and context is preserved
                    answer = await llm_service.generate_text(
                        prompt="",  # Not needed when passing messages directly
                        system_prompt="",  # Not needed when passing messages directly
                        temperature=0.7,
                        messages=messages  # Pass the complete messages array
                    )
                    
                    logging.info(f"Successfully generated answer with {provider}")
                    return answer
                elif self.openai_client:
                    # Fallback to OpenAI if no provider specified but OpenAI client is available
                    logging.info("Using OpenAI for question answering")
                    response = await asyncio.to_thread(
                        lambda: self.openai_client.chat.completions.create(
                            model="gpt-4",  # Using gpt-4 instead of gpt-4-turbo for better stability
                            messages=messages,
                            temperature=0.7
                        )
                    )
                    answer = response.choices[0].message.content.strip()
                    logging.info("Successfully generated answer with OpenAI")
                    return answer
                else:
                    return "⚠️ Error: No LLM provider available. Please provide an API key for at least one provider in the settings panel."    
            except Exception as api_error:
                logging.error(f"LLM API error: {str(api_error)}")
                
                # Try with OpenAI as fallback if it's available and not the original provider
                if provider != "openai" and self.openai_client:
                    try:
                        logging.info("Trying fallback to OpenAI gpt-3.5-turbo model")
                        response = await asyncio.to_thread(
                            lambda: self.openai_client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=messages,
                                temperature=0.7
                            )
                        )
                        answer = response.choices[0].message.content.strip()
                        logging.info("Successfully generated answer with OpenAI fallback")
                        return answer
                    except Exception as fallback_error:
                        logging.error(f"OpenAI fallback error: {str(fallback_error)}")
                        raise fallback_error
                else:
                    raise api_error
        except Exception as e:
            logging.error(f"Error answering question with RAG: {str(e)}")
            return f"I'm sorry, I encountered an error while answering your question: {str(e)}. Please check your API key and try again."
