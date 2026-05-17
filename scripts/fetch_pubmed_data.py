#!/usr/bin/env python3
"""
PubMed Data Fetcher for AI Healthcare Assistant.
Uses NCBI Entrez E-utilities to pull abstracts and save them as YAML for the RAG pipeline.
"""

import asyncio
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

import httpx
import yaml

# Configuration
NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
SEARCH_TERMS = [
    "fever management in children",
    "common cold symptoms and treatment",
    "headache types and management",
    "gastroenteritis guidelines",
    "fracture first aid",
    "respiratory infection symptoms"
]
MAX_RESULTS_PER_TERM = 5
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "pubmed"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

async def fetch_pubmed_ids(client: httpx.AsyncClient, term: str) -> List[str]:
    """Search for PubMed IDs matching a search term."""
    params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "retmax": MAX_RESULTS_PER_TERM
    }
    try:
        response = await client.get(f"{NCBI_BASE_URL}/esearch.fcgi", params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        logger.error(f"Error searching PubMed for '{term}': {e}")
        return []

async def fetch_pubmed_abstracts(client: httpx.AsyncClient, pmids: List[str]) -> str:
    """Fetch full XML details for a list of PubMed IDs."""
    if not pmids:
        return ""
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    try:
        response = await client.get(f"{NCBI_BASE_URL}/efetch.fcgi", params=params)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching abstracts for PMIDs {pmids}: {e}")
        return ""

def parse_pubmed_xml(xml_content: str, topic: str = "Medical Literature") -> List[Dict[str, Any]]:
    """Parse PubMed XML and extract metadata and abstracts."""
    if not xml_content:
        return []
    
    root = ET.fromstring(xml_content)
    articles = []
    
    for article_tag in root.findall(".//PubmedArticle"):
        try:
            # Basic metadata with safety checks
            pmid_el = article_tag.find(".//PMID")
            title_el = article_tag.find(".//ArticleTitle")
            
            if pmid_el is None or title_el is None:
                logger.warning("Skipping article with missing PMID or title")
                continue
                
            pmid = pmid_el.text
            title = title_el.text
            
            # Abstract extraction (handling multiple parts)
            abstract_parts = article_tag.findall(".//AbstractText")
            abstract = " ".join([part.text for part in abstract_parts if part.text])
            
            # Author extraction
            authors = []
            for author in article_tag.findall(".//Author"):
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")
            
            # Date extraction
            pub_date = article_tag.find(".//PubDate/Year")
            year = pub_date.text if pub_date is not None else "Unknown"

            articles.append({
                "title": title,
                "content": abstract,
                "metadata": {
                    "source": "pubmed",
                    "pmid": pmid,
                    "authors": authors,
                    "year": year,
                    "topic": topic,
                    "type": "medical_abstract"
                }
            })
        except Exception as e:
            logger.warning(f"Failed to parse an article: {e}")
            continue
            
    return articles

async def main():
    logger.info(f"Ensuring output directory exists: {OUTPUT_DIR}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        all_articles = []
        
        for term in SEARCH_TERMS:
            logger.info(f"Searching for term: {term}")
            pmids = await fetch_pubmed_ids(client, term)
            
            # Rate limiting fix: NCBI Entrez API allows 3 requests/sec without an API key.
            # Add a small delay to avoid "429 Too Many Requests" errors.
            await asyncio.sleep(1.0)
            
            if pmids:
                logger.info(f"Found {len(pmids)} PMIDs. Fetching details...")
                xml_content = await fetch_pubmed_abstracts(client, pmids)
                articles = parse_pubmed_xml(xml_content, topic=term)
                all_articles.extend(articles)
                
                # Additional delay after fetching abstracts
                await asyncio.sleep(1.0)
        
        if all_articles:
            # Save all findings as one medical knowledge YAML file
            output_file = OUTPUT_DIR / "pubmed_knowledge.yml"
            with open(output_file, "w", encoding="utf-8") as f:
                yaml.dump(all_articles, f, sort_keys=False, allow_unicode=True)
            logger.info(f"Successfully saved {len(all_articles)} medical abstracts to {output_file}")
        else:
            logger.warning("No medical articles were found or parsed.")

if __name__ == "__main__":
    asyncio.run(main())
