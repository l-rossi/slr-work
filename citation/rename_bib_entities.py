import re


def rename_bib_entries(input_bib, output_bib, offset=0):
    with open(input_bib, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Pattern: match @type{old_key,
    entry_pattern = re.compile(r'@(\w+)\s*{\s*([^,]+)\s*,', re.IGNORECASE)

    entries = list(entry_pattern.finditer(content))
    new_content = content
    position = 0

    for i, match in enumerate(entries, offset + 1):
        old_key = match.group(2)
        new_key = f"PS_{i:04d}"

        start, end = match.span(2)
        # Adjust for previously inserted characters
        start += position
        end += position

        new_content = new_content[:start] + new_key + new_content[end:]
        position += len(new_key) - len(old_key)

    with open(output_bib, 'w', encoding='utf-8') as outfile:
        outfile.write(new_content)


if __name__ == "__main__":
    # Removed PS313 as duplicate
    input_bib_path = "./data/citation_data/acm.bib"  # Replace with your original .bib file
    output_bib_path = "./data/citation_data/acm_normalized.bib"
    rename_bib_entries(input_bib_path, output_bib_path, offset=0)
