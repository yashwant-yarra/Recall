from google import genai
from google.genai import types
from recall.config import settings

def make_genai_client() -> genai.Client:
    return genai.Client(vertexai=True, project=settings.google_cloud_project,
                        location=settings.vertex_location)

async def embed(client: genai.Client, texts: list[str],
                task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    vectors = []
    for text in texts:  # Vertex: one input per request
        resp = await client.aio.models.embed_content(
            model=settings.embed_model,
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type,
                                            output_dimensionality=settings.embed_dims),
        )
        vectors.append(resp.embeddings[0].values)
    return vectors