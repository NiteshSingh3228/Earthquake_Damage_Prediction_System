import re
import os

def html_to_jsx(html):
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return ""
    content = body_match.group(1)
    
    # Replace class with className
    content = content.replace('class="', 'className="')
    content = content.replace("class='", "className='")
    
    # Replace for with htmlFor
    content = content.replace('for="', 'htmlFor="')
    
    # Close unclosed tags (img, input, hr, br)
    content = re.sub(r'(<(img|input|hr|br)[^>]*?)(?<!/)>', r'\1 />', content)
    
    # Replace style="width: 15%" with style={{ width: '15%' }}
    def style_repl(match):
        style_str = match.group(1)
        # very basic conversion, assumes simple styles like width: 15%
        styles = []
        for s in style_str.split(';'):
            s = s.strip()
            if not s: continue
            k, v = s.split(':', 1)
            k = k.strip()
            # camelCase key
            parts = k.split('-')
            k = parts[0] + ''.join(x.title() for x in parts[1:])
            v = v.strip().replace("'", '"')
            styles.append(f"{k}: '{v}'")
        return 'style={{ ' + ', '.join(styles) + ' }}'

    content = re.sub(r'style="([^"]*)"', style_repl, content)
    
    return content

# Convert dashboard
with open('richter-web/stitch_html/dashboard.html', 'r') as f:
    dashboard_html = f.read()

dashboard_jsx = f"""export default function Home() {{
  return (
    <>
{html_to_jsx(dashboard_html)}
    </>
  );
}}"""
with open('richter-web/src/app/page.tsx', 'w') as f:
    f.write(dashboard_jsx)

# Convert predict
with open('richter-web/stitch_html/predict.html', 'r') as f:
    predict_html = f.read()

predict_jsx = f"""export default function Predict() {{
  return (
    <>
{html_to_jsx(predict_html)}
    </>
  );
}}"""
os.makedirs('richter-web/src/app/predict', exist_ok=True)
with open('richter-web/src/app/predict/page.tsx', 'w') as f:
    f.write(predict_jsx)

# Convert model
with open('richter-web/stitch_html/model.html', 'r') as f:
    model_html = f.read()

model_jsx = f"""export default function Model() {{
  return (
    <>
{html_to_jsx(model_html)}
    </>
  );
}}"""
os.makedirs('richter-web/src/app/model', exist_ok=True)
with open('richter-web/src/app/model/page.tsx', 'w') as f:
    f.write(model_jsx)

print("Conversion complete!")
