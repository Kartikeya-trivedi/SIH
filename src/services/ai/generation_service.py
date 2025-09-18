import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pineconedb import PineconeDb
from agno.knowledge.embedder.mistral import MistralEmbedder
from google import genai
from google.genai import types

load_dotenv()

# --- System prompt ---
system_prompt = """
You are an AI assistant that specializes in retrieving knowledge from a Pinecone-powered knowledge base and using it to generate traditional Indian floor art illustrations, including Kolam, Rangoli, Phuhari, Thupka, and similar designs.

- When a user asks a question, first search the knowledge base for relevant information and use it to enhance your answer.
- Always provide a clear, text-based explanation of the design, including its cultural, regional, mathematical, or artistic significance if available.
- If the user requests a drawing, sketch, or image, convert the retrieved knowledge into a creative and descriptive text prompt for an image generation model (e.g., Imagen). 
- Make image prompts detailed, mentioning style, symmetry, colors, materials (chalk, rice, flower petals, powders, etc.), and any specific motifs or patterns where appropriate.
- Return both the explanatory text and the generated image to the user.
- If no relevant knowledge is found, fall back to a generic description of the requested art form and clearly mention that specific references were not available.
- Ensure that your answers cover all traditional designs, not just Kolam.
"""

# --- Pinecone setup ---
vector_db = PineconeDb(
    name="kolams",
    dimension=1024,
    metric="cosine",
    spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
    api_key=os.getenv("PINECONE_API_KEY"),
    use_hybrid_search=False,
    embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY"))
)
knowledge = Knowledge(vector_db=vector_db)

# --- Imagen client ---
client = genai.Client()


from io import BytesIO
import base64

def query_knowledge_and_generate(query: str, generate_image: bool = False):
    context = knowledge.search(query)
    explanation = f"Query: {query}\nContext: {context}\n\n{system_prompt}"

    image_base64 = None
    if generate_image:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=f"{query} + {context} + {system_prompt}",
            config=types.GenerateImagesConfig(number_of_images=1),
        )

        for generated_image in response.generated_images:
            # ✅ Use image_bytes instead of image.data
            image_bytes = generated_image.image.image_bytes
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return explanation, image_base64