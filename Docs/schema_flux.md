flowchart LR

    %% Sources de donnees
    subgraph S0[Sources de donnees]
        A1["CSV Nutrition"]
        A2["CSV Utilisateurs"]
        A3["CSV Activite"]
        A4["API externes"]
    end

    %% Ingestion et nettoyage
    B["Ingestion / ETL (Pandas)"]
    C["Nettoyage et transformation"]

    %% Stockage
    D["Base de donnees relationnelle (PostgreSQL)"]

    %% API Backend
    E["API REST (CRUD donnees)"]

    %% Front / Visualisation
    F["Interface Streamlit (tableaux, filtres, graphiques)"]
    G["KPIs et insights pour les equipes metier"]

    %% Flux
    A1 --> B
    A2 --> B
    A3 --> B
    A4 --> B

    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
