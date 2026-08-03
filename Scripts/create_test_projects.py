import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


# -------------------------
# Projets
# -------------------------

cursor.execute("""
INSERT INTO projects
(project_name, description, locality)
VALUES
(
'Flore urbaine Bukavu',
'Observations botaniques opportunistes',
'Bukavu'
)
""")


cursor.execute("""
INSERT INTO projects
(project_name, description, locality)
VALUES
(
'Inventaire forestier Itombwe',
'Inventaire par plots',
'Réserve Naturelle d’Itombwe'
)
""")


cursor.execute("""
INSERT INTO projects
(project_name, description, locality)
VALUES
(
'Gradient altitudinal Kahuzi-Biega',
'Inventaire par transects',
'Parc National de Kahuzi-Biega'
)
""")


conn.commit()


# récupérer les IDs
cursor.execute("SELECT project_id, project_name FROM projects")

print("Projets disponibles :")

for row in cursor.fetchall():
    print(row)


conn.close()