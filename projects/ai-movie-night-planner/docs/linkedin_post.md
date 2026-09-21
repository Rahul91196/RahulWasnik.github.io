# LinkedIn Post

🎬 **I built an AI Movie Night Planner on Databricks**

I wanted to explore what happens when a traditional data pipeline is combined with semantic search and agent-ready tools — so I built a movie discovery application that understands natural-language movie preferences.

### What I built
- Pulls movie data from TMDB
- Stores movie documents and watchlists in Databricks Lakebase / PostgreSQL
- Generates embeddings with sentence-transformers/all-MiniLM-L6-v2
- Uses pgvector for semantic similarity search
- Supports natural-language movie discovery
- Provides personalized watchlists
- Exposes movie capabilities through an MCP server for agent-based workflows
- Runs as a Databricks App

### Architecture
User → Databricks App → Lakebase / pgvector → Semantic Search
                    ↘ TMDB API
                    ↘ MCP tools / agent workflow

### What I learned
This project gave me hands-on experience at the intersection of **Data Engineering + Vector Search + Databricks + AI/Agent Workflows**.

The next area I would explore is improving the recommendation layer with stronger ranking and preference-aware planning.

#Databricks #DataEngineering #GenerativeAI #AI #VectorSearch #MCP #Python #SQL #Lakebase #PostgreSQL #DataAnalytics
