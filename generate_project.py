#!/usr/bin/env python3
"""
Generate a photography project HTML page from a folder of images.

Usage:
    python3 generate_project.py <project_folder> <project_title> [description]

Example:
    python3 generate_project.py point_reyes "Point Reyes" "California / Winter 2024"
"""

import sys
import subprocess
from pathlib import Path
from PIL import Image


def get_image_dimensions(image_path):
    """Get the dimensions of an image file."""
    try:
        with Image.open(image_path) as img:
            return img.size  # Returns (width, height)
    except (OSError, IOError) as e:
        print(f"Error reading {image_path}: {e}")
        return None


def create_thumbnail(image_path, thumbnail_path, max_size=800):
    """
    Create a thumbnail version of an image.

    Args:
        image_path: Path to the original image
        thumbnail_path: Path where thumbnail should be saved
        max_size: Maximum dimension (width or height) for the thumbnail

    Returns:
        Tuple of (width, height) of the thumbnail, or None on error
    """
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
                )
                img = background

            # Calculate new dimensions maintaining aspect ratio
            width, height = img.size
            if width > height:
                new_width = max_size
                new_height = int((max_size / width) * height)
            else:
                new_height = max_size
                new_width = int((max_size / height) * width)

            # Resize and save with optimization
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_resized.save(thumbnail_path, "JPEG", quality=85, optimize=True)

            return (new_width, new_height)
    except (OSError, IOError) as e:
        print(f"Error creating thumbnail for {image_path}: {e}")
        return None


def generate_photo_item(
    photo_path, thumbnail_path, width, height, thumb_width, thumb_height
):
    """Generate HTML for a single photo item."""
    return f"""
            <div class="photoswipe-item fade-in">
                <a href="../media/projects/{photo_path}" itemprop="contentUrl" \
data-size="{width}x{height}">
                    <img src="../media/projects/{photo_path}" \
width="{width}" height="{height}"/>
                        <div class="overlay"></div>
                        <svg xmlns="http://www.w3.org/2000/svg" \
viewBox="0 0 24 24">
                        <path d="M22,12a11.6,11.6,0,0,1-10,6A11.6,11.6,0,0,1,\
2,12,11.6,11.6,0,0,1,12,6,11.6,11.6,0,0,1,22,12Z" fill="none" \
stroke="#fff" stroke-width="1.5"/>
                        <circle cx="12" cy="12" r="3" fill="none" \
stroke="#fff" stroke-width="1.5"/>
                    </svg>
                </a>
            </div>
"""


def generate_html(project_name, project_title, description, photos_html):
    """Generate the complete HTML page."""
    return f"""<!DOCTYPE html>
<html lang="en">
    <head>

        <meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

        <title>{project_title}</title>
        <meta name="description" content="{project_title} photography project by Oliver Howard.">
                <meta name="robots" content="index, follow">

        <meta property="og:url" content="https://oliverhoward.co/projects/{project_name}">
        <meta property="og:title" \
content="{project_title} - Oliver Howard">
        <meta property="og:discription" \
content="{project_title} photography project by Oliver Howard.">
        <meta property="og:site_name" content="Oliver Howard" />
        <meta property="og:type" content="website" />

        <link rel="canonical" href="../projects/{project_name}.html">

        <link rel="icon" type="image/x-icon" href="../assets/img/oliver-howard-logo-black.png">
        <link rel="apple-touch-icon" href="../assets/img/oliver-howard-logo-black.png">

        <link href="../assets/css/normalize.css" rel="stylesheet">
        <link href="../assets/css/navigation.css" rel="stylesheet">
        <link href="../assets/css/photoswipe.css" rel="stylesheet">
        <link href="../assets/css/photoswipe-skin.css" rel="stylesheet">
        <link href="../assets/css/BeerSlider.css" rel="stylesheet">
        <link href="../assets/css/style.css" rel="stylesheet">
    </head>

    <body>
        <div class="overlay-transition"></div>
        <main class="" id="portfolio">
            <div class="black-overlay"></div>
            <div class="navigation-fade"></div>
            <a href="../index.html" class="logo animatelink">
                <img src="../assets/img/oliver-howard-logo.png" height="23"/>
            </a>
            <nav>
                <div class="background-image" style="background: url('../media/site/banner.jpg') center center; background-size: cover;"></div>
                <div class="top-fade"></div>
                <div class="left-fade"></div>
                <ul>
                                    <li class="big-li ">
                        <a href="../index.html" class="animatelink">Homepage</a>
                    </li>
                                    <li class="big-li active">
                        <a href="../portfolio.html" class="animatelink">Portfolio</a>
                    </li>
                                    <li class="big-li ">
                        <a href="../video.html" class="animatelink">Video</a>
                    </li>
                </ul>
            </nav>
            <div class="nav-icon">
                <div class="hamburger-bar"></div>
            </div>

   <section class="default-header">
      <h1>{project_title}</h1>
      <p>{description}</p>
   </section>

   <a href="../portfolio.html" class="back-to-portfolio animatelink">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" \
viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" \
stroke-linecap="round" stroke-linejoin="round">
         <path d="M19 12H5M12 19l-7-7 7-7"/>
      </svg>
      <span>Back to Portfolio</span>
   </a>

   <section class="grid">
      <div class="wrap-wide">
         <div class="photoswipe-wrapper fade-in" itemscope itemtype="http://schema.org/ImageGallery">
{photos_html}
         </div>
      </div>
   </section>
   <!-- Root element of PhotoSwipe. Must have class pswp. -->
   <div class="pswp" tabindex="-1" role="dialog" aria-hidden="true">
      <div class="pswp__bg"></div>
      <div class="pswp__scroll-wrap">
         <div class="pswp__container">
            <div class="pswp__item"></div>
            <div class="pswp__item"></div>
            <div class="pswp__item"></div>
         </div>
         <div class="pswp__ui pswp__ui--hidden">
            <div class="pswp__top-bar">
               <div class="pswp__counter"></div>
               <button class="pswp__button pswp__button--close" title="Close (Esc)"><span>Close</span></button>
               <div class="pswp__preloader">
                  <div class="pswp__preloader__icn">
                     <div class="pswp__preloader__cut">
                        <div class="pswp__preloader__donut"></div>
                     </div>
                  </div>
               </div>
            </div>
            <button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)">
            </button>
            <button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)">
            </button>
            <div class="pswp__caption">
               <div class="pswp__caption__center"></div>
            </div>
         </div>
      </div>
   </div>

        <footer>
            <div class="background-image" style="background: url('../media/site/banner.jpg') center center; background-size: cover;"></div>
            <div class="top-fade"></div>
            <div class="left-fade"></div>
            <div class="wrap-text">
                <div class="logo-row"><img src="../assets/img/oliver-howard-logo.png" height="23"/></div>
                <div class="credits-row">
                    <li>© 2025 Oliver Howard</li>
                </div>
            </div>
        </footer>

        </main>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
        <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/masonry/4.2.1/masonry.pkgd.js"></script>

        <script src="../assets/js/navigation.js"></script>
        <script src="../assets/js/observers.js"></script>
        <script src="../assets/js/photoswipe.min.js"></script>
        <script src="../assets/js/photoswipe-ui-default.min.js"></script>
        <script src="../assets/js/photoswipe.js"></script>

    </body>
</html>
"""


def add_to_portfolio(
    project_folder, project_title, description, cover_image_path, script_dir
):
    """Add project card to portfolio.html"""
    portfolio_file = script_dir / "portfolio.html"

    if not portfolio_file.exists():
        print(f"Warning: portfolio.html not found at {portfolio_file}")
        return False

    portfolio_content = portfolio_file.read_text()

    # Replace '/' with '•' in description for portfolio display
    portfolio_description = description.replace("/", "•")

    project_card = f"""
             <a href="projects/{project_folder}.html" class="project-card animatelink">
                   <img src="media/projects/{cover_image_path}" alt="{project_title}"/>
                   <div class="overlay">
                       <div class="overlay-text">
                           <h3 class="project-title">{project_title}</h3>
                           <p>{portfolio_description}</p>
                       </div>
                   </div>
               </a>

"""

    # Find the insertion point after the opening comments and insert at the TOP
    # This ensures new projects appear first in the grid
    marker = "<!-- Duplicate and customize these for each of your shoots/trips -->\n"

    if marker in portfolio_content:
        # Insert after the comment at the top
        portfolio_content = portfolio_content.replace(
            marker, marker + "\n" + project_card
        )

        # Write back to portfolio.html
        portfolio_file.write_text(portfolio_content)
        return True

    print("Warning: Could not find insertion point in portfolio.html")
    return False


def main():
    """Main function to generate a photography project page from a folder of images."""
    if len(sys.argv) < 3:
        print(
            "Usage: python3 generate_project.py <project_folder> <project_title> [description]"
        )
        print("\nExample:")
        print(
            '  python3 generate_project.py point_reyes "Point Reyes" "California / Winter 2024"'
        )
        sys.exit(1)

    # Parse command-line arguments
    project_folder, project_title = sys.argv[1], sys.argv[2]
    description = sys.argv[3] if len(sys.argv) > 3 else ""

    # Determine paths
    script_dir = Path(__file__).parent
    paths = {
        "media": script_dir / "media" / "projects" / project_folder,
        "output": script_dir / "projects" / f"{project_folder}.html",
    }

    # Check if media folder exists
    if not paths["media"].exists():
        print(f"Error: Media folder not found: {paths['media']}")
        sys.exit(1)

    # Create thumbnails directory
    thumbnails_dir = paths["media"] / "thumbnails"
    thumbnails_dir.mkdir(exist_ok=True)

    # Find all image files with dimensions
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    images = [
        (file.name, dimensions)
        for file in sorted(paths["media"].iterdir())
        if file.suffix.lower() in image_extensions
        and file.name != "thumbnails"  # Skip thumbnails directory
        and (dimensions := get_image_dimensions(file)) is not None
    ]

    if not images:
        print(f"Error: No images found in {paths['media']}")
        sys.exit(1)

    print(f"Found {len(images)} images in {paths['media']}")
    print("Creating thumbnails...")

    # Create thumbnails and collect image data
    image_data = []
    for filename, (width, height) in images:
        original_path = paths["media"] / filename
        # Keep original extension for thumbnail, but save as .jpg
        thumbnail_filename = Path(filename).stem + "_thumb.jpg"
        thumbnail_path = thumbnails_dir / thumbnail_filename

        # Create thumbnail
        thumb_dimensions = create_thumbnail(original_path, thumbnail_path)

        if thumb_dimensions:
            thumb_width, thumb_height = thumb_dimensions
            image_data.append(
                {
                    "filename": filename,
                    "width": width,
                    "height": height,
                    "thumbnail": f"thumbnails/{thumbnail_filename}",
                    "thumb_width": thumb_width,
                    "thumb_height": thumb_height,
                }
            )
            print(f"  ✓ {filename} -> {thumbnail_filename}")
        else:
            print(f"  ✗ Failed to create thumbnail for {filename}")

    if not image_data:
        print("Error: No thumbnails were created successfully")
        sys.exit(1)

    # Generate HTML and write to file
    photos_html = "".join(
        generate_photo_item(
            f"{project_folder}/{img['filename']}",
            f"{project_folder}/{img['thumbnail']}",
            img["width"],
            img["height"],
            img["thumb_width"],
            img["thumb_height"],
        )
        for img in image_data
    )
    html_content = generate_html(
        project_folder, project_title, description, photos_html
    )

    paths["output"].parent.mkdir(parents=True, exist_ok=True)
    paths["output"].write_text(html_content)

    print(f"\nSuccessfully generated: {paths['output']}")
    print(f"Project: {project_title}")
    print(f"Images: {len(image_data)}")

    # Add to portfolio.html with first image (full-size) as cover
    cover_image_path = f"{project_folder}/{image_data[0]['filename']}"
    if add_to_portfolio(
        project_folder, project_title, description, cover_image_path, script_dir
    ):
        print("Added project card to portfolio.html")

    print(f"\nYou can now view it at: projects/{project_folder}.html")

    # Automatically sync recent projects to index.html
    sync_script = script_dir / "sync_recent_projects.py"
    if sync_script.exists():
        print("\nSyncing recent projects to index.html...")
        try:
            result = subprocess.run(
                [sys.executable, str(sync_script)],
                cwd=script_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            # Print the sync script output
            if result.stdout:
                print(result.stdout.rstrip())
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to sync recent projects: {e}")
            if e.stderr:
                print(e.stderr)


if __name__ == "__main__":
    main()
