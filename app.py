import urllib.parse
import json
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, request, Response

app = Flask(__name__)

# ==========================================
# 🎨 FRONTEND TEMPLATE (Bootstrap 5 Dark Mode)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S.E.E.K.E.R - OSINT Recon Tool</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --brand-color: #0ea5e9; /* Sky Blue */
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --border-color: #334155;
        }
        body {
            background-color: var(--bg-dark);
            color: #cbd5e1;
            font-family: 'Segoe UI', system-ui, sans-serif;
            background-image: radial-gradient(rgba(14, 165, 233, 0.1) 1px, transparent 1px);
            background-size: 40px 40px;
        }
        .navbar {
            background: rgba(15, 23, 42, 0.9);
            border-bottom: 1px solid var(--border-color);
            backdrop-filter: blur(10px);
        }
        .search-hero {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 0 30px rgba(14, 165, 233, 0.15);
        }
        .dork-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            transition: transform 0.2s, border-color 0.2s;
            height: 100%;
        }
        .dork-card:hover {
            transform: translateY(-4px);
            border-color: var(--brand-color);
        }
        .dork-code {
            background: #020617;
            color: #22d3ee;
            font-family: monospace;
            padding: 8px;
            border-radius: 4px;
            font-size: 0.85rem;
            word-break: break-all;
            border-left: 3px solid var(--brand-color);
        }
        .btn-scan {
            background: var(--brand-color);
            color: white;
            font-weight: 600;
        }
        .btn-scan:hover { background: #0284c7; color: white; }
        
        /* Category Badges */
        .cat-header {
            color: var(--brand-color);
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin: 2rem 0 1rem 0;
            text-transform: uppercase;
            font-size: 0.9rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    <div class="container">
        <a class="navbar-brand fw-bold" href="#">
            <i class="fas fa-satellite-dish text-info"></i> S.E.E.K.E.R <span class="badge bg-dark border border-secondary text-secondary ms-2">v12.0</span>
        </a>
    </div>
</nav>

<div class="container py-5">
    
    <div class="row justify-content-center mb-5">
        <div class="col-lg-10">
            <div class="search-hero">
                <form method="POST" action="/">
                    <div class="row g-3">
                        <div class="col-md-5">
                            <label class="form-label text-muted small fw-bold">TARGET DOMAIN</label>
                            <input type="text" name="domain" class="form-control form-control-lg bg-dark text-white border-secondary" 
                                   placeholder="example.com" value="{{ domain }}" required>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label text-muted small fw-bold">YEAR FILTER</label>
                            <select name="year" class="form-select form-select-lg bg-dark text-white border-secondary">
                                <option value="any">All Time</option>
                                <option value="2025" {% if year == '2025' %}selected{% endif %}>2025</option>
                                <option value="2024" {% if year == '2024' %}selected{% endif %}>2024</option>
                                <option value="2023" {% if year == '2023' %}selected{% endif %}>2023</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                             <label class="form-label text-muted small fw-bold">STACK</label>
                            <select name="tech" class="form-select form-select-lg bg-dark text-white border-secondary">
                                <option value="general">General</option>
                                <option value="php" {% if tech == 'php' %}selected{% endif %}>PHP</option>
                                <option value="python" {% if tech == 'python' %}selected{% endif %}>Python</option>
                            </select>
                        </div>
                        <div class="col-md-2 d-grid">
                            <label class="form-label">&nbsp;</label>
                            <button type="submit" class="btn btn-scan btn-lg">SCAN</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    {% if domain %}
    <div class="d-flex justify-content-end mb-4">
        <form action="/download" method="POST">
            <input type="hidden" name="domain" value="{{ domain }}">
            <input type="hidden" name="tech" value="{{ tech }}">
            <input type="hidden" name="year" value="{{ year }}">
            <button class="btn btn-outline-light btn-sm" type="submit"><i class="fas fa-file-export"></i> Export JSON</button>
        </form>
    </div>

    <div class="row">
        {% for category, dorks in all_dorks.items() %}
        <div class="col-12">
            <div class="cat-header">
                <i class="fas fa-folder-open"></i> {{ category }} 
                <span class="badge bg-secondary ms-auto">{{ dorks|length }}</span>
            </div>
            <div class="row g-3">
                {% for dork in dorks %}
                <div class="col-md-6 col-lg-4">
                    <div class="dork-card p-3 h-100 d-flex flex-column">
                        <div class="fw-bold mb-2 text-light">{{ dork.title }}</div>
                        <div class="dork-code mb-3">{{ dork.query }}</div>
                        <div class="mt-auto d-flex gap-2">
                            <a href="{{ dork.link }}" target="_blank" class="btn btn-sm btn-outline-info flex-grow-1">
                                <i class="fab fa-google"></i> Search
                            </a>
                            <button class="btn btn-sm btn-outline-secondary" onclick="navigator.clipboard.writeText('{{ dork.query | replace("'", "\\'") }}')">
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <footer class="text-center mt-5 text-muted small pb-4">
        <p>⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes and authorized security testing only.</p>
    </footer>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ==========================================
# 🧠 DORK ENGINE
# ==========================================
def generate_dorks(domain, tech="general", year="any"):
    def g_url(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"
    
    # Base Filters
    y_str = f" \"{year}\"" if year != "any" else ""
    
    # 1. Critical Files
    files = [
        {"title": "Config Files", "query": f"site:{domain} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ini"},
        {"title": "Database Files", "query": f"site:{domain} ext:sql | ext:dbf | ext:mdb"},
        {"title": "Log Files", "query": f"site:{domain} ext:log"},
        {"title": "Backup Files", "query": f"site:{domain} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"},
        {"title": "Git/SVN", "query": f"site:{domain} inurl:/.git | inurl:/.svn"},
    ]

    # 2. Sensitive Info
    secrets = [
        {"title": "Public RSA Keys", "query": f"site:{domain} ext:pem | ext:key | ext:pub"},
        {"title": "Login Portals", "query": f"site:{domain} inurl:admin | inurl:login | inurl:portal | inurl:signin"},
        {"title": "Exposed Documents", "query": f"site:{domain} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:ppt | ext:pptx | ext:xls | ext:xlsx{y_str}"},
        {"title": "Directory Listing", "query": f"site:{domain} intitle:\"index of\""},
    ]

    # 3. Cloud & Infra
    cloud = [
        {"title": "S3 Buckets", "query": f"site:s3.amazonaws.com \"{domain}\""},
        {"title": "Azure Blobs", "query": f"site:blob.core.windows.net \"{domain}\""},
        {"title": "Google Storage", "query": f"site:storage.googleapis.com \"{domain}\""},
        {"title": "Github Repos", "query": f"site:github.com \"{domain}\""},
    ]
    
    # Tech Specific
    if tech == "php":
        files.append({"title": "PHP Info", "query": f"site:{domain} ext:php intitle:phpinfo"})
        files.append({"title": "PHP Errors", "query": f"site:{domain} \"Fatal error:\" | \"Warning: include()\""})
    
    categories = {
        "Critical Files": files,
        "Sensitive Information": secrets,
        "Cloud Infrastructure": cloud
    }

    # Add links
    for cat in categories.values():
        for d in cat:
            d['link'] = g_url(d['query'])

    return categories

# ==========================================
# 🚦 ROUTES
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def home():
    domain, tech, year, dorks = "", "general", "any", {}
    if request.method == 'POST':
        domain = request.form.get('domain', '').strip()
        tech = request.form.get('tech', 'general')
        year = request.form.get('year', 'any')
        if domain:
            # Clean domain input
            domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
            dorks = generate_dorks(domain, tech, year)
    
    return render_template_string(HTML_TEMPLATE, domain=domain, tech=tech, year=year, all_dorks=dorks)

@app.route('/download', methods=['POST'])
def download():
    domain = request.form.get('domain', '')
    if domain:
        data = generate_dorks(domain, request.form.get('tech'), request.form.get('year'))
        return Response(json.dumps(data, indent=4), 
                       mimetype="application/json", 
                       headers={"Content-disposition": f"attachment; filename={domain}_recon.json"})
    return "{}"

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    print("🚀 S.E.E.K.E.R Running on http://127.0.0.1:5000")
    app.run(port=5000)
