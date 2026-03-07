#!/usr/bin/env python3
"""
Generate PDF from Zero Person Company book chapters.
Same mechanism as the GEO whitepaper (weasyprint + markdown + PyPDF2).
"""

import os
import re
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io


def create_cover_pdf(output_path):
    """Create a cover page PDF from the O'Reilly-style cover image"""
    from reportlab.lib.utils import ImageReader

    base_dir = Path(__file__).parent
    cover_image = base_dir / "assets" / "images" / "cover-oreilly.png"

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    width, height = A4

    # Draw cover image scaled to fill the full A4 page
    img = ImageReader(str(cover_image))
    c.drawImage(img, 0, 0, width=width, height=height, preserveAspectRatio=True, anchor='c')

    c.save()
    packet.seek(0)

    with open(output_path, 'wb') as f:
        f.write(packet.getvalue())

    return output_path


def create_pdf_with_cover(output_pdf="Zero Person Company (preview).pdf"):
    """
    Generate PDF from markdown chapters with cover page.
    Same mechanism as the GEO whitepaper.
    """
    base_dir = Path(__file__).parent
    chapters_dir = base_dir / "chapters"

    # Define chapter order (same structure as GEO whitepaper)
    chapter_files = [
        "00-preface.md",
        "01-vanishing-workforce.md",
        "02-intelligence-fallacy.md",
        "03-anatomy-of-autonomy.md",
        "04-great-displacement.md",
        "05-one-to-zero.md",
        "06-references.md",
    ]

    # Build HTML content
    html_parts = []

    # Add HTML header with styling
    html_parts.append("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {
                size: A4;
                margin: 2cm;
                @bottom-center {
                    content: counter(page);
                    font-family: 'Helvetica', 'Arial', sans-serif;
                    font-size: 9pt;
                    color: #666;
                }
            }
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 9pt;
                line-height: 1.4;
                color: #333;
            }
            h1 {
                color: #0a1628;
                font-size: 16pt;
                margin-top: 1.2em;
                margin-bottom: 0.3em;
                border-bottom: 2px solid #2563eb;
                padding-bottom: 0.3em;
            }
            h2 {
                color: #1e40af;
                font-size: 13pt;
                margin-top: 1.2em;
                margin-bottom: 0.25em;
            }
            h3 {
                color: #2563eb;
                font-size: 11pt;
                margin-top: 1em;
                margin-bottom: 0.25em;
            }
            h4 {
                color: #1e3a5f;
                font-size: 10pt;
                margin-top: 0.8em;
                margin-bottom: 0.2em;
            }
            p {
                text-align: justify;
                margin-bottom: 0.8em;
            }
            img {
                max-width: 85%;
                height: auto;
                display: block;
                margin: 1em auto;
            }
            em {
                font-style: italic;
                font-size: 8pt;
                color: #666;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 8pt;
                word-wrap: break-word;
            }
            pre {
                background-color: #f4f4f4;
                padding: 0.8em;
                border-radius: 5px;
                font-size: 7.5pt;
                white-space: pre-wrap;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            pre code {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            ul, ol {
                margin-left: 1.5em;
                font-size: 9pt;
            }
            li {
                margin-bottom: 0.3em;
            }
            blockquote {
                border-left: 4px solid #2563eb;
                padding-left: 1em;
                margin-left: 0;
                font-style: italic;
                color: #555;
                font-size: 8.5pt;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                font-size: 8pt;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 6px;
                text-align: left;
            }
            th {
                background-color: #1e40af;
                color: white;
            }
            a {
                color: #1e40af;
                text-decoration: none;
                font-size: 7pt;
            }
            strong {
                font-weight: bold;
            }
            .chapter-break {
                page-break-before: always;
            }
            hr {
                border: none;
                border-top: 1px solid #ddd;
                margin: 1.5em 0;
            }
        </style>
    </head>
    <body>
    """)

    # Process each chapter
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables', 'fenced_code'])

    for i, chapter_file in enumerate(chapter_files):
        chapter_path = chapters_dir / chapter_file

        if not chapter_path.exists():
            print(f"Warning: {chapter_file} not found, skipping...")
            continue

        print(f"Processing {chapter_file}...")

        with open(chapter_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix relative image paths - convert to absolute paths
        assets_path = (base_dir / "assets" / "images").as_posix()
        content = re.sub(
            r'\!\[(.*?)\]\(assets/images/(.*?)\)',
            rf'![\1]({assets_path}/\2)',
            content
        )

        # Convert markdown to HTML
        chapter_html = md.convert(content)

        # Add chapter with page break
        if i > 0:
            html_parts.append('<div class="chapter-break"></div>')
        html_parts.append(chapter_html)

        # Reset markdown converter for next chapter
        md.reset()

    # Close HTML
    html_parts.append("""
    </body>
    </html>
    """)

    # Combine all HTML
    full_html = '\n'.join(html_parts)

    # Generate content PDF (without cover)
    content_pdf = "temp_content.pdf"
    print(f"\nGenerating content PDF...")
    HTML(string=full_html, base_url=str(base_dir)).write_pdf(content_pdf)

    # Create cover PDF
    cover_pdf = "temp_cover.pdf"
    print("Creating cover page...")
    create_cover_pdf(cover_pdf)

    # Merge PDFs (cover first, then content)
    print(f"Merging PDFs into: {output_pdf}...")
    pdf_writer = PdfWriter()

    # Add cover page
    with open(cover_pdf, 'rb') as cover_file:
        pdf_reader = PdfReader(cover_file)
        pdf_writer.add_page(pdf_reader.pages[0])

    # Add content pages
    with open(content_pdf, 'rb') as content_file:
        pdf_reader = PdfReader(content_file)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    # Write final PDF
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

    # Clean up temp files
    os.remove(content_pdf)
    os.remove(cover_pdf)

    # Validate PDF was created
    if not os.path.exists(output_pdf):
        print(f"ERROR: PDF was not created at {output_pdf}")
        return False

    print(f"\nPDF generated successfully: {output_pdf}")

    # Get file size
    file_size = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"  File size: {file_size:.2f} MB")

    # Count images in HTML to verify they're included
    img_count = full_html.count('<img')
    print(f"  Images included: {img_count}")

    return True


if __name__ == "__main__":
    create_pdf_with_cover()
