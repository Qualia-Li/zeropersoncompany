#!/usr/bin/env python3
"""Split the single MD file into chapter files like the GEO whitepaper."""
import re

with open("Zero-Person-Company.md", "r") as f:
    content = f.read()

# Extract preface (everything before Chapter 1)
ch1_start = content.index("# Chapter 1:")
preface = content[:ch1_start].rstrip()

# Split into chapters
chapter_pattern = r'(# Chapter \d+:.*?)(?=# Chapter \d+:|## A Note on Methodology)'
chapters = re.findall(chapter_pattern, content, re.DOTALL)

# Extract references section (from "## A Note on Methodology" to end)
refs_start = content.index("## A Note on Methodology")
references = content[refs_start:].rstrip()

# Write preface
with open("chapters/00-preface.md", "w") as f:
    f.write(preface + "\n")
print("Written: 00-preface.md")

# Write chapters
filenames = [
    "01-shrinking-company.md",
    "02-one-to-zero.md",
    "03-technology-stack.md",
    "04-zero-person-playbook.md",
    "05-human-question-future.md",
]
for i, (chapter, filename) in enumerate(zip(chapters, filenames)):
    with open(f"chapters/{filename}", "w") as f:
        f.write(chapter.rstrip() + "\n")
    print(f"Written: {filename}")

# Write references
with open("chapters/06-references.md", "w") as f:
    f.write(references + "\n")
print("Written: 06-references.md")

print("\nAll chapter files created!")
