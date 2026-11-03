#!/usr/bin/env python3
"""
generate_fl_queries.py - Generates 600+ high-yield Florida Auto Body & Collision search queries
Covering all major Florida metros, suburbs, tourist corridors, and regional industrial hubs.
"""

FLORIDA_CITIES = [
    # --- 1. Miami-Dade County (South Florida Hub) ---
    "Miami", "Hialeah", "Miami Beach", "Homestead", "Coral Gables", "Doral", 
    "North Miami", "Miami Gardens", "Aventura", "North Miami Beach", "South Miami", 
    "Cutler Bay", "Miami Lakes", "Palmetto Bay", "Hialeah Gardens", "Sweetwater", 
    "Opa-locka", "Florida City", "Pinecrest", "Key Biscayne",

    # --- 2. Broward County (Greater Fort Lauderdale) ---
    "Fort Lauderdale", "Pembroke Pines", "Hollywood", "Miramar", "Coral Springs", 
    "Pompano Beach", "Davie", "Sunrise", "Plantation", "Deerfield Beach", "Lauderhill", 
    "Weston", "Tamarac", "Margate", "Coconut Creek", "Oakland Park", "North Lauderdale", 
    "Hallandale Beach", "Lauderdale Lakes", "Dania Beach", "Cooper City", "Parkland", 
    "Wilton Manors",

    # --- 3. Palm Beach County & Treasure Coast ---
    "West Palm Beach", "Boca Raton", "Boynton Beach", "Delray Beach", "Wellington", 
    "Jupiter", "Palm Beach Gardens", "Greenacres", "Lake Worth", "Royal Palm Beach", 
    "Riviera Beach", "Palm Springs", "Belle Glade", "North Palm Beach", "Lantana", 
    "Port St. Lucie", "Fort Pierce", "Stuart", "Jensen Beach", "Vero Beach", "Sebastian",

    # --- 4. Tampa Bay Area & Central West Coast ---
    "Tampa", "St. Petersburg", "Clearwater", "Brandon", "Largo", "Pinellas Park", 
    "Dunedin", "Tarpon Springs", "Palm Harbor", "Safety Harbor", "Plant City", 
    "Temple Terrace", "Riverview", "Valrico", "Wesley Chapel", "Land O Lakes", 
    "New Port Richey", "Port Richey", "Spring Hill", "Brooksville", "Zephyrhills",

    # --- 5. Greater Orlando & Central Florida ---
    "Orlando", "Kissimmee", "Sanford", "Altamonte Springs", "Apopka", "Winter Park", 
    "Ocoee", "Winter Garden", "Oviedo", "Casselberry", "Lake Mary", "Maitland", 
    "Clermont", "Leesburg", "Eustis", "Tavares", "Mount Dora", "St. Cloud", 
    "Groveland", "Haines City", "Davenport",

    # --- 6. Polk County (Lakeland / Winter Haven) ---
    "Lakeland", "Winter Haven", "Bartow", "Lake Wales", "Auburndale",

    # --- 7. Sarasota & Manatee Counties ---
    "Sarasota", "Bradenton", "Venice", "North Port", "Lakewood Ranch", "Palmetto", "Englewood",

    # --- 8. Southwest Florida (Fort Myers, Cape Coral, Naples) ---
    "Fort Myers", "Cape Coral", "Lehigh Acres", "Bonita Springs", "Estero", 
    "Naples", "Marco Island", "Immokalee", "Port Charlotte", "Punta Gorda",

    # --- 9. Space Coast & Daytona / Volusia County ---
    "Melbourne", "Palm Bay", "Titusville", "Cocoa", "Rockledge", "Merritt Island", 
    "Cape Canaveral", "Satellite Beach", "Daytona Beach", "Deltona", "Ormond Beach", 
    "DeLand", "Port Orange", "New Smyrna Beach", "Edgewater",

    # --- 10. Greater Jacksonville & Northeast Florida ---
    "Jacksonville", "St. Augustine", "Jacksonville Beach", "Atlantic Beach", 
    "Orange Park", "Middleburg", "Green Cove Springs", "Palm Coast", 
    "Fernandina Beach", "Yulee", "Palatka",

    # --- 11. North Florida & Panhandle ---
    "Tallahassee", "Pensacola", "Panama City", "Panama City Beach", "Fort Walton Beach", 
    "Crestview", "Destin", "Milton", "Niceville", "Lynn Haven", "Gulf Breeze", 
    "Marianna", "Perry",

    # --- 12. North Central Florida (Gainesville & Ocala) ---
    "Gainesville", "Ocala", "Lake City", "The Villages", "Inverness", "Belleview", 
    "Alachua", "Starke",

    # --- 13. Florida Keys ---
    "Key West", "Key Largo", "Marathon", "Islamorada"
]

KEYWORDS = [
    "auto body shop",
    "collision repair",
    "car paint and body",
    "auto collision center"
]

def main():
    seen_cities = set()
    unique_cities = []
    for c in FLORIDA_CITIES:
        if c.lower() not in seen_cities:
            seen_cities.add(c.lower())
            unique_cities.append(c)

    queries = []
    for kw in KEYWORDS:
        for city in unique_cities:
            queries.append(f"{kw} in {city} FL")

    output_path = "queries.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# =====================================================================\n")
        f.write(f"# 🚗 FLORIDA AUTO BODY 10,000+ LEAD GENERATION QUERIES ({len(queries)} Total Searches)\n")
        f.write(f"# Covering {len(unique_cities)} Unique Florida Cities across 4 Keywords\n")
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

    print(f"✅ Generated {len(queries)} Florida Auto Body search queries across {len(unique_cities)} cities in '{output_path}'!")

if __name__ == "__main__":
    main()
