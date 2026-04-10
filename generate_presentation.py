import json
import os

def generate_html(women_no_beard=[], men_with_beard=[]):
    try:
        with open('beard_stats.json', 'r') as f:
            data = json.load(f)
        with open('mp_names.json', 'r', encoding='utf-8') as f:
            names = json.load(f)
    except FileNotFoundError:
        print("Error: Required JSON files not found. Run analysis/mapping first.")
        return

    details = data['details']
    
    processed_details = []
    stats = {"with_beard": 0, "without_beard": 0}

    for item in details:
        img_name = item['image']
        if not os.path.exists(os.path.join('mp_images', img_name)):
            continue
            
        mp_id = img_name.split('_')[0]
        # Use provided ID 313 name if name is missing from mapping
        original_name = names.get(mp_id, f"MP {mp_id}")
        
        is_beard = item['label'] == 'a person with a beard'
        
        # Check against manual overrides (using exact matches)
        if original_name in women_no_beard or f"MP {mp_id}" in women_no_beard:
            is_beard = False
        if original_name in men_with_beard:
            is_beard = True

        processed_details.append({
            "image": img_name,
            "name": original_name if original_name != f"MP 313" else "Oana-Silvia Ţoiu (MP 313)",
            "is_beard": is_beard
        })
        
        if is_beard:
            stats["with_beard"] += 1
        else:
            stats["without_beard"] += 1

    processed_details.sort(key=lambda x: x['name'])

    html_content = f"""
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistici Barbă Parlamentari</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
            color: #1c1e21;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}
        h1 {{ text-align: center; color: #1a73e8; margin-bottom: 10px; }}
        h2 {{ text-align: center; color: #5f6368; font-weight: 400; margin-bottom: 40px; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e8eaed;
        }}
        .stat-item {{ text-align: center; }}
        .stat-value {{ font-size: 2.8em; font-weight: bold; color: #1967d2; display: block; }}
        .stat-label {{ color: #70757a; font-size: 1.1em; }}

        .filters {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 40px;
            position: sticky;
            top: 10px;
            z-index: 100;
        }}
        .filter-btn {{
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            background: #fff;
            color: #5f6368;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s;
            border: 1px solid #dadce0;
        }}
        .filter-btn.active {{
            background: #1a73e8 !important;
            color: white !important;
            border-color: #1a73e8 !important;
        }}
        .filter-btn:hover:not(.active) {{
            background: #f1f3f4;
        }}

        .mp-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 25px;
        }}
        .mp-card {{
            background: white;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            border: 1px solid #e8eaed;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .mp-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .mp-card img {{
            width: 100%;
            aspect-ratio: 1/1.2;
            object-fit: cover;
            border-radius: 6px;
            margin-bottom: 12px;
        }}
        .mp-name {{
            font-size: 0.9em;
            font-weight: 600;
            color: #202124;
            display: block;
            height: 2.4em;
            line-height: 1.2em;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}
        
        .hidden {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Analiză Parlamentari România</h1>
        <h2>Statistici prezenţă barbă (Legislatura 2024-2028)</h2>
        
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-value">{stats['with_beard'] + stats['without_beard']}</span>
                <span class="stat-label">Total Analizaţi</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{stats['with_beard']}</span>
                <span class="stat-label">Cu Barbă</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{stats['without_beard']}</span>
                <span class="stat-label">Fără Barbă</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{((stats['with_beard'] / (stats['with_beard'] + stats['without_beard'])) * 100):.1f}%</span>
                <span class="stat-label">Rată Barbă</span>
            </div>
        </div>

        <div class="filters">
            <button class="filter-btn active" onclick="applyFilter('all', this)">Toţi</button>
            <button class="filter-btn" onclick="applyFilter('beard', this)">Cu Barbă</button>
            <button class="filter-btn" onclick="applyFilter('nobeard', this)">Fără Barbă</button>
        </div>

        <div class="mp-grid" id="mpGrid">
"""

    for mp in processed_details:
        beard_attr = "true" if mp['is_beard'] else "false"
        html_content += f"""            <div class="mp-card" data-beard="{beard_attr}">
                <img src="mp_images/{mp['image']}" loading="lazy">
                <span class="mp-name">{mp['name']}</span>
            </div>\n"""

    html_content += """
        </div>
    </div>

    <script>
        function applyFilter(type, btnElement) {
            const cards = document.querySelectorAll('.mp-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update button styles
            buttons.forEach(btn => btn.classList.remove('active'));
            btnElement.classList.add('active');

            // Show/Hide cards
            cards.forEach(card => {
                if (type === 'all') {
                    card.classList.remove('hidden');
                } else if (type === 'beard') {
                    if (card.getAttribute('data-beard') === 'true') {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                } else if (type === 'nobeard') {
                    if (card.getAttribute('data-beard') === 'false') {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

    with open('presentation.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Presentation fixed and regenerated.")

if __name__ == "__main__":
    # Names exactly as they appear in mp_names.json
    WOMEN_NO_BEARD = [
        "Aurora-Tasica Simu", "Ancuþa-Florina Irimia", "Bianca-Eugenia Gavrilã",
        "Codruþa-Maria Corcheº", "Cristina-Irina Buturã", "Dumitriþa Albu",
        "Lidia Vadim-Tudor", "Oana-Silvia Þoiu", "Mariana Vârgã", "Pollyanna-Hanellore Hangan",
        "Gabriela Porumboiu", "Brigitta-Eva Zahoranszki", "Mirela Elena Adomnicãi",
        "Ana-Marcela Baº", "Monica-Elena Berescu", "Rozália-Ibolya Biró",
        "Ramona-Ioana Bruynseels", "Ariana-Oana Bucur", "Simona Bucura-Oprescu",
        "Maria Cernit", "Crina-Fiorela Chilat", "Doiniþa Ciocan",
        "Andreea-Petronela Cîmpianu", "Ariadna-Elena Cîrligeanu", "Andra-Claudia Constantinescu",
        "Éva-Andrea Csép", "Cristina-Emanuela Dascãlu", "Diana Enache",
        "Raisa Enachi", "Gabriela-Corina Ene", "Mirela Furtunã",
        "Anamaria Gavrilã", "Graþiela Leocadia Gavrilescu", "Aurora-Adela Geamãnu",
        "Laura Gherasim", "Dumitriþa Gliga", "Alina-ªtefania Gorghiu",
        "Ioana Grosaru", "Veronica Grosu", "Georgeta-Carmen Holban",
        "Monica Iagãr", "Natalia-Elena Intotero", "Ancuþa-Florina Irimia",
        "Boglárka Kántor", "Elisabeta Lipã", "Ramona Lovin",
        "Simona-Elena Macovei Ilie", "Aneta Matei", "Mirela-Florenþa Matichescu",
        "Silvia-Claudia Mihalcea", "Dumitrina Mitrea", "Patricia-Simina-Arina Moº",
        "Oana Murariu", "Rodica Nassar", "Andreea-Firuþa Neacºu",
        "Eliza-Mãdălina Peþa-ªtefãnescu", "Simona-Geanina Pistru-Popa", "Rodica Plopeanu",
        "Ionelia-Florenþa Priescu", "Cristina-Mãdălina Prunã", "Ana-Smaranda Rinder",
        "Viorica Sandu", "Vetuþa Stãnescu", "Irina-Florentina Stoenicã",
        "Diana Stoica", "Ecaterina-Mariana Szõke", "Gianina ªerban",
        "Elena-Laura Toader", "Raluca Turcan", "Adriana Diana Tuºa",
        "Verginia Vedinaº", "Diana-Anda Buzoianu", "MP 313"
    ]
    
    MEN_WITH_BEARD = [
        "Iusein Ibram",
        "Cosmin-Ioan Corendea", "Csaba Könczei",
        "Alexandru Bordian", "Alin-Bogdan Stoica",
        "Andrei Csillag", "Alexandrin Moiseev", "Alexandru Rafila", "Alexandru-Florin Rogobete",
        "Alexandru-Ioan Andrei", "Alexandru-Mihai Ghigiu", "Adrian Wiener", "Bogdan-Florian Mihuþi",
        "Cosmin Hristu", "Cãlin-Florin Groza", "Cãlin-Gheorghe Matieº", "Cãtãlin Drulã",
        "Dan Tanasã", "Daniel-Rãzvan Biro", "Dorin Popa", "Dragoº-Florin Coman",
        "Eduard-Tatian Mititelu", "Fabian-Cristian Radu", "George-Adrian Popa", "Gheorghe-Petru Pîcliºan",
        "Ion-Marcel Ciolacu", "Laurenþiu Adrian Neculaescu", "Loránd-Bálint Magyar", "Marius-Felix Bulearcã",
        "Maricel Popa", "Mihai-Adrian Enache", "Mihai-Cosmin Pascariu", "Mihai-Cãtãlin Botez",
        "Miticã-Marius Mãrgãrit", "Ovidiu-Romulus Paraschivescu", "Paul-Claudiu Cotîrleþ", "Petre-Florin Manole",
        "Robert Alecu", "Remus-Gabriel Mihalcea", "Silviu-Florin Oancea", "Tiberiu-Claudiu Barstan",
        "Vlad-Ioan ªendroiu", "Vlad-Florentin Drinceanu"
    ]
    
    generate_html(WOMEN_NO_BEARD, MEN_WITH_BEARD)
