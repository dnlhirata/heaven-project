import random


def split_content(content: str, chuck_size: int = 10000) -> list[str]:
    return [content[i : i + chuck_size] for i in range(0, len(content), chuck_size)]


def get_random_chunk(content, chunk_size, token_limit):
    chunk_size = min(chunk_size, token_limit)

    max_start = max(0, len(content) - token_limit)

    start = random.randint(0, max_start)

    chunk = content[start : (start + chunk_size)]
    return chunk
