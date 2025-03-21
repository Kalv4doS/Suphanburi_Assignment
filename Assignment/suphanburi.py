import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation import traveling_salesman_problem

# 1️⃣ สร้างกราฟเริ่มต้นที่มี 20 สถานที่
def create_graph():
    G = nx.Graph()
    
    locations = {
        "Bueng Chawak": {"Wat Pa Lelai Worawihan": 30, "Dragon Descendants Museum": 25},
        "Wat Pa Lelai Worawihan": {"Sam Chuk Market": 20, "Banharn-Jamsai Tower": 15},
        "Sam Chuk Market": {"Dragon Descendants Museum": 15, "Wat Khao Dee Salak": 35},
        "Dragon Descendants Museum": {"Banharn-Jamsai Tower": 10, "Wat Phai Rong Wua": 40},
        "Banharn-Jamsai Tower": {"Thai Buffalo Conservation Village": 12},
        "Wat Khao Dee Salak": {"Phu Toei National Park": 50},
        "Phu Toei National Park": {"Kra Seaw Dam": 30},
        "Kra Seaw Dam": {"Wat Phai Rong Wua": 45},
        "Wat Phai Rong Wua": {"Thai Buffalo Conservation Village": 20},
        "Thai Buffalo Conservation Village": {"Wat Phra Non Chaksi Worawihan": 35},
        "Wat Phra Non Chaksi Worawihan": {"Weluwan Cave": 28},
        "Weluwan Cave": {"Orchid Conservation Center (Lady Slipper Orchid)": 40},
        "Orchid Conservation Center (Lady Slipper Orchid)": {"Thai Buffalo Conservation Village": 22},
        "Thai Buffalo Conservation Village": {"Suphan Buri National Museum": 18},
        "Suphan Buri National Museum": {"Saphan Khong Floating Market": 15},
        "Saphan Khong Floating Market": {"Phu Hang Nak Natural Stone Park": 25},
        "Phu Hang Nak Natural Stone Park": {"Wat Khao Phra Si Sanphet Ram": 20},
        "Wat Khao Phra Si Sanphet Ram": {"Bueng Rahan": 30},
        "Bueng Rahan": {"Hub Khao Wong Reservoir (Pang Oung Suphan)": 50, "Wat Thap Kradan":15 },
    }

    for place, connections in locations.items():
        for dest, distance in connections.items():
            G.add_edge(place, dest, weight=distance)
    
    return G

# 2️⃣ ฟังก์ชันเพิ่มสถานที่ใหม่
def add_location(G):
    new_place = input("ชื่อสถานที่ใหม่: ").strip()
    if new_place in G.nodes:
        print("❌ สถานที่นี้มีอยู่แล้ว!")
        return
    
    G.add_node(new_place)
    print("เพิ่มสถานที่สำเร็จ ✅\nตอนนี้เพิ่มเส้นทางระหว่างสถานที่...")
    
    while True:
        connect_to = input("เชื่อมต่อกับ (เว้นว่างเพื่อหยุด): ").strip()
        if not connect_to:
            break
        if connect_to not in G.nodes:
            print("❌ สถานที่นี้ไม่มีอยู่ในรายการ!")
            continue
        distance = int(input(f"ระยะทางจาก {new_place} ไป {connect_to} (กม.): "))
        G.add_edge(new_place, connect_to, weight=distance)
    
    print("📍 สถานที่และเส้นทางใหม่ถูกเพิ่มเรียบร้อยแล้ว!")

# 3️⃣ ฟังก์ชันวาดกราฟ พร้อมไฮไลต์เส้นทางที่ดีที่สุด
def plot_graph(G, best_route):
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=9, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    best_edges = [(best_route[i], best_route[i+1]) for i in range(len(best_route)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=best_edges, edge_color='red', width=2)

    plt.title("แผนที่เส้นทางท่องเที่ยว สุพรรณบุรี")
    plt.show()

# 4️⃣ คำนวณเส้นทางที่ดีที่สุดโดยใช้ TSP
def find_best_route(G, selected_places):
    subgraph = G.subgraph(selected_places)
    best_route = traveling_salesman_problem(subgraph, cycle=True, weight="weight")
    total_distance = sum(G[best_route[i]][best_route[i+1]]['weight'] for i in range(len(best_route)-1))
    return best_route, total_distance

# 5️⃣ ส่วนหลักของโปรแกรม
def main():
    G = create_graph()

    while True:
        print("\n📍 สถานที่ท่องเที่ยวทั้งหมด:")
        places_list = list(G.nodes)
        for i, place in enumerate(places_list, 1):
            print(f"{i}. {place}")

        print("\n🛠 เมนู:")
        print("1️⃣ เลือกสถานที่และคำนวณเส้นทาง")
        print("2️⃣ เพิ่มสถานที่ใหม่")
        print("3️⃣ ออกจากโปรแกรม")
        choice = input("เลือกเมนู (1-3): ").strip()

        if choice == "1":
            selected_indexes = input("\n🛤 เลือกสถานที่ที่ต้องการเดินทาง (พิมพ์หมายเลข แยกด้วยช่องว่าง)\n👉: ").strip().split()
            
            selected_places = []
            for i in selected_indexes:
                if i.isdigit():
                    idx = int(i) - 1
                    if 0 <= idx < len(places_list):
                        selected_places.append(places_list[idx])
                    else:
                        print(f"❌ เลข {i} ไม่มีอยู่ในรายการ!")
                else:
                    print(f"❌ '{i}' ไม่ใช่ตัวเลขที่ถูกต้อง!")
            
            if len(selected_places) < 2:
                print("❌ ต้องเลือกอย่างน้อย 2 สถานที่!")
                continue
            
            best_route, total_distance = find_best_route(G, selected_places)
            print(f"\n✅ เส้นทางที่ดีที่สุด: {' → '.join(best_route)}")
            print(f"📏 ระยะทางรวม: {total_distance} กม.")
            plot_graph(G, best_route)

        elif choice == "2":
            add_location(G)
        elif choice == "3":
            print(" ออกจากโปรแกรม...")
            break
        else:
            print("❌ เลือกเมนูไม่ถูกต้อง!")

# ▶️ เรียกใช้งานโปรแกรม
if __name__ == "__main__":
    main()
