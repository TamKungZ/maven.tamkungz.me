from __future__ import annotations

import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path

import maven_pages
import package_pages
import site_config as data


def find_repo_root() -> Path:
    """Return the package-site root in release.yml and local runs.

    The publish job runs this after cd-ing into the cloned packages-site repo.
    PACKAGE_INDEX_ROOT exists for local tests that need a temporary root.
    """
    explicit_root = os.environ.get("PACKAGE_INDEX_ROOT")
    if explicit_root:
        return Path(explicit_root).resolve()

    return Path(__file__).resolve().parent.parent


def display_path(root: Path, directory: Path) -> str:
    if directory == root:
        return "/"
    return "/" + directory.relative_to(root).as_posix().strip("/") + "/"


def canonical_url(root: Path, directory: Path) -> str:
    path = display_path(root, directory)
    if path == "/":
        return data.BASE_URL + "/"
    return data.BASE_URL + path


def write_robots(root: Path) -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {data.BASE_URL}/sitemap.xml
"""
    (root / "robots.txt").write_text(content, encoding="utf-8")


def write_sitemap(root: Path, generated_pages: list[Path]) -> None:
    now = datetime.now(timezone.utc).date().isoformat()

    urls = []
    for directory in sorted(generated_pages, key=lambda p: display_path(root, p)):
        urls.append(
            f"""  <url>
    <loc>{escape(canonical_url(root, directory))}</loc>
    <lastmod>{now}</lastmod>
  </url>"""
        )

    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""
    (root / "sitemap.xml").write_text(content, encoding="utf-8")


def build_site(root: Path | None = None) -> list[Path]:
    root = root or find_repo_root()
    (root / ".nojekyll").touch()

    generated_pages = package_pages.generate_package_pages(root)
    generated_pages.extend(maven_pages.generate_maven_pages(root))

    write_robots(root)
    write_sitemap(root, generated_pages)
    return generated_pages


def main() -> None:
    build_site()


if __name__ == "__main__":
    main()
