import random
from collections import defaultdict

from rdflib import Graph, Namespace


def split_content(content: str, chuck_size: int = 10000) -> list[str]:
    return [content[i : i + chuck_size] for i in range(0, len(content), chuck_size)]


def get_random_chunk(content, chunk_size, token_limit):
    chunk_size = min(chunk_size, token_limit)

    max_start = max(0, len(content) - token_limit)

    start = random.randint(0, max_start)

    chunk = content[start : (start + chunk_size)]
    return chunk


def parse_rdf_metadata(metadata: str) -> dict:
    graph = Graph()
    graph.parse(data=metadata, format="xml")

    PGTERMS = Namespace("http://www.gutenberg.org/2009/pgterms/")
    DCTERMS = Namespace("http://purl.org/dc/terms/")
    RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    metadata = defaultdict(str)
    for _, p, o in graph:
        if p == DCTERMS.title:
            metadata["title"] = str(o)
        elif p == PGTERMS.name:
            metadata["author"] = str(o)
        elif p == DCTERMS.language:
            for _, _, lang_o in graph.triples((o, RDF.value, None)):
                metadata["language"] = str(lang_o)

    return metadata
