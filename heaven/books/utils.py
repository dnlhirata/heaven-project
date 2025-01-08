def split_content(content: str, chuck_size: int = 10000) -> list[str]:
    return [content[i:i + chuck_size] for i in range(0, len(content), chuck_size)]