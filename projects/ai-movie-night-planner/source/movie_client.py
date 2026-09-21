"""Client for The Movie Database (TMDB) API.

The TMDB API requires a free API key.
"""

import os
from typing import Any
import requests
import time

_BASE_URL = os.environ.get("TMDB_API_BASE_URL", "https://api.themoviedb.org/3")
_DEFAULT_TIMEOUT = 30
_DEFAULT_LANGUAGE = "en-US"
_DEFAULT_REGION = "US"
_USER_AGENT = "(Databricks Movie App, contact@example.com)"

class TMDBClient:
    def __init__(self, api_key: str, base_url: str | None = None, timeout: int = _DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.base_url = (base_url or _BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": _USER_AGENT, "Accept": "application/json"})

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        params = params or {}
        params["api_key"] = self.api_key
        resp = self._session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def search_movies(self, query: str, page: int = 1, language: str = _DEFAULT_LANGUAGE, year: int | None = None) -> dict[str, Any]:
        params = {"query": query, "page": page, "language": language}
        if year: params["year"] = year
        return self.get("/search/movie", params=params)

    def get_movie_details(self, movie_id: int, language: str = _DEFAULT_LANGUAGE) -> dict[str, Any]:
        return self.get(f"/movie/{movie_id}", params={"language": language, "append_to_response": "credits,videos,reviews,images,keywords,recommendations,similar"})

    def get_streaming_providers(self, movie_id: int, region: str = _DEFAULT_REGION) -> dict[str, Any]:
        return self.get(f"/movie/{movie_id}/watch/providers", params={"watch_region": region})

    def get_person_details(self, person_id: int, language: str = _DEFAULT_LANGUAGE) -> dict[str, Any]:
        return self.get(f"/person/{person_id}", params={"language": language, "append_to_response": "movie_credits,tv_credits,images"})

    def search_person(self, query: str, page: int = 1, language: str = _DEFAULT_LANGUAGE) -> dict[str, Any]:
        return self.get("/search/person", params={"query": query, "page": page, "language": language})

    def discover_movies(self, page: int = 1, language: str = _DEFAULT_LANGUAGE, region: str | None = None, sort_by: str = "popularity.desc", year: int | None = None, with_genres: str | None = None, with_cast: str | None = None, with_crew: str | None = None, with_watch_providers: str | None = None, watch_region: str | None = None) -> dict[str, Any]:
        params={"page":page,"language":language,"sort_by":sort_by}
        for k,v in {"region":region,"year":year,"with_genres":with_genres,"with_cast":with_cast,"with_crew":with_crew,"with_watch_providers":with_watch_providers,"watch_region":watch_region}.items():
            if v is not None: params[k]=v
        return self.get("/discover/movie", params=params)

    def get_genres(self, language: str = _DEFAULT_LANGUAGE) -> dict[str, Any]:
        return self.get("/genre/movie/list", params={"language": language})

    def get_popular_movies(self, page: int = 1, language: str = _DEFAULT_LANGUAGE, region: str | None = None) -> dict[str, Any]:
        params={"page":page,"language":language}
        if region: params["region"]=region
        return self.get("/movie/popular", params=params)

    def get_trending_movies(self, time_window: str = "week", language: str = _DEFAULT_LANGUAGE) -> dict[str, Any]:
        return self.get(f"/trending/movie/{time_window}", params={"language": language})

    def get_now_playing(self, page: int = 1, language: str = _DEFAULT_LANGUAGE, region: str | None = None) -> dict[str, Any]:
        params={"page":page,"language":language}
        if region: params["region"]=region
        return self.get("/movie/now_playing", params=params)

    def fetch_movie_documents(self, movie_ids: list[int] | None = None, search_query: str | None = None, limit: int = 50, delay: float = 0.25) -> list[dict[str, Any]]:
        documents=[]; movies_to_fetch=[]
        if movie_ids: movies_to_fetch=[{"id":mid} for mid in movie_ids[:limit]]
        elif search_query: movies_to_fetch=self.search_movies(search_query).get("results",[])[:limit]
        else: movies_to_fetch=self.get_popular_movies().get("results",[])[:limit]
        for i,movie in enumerate(movies_to_fetch):
            movie_id=movie.get("id")
            try:
                details=self.get_movie_details(movie_id)
                genres=[g["name"] for g in details.get("genres",[])]
                cast=[{"id":p["id"],"name":p["name"],"character":p.get("character","")} for p in details.get("credits",{}).get("cast",[])[:10]]
                directors=[{"id":p["id"],"name":p["name"]} for p in details.get("credits",{}).get("crew",[]) if p.get("job")=="Director"]
                trailers=[{"key":v["key"],"site":v["site"],"type":v["type"],"name":v["name"]} for v in details.get("videos",{}).get("results",[]) if v.get("type") in ["Trailer","Teaser"] and v.get("site")=="YouTube"][:5]
                reviews=[{"author":r["author"],"content":r["content"][:500]} for r in details.get("reviews",{}).get("results",[])[:5]]
                narrative_text=f"{details.get('title','')}\n\nOverview: {details.get('overview','')}\n\nGenres: {', '.join(genres)}\nCast: {', '.join(c['name'] for c in cast)}\nDirector(s): {', '.join(d['name'] for d in directors)}\n"
                documents.append({"id":str(movie_id),"title":details.get("title",""),"original_title":details.get("original_title",""),"overview":details.get("overview",""),"tagline":details.get("tagline",""),"release_date":details.get("release_date"),"runtime":details.get("runtime"),"genres":genres,"cast":cast,"directors":directors,"trailers":trailers,"reviews":reviews,"vote_average":details.get("vote_average"),"vote_count":details.get("vote_count"),"popularity":details.get("popularity"),"poster_path":details.get("poster_path"),"backdrop_path":details.get("backdrop_path"),"narrative_text":narrative_text,"payload":details})
                if i < len(movies_to_fetch)-1: time.sleep(delay)
            except Exception as e:
                print(f"Error fetching movie {movie_id}: {e}")
        return documents
