def format_text(text: str) -> str:
    lines = text.split('\n')
    formatted_text = '\n\n'.join([f'- {line.strip()}' for line in lines])
    return formatted_text



