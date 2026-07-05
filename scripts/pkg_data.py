"""Static configuration and content for the package index site.

This module intentionally contains no filesystem or network logic - it is
the "data" half of the generator. Anything here should be safe to read top
to bottom to understand what the site says, without needing to trace through
control flow.
"""

from __future__ import annotations

# --- Site identity -----------------------------------------------------

SITE_NAME = "TamKungZ_ Packages"
BASE_URL = "https://packages.tamkungz.me"
FAVICON_URL = "https://pub-df28fb9f69aa4326a1c6e10fb1f2abdc.r2.dev/assets-image/maven/tamkungz-repo-favicon-v2-nobg.ico"

# --- Author / SEO identity ---------------------------------------------

AUTHOR_NAME = "TamKungZ_"
AUTHOR_TWITTER_HANDLE = "@TamKungZ_"
AUTHOR_EMAIL = "dev@tamkungz.me"
AUTHOR_GITHUB_URL = "https://github.com/TamKungZ"

# --- Repository layout ---------------------------------------------------

# Root-level package repository layout:
# /apt              APT repository shared by all Debian packages
# /rpm/<basearch>   RPM repository shared by all RPM packages
# /maven            Maven repository, preferred new layout
# /me               Maven legacy group root, supported for compatibility
# /apps/<app>       human-readable product pages only
PROJECT_ROOTS = {
    "apt",
    "rpm",
    "maven",
    "me",  # legacy Maven group root
    "apps",
}

IGNORE_DIRS = {
    ".git",
    ".github",
    "scripts",
    "examples",
    "target",
    "node_modules",
    "__pycache__",
}

IGNORE_FILES = {
    "index.html",
    "CNAME",
    ".nojekyll",
    "README.md",
    "LICENSE",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "push.txt",
}

# --- Remote README sources -------------------------------------------

# Some /apps/<name>/ pages describe a project that lives in its own repo
# rather than in this one. For those, fetch the description straight from
# the upstream README instead of expecting a local README.md copy.
TARMINAL_README_URL = "https://raw.githubusercontent.com/TamKungZ/tarminal-tar-install/refs/heads/main/README.md"

APP_README_SOURCES = {
    "tarminal": TARMINAL_README_URL,
}

# --- Usage snippets ----------------------------------------------------
#
# Each "usage" block is (label, language, code). `language` should match a
# highlight.js language class (e.g. "bash", "groovy") so the rendered page
# can syntax-highlight it, and each block gets its own copy button.

UsageBlock = tuple[str, str, str]


def root_usage_blocks(base_url: str, maven_repo_url: str) -> list[UsageBlock]:
    return [
        (
            "Debian / Ubuntu / Zorin",
            "bash",
            f"""curl -fsSL {base_url}/gpg.key | \\
  sudo gpg --dearmor -o /usr/share/keyrings/tamkungz-packages.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/tamkungz-packages.gpg] {base_url}/apt stable main" | \\
  sudo tee /etc/apt/sources.list.d/tamkungz-packages.list

sudo apt update
sudo apt install tarminal""",
        ),
        (
            "Fedora / RPM",
            "bash",
            f"""sudo tee /etc/yum.repos.d/tamkungz-packages.repo >/dev/null <<'EOF'
[tamkungz-packages]
name=TamKungZ Packages
baseurl={base_url}/rpm/$basearch/
enabled=1
gpgcheck=0
repo_gpgcheck=1
gpgkey={base_url}/gpg.key
EOF

sudo dnf install tarminal""",
        ),
        (
            "Maven / Gradle",
            "groovy",
            f"""repositories {{
    maven {{
        name = "TamKungZ Packages"
        url = uri("{maven_repo_url}")
    }}
}}""",
        ),
    ]


def tarminal_usage_blocks(base_url: str) -> list[UsageBlock]:
    return [
        (
            "Debian / Ubuntu / Zorin",
            "bash",
            f"""curl -fsSL {base_url}/gpg.key | \\
  sudo gpg --dearmor -o /usr/share/keyrings/tamkungz-packages.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/tamkungz-packages.gpg] {base_url}/apt stable main" | \\
  sudo tee /etc/apt/sources.list.d/tamkungz-packages.list

sudo apt update
sudo apt install tarminal""",
        ),
        (
            "Fedora / RPM",
            "bash",
            f"""sudo tee /etc/yum.repos.d/tamkungz-packages.repo >/dev/null <<'EOF'
[tamkungz-packages]
name=TamKungZ Packages
baseurl={base_url}/rpm/$basearch/
enabled=1
gpgcheck=0
repo_gpgcheck=1
gpgkey={base_url}/gpg.key
EOF

sudo dnf install tarminal""",
        ),
    ]


def maven_usage_blocks(maven_repo_url: str) -> list[UsageBlock]:
    return [
        (
            "Gradle",
            "groovy",
            f"""repositories {{
    maven {{
        name = "TamKungZ Packages"
        url = uri("{maven_repo_url}")
    }}
}}""",
        ),
    ]
