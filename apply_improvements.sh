#!/bin/bash
set -e

cd /home/ubuntu/.openclaw/workspace/GenAI-news-site

# Improve CSS
cat << 'EOF' >> static/css/custom.css

/* Additional Design Improvements */
body {
  line-height: 1.8;
  color: #e4e4e7;
}
h1 { font-size: 2.5rem; letter-spacing: -0.03em; }
h2 { font-size: 2rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem; }
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.5);
}
.article-content { font-size: 1.15rem; }
img {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
EOF

# Make sure canonical tag is in head-additions
if ! grep -q "rel=\"canonical\"" layouts/partials/head-additions.html; then
  sed -i '1s|^|<link rel="canonical" href="{{ .Permalink }}">\n|' layouts/partials/head-additions.html
fi

# Add a meta keywords tag if not present
if ! grep -q "name=\"keywords\"" layouts/partials/head-additions.html; then
  sed -i '1s|^|<meta name="keywords" content="{{ with .Params.tags }}{{ delimit . \", \" }}{{ else }}{{ delimit .Site.Params.keywords \", \" }}{{ end }}">\n|' layouts/partials/head-additions.html
fi

# Build
hugo

# Git commit and push
git config user.name "OpenClaw Assistant"
git config user.email "assistant@openclaw.local"
git add static/css/custom.css layouts/partials/head-additions.html
git commit -m "Enhance SEO meta tags and improve CSS design"
git push

echo "Improvements applied, committed, and pushed."
