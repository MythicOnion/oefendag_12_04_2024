# Geo-oefendag 12-04-2024

## Introductie
Dit is de repo voor onze oefendag, waarin we probeerden een generieke applicatie te bouwen die op een gemakkelijke manier geo-data kan verwerken en visualiseren. Deze eerste versie kan live-API-calls en .csv-files verwerken om daar vervolgens met markers op een Leaflet-kaart visualisaties van te maken. In de toekomst kunnen we wellicht meer gaan opzetten. Zie de PowerPoint voor ideeën rondom meer mogelijkheden!

## De applicatie werkend krijgen
1. Maak een nieuwe virtuele Python-omgeving (Python versie = 3.11): conda create --name oefendag python=3.11
2. Installeer de benodigde dependencies: pip install -r requirements.txt
3. Open een terminal in je favoriete IDE en kloon deze repo: git clone https://github.com/WesselB90/oefendag_12_04_2024.git
4. Ga naar de directory waar je de repo hebt gekloond: cd ~/oefendag_12_04_2024
5. Draai app.py: streamlit run app.py --theme.primaryColor="#32cd32" --server.maxUploadSize 100000