import re

with open('richter-web/stitch_html/dashboard.html', 'r') as f:
    html = f.read()

# Extract colors
color_matches = re.finditer(r'"([\w-]+)"\s*:\s*"([^"]+)"', html)
colors = {m.group(1): m.group(2) for m in color_matches if m.group(1) not in ["darkMode", "extend", "colors", "fontFamily", "fontSize", "spacing", "borderRadius"]}

# Extract spacing
spacing_matches = re.finditer(r'"([\w-]+)"\s*:\s*"(\d+px)"', html)
spacing = {m.group(1): m.group(2) for m in spacing_matches if m.group(1) not in colors}

css = ["""@import "tailwindcss";

@theme {"""]

for k, v in colors.items():
    if k.startswith("http"): continue
    if v.startswith("#"):
        css.append(f"  --color-{k}: {v};")

css.append("  /* Fonts */")
css.append("  --font-inter: 'Inter', sans-serif;")
css.append("  --font-body-md: 'Inter', sans-serif;")
css.append("  --font-label-sm: 'Inter', sans-serif;")
css.append("  --font-body-lg: 'Inter', sans-serif;")
css.append("  --font-display-xl: 'Inter', sans-serif;")
css.append("  --font-headline-lg: 'Inter', sans-serif;")
css.append("  --font-data-mono: 'Inter', sans-serif;")
css.append("  --font-headline-md: 'Inter', sans-serif;")

css.append("  /* Spacing */")
for k, v in spacing.items():
    css.append(f"  --spacing-{k}: {v};")

css.append("}")

css.append("""
body {
    background-color: #0e1322;
    color: #dee1f7;
    overflow-x: hidden;
}
.glass-card {
    background: rgba(37, 41, 58, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(173, 198, 255, 0.1);
    transition: all 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(173, 198, 255, 0.3);
    background: rgba(37, 41, 58, 0.5);
}
.glow-border {
    position: relative;
}
.glow-border::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, rgba(173, 198, 255, 0.4) 0%, rgba(173, 198, 255, 0) 50%, rgba(173, 198, 255, 0.1) 100%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
.heatmap-grid {
    background-image: radial-gradient(circle at 2px 2px, rgba(173, 198, 255, 0.1) 1px, transparent 0);
    background-size: 24px 24px;
}
""")

with open('richter-web/src/app/globals.css', 'w') as f:
    f.write("\n".join(css))

# Add font links to layout.tsx
with open('richter-web/src/app/layout.tsx', 'r') as f:
    layout = f.read()

font_links = """
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
"""

layout = layout.replace('<body', f'<head>{font_links}</head>\n      <body className="dark"')
with open('richter-web/src/app/layout.tsx', 'w') as f:
    f.write(layout)
    
print("CSS updated")
