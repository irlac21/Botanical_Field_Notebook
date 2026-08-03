import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path


# =====================================================
# DATABASE
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_DIR / "Database" / "botanical.db"


conn = sqlite3.connect(DB_FILE)


query = """

SELECT

projects.project_id,
projects.project_name,
projects.description,
projects.locality,

COUNT(field_notes.noteID) AS records_count


FROM projects


LEFT JOIN field_notes

ON projects.project_id = field_notes.projectID


WHERE projects.deleted = 1


GROUP BY projects.project_id


ORDER BY projects.project_name

"""


archived_projects = pd.read_sql(
    query,
    conn
)


conn.close()



# =====================================================
# PAGE
# =====================================================

st.title("📦 Archived Projects")


st.markdown(
"""
Manage archived botanical projects.
You can restore them or permanently delete them.
"""
)



# =====================================================
# DISPLAY ARCHIVED PROJECTS
# =====================================================


if len(archived_projects) == 0:

    st.info(
        "No archived projects available."
    )


else:


    st.write(
        f"**{len(archived_projects)} archived project(s)**"
    )


    for index, row in archived_projects.iterrows():


        with st.expander(
            f"📦 {row['project_name']} ({row['records_count']} records)"
        ):


            st.write(
                f"""
                **Description:** {row['description'] if pd.notna(row['description']) else '-'}  

                **Locality:** {row['locality'] if pd.notna(row['locality']) else '-'}  

                **Field records:** {row['records_count']}
                """
            )


            col1, col2 = st.columns(2)



            # =====================================================
            # RESTORE
            # =====================================================

            with col1:


                if st.button(
                    "♻️ Restore project",
                    key=f"restore_{row['project_id']}"
                ):


                    conn = sqlite3.connect(DB_FILE)

                    cur = conn.cursor()


                    cur.execute(
                        """
                        UPDATE projects
                        SET deleted = 0
                        WHERE project_id = ?
                        """,
                        (
                            int(row["project_id"]),
                        )
                    )


                    cur.execute(
                        """
                        UPDATE field_notes
                        SET deleted = 0,
                            updatedAt = datetime('now')
                        WHERE projectID = ?
                        """,
                        (
                            int(row["project_id"]),
                        )
                    )


                    conn.commit()

                    conn.close()


                    st.success(
                        "Project restored successfully."
                    )


                    st.rerun()



            # =====================================================
            # DELETE PERMANENTLY
            # =====================================================

            with col2:


                if st.button(
                    "❌ Delete permanently",
                    key=f"delete_{row['project_id']}"
                ):


                    conn = sqlite3.connect(DB_FILE)

                    cur = conn.cursor()


                    cur.execute(
                        """
                        DELETE FROM field_notes
                        WHERE projectID = ?
                        """,
                        (
                            int(row["project_id"]),
                        )
                    )


                    cur.execute(
                        """
                        DELETE FROM projects
                        WHERE project_id = ?
                        """,
                        (
                            int(row["project_id"]),
                        )
                    )


                    conn.commit()

                    conn.close()


                    st.warning(
                        "Project permanently deleted."
                    )


                    st.rerun()