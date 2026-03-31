
import os
import frontmatter

def add_descriptions_to_posts(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                post = frontmatter.load(f)
                if 'description' not in post.metadata:
                    # Generate a summary here. For now, a placeholder.
                    summary = f"Summary for {post.metadata['title']}"
                    post.metadata['description'] = summary
                    with open(filepath, 'w') as f_write:
                        f_write.write(frontmatter.dumps(post))
                        print(f"Added description to {filename}")

if __name__ == "__main__":
    add_descriptions_to_posts("content/posts")
