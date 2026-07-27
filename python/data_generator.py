import random
from datetime import date, timedelta
import csv

random.seed(42)

vendors = ["Acme Supplies", "Nordic Freight", "BlueLine Logistics", "SameDay", "Mustang101", "Zenith Freight", "Apex More", "Shift Cargo", "Flow Freight", "Vectra Movers", "Swiftstream Logistics", "Quantum Express", "Compass Crate", "Wayfinder Logistics", "Anchor", "Pinnacle", "Steadfast", "Vanguard", "NordicTech Solutions", "EuroSupply GmbH", "Atlas Industrial Parts", "BlueRiver Logistics", "Vertex Systems", "GreenField Components", "AlphaCore Technologies", "GlobalTrade Europe", "PrimeLine Manufacturing", "SilverOak Consulting", "NovaEdge Services", "Titan Machinery Group", "BrightWave Electronics", "UrbanSource Supplies", "Apex Distribution", "Continental Solutions", "FusionWorks Europe", "Helix Innovations", "DeltaPro Industries", "Orion Business Services", "Everest Trading Co.", "QuantumWare Ltd.", "Pioneer Logistics", "RedStone Materials", "Skyline Equipment", "Vantage Partners", "IronGate Engineering", "ClearPath Solutions", "WestBridge Suppliers", "OmegaTech Europe"]

employees = ["J. Kovacs", "A. Nagy", "Camila Cantrell", "Haley Rivas", "Winter Underwood","Lukas Müller", "Sofia Rossi", "Mateo García", "Anna Kowalska", "Nicolas Dubois", "Elena Petrova", "Jakub Novák", "Laura Schmidt", "Marco Bianchi", "Ingrid Hansen", "Andreas Weber", "Clara Silva", "Pavel Horák", "Emma Johansson", "Thomas Lefèvre", "Katarina Jovanović", "Felix Bauer", "Marta Nowak", "Victor Popescu", "Eva Andersson"]

start_date = date(2026, 1, 1)

def random_date(start, days_range):
    return start + timedelta(days=random.randint(0, days_range))

purchase_orders = []

for i in range(700):
    po = {
        "po_number": f"PO{1000+i}",
        "vendor": random.choice(vendors),
        "order_date": random_date(start_date, 150),
        "po_quantity": random.randint(10, 500),
        "po_unit_price": round(random.uniform(5, 200), 2),
        "approved_by": random.choice(employees)
    }
    po["promised_delivery_date"] = po["order_date"] + timedelta(days=random.randint(5, 21))
    purchase_orders.append(po)

for po in purchase_orders:
    if random.random() < 0.05:
        po["approved_by"] = ""

goods_receipts = []

for po in purchase_orders:
    if random.random() < 0.08:
        continue

    gr_quantity = po["po_quantity"]

    if random.random() < 0.08:
        gr_quantity += random.choice([-1, 1]) * random.randint(1, 20)
        gr_quantity = max(gr_quantity, 0)

    actual_delivery_date = po["promised_delivery_date"] + timedelta(days=random.randint(-2, 2))

    if random.random() < 0.15:
        actual_delivery_date = po["promised_delivery_date"] + timedelta(days=random.randint(5, 20))

    goods_receipts.append({
        "po_number": po["po_number"],
        "gr_quantity": gr_quantity,
        "actual_delivery_date": actual_delivery_date,
    })

invoices = []
invoice_counter = 5000
for po in purchase_orders:
    invoice_counter += 1
    unit_price = po["po_unit_price"]
    # 10% chance of price variance (billed above agreed price)
    if random.random() < 0.10:
        unit_price = round(unit_price * random.uniform(1.05, 1.20), 2)

    invoice_date = po["promised_delivery_date"] + timedelta(days=random.randint(1, 10))

    invoices.append({
        "po_number": po["po_number"],
        "invoice_number": f"INV{invoice_counter}",
        "invoice_quantity": po["po_quantity"],
        "invoice_unit_price": unit_price,
        "invoice_date": invoice_date,
    })

    if random.random() < 0.04:
        invoice_counter += 1
        invoices.append({
            "po_number": po["po_number"],
            "invoice_number": f"INV{invoice_counter}",
            "invoice_quantity": po["po_quantity"],
            "invoice_unit_price": unit_price,
            "invoice_date": invoice_date + timedelta(days=random.randint(1, 5)),
        })

with open("../data/purchase_orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=purchase_orders[0].keys())
    writer.writeheader()
    writer.writerows(purchase_orders)

with open("../data/goods_receipts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=goods_receipts[0].keys())
    writer.writeheader()
    writer.writerows(goods_receipts)

with open("../data/invoices.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=invoices[0].keys())
    writer.writeheader()
    writer.writerows(invoices)

print(f"POs: {len(purchase_orders)}, GRs: {len(goods_receipts)}, Invoices: {len(invoices)}")