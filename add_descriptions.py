import os
import re
from pathlib import Path

def add_descriptions_to_posts(posts_dir):
    """
    Adds a 'description' field to the front matter of Markdown posts if it's missing.
    The description is generated from the first 160 characters of the post's content.
    """
    for filepath in Path(posts_dir).rglob('*.md'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple front matter and body extraction
            parts = content.split('---', 2)
            if len(parts) < 3:
                print(f"Skipping {filepath}: Not a valid front matter format.")
                continue

            front_matter_str = parts[1]
            body = parts[2].strip()

            # Check if description exists
            if 'description:' in front_matter_str:
                continue

            # Create description
            # Remove markdown and newlines for a cleaner description
            clean_body = re.sub(r'#+\s*', '', body)  # Remove headers
            clean_body = re.sub(r'!?\[.*?\]\(.*?\)', '', clean_body) # Remove links and images
            clean_body = clean_body.replace('\n', ' ')
            description = (clean_body[:157] + '...') if len(clean_body) > 160 else clean_body

            # Add description to front matter
            new_front_matter_str = front_matter_str.strip() + f'\ndescription: "{description}"\n'
            
            # Write back to file
            new_content = f'---\n{new_front_matter_str}---\n{body}'
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Added description to {filepath}")

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == '__main__':
    posts_directory = 'content/posts'
    add_descriptions_to_posts(posts_directory)
