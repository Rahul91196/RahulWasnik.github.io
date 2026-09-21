# 🎬 AI Movie Night Planner — Databricks

An end-to-end movie discovery and planning application built as a Databricks App.

## What it does
- Pulls movie metadata from TMDB
- Stores movie documents and user watchlists in Lakebase/PostgreSQL
- Generates embeddings using sentence-transformers/all-MiniLM-L6-v2
- Stores vectors in PostgreSQL/pgvector
- Performs natural-language semantic movie search
- Supports personalized watchlists
- Exposes movie discovery, details, streaming providers, watchlist and vector-search tools through MCP
- Runs as a Databricks App

## Architecture
User → Databricks App → Lakebase / pgvector → Semantic Search
                     ↘ TMDB API
                     ↘ MCP tools / agent workflow

## Main components
- Flask application and REST API
- Databricks-managed Lakebase/PostgreSQL
- TMDB API integration
- Sentence Transformers embeddings
- pgvector similarity search
- MCP server for agent-ready movie tools
- Databricks Asset Bundle configuration

## API capabilities
/healthz, /movies, /movies/sync, /movies/search, /api/vector-lookup, /watchlist

## MCP tools
search_movies, get_movie_details, get_streaming_providers, get_trending_movies, get_watchlist, add_to_watchlist, remove_from_watchlist, get_current_user, vector_search

## Security
No real credentials are included. Use Databricks secret scopes and the provided environment template for local development.

> Project source package and supporting documentation are maintained with this project branch.
