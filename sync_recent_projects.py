#!/usr/bin/env python3
"""
Sync the first 4 projects from portfolio.html to the recent projects section on index.html.
This ensures the homepage always shows the 4 most recent projects.
"""

import re
import sys
from pathlib import Path
from PIL import Image


def extract_projects_from_portfolio(portfolio_path):
    """Extract project details from portfolio.html."""
    content = portfolio_path.read_text()

    # Pattern to match project cards in portfolio.html
    pattern = r'<a href="projects/([^"]+)" class="project-card[^"]*">\s*' \
              r'<img src="media/projects/([^"]+)"[^>]*alt="([^"]*)"'

    matches = re.findall(pattern, content)

    projects = []
    for project_folder, cover_image, title in matches:
        # Extract just the filename without the project folder path
        projects.append({
            'folder': project_folder.replace('.html', ''),
            'title': title or project_folder.replace('.html', '').replace('_', ' ').title(),
            'cover_image': cover_image
        })

    return projects[:4]  # Return only first 4


def determine_orientation(image_path, script_dir):
    """
    Determine if an image should be portrait or landscape based on actual dimensions.
    Returns 'portrait' if height > width, otherwise 'landscape'.
    """
    try:
        full_path = script_dir / "media" / "projects" / image_path
        with Image.open(full_path) as img:
            width, height = img.size
            return 'portrait' if height > width else 'landscape'
    except (OSError, IOError, FileNotFoundError):
        # Default to landscape if image can't be read
        return 'landscape'


def generate_recent_projects_html(projects, script_dir):
    """Generate HTML for the recent projects section."""

    html_parts = []
    svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">' \
               '<path d="M22,12a11.6,11.6,0,0,1-10,6A11.6,11.6,0,0,1,2,12,' \
               'A11.6,11.6,0,0,1,12,6,A11.6,11.6,0,0,1,22,12Z" fill="none" ' \
               'stroke="#fff" stroke-width="1.5"/>' \
               '<circle cx="12" cy="12" r="3" fill="none" stroke="#fff" ' \
               'stroke-width="1.5"/></svg>'

    for project in projects:
        # Determine orientation based on actual image dimensions
        orientation = determine_orientation(project['cover_image'], script_dir)

        project_html = f'''      <a href="projects/{project['folder']}.html" ''' \
                      f'''class="single-image {orientation} animatelink" ''' \
                      f'''style="background: url('media/projects/{project['cover_image']}') ''' \
                      f'''center center; background-size: cover;">
         <div class="overlay">
            <h3 class="project-title">{project['title']}</h3>
         </div>
         {svg_icon}
      </a>
'''
        html_parts.append(project_html)

    return '\n'.join(html_parts)


def update_index_html(index_path, new_projects_html):
    """Update the recent projects section in index.html."""
    content = index_path.read_text()

    # Pattern to match just the project items, preserving the button
    pattern = r'(<section class="portfolio fade-in" id="recent-projects">\s*' \
              r'<div class="wrap">\s*)(.*?)(\s*</div>\s*' \
              r'<div style="text-align: center; margin-top: 20px; ' \
              r'margin-bottom: 20px;">.*?</div>\s*' \
              r'</section>)'

    replacement = rf'\1{new_projects_html}\n\n   \3'

    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if updated_content == content:
        print("Warning: Could not find recent projects section in index.html")
        return False

    index_path.write_text(updated_content)
    return True


def main():
    """Main function to sync recent projects."""
    script_dir = Path(__file__).parent
    portfolio_path = script_dir / "portfolio.html"
    index_path = script_dir / "index.html"

    # Check files exist
    if not portfolio_path.exists():
        print(f"Error: {portfolio_path} not found")
        sys.exit(1)

    if not index_path.exists():
        print(f"Error: {index_path} not found")
        sys.exit(1)

    # Extract first 4 projects from portfolio
    projects = extract_projects_from_portfolio(portfolio_path)

    if len(projects) < 4:
        print(f"Warning: Only found {len(projects)} projects in portfolio.html")
        if not projects:
            print("Error: No projects found to sync")
            sys.exit(1)

    print(f"Found {len(projects)} projects to sync:")
    for project in projects:
        print(f"  - {project['title']} ({project['folder']})")

    # Generate new HTML
    new_html = generate_recent_projects_html(projects, script_dir)

    # Update index.html
    if update_index_html(index_path, new_html):
        print("\n✓ Successfully synced recent projects to index.html")
        sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    main()
