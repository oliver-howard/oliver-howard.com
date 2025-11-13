# Oliver Howard Photography

Personal photography portfolio website showcasing travel, landscape, and street photography.

**Live Site:** [oliver-howard.com](https://oliver-howard.com)

## Adding New Projects

```bash
# Add images to media/projects/your_project_name/
python3 generate_project.py your_project_name "Project Title" "Location / Date"
```

This automatically:
- Generates the project HTML page
- Adds it to the portfolio grid
- Updates recent projects on homepage (only displays 4 most recent projects)

## Local Development

```bash
# Serve locally
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Tech Stack

Static HTML/CSS/JS with:
- PhotoSwipe (lightbox galleries)
- Masonry (grid layouts)
- BeerSlider (depricated)
