#!/usr/bin/env python3
"""
generate_ca_queries.py - Generates 500+ high-yield California Auto Body & Collision search queries
Covering all major California metros, suburbs, and industrial auto body hubs.
"""

CALIFORNIA_CITIES = [
    # --- 1. Los Angeles County (Major Metros & Auto Repair Hubs) ---
    "Los Angeles", "Long Beach", "Glendale", "Santa Clarita", "Lancaster", "Palmdale", 
    "Pomona", "Torrance", "Pasadena", "El Monte", "Downey", "West Covina", "Inglewood", 
    "Burbank", "Norwalk", "Compton", "Carson", "Santa Monica", "Whittier", "Hawthorne", 
    "Alhambra", "Lakewood", "Bellflower", "Baldwin Park", "Lynwood", "Redondo Beach", 
    "Pico Rivera", "Montebello", "Monterey Park", "Gardena", "Arcadia", "Diamond Bar", 
    "Paramount", "Rosemead", "Glendora", "Covina", "Azusa", "South Gate", "Culver City",

    # --- 2. Orange County ---
    "Anaheim", "Santa Ana", "Irvine", "Huntington Beach", "Garden Grove", "Orange", 
    "Fullerton", "Costa Mesa", "Mission Viejo", "Westminster", "Newport Beach", "Buena Park", 
    "Lake Forest", "Tustin", "Yorba Linda", "San Clemente", "Laguna Niguel", "La Habra", 
    "Fountain Valley", "Placentia", "Brea", "Cypress", "Aliso Viejo", "Rancho Santa Margarita",

    # --- 3. Inland Empire (Riverside & San Bernardino Counties) ---
    "Riverside", "San Bernardino", "Fontana", "Moreno Valley", "Rancho Cucamonga", "Ontario", 
    "Corona", "Victorville", "Temecula", "Murrieta", "Rialto", "Hesperia", "Chino", 
    "Chino Hills", "Indio", "Hemet", "Menifee", "Apple Valley", "Redlands", "Lake Elsinore", 
    "Eastvale", "Colton", "San Jacinto", "Beaumont", "Coachella", "Palm Springs", "Yucaipa", 
    "Highland", "Norco", "Banning", "Cathedral City",

    # --- 4. San Diego County ---
    "San Diego", "Chula Vista", "Oceanside", "Escondido", "Carlsbad", "El Cajon", "Vista", 
    "San Marcos", "Encinitas", "National City", "La Mesa", "Santee", "Poway", "Imperial Beach",

    # --- 5. San Francisco Bay Area & Silicon Valley ---
    "San Jose", "San Francisco", "Oakland", "Fremont", "Sunnyvale", "Hayward", "Santa Clara", 
    "Concord", "Berkeley", "Richmond", "Antioch", "Daly City", "San Mateo", "Vallejo", 
    "Fairfield", "Santa Rosa", "Livermore", "San Leandro", "Redwood City", "Napa", 
    "Mountain View", "Alameda", "San Ramon", "Pleasanton", "Walnut Creek", "Milpitas", 
    "Palo Alto", "Union City", "Pittsburg", "San Rafael", "Petaluma", "Novato", "Cupertino", 
    "Vacaville", "San Bruno", "South San Francisco",

    # --- 6. Central Valley (Sacramento & San Joaquin Valley) ---
    "Sacramento", "Fresno", "Bakersfield", "Stockton", "Modesto", "Elk Grove", "Roseville", 
    "Visalia", "Clovis", "Chico", "Redding", "Merced", "Tracy", "Manteca", "Turlock", 
    "Folsom", "Citrus Heights", "Davis", "Rancho Cordova", "Lodi", "Madera", "Tulare", 
    "Hanford", "Porterville", "Rocklin", "Woodland", "Yuba City", "Delano", "Los Banos",

    # --- 7. Central Coast & Coastal Hubs ---
    "Oxnard", "Thousand Oaks", "Simi Valley", "Ventura", "Santa Maria", "Salinas", 
    "Santa Barbara", "Santa Cruz", "Watsonville", "San Luis Obispo", "Camarillo", "Monterey", 
    "Paso Robles", "Lompoc", "Seaside", "Eureka", "Atascadero"
]

KEYWORDS = [
    "auto body shop",
    "collision repair",
    "car paint and body",
    "auto collision center"
]

def main():
    # Remove duplicates while preserving order
    seen_cities = set()
    unique_cities = []
    for c in CALIFORNIA_CITIES:
        if c.lower() not in seen_cities:
            seen_cities.add(c.lower())
            unique_cities.append(c)

    queries = []
    for kw in KEYWORDS:
        for city in unique_cities:
            queries.append(f"{kw} in {city} CA")

    output_path = "queries.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# =====================================================================\n")
        f.write(f"# 🚗 CALIFORNIA AUTO BODY 10,000+ LEAD GENERATION QUERIES ({len(queries)} Total Searches)\n")
        f.write(f"# Covering {len(unique_cities)} Unique California Cities across 4 Keywords\n")
        f.write("# পাইপলাইন প্রতি ৩টি সার্চের পর ৬০ সেকেন্ড অটোমেটিক বিরতি নেবে (IP সুরক্ষিত রাখতে)।\n")
        f.write("# যেকোনো সময় Ctrl+C দিয়ে থামাতে পারেন, পরে আবার রান করলে আগের ডাটা বজায় থাকবে।\n")
        f.write("# =====================================================================\n\n")
        
        current_kw = None
        for q in queries:
            kw_part = q.split(" in ")[0]
            if kw_part != current_kw:
                current_kw = kw_part
                f.write(f"\n# --- Keyword Group: {current_kw.upper()} ---\n")
            f.write(f"{q}\n")

    print(f"✅ Generated {len(queries)} California Auto Body search queries across {len(unique_cities)} cities in '{output_path}'!")

if __name__ == "__main__":
    main()
