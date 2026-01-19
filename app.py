import plotly.express as px
import pandas as pd

# =========================
# 1) Chargement des données
# =========================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv"
donnees = pd.read_csv(URL_CSV)

# Normaliser / sécuriser les types
donnees["qte"] = pd.to_numeric(donnees["qte"], errors="coerce")
donnees["prix"] = pd.to_numeric(donnees["prix"], errors="coerce")

# Colonne chiffre d'affaires
donnees["ca"] = donnees["prix"] * donnees["qte"]

# =========================
# 2) Analyses Pandas
# =========================
stats_par_produit = donnees.groupby("produit").agg(
    ca_moyenne=("ca", "mean"),
    ca_mediane=("ca", "median"),
    qte_moyenne=("qte", "mean"),
    qte_mediane=("qte", "median"),
    qte_ecart_type=("qte", "std"),
    qte_variance=("qte", "var"),
).reset_index()

print("\n=== Statistiques par produit (Pandas) ===")
print(stats_par_produit)

# =========================
# 3) Python natif (sans Pandas)
# =========================
lignes = donnees.to_dict(orient="records")

totaux_qte = {}
for row in lignes:
    produit = row["produit"]
    qte = row["qte"]
    if pd.isna(qte):
        continue
    totaux_qte[produit] = totaux_qte.get(produit, 0) + int(qte)

produit_plus_vendu = max(totaux_qte, key=totaux_qte.get)
produit_moins_vendu = min(totaux_qte, key=totaux_qte.get)

print("\n=== Python natif (sans Pandas) ===")
print("Totaux unités par produit :", totaux_qte)
print(f"Produit le plus vendu : {produit_plus_vendu} ({totaux_qte[produit_plus_vendu]} unités)")
print(f"Produit le moins vendu : {produit_moins_vendu} ({totaux_qte[produit_moins_vendu]} unités)")

# =========================
# 4) Graphiques (avec couleurs)
# =========================

# Palette cohérente et professionnelle
palette_produits = px.colors.qualitative.Set2

# 4.1 Quantité vendue par région (camembert)
figure_region = px.pie(
    donnees,
    values="qte",
    names="region",
    title="Quantité vendue par région",
    color_discrete_sequence=px.colors.qualitative.Set3
)
figure_region.write_html("ventes-par-region.html")

# 4.2 Ventes par produit (quantités)
qte_par_produit = donnees.groupby("produit")["qte"].sum().reset_index()

figure_ventes_produit = px.bar(
    qte_par_produit,
    x="produit",
    y="qte",
    color="produit",
    color_discrete_sequence=palette_produits,
    title="Ventes par produit (quantités)"
)
figure_ventes_produit.write_html("ventes-par-produit.html")

# 4.3 Chiffre d'affaires par produit
ca_par_produit = donnees.groupby("produit")["ca"].sum().reset_index()

figure_ca_produit = px.bar(
    ca_par_produit,
    x="produit",
    y="ca",
    color="produit",
    color_discrete_sequence=palette_produits,
    title="Chiffre d'affaires par produit"
)
figure_ca_produit.write_html("chiffre-affaires-par-produit.html")

print("\nCela faisait des années que je n'avais pas touché à Python : c'est vraiment cool de redécouvrir le langage et ses nouveautés ! 🚀")
