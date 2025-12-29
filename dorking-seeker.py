import urllib.parse
import json
from flask import Flask, render_template_string, request, Response

app = Flask(__name__)

# ==========================================
# 🎨 FRONTEND TEMPLATE (v12.0 System Edition)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S.E.E.K.E.R v12.0 - Ultimate Recon</title>
    <!-- Dependencies -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --brand-color: #14b8a6; /* Teal */
            --brand-glow: #0d9488;
            --finance-gold: #f59e0b;
            --statement-white: #f1f5f9;
            --secret-red: #ef4444;
            --social-pink: #ec4899;
            --file-blue: #3b82f6;
            --vuln-orange: #f97316;
            --media-purple: #d946ef;
            --system-green: #22c55e; /* New System/Linux Color */
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
        }
        body {
            background-color: var(--bg-dark);
            color: #cbd5e1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-image: radial-gradient(#334155 1px, transparent 1px);
            background-size: 30px 30px;
        }
        .navbar {
            background: rgba(15, 23, 42, 0.95);
            border-bottom: 1px solid #1e293b;
            backdrop-filter: blur(10px);
        }
        .brand-logo {
            font-weight: 800;
            color: var(--brand-color);
            letter-spacing: 1px;
            font-size: 1.5rem;
        }
        .search-hero {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 10px 40px -10px rgba(20, 184, 166, 0.2);
        }
        .form-label {
            color: #94a3b8;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        .form-control, .form-select {
            background: #020617;
            border: 1px solid #334155;
            color: white;
            font-family: 'Courier New', monospace;
            padding: 12px;
        }
        .form-control:focus, .form-select:focus {
            background: #020617;
            color: white;
            border-color: var(--brand-color);
            box-shadow: 0 0 0 0.25rem rgba(20, 184, 166, 0.25);
        }
        .btn-scan {
            background: var(--brand-color);
            border: none;
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .btn-scan:hover {
            background: var(--brand-glow);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(20, 184, 166, 0.3);
        }
        
        /* Category Headers */
        .category-header {
            color: var(--brand-color);
            border-bottom: 2px solid #334155;
            padding-bottom: 10px;
            margin-bottom: 20px;
            margin-top: 40px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Cards */
        .dork-card {
            background: var(--card-bg);
            border: 1px solid #334155;
            border-radius: 10px;
            transition: all 0.2s ease;
            height: 100%;
            position: relative;
        }
        .dork-card:hover {
            transform: translateY(-5px);
            border-color: var(--brand-color);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        /* Context Colors */
        .card-finance { border-top: 4px solid var(--finance-gold); }
        .card-statement { border-top: 4px solid var(--statement-white); }
        .card-secret { border-top: 4px solid var(--secret-red); }
        .card-social { border-top: 4px solid var(--social-pink); }
        .card-files { border-top: 4px solid var(--file-blue); }
        .card-vuln { border-top: 4px solid var(--vuln-orange); }
        .card-media { border-top: 4px solid var(--media-purple); }
        .card-system { border-top: 4px solid var(--system-green); }

        .dork-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 10px;
        }
        .dork-code {
            background: #020617;
            padding: 10px;
            border-radius: 6px;
            color: #5eead4;
            font-family: 'Courier New', monospace;
            font-size: 0.75rem;
            word-break: break-all;
            margin-bottom: 15px;
            border-left: 3px solid #334155;
        }
        .badge-count {
            background: #334155;
            color: white;
            font-size: 0.7rem;
            padding: 4px 10px;
            border-radius: 12px;
            margin-left: auto;
        }

        /* Filters */
        .filter-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }
        .btn-filter {
            background: transparent;
            border: 1px solid #334155;
            color: #94a3b8;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 0.85rem;
        }
        .btn-filter:hover, .btn-filter.active {
            background: var(--brand-color);
            color: white;
            border-color: var(--brand-color);
        }
        /* Specific filter active colors */
        .btn-filter.finance-filter.active { background: var(--finance-gold); border-color: var(--finance-gold); color: black; }
        .btn-filter.secret-filter.active { background: var(--secret-red); border-color: var(--secret-red); }
        .btn-filter.social-filter.active { background: var(--social-pink); border-color: var(--social-pink); }
        .btn-filter.files-filter.active { background: var(--file-blue); border-color: var(--file-blue); }
        .btn-filter.vuln-filter.active { background: var(--vuln-orange); border-color: var(--vuln-orange); }
        .btn-filter.media-filter.active { background: var(--media-purple); border-color: var(--media-purple); }
        .btn-filter.system-filter.active { background: var(--system-green); border-color: var(--system-green); }
    </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    <div class="container">
        <a class="navbar-brand brand-logo" href="#">
            <i class="fas fa-terminal"></i> S.E.E.K.E.R <span class="badge bg-secondary fs-6 align-middle">v12.0</span>
        </a>
    </div>
</nav>

<div class="container py-5">
    
    <!-- SEARCH HERO -->
    <div class="row justify-content-center mb-5">
        <div class="col-lg-10">
            <div class="search-hero">
                <form method="POST" action="/" id="scanForm">
                    <div class="row g-3">
                        <!-- DOMAIN -->
                        <div class="col-md-5">
                            <label class="form-label">TARGET DOMAIN</label>
                            <input type="text" name="domain" class="form-control form-control-lg" 
                                   placeholder="e.g. ubuntu.com" value="{{ domain }}" required>
                        </div>
                        
                        <!-- YEAR (TIME TRAVEL) -->
                        <div class="col-md-3">
                            <label class="form-label"><i class="far fa-calendar-alt"></i> FISCAL YEAR</label>
                            <select name="year" class="form-select form-select-lg">
                                <option value="any" {% if year == 'any' %}selected{% endif %}>All Time</option>
                                <option value="2026" {% if year == '2026' %}selected{% endif %}>2026</option>
                                <option value="2025" {% if year == '2025' %}selected{% endif %}>2025</option>
                                <option value="2024" {% if year == '2024' %}selected{% endif %}>2024</option>
                                <option value="2023" {% if year == '2023' %}selected{% endif %}>2023</option>
                            </select>
                        </div>

                        <!-- TECH -->
                        <div class="col-md-2">
                            <label class="form-label"><i class="fas fa-code"></i> STACK</label>
                            <select name="tech" class="form-select form-select-lg">
                                <option value="general" {% if tech == 'general' %}selected{% endif %}>General</option>
                                <option value="php" {% if tech == 'php' %}selected{% endif %}>PHP</option>
                                <option value="python" {% if tech == 'python' %}selected{% endif %}>Python</option>
                                <option value="node" {% if tech == 'node' %}selected{% endif %}>NodeJS</option>
                                <option value="asp" {% if tech == 'asp' %}selected{% endif %}>ASP.NET</option>
                            </select>
                        </div>

                        <!-- BUTTON -->
                        <div class="col-md-2">
                            <label class="form-label">&nbsp;</label>
                            <button type="submit" class="btn btn-scan btn-lg w-100 h-50">SCAN</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    {% if domain %}
    <!-- CONTROLS & FILTERS -->
    <div class="filter-container mb-4">
        <button type="button" class="btn btn-filter active" onclick="filterCards('all')">All</button>
        <button type="button" class="btn btn-filter system-filter" onclick="filterCards('system')"><i class="fas fa-cogs"></i> System & Bin</button>
        <button type="button" class="btn btn-filter finance-filter" onclick="filterCards('finance')"><i class="fas fa-chart-line"></i> Finance</button>
        <button type="button" class="btn btn-filter" onclick="filterCards('statement')"><i class="fas fa-file-invoice"></i> Statements</button>
        <button type="button" class="btn btn-filter media-filter" onclick="filterCards('media')"><i class="fas fa-photo-video"></i> Media</button>
        <button type="button" class="btn btn-filter secret-filter" onclick="filterCards('secret')"><i class="fas fa-user-secret"></i> Confidential</button>
        <button type="button" class="btn btn-filter social-filter" onclick="filterCards('social')"><i class="fas fa-users"></i> Social</button>
        <button type="button" class="btn btn-filter files-filter" onclick="filterCards('files')"><i class="fas fa-file-code"></i> Files</button>
        <button type="button" class="btn btn-filter" onclick="filterCards('cloud')"><i class="fas fa-cloud"></i> Cloud</button>
        <button type="button" class="btn btn-filter vuln-filter" onclick="filterCards('vuln')"><i class="fas fa-bug"></i> Vulns</button>
    </div>
    
    <div class="d-flex justify-content-end mb-4">
        <form action="/download" method="POST">
            <input type="hidden" name="domain" value="{{ domain }}">
            <input type="hidden" name="tech" value="{{ tech }}">
            <input type="hidden" name="year" value="{{ year }}">
            <button class="btn btn-outline-light btn-sm" type="submit"><i class="fas fa-download"></i> Export JSON</button>
        </form>
    </div>

    <!-- GRID -->
    <div class="row">
        {% for category, dorks in all_dorks.items() %}
        <div class="col-12 filter-section" data-cat="{{ category_slugs[category] }}">
            <div class="category-header">
                <i class="{{ category_icons[category] }}"></i> {{ category }} 
                <span class="badge-count">{{ dorks|length }} checks</span>
            </div>
            <div class="row g-3">
                {% for dork in dorks %}
                <div class="col-md-6 col-lg-4 col-xl-3">
                    <div class="dork-card p-3 {{ dork.style_class }}">
                        <div class="dork-title">{{ dork.title }}</div>
                        <div class="dork-code">{{ dork.query }}</div>
                        <div class="d-flex gap-2">
                            <a href="{{ dork.link }}" target="_blank" class="btn btn-sm btn-outline-light flex-grow-1">
                                <i class="fab fa-google"></i> Check
                            </a>
                            <button class="btn btn-sm btn-outline-secondary" onclick="copyText('{{ dork.query | replace("'", "\\'") }}')">
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

    <!-- CUSTOM BUILDER -->
    <div class="row mt-5">
        <div class="col-12">
            <div class="card bg-dark border-secondary">
                <div class="card-header border-secondary text-white">
                    <i class="fas fa-wrench"></i> Custom Dork Builder
                </div>
                <div class="card-body">
                    <div class="input-group">
                        <span class="input-group-text bg-dark text-light border-secondary">site:{{ domain }}</span>
                        <input type="text" id="customDorkInput" class="form-control bg-dark text-light border-secondary" placeholder='ext:sh "install"'>
                        <button class="btn btn-light" onclick="launchCustomDork('{{ domain }}')">Search</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endif %}

    <footer class="text-center mt-5 text-muted small pb-4">
        <p>⚠️ <strong>Disclaimer:</strong> This tool aggregates public search operators. Do not use for unauthorized scanning.</p>
    </footer>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    function copyText(text) {
        navigator.clipboard.writeText(text);
    }

    function filterCards(category) {
        let sections = document.querySelectorAll('.filter-section');
        let buttons = document.querySelectorAll('.btn-filter');
        buttons.forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');

        sections.forEach(sec => {
            if(category === 'all' || sec.getAttribute('data-cat') === category) {
                sec.style.display = 'block';
            } else {
                sec.style.display = 'none';
            }
        });
    }

    function launchCustomDork(domain) {
        let input = document.getElementById('customDorkInput').value;
        let query = `site:${domain} ${input}`;
        let url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
        window.open(url, '_blank');
    }
</script>
</body>
</html>
"""

# ==========================================
# 🧠 INTELLIGENCE ENGINE (v12.0)
# ==========================================
def generate_advanced_dorks(domain, tech="general", year="any"):
    def g_url(q): return f"https://www.google.com/search?q={urllib.parse.quote(q)}"
    
    def append_year(query):
        if year != "any":
            return f"{query} \"{year}\""
        return query

    # --- 1. SYSTEM & BINARIES (NEW FEATURE) ---
    system_dorks = [
        {"title": "Executables/Binaries", "query": f"site:{domain} ext:sh | ext:bin | ext:run | ext:elf"},
        {"title": "Shared Libraries", "query": f"site:{domain} ext:so | ext:dll"},
        {"title": "Archives (Compressed)", "query": f"site:{domain} ext:tar | ext:gz | ext:tgz | ext:zip | ext:7z | ext:rar | ext:xz | ext:bz2"},
        {"title": "System Configs", "query": f"site:{domain} ext:conf | ext:cfg | ext:ini | ext:yaml | ext:yml | ext:json"},
        {"title": "Core System Files", "query": f"site:{domain} inurl:\"/etc/passwd\" | inurl:\"/etc/shadow\" | inurl:\"/etc/group\" | inurl:\"/etc/hosts\""},
        {"title": "Backup Extensions", "query": f"site:{domain} ext:bak | ext:old | ext:swp | ext:save"},
    ]

    # --- 2. MEDIA & RECORDINGS ---
    media_dorks = [
        {"title": "Common Video Files", "query": f"site:{domain} ext:mp4 | ext:m4v | ext:mov | ext:avi | ext:wmv"},
        {"title": "High-Res/Web Video", "query": f"site:{domain} ext:mkv | ext:webm | ext:mpg | ext:mpeg"},
        {"title": "Meeting Recordings", "query": f"site:{domain} \"recording\" | \"meeting\" | \"zoom\" | \"teams\" ext:mp4 | ext:mov | ext:m4a"},
        {"title": "Common Audio Files", "query": f"site:{domain} ext:mp3 | ext:aac | ext:wma | ext:m4a"},
        {"title": "Lossless/HQ Audio", "query": f"site:{domain} ext:wav | ext:flac"},
    ]

    # --- 3. STATEMENTS & BILLING ---
    statement_dorks = [
        {"title": "Bank Statements", "query": f"site:{domain} \"Bank Statement\" | \"Account Statement\" ext:pdf"},
        {"title": "Credit Card Statements", "query": f"site:{domain} \"Credit Card Statement\" | \"Visa Statement\" | \"Mastercard\" ext:pdf"},
        {"title": "Invoices & Bills", "query": f"site:{domain} \"Invoice\" | \"Bill To\" | \"Amount Due\" ext:pdf"},
        {"title": "Tax Documents", "query": f"site:{domain} \"Tax Return\" | \"W-2\" | \"1099\" | \"VAT\" ext:pdf"},
        {"title": "Payroll/Salary", "query": f"site:{domain} \"Payroll\" | \"Payslip\" | \"Salary\" | \"Compensation\" ext:pdf | ext:xls"},
    ]

    # --- 4. FINANCE & BUSINESS ---
    finance_dorks = [
        {"title": "Core Financials (Assets/Rev)", "query": f"site:{domain} \"Assets\" | \"Liabilities\" | \"Equity\" | \"Revenue\" | \"Profit\" ext:pdf | ext:xls | ext:xlsx"},
        {"title": "Cash Flow & Budgets", "query": f"site:{domain} \"Cash Flow\" | \"Budget\" | \"Interest Rate\" | \"Debt\" ext:pdf | ext:xls | ext:xlsx"},
        {"title": "Accounting Docs", "query": f"site:{domain} \"Balance Sheet\" | \"Income Statement\" | \"Accounts Payable\" | \"Accounts Receivable\""},
        {"title": "Business Operations", "query": f"site:{domain} \"ROI\" | \"Capital Budgeting\" | \"Mergers and acquisitions\" | \"Compliance\""},
        {"title": "Investment Instruments", "query": f"site:{domain} \"Stock market\" | \"Shares\" | \"Bonds\" | \"Mutual funds\" | \"Venture capital\""},
        {"title": "Personal Finance Services", "query": f"site:{domain} \"Financial advisor\" | \"Wealth management\" | \"Mortgage\" | \"Loans\" | \"Retirement planning\""},
    ]

    # --- 5. CONFIDENTIAL & SECRETS ---
    secret_dorks = [
        {"title": "Classification Markers", "query": f"site:{domain} \"Confidential\" | \"Internal use only\" | \"Not for distribution\" | \"Top Secret\""},
        {"title": "Sensitive Data Types", "query": f"site:{domain} \"Social Security number\" | \"Trade secrets\" | \"NDA\" | \"Medical records\" | \"Patient data\""},
        {"title": "Legal & Employee", "query": f"site:{domain} \"Employee information\" | \"Financial projections\" | \"Legal documents\" | \"Patents\""},
        {"title": "Encryption & Security", "query": f"site:{domain} \"Searchable encryption\" | \"Trapdoor\" | \"Cryptanalysis\" | \"Access control\" | \"TEE\""},
        {"title": "Privacy Preserving", "query": f"site:{domain} \"Attribute-based search\" | \"Keyword privacy\" | \"Secret sharing\""},
    ]

    # --- 6. SOCIAL & ACCESS ---
    social_dorks = [
        {"title": "Admin Portals", "query": f"site:{domain} inurl:admin | inurl:login | inurl:portal | inurl:cpanel | inurl:signin"},
        {"title": "User Registration", "query": f"site:{domain} inurl:register | inurl:signup | inurl:create-account"},
        {"title": "Internal Email Lists", "query": f"site:{domain} inurl:email | inurl:contact | inurl:directory"}, 
        {"title": "Linkedin Employees", "query": f"site:linkedin.com/in/ \"{domain}\""},
        {"title": "Twitter Mentions", "query": f"site:twitter.com \"{domain}\""},
        {"title": "Facebook Posts", "query": f"site:facebook.com \"{domain}\""},
        {"title": "Subdomains (Minus WWW)", "query": f"site:*.{domain} -site:www.{domain}"},
    ]

    # --- 7. CRITICAL FILES ---
    files_dorks = [
        {"title": "Database Dumps", "query": f"site:{domain} ext:sql | ext:dbf | ext:mdb | ext:dump"},
        {"title": "Log Files", "query": f"site:{domain} ext:log | intext:\"Error Log\""},
        {"title": "Git Folders", "query": f"site:{domain} inurl:/.git"},
        {"title": "Public RSA Keys", "query": f"site:{domain} ext:pem | ext:key | ext:pub"},
        {"title": "Sensitive Docs (PDF/XLS)", "query": f"site:{domain} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:ppt | ext:pptx | ext:csv"},
        {"title": "Wordpress Backup", "query": f"site:{domain} inurl:wp-content/uploads/ ext:zip"},
        {"title": "NPM/Yarn Locks", "query": f"site:{domain} inurl:package-lock.json | inurl:yarn.lock"},
        {"title": "Docker/Compose", "query": f"site:{domain} inurl:docker-compose.yml | inurl:Dockerfile"},
    ]

    # --- 8. CLOUD & INFRA ---
    cloud_dorks = [
        {"title": "AWS S3 Buckets", "query": f"site:s3.amazonaws.com | site:storage.googleapis.com | site:blob.core.windows.net \"{domain}\""},
        {"title": "DigitalOcean Spaces", "query": f"site:digitaloceanspaces.com \"{domain}\""},
        {"title": "Firebase Configs", "query": f"site:firebaseio.com \"{domain}\""},
        {"title": "Exposed FTP", "query": f"site:{domain} inurl:ftp | inurl:\"ftp://\""},
        {"title": "Heroku Apps", "query": f"site:herokuapp.com \"{domain}\""},
        {"title": "Code Pen Snippets", "query": f"site:codepen.io \"{domain}\""},
        {"title": "JSFiddle Snippets", "query": f"site:jsfiddle.net \"{domain}\""},
        {"title": "Pastebin Leaks", "query": f"site:pastebin.com \"{domain}\""},
    ]

    # --- 9. VULNERABILITY HINTS ---
    vuln_dorks = [
        {"title": "Directory Listing", "query": f"site:{domain} intitle:\"index of\""},
        {"title": "SQL Errors", "query": f"site:{domain} intext:\"sql syntax near\" | intext:\"syntax error has occurred\" | intext:\"incorrect syntax near\""},
        {"title": "PHP Errors", "query": f"site:{domain} \"Fatal error:\" | \"Warning: include()\""},
        {"title": "Open Redirects", "query": f"site:{domain} inurl:redir | inurl:url= | inurl:redirect= | inurl:return= | inurl:src=http"},
        {"title": "SQLi Params (ID)", "query": f"site:{domain} inurl:id= | inurl:pid= | inurl:category= | inurl:cat= | inurl:action="},
        {"title": "XSS Vectors", "query": f"site:{domain} inurl:q= | inurl:s= | inurl:search= | inurl:query= | inurl:keyword="},
        {"title": "Apache Status", "query": f"site:{domain} intitle:\"Apache Status\" | intitle:\"Apache Server Status\""},
        {"title": "Jira Dashboard", "query": f"site:{domain} inurl:/Dashboard.jspa"},
    ]
    
    # --- 10. IOT & DEVICES ---
    iot_dorks = [
        {"title": "Exposed Webcams", "query": f"site:{domain} intitle:\"webcam 7\" | intitle:\"Network Camera\" | intitle:\"ip camera\""},
        {"title": "Printers & Scanners", "query": f"site:{domain} intitle:\"printer status\" | inurl:printer/main.html"},
    ]

    # --- APPLY YEAR FILTER TO RELEVANT CATEGORIES ---
    for d in statement_dorks: d['query'] = append_year(d['query'])
    for d in finance_dorks: d['query'] = append_year(d['query'])
    for d in secret_dorks: d['query'] = append_year(d['query'])
    # Meeting recordings also often need a year
    for d in media_dorks: 
        if "Meeting" in d['title']:
            d['query'] = append_year(d['query'])
    # Only apply year to "Docs" in files
    for d in files_dorks: 
        if "Docs" in d['title']:
            d['query'] = append_year(d['query'])

    # --- TECH STACK LOGIC ---
    if tech == "php":
        vuln_dorks.insert(0, {"title": "PHP Info", "query": f"site:{domain} ext:php intitle:phpinfo"})
    elif tech == "python":
        vuln_dorks.insert(0, {"title": "Django Debug", "query": f"site:{domain} \"DisallowedHost\" debug"})
    elif tech == "asp":
        vuln_dorks.insert(0, {"title": "IIS Errors", "query": f"site:{domain} \"Server Error in '/' Application\""})

    # --- STYLING METADATA ---
    for d in system_dorks: d['style_class'] = "card-system"
    for d in statement_dorks: d['style_class'] = "card-statement"
    for d in finance_dorks: d['style_class'] = "card-finance"
    for d in secret_dorks: d['style_class'] = "card-secret"
    for d in social_dorks: d['style_class'] = "card-social"
    for d in files_dorks: d['style_class'] = "card-files"
    for d in vuln_dorks: d['style_class'] = "card-vuln"
    for d in media_dorks: d['style_class'] = "card-media"
    
    for d in cloud_dorks + iot_dorks: 
        if 'style_class' not in d: d['style_class'] = ""

    # Generate Links
    all_lists = system_dorks + media_dorks + statement_dorks + finance_dorks + secret_dorks + social_dorks + files_dorks + cloud_dorks + vuln_dorks + iot_dorks
    for d in all_lists:
        d['link'] = g_url(d['query'])

    return {
        "System & Archives": system_dorks,
        "Media & Recordings": media_dorks,
        "Statements & Billing": statement_dorks,
        "Finance & Business": finance_dorks,
        "Confidential & Secrets": secret_dorks,
        "Social & Access": social_dorks,
        "Critical Files": files_dorks,
        "Cloud & Infra": cloud_dorks,
        "Vulnerability Hints": vuln_dorks,
        "IoT & Devices": iot_dorks
    }

# ==========================================
# 🚦 ROUTING
# ==========================================
@app.route('/', methods=['GET', 'POST'])
def home():
    domain = ""
    tech = "general"
    year = "any"
    all_dorks = {}
    
    category_slugs = {
        "System & Archives": "system",
        "Media & Recordings": "media",
        "Statements & Billing": "statement",
        "Finance & Business": "finance",
        "Confidential & Secrets": "secret",
        "Social & Access": "social",
        "Critical Files": "files",
        "Cloud & Infra": "cloud",
        "Vulnerability Hints": "vuln",
        "IoT & Devices": "iot"
    }
    
    category_icons = {
        "System & Archives": "fas fa-cogs",
        "Media & Recordings": "fas fa-photo-video",
        "Statements & Billing": "fas fa-file-invoice-dollar",
        "Finance & Business": "fas fa-chart-line",
        "Confidential & Secrets": "fas fa-user-secret",
        "Social & Access": "fas fa-users",
        "Critical Files": "fas fa-file-code",
        "Cloud & Infra": "fas fa-cloud",
        "Vulnerability Hints": "fas fa-bug",
        "IoT & Devices": "fas fa-wifi"
    }

    if request.method == 'POST':
        raw = request.form.get('domain', '').strip()
        tech = request.form.get('tech', 'general')
        year = request.form.get('year', 'any')
        
        if raw:
            domain = raw.replace("https://", "").replace("http://", "").replace("www.", "").split('/')[0]
            all_dorks = generate_advanced_dorks(domain, tech, year)
            
    return render_template_string(HTML_TEMPLATE, 
                                  domain=domain, 
                                  tech=tech,
                                  year=year,
                                  all_dorks=all_dorks, 
                                  category_slugs=category_slugs,
                                  category_icons=category_icons)

@app.route('/download', methods=['POST'])
def download():
    domain = request.form.get('domain', '').strip()
    tech = request.form.get('tech', 'general')
    year = request.form.get('year', 'any')
    if domain:
        data = generate_advanced_dorks(domain, tech, year)
        return Response(
            json.dumps(data, indent=4),
            mimetype="application/json",
            headers={"Content-disposition": f"attachment; filename={domain}_{year}_audit.json"}
        )
    return "{}"

if __name__ == '__main__':
    print("-------------------------------------------------------")
    print("🚀 S.E.E.K.E.R v12.0 (System Edition) Running")
    print("👉 Open Browser: http://127.0.0.1:5000")
    print("-------------------------------------------------------")
    app.run(debug=True, port=5000)
