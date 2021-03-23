import re


def scrapbox_to_markdown(text: str) -> str:
    replace_patterns = [
        {'name': 'heading1', 'scrapbox': r'\t*\[#*\*{3,}#* (.+)]', 'markdown': r'# \1'},
        {'name': 'heading2', 'scrapbox': r'\t*\[#*\*{2}#* (.+)]', 'markdown': r'## \1'},
        {'name': 'heading3', 'scrapbox': r'\t*\[#*\*{1}#* (.+)]', 'markdown': r'### \1'},
        {'name': 'image', 'scrapbox': r'\[([^\s]*[png|jpeg|jpg|bmp|svg|gif])\]', 'markdown': r'![image](\1)'},
        {'name': 'link', 'scrapbox': r'\[([^ ]*) (http.+)\]', 'markdown': r'[\1](\2)'},
        {'name': 'list', 'scrapbox': r'^\t(\t*)(.*)', 'markdown': r'\1- \2'},
        {'name': 'italic', 'scrapbox': r'\[\/ ([^\]]+)]', 'markdown': r'_\1_'},
        {'name': 'strike', 'scrapbox': r'\[- ([^\]]+)]', 'markdown': r'~~\1~~'}
    ]
    for replace_pattern in replace_patterns:
        text = re.sub(
            replace_pattern['scrapbox'],
            replace_pattern['markdown'],
            text
        )
    return text
