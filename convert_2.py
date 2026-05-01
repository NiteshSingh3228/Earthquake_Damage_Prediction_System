import re
import os

def html_to_jsx(html):
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_match: return ""
    content = body_match.group(1)
    
    content = content.replace('class="', 'className="')
    content = content.replace("class='", "className='")
    content = content.replace('for="', 'htmlFor="')
    
    content = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', content, flags=re.DOTALL)
    content = re.sub(r'(<(img|input|hr|br)[^>]*?)(?<!/)>', r'\1 />', content)
    
    def style_repl(match):
        style_str = match.group(1)
        styles = []
        for s in style_str.split(';'):
            s = s.strip()
            if not s: continue
            if ':' not in s: continue
            k, v = s.split(':', 1)
            k = k.strip()
            parts = k.split('-')
            k = parts[0] + ''.join(x.title() for x in parts[1:])
            v = v.strip().replace("'", '"')
            styles.append(f"{k}: '{v}'")
        return 'style={{ ' + ', '.join(styles) + ' }}'

    content = re.sub(r'style="([^"]*)"', style_repl, content)
    return content

pages = {
    'prediction.html': 'src/app/page.tsx',
    'map.html': 'src/app/map/page.tsx',
    'analytics.html': 'src/app/analytics/page.tsx',
    'benchmark.html': 'src/app/benchmark/page.tsx',
    'batch.html': 'src/app/batch/page.tsx'
}

for html_file, jsx_file in pages.items():
    with open(f'richter-web-2/stitch_html/{html_file}', 'r') as f:
        html = f.read()
    
    func_name = os.path.basename(os.path.dirname(jsx_file)).title() if '/' in jsx_file and 'page' not in os.path.basename(os.path.dirname(jsx_file)) else 'Home'
    if func_name == 'App': func_name = 'Home'
    if func_name == 'Map': func_name = 'MapPage'
    if func_name == 'Analytics': func_name = 'AnalyticsPage'
    if func_name == 'Benchmark': func_name = 'BenchmarkPage'
    if func_name == 'Batch': func_name = 'BatchPage'

    jsx = f"""export default function {func_name}() {{
  return (
    <>
{html_to_jsx(html)}
    </>
  );
}}"""
    os.makedirs(os.path.dirname(f'richter-web-2/{jsx_file}'), exist_ok=True)
    with open(f'richter-web-2/{jsx_file}', 'w') as f:
        f.write(jsx)

# Extract styles from prediction.html
with open('richter-web-2/stitch_html/prediction.html', 'r') as f:
    html = f.read()

color_matches = re.finditer(r'"([\w-]+)"\s*:\s*"([^"]+)"', html)
colors = {m.group(1): m.group(2) for m in color_matches if m.group(1) not in ["darkMode", "extend", "colors", "fontFamily", "fontSize", "spacing", "borderRadius"]}

spacing_matches = re.finditer(r'"([\w-]+)"\s*:\s*"(\d+px)"', html)
spacing = {m.group(1): m.group(2) for m in spacing_matches if m.group(1) not in colors}

css = ["""@import "tailwindcss";

@theme {"""]

for k, v in colors.items():
    if k.startswith("http"): continue
    if v.startswith("#"): css.append(f"  --color-{k}: {v};")

css.append("  --font-inter: 'Inter', sans-serif;")
css.append("  --font-body-md: 'Inter', sans-serif;")
css.append("  --font-label-sm: 'Inter', sans-serif;")
css.append("  --font-body-lg: 'Inter', sans-serif;")
css.append("  --font-display-xl: 'Inter', sans-serif;")
css.append("  --font-headline-lg: 'Inter', sans-serif;")
css.append("  --font-data-mono: 'Inter', sans-serif;")
css.append("  --font-headline-md: 'Inter', sans-serif;")

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

with open('richter-web-2/src/app/globals.css', 'w') as f:
    f.write("\n".join(css))

with open('richter-web-2/src/app/layout.tsx', 'r') as f:
    layout = f.read()

font_links = """
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
"""

layout = layout.replace('<body', f'<head>{font_links}</head>\n      <body className="dark min-h-full flex flex-col bg-[#0e1322] text-[#dee1f7]" ')
with open('richter-web-2/src/app/layout.tsx', 'w') as f:
    f.write(layout)

print("Setup complete for project 2")
