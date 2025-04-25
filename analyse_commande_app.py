import streamlit as st
import re
from collections import defaultdict

st.set_page_config(page_title="Analyse Commande Klimagiel", layout="centered")

st.title("🔍 Analyseur de Commande Klimagiel")
st.markdown("Collez ici votre commande ci-dessous 👇")

commande_text = st.text_area("Commande :", height=300)

def analyser_commande(texte):
    lignes = texte.strip().split("\n")
    resultats = defaultdict(lambda: {
        "gaines": 0.0,
        "coudes": 0,
        "bouchons": 0,
        "raccordements": 0,
        "reductions": 0
    })

    for ligne in lignes:
        if "Merce" in ligne:
            parties = ligne.split("\t")
            if len(parties) >= 5:
                code = parties[1]
                variante = parties[2]
                quantite = parties[4].replace(",", ".")
                diametre_match = re.search(r"(\d{3})", variante)
                if diametre_match:
                    diam = diametre_match.group(1)
                    try:
                        qte = float(quantite)
                    except ValueError:
                        continue

                    if code.startswith("CCM"):
                        resultats[diam]["gaines"] += qte
                    elif code.startswith("CU_"):
                        resultats[diam]["coudes"] += int(qte)
                    elif code.startswith("TAP"):
                        resultats[diam]["bouchons"] += int(qte)
                    elif code.startswith("QT") or code.startswith("TEE"):
                        resultats[diam]["raccordements"] += int(qte)
                    elif code.startswith("RID"):
                        resultats[diam]["reductions"] += int(qte)

    return resultats

if st.button("Analyser la commande"):
    if commande_text.strip() == "":
        st.warning("Veuillez coller une commande pour l'analyser.")
    else:
        resultats = analyser_commande(commande_text)
        if resultats:
            for diam, données in sorted(resultats.items()):
                st.markdown(f"### 📦 Diamètre {diam}")
                st.write(f"• Gaines : {données['gaines']} mètres")
                st.write(f"- Coudes : {données['coudes']}")
                st.write(f"- Bouchons : {données['bouchons']}")
                st.write(f"- Raccordements : {données['raccordements']}")
                st.write(f"- Réductions : {données['reductions']}")
        else:
            st.info("Aucun élément reconnu dans la commande.")
