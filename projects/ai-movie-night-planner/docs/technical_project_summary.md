# Technical Project Summary

## Architecture
1. TMDB supplies movie metadata, cast/crew, trailers, reviews and provider data.
2. The Flask Databricks App syncs movie documents into Lakebase/PostgreSQL.
3. Sentence Transformers (all-MiniLM-L6-v2) creates embeddings.
4. Embeddings are stored in pgvector tables with HNSW indexes.
5. Natural-language queries are embedded and compared using cosine distance.
6. Results return movie metadata, relevant text chunks and similarity values.
7. An MCP server exposes movie and vector-search tools for MCP-compatible agent workflows.

## Technologies
Databricks Apps, Databricks SDK, Flask, Lakebase/PostgreSQL, pgvector, Python, SQL, TMDB API, Sentence Transformers, FastMCP/MCP, SQLAlchemy, psycopg2, Pandas and PyTorch.

## Accuracy note
The reviewed source imports the OpenAI SDK and defines an LLM model environment variable, but the main Flask path demonstrates semantic/vector search and MCP tool integration. The project documentation therefore does not claim an LLM inference pipeline that is not clearly implemented in the reviewed source.
