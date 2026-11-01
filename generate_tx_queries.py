#!/usr/bin/env python3
"""
generate_tx_queries.py - Generates 300+ high-yield Texas Auto Body & Collision search queries
"""

TEXAS_CITIES = [
    # Top Metros & Core Cities
    "Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso", "Arlington", "Corpus Christi",
    # DFW Metroplex Suburbs & Hubs
    "Plano", "Irving", "Garland", "Frisco", "McKinney", "Grand Prairie", "Denton", "Carrollton", 
    "Richardson", "Lewisville", "Allen", "Flower Mound", "Grapevine", "Euless", "Bedford", "Hurst",
    "Rowlett", "DeSoto", "Mansfield", "North Richland Hills", "Rockwall", "Coppell", "Cedar Hill", "Mesquite",
    # Greater Houston Area Suburbs
    "Pasadena", "Pearland", "Sugar Land", "The Woodlands", "League City", "Baytown", "Missouri City", 
    "Conroe", "Spring", "Katy", "Cypress", "Tomball", "Humble", "Friendswood", "Atascocita", "Rosenberg",
    # Central Texas & Austin Metro
    "Round Rock", "Killeen", "Waco", "College Station", "Bryan", "Temple", "New Braunfels", 
    "San Marcos", "Cedar Park", "Georgetown", "Pflugerville", "Kyle", "Buda", "Leander", "Harker Heights",
    # West Texas & Panhandle
    "Lubbock", "Amarillo", "Midland", "Odessa", "Abilene", "San Angelo", "Wichita Falls",
    # South Texas & Rio Grande Valley
    "Laredo", "Brownsville", "McAllen", "Edinburg", "Mission", "Pharr", "Harlingen", "Victoria", "Weslaco",
    # East Texas & Gulf Coast
    "Beaumont", "Port Arthur", "Tyler", "Longview", "Lufkin", "Nacogdoches", "Texarkana", "Sherman"
]

KEYWORDS = [
    "auto body shop",
    "collision repair",
    "car paint and body",
    "auto collision center"
]

def main():
    queries = []
    for kw in KEYWORDS:
        for city in TEXAS_CITIES:
            queries.append(f"{kw} in {city} TX")

    output_path = "queries.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# =====================================================================\n")
        f.write(f"# 🚗 TEXAS AUTO BODY 10,000 LEAD GENERATION QUERIES ({len(queries)} Total Searches)\n")
        f.write("# পাইপলাইন প্রতি ৩টি সার্চের পর ৩ মিনিট অটোমেটিক বিরতি নেবে (IP সুরক্ষিত রাখতে)।\n")
        f.write("# যেকোনো সময় Ctrl+C দিয়ে থামাতে পারেন, পরে আবার রান করলে আগের ডাটা বজায় থাকবে।\n")
        f.write("# =====================================================================\n\n")
        
        current_kw = None
        for q in queries:
            kw_part = q.split(" in ")[0]
            if kw_part != current_kw:
                current_kw = kw_part
                f.write(f"\n# --- Keyword Group: {current_kw.upper()} ---\n")
            f.write(f"{q}\n")

    print(f"✅ Generated {len(queries)} Texas Auto Body search queries in '{output_path}'!")

if __name__ == "__main__":
    main()
