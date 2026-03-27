import csv
import random
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "foods.csv")

def load_csv_data():
    """Loads all food data from the CSV file."""
    foods = []
    try:
        with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                foods.append(row)
    except Exception as e:
        print(f"Error loading local CSV: {e}")
    return foods

def search_food(query):
    """Searches for food items matching the query string."""
    foods = load_csv_data()
    if not query:
        return []
    query = query.lower()
    results = [f for f in foods if query in f['Food Items'].lower()]
    return results[:10]

def _parse_keywords(text):
    """Split a multi-line or comma-separated profile field into lowercase keywords."""
    keywords = []
    for part in text.replace('\n', ',').split(','):
        kw = part.strip().lower()
        if kw:
            keywords.append(kw)
    return keywords

def get_profile_meals(health_profile, count=21):
    """
    Returns meals filtered and scored intelligently based on the full user health profile.
    Considers: goals, conditions, preferences, restrictions, routines.
    """
    foods = load_csv_data()
    if not foods:
        return []

    goals       = health_profile.get('goals', '').lower()
    conditions  = health_profile.get('conditions', '').lower()
    prefs       = _parse_keywords(health_profile.get('preferences', ''))
    restrictions = _parse_keywords(health_profile.get('restrictions', ''))
    routines    = health_profile.get('routines', '').lower()

    exclusion_map = {
        'dairy':     ['milk', 'cheese', 'paneer', 'curd', 'kheer', 'lassi', 'raita', 'cream', 'butter', 'khoa', 'burfi'],
        'nut':       ['almond', 'cashew', 'walnut', 'peanut', 'nut'],
        'gluten':    ['naan', 'bread', 'roti', 'paratha', 'biscuit', 'cake', 'cookie', 'pizza', 'pasta'],
        'egg':       ['egg', 'omelette', 'scrambled', 'poached', 'boiled egg'],
        'meat':      ['chicken', 'mutton', 'fish', 'prawn', 'keema', 'lamb', 'beef', 'pork'],
        'sugar':     ['cake', 'cookie', 'biscuit', 'halwa', 'ladoo', 'burfi', 'gulab', 'kheer', 'ice cream'],
        'spicy':     ['chilli', 'mirch', 'masala'],
        'vegan':     ['milk', 'cheese', 'paneer', 'curd', 'butter', 'cream', 'egg', 'chicken', 'mutton', 'fish'],
    }

    excluded_terms = []
    for restriction in restrictions:
        for key, terms in exclusion_map.items():
            if key in restriction:
                excluded_terms.extend(terms)

    def is_excluded(food_name_lower):
        return any(term in food_name_lower for term in excluded_terms)

    def score(food):
        name = food['Food Items'].lower()
        try:
            kcal     = float(food['Energy kcal'])
            protein  = float(food['Protein(g)'])
            carbs    = float(food['Carbs'])
            fat      = float(food['Fat(g)'])
            sugar    = float(food['Freesugar(g)'])
            fibre    = float(food['Fibre(g)'])
            calcium  = float(food['Calcium(mg)'])
            chol     = float(food['Cholestrol(mg)'])
        except (ValueError, KeyError):
            return 0

        s = 0

        for pref in prefs:
            if pref in name:
                s += 30

        if any(w in goals for w in ['weight', 'lose', 'fat', 'slim', 'lean']):
            if kcal < 150: s += 20
            if kcal < 250: s += 10
            if fat < 5:    s += 10
            if sugar < 5:  s += 5

        if any(w in goals for w in ['muscle', 'strength', 'build', 'protein', 'gym']):
            if protein > 10: s += 25
            if protein > 7:  s += 10

        if any(w in goals for w in ['heart', 'cardiovascular', 'cholesterol', 'blood pressure']):
            if chol < 30:  s += 20
            if fat < 8:    s += 10
            if fibre > 3:  s += 10

        if any(w in goals for w in ['digest', 'gut', 'fibre', 'bowel']):
            if fibre > 4: s += 20
            if fibre > 2: s += 10

        if any(w in goals for w in ['bone', 'calcium', 'osteo']):
            if calcium > 100: s += 25
            if calcium > 50:  s += 10

        if any(w in goals for w in ['energy', 'stamina', 'endurance', 'performance', 'active']):
            if carbs > 20: s += 15
            if kcal > 150: s += 5

        if any(w in conditions for w in ['diabetes', 'diabetic', 'sugar', 'insulin']):
            if sugar < 3:  s += 25
            if sugar < 8:  s += 10
            if sugar > 15: s -= 30

        if any(w in conditions for w in ['hypertension', 'blood pressure', 'bp']):
            if chol < 20:  s += 15
            if fat < 5:    s += 10

        if any(w in conditions for w in ['anemia', 'iron', 'haemoglobin']):
            if protein > 5: s += 15

        if any(w in conditions for w in ['lactose', 'dairy']):
            is_excluded(name)                                

        if any(w in routines for w in ['run', 'jog', 'cardio', 'walk']):
            if carbs > 25: s += 10
            if kcal < 300: s += 5

        if any(w in routines for w in ['yoga', 'pilates', 'stretch', 'meditat']):
            if kcal < 200: s += 10
            if fibre > 3:  s += 5

        if any(w in routines for w in ['weight', 'gym', 'lift', 'strength train']):
            if protein > 8:  s += 20
            if carbs > 15:   s += 5

        s += random.uniform(0, 5)
        return s

    eligible = [f for f in foods if not is_excluded(f['Food Items'].lower())]
    if not eligible:
        eligible = foods                                   

    scored = sorted(eligible, key=score, reverse=True)

    top_pool = scored[:min(120, len(scored))]
    selected = random.sample(top_pool, min(count, len(top_pool)))

    if len(selected) < count:
        extras = [f for f in scored if f not in selected]
        selected += extras[:count - len(selected)]

    return selected[:count]

def get_random_meals(count=3, preferences=""):
    """Returns random food items, optionally filtered by keywords."""
    foods = load_csv_data()
    if not foods:
        return []

    pref_list = [p.strip().lower() for p in preferences.replace('\n', ',').split(',') if p.strip()]

    if pref_list:
        filtered_foods = []
        for f in foods:
            for pref in pref_list:
                if pref in f['Food Items'].lower():
                    filtered_foods.append(f)
                    break

        if len(filtered_foods) >= count:
            return random.sample(filtered_foods, count)
        elif filtered_foods:
            remaining = count - len(filtered_foods)
            others = [f for f in foods if f not in filtered_foods]
            return filtered_foods + random.sample(others, min(remaining, len(others)))

    return random.sample(foods, min(count, len(foods)))
