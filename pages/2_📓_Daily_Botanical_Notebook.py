import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from streamlit_searchbox import st_searchbox

from utils.database import get_connection
from utils.species import search_species, get_species
from utils.collectors import get_collector_names, add_collector
from utils.projects import get_project_names, save_project
from utils.locations import get_locality_names, save_location
from utils.habitats import get_habitat_names, save_habitat

def get_exif_data(photo):

    exif_data = {}

    try:

        photo.seek(0)

        image = Image.open(photo)

        exif = image.getexif()

        if exif:

            for tag_id, value in exif.items():

                tag = TAGS.get(
                    tag_id,
                    tag_id
                )

                exif_data[tag] = value

    except Exception:

        pass

    return exif_data
geolocator = Nominatim(
    user_agent="daily_botanical_notebook"
)

def get_coordinates(country, province, territory, locality):

    queries = [
        f"{locality}, {territory}, {province}, {country}",
        f"{locality}, {province}, {country}"
    ]

    for query in queries:

        try:

            location = geolocator.geocode(
                query,
                timeout=10
            )

            if location:

                return (
                    location.latitude,
                    location.longitude
                )

        except GeocoderTimedOut:
            pass

    return None, None
# =====================================================
# DATABASE
# =====================================================

conn = get_connection()
cur = conn.cursor()


# =====================================================
# PAGE
# =====================================================

st.title("📓 Daily Botanical Notebook")

st.write(
    """
    Record a botanical observation during field work.
    """
)


# =====================================================
# AUTOMATIC DATE AND TIME
# =====================================================

now = datetime.now()

date = now.strftime("%Y-%m-%d")

time = now.strftime("%H:%M:%S")


st.info(
    f"Date: {date} | Time: {time}"
)


# =====================================================
# FORM
# =====================================================

collector_names = get_collector_names()

if len(collector_names) == 0:

    st.warning("No collector registered.")

    collector_name = st.text_input("Collector name")

    collector_institution = st.text_input("Institution")

    collector_email = st.text_input("Email")

    if st.button("💾 Save collector"):

        add_collector(
            collector_name,
            collector_institution,
            collector_email
        )

        st.success("Collector added.")

        st.rerun()

    observer = collector_name

else:

    collector_names.append("➕ Add a new collector")

    observer = st.selectbox(
        "Observer / Collector",
        collector_names
    )

    if observer == "➕ Add a new collector":

        collector_name = st.text_input("Collector name")

        collector_institution = st.text_input("Institution")

        collector_email = st.text_input("Email")

        if st.button("💾 Save collector"):

            add_collector(
                collector_name,
                collector_institution,
                collector_email
            )

            st.success("Collector added.")

            st.rerun()

        observer = collector_name
collectorNumber = st.text_input(
    "Voucher / Collection Number",
    placeholder="Ex: ILC-0254"
)
habitat_names = get_habitat_names()

habitat = st.selectbox(
    "Habitat",
    habitat_names + ["➕ Add new habitat"]
)
if habitat == "➕ Add new habitat":

    new_habitat = st.text_input("New habitat")

    if st.button("💾 Save habitat"):

        if new_habitat.strip() == "":
            st.error("Please enter a habitat name.")
            st.stop()

        save_habitat(new_habitat)

        st.success("Habitat saved.")

        st.rerun()

# =====================================================
# LOCATION
# =====================================================

st.subheader("📍 Locality")


country = st.text_input(
    "Country",
    value="Democratic Republic of the Congo"
)


province = st.text_input(
    "Province",
    value="South Kivu"
)


territory = st.text_input(
    "Territory"
)


locality_names = get_locality_names()


locality_choice = st.selectbox(
    "Locality",
    locality_names + ["➕ Add new locality"]
)


if locality_choice == "➕ Add new locality":

    locality = st.text_input(
        "New locality name"
    )

    if st.button("💾 Save locality"):

        save_location(
            country,
            province,
            territory,
            locality,
            0,
            0,
            0
        )

        st.success("Locality saved")

else:

    locality = locality_choice

localityDescription = st.text_area(
    "Locality description",
    placeholder="Example: roadside, forest edge, cultivated field..."
)
# =====================================================
# SAMPLING DESIGN
# =====================================================

st.subheader("📐 Sampling design")


design_type = st.selectbox(
    "Observation type",
    [
        "Opportunistic",
        "Plot",
        "Transect"
    ]
)


designID = None
samplingUnitID = None
transectPointID = None
plotID = None
subplotID = None
quadratID = None
transectID = None
point_choice = None

default_altitude = 0.0
default_latitude = 0.0
default_longitude = 0.0


# =====================================================
# PLOT
# =====================================================

if design_type == "Plot":

    cur.execute("""
    SELECT designID
    FROM sampling_designs
    WHERE designType='plot'
    """)

    design = cur.fetchone()

    if design:
        designID = design[0]


    cur.execute("""
    SELECT
        unitID,
        unitName
    FROM sampling_units
    WHERE unitType='Plot'
    """)

    plots = [
        tuple(p) for p in cur.fetchall()
    ]


    plot_options = [p[1] for p in plots]

    plot_options.append("➕ Add new Plot")


    plot_choice = st.selectbox(
        "Select Plot",
        plot_options
    )


    # CREATION NOUVEAU PLOT

    if plot_choice == "➕ Add new Plot":

        new_plot = st.text_input(
            "New Plot name",
            placeholder="Example: P01"
        )


        if st.button("💾 Save Plot"):

            if new_plot.strip() == "":

                st.error(
                    "Please enter a plot name."
                )
                st.stop()


            cur.execute(
                """
                INSERT INTO sampling_units
                (
                unitName,
                unitType,
                parentUnitID
                )
                VALUES (?,?,?)
                """,
                (
                new_plot,
                "Plot",
                None
                )
            )


            conn.commit()

            st.success(
                "Plot created."
            )

            st.rerun()


    # SELECTION PLOT EXISTANT

    else:

        for p in plots:

            if p[1] == plot_choice:

                plotID = p[0]
                samplingUnitID = plotID
                break



    # =====================================================
    # SUBPLOT
    # =====================================================

    if plotID:


        cur.execute(
            """
            SELECT
                unitID,
                unitName
            FROM sampling_units
            WHERE parentUnitID=?
            AND unitType='Subplot'
            """,
            (plotID,)
        )


        subplots = [
            tuple(s) for s in cur.fetchall()
        ]


        subplot_options = [
            s[1] for s in subplots
        ]


        subplot_options.append(
            "➕ Add new Subplot"
        )


        subplot_choice = st.selectbox(
            "Select Subplot (optional)",
            ["None"] + subplot_options
        )


        # CREATION SUBPLOT

        if subplot_choice == "➕ Add new Subplot":

            new_subplot = st.text_input(
                "New Subplot name",
                placeholder="Example: S01"
            )


            if st.button("💾 Save Subplot"):


                if new_subplot.strip() == "":

                    st.error(
                        "Please enter a subplot name."
                    )

                    st.stop()


                cur.execute(
                    """
                    INSERT INTO sampling_units
                    (
                    unitName,
                    unitType,
                    parentUnitID
                    )
                    VALUES (?,?,?)
                    """,
                    (
                    new_subplot,
                    "Subplot",
                    plotID
                    )
                )


                conn.commit()


                st.success(
                    "Subplot created."
                )


                st.rerun()



        # SELECTION SUBPLOT EXISTANT

        elif subplot_choice != "None":

            for s in subplots:

                if s[1] == subplot_choice:

                    subplotID = s[0]
                    samplingUnitID = subplotID
                    break



# =====================================================
# TRANSECT
# =====================================================

elif design_type == "Transect":

    cur.execute("""
    SELECT designID
    FROM sampling_designs
    WHERE designType='transect'
    """)

    design = cur.fetchone()


    if design:

        designID = design[0]


    cur.execute("""
    SELECT
        unitID,
        unitName
    FROM sampling_units
    WHERE unitType='Transect'
    """)


    transects = [
        tuple(t) for t in cur.fetchall()
    ]


    if transects:

        transect_choice = st.selectbox(
            "Select Transect",
            transects,
            format_func=lambda x:x[1]
        )


        transectID = transect_choice[0]

        samplingUnitID = transectID


        cur.execute(
            """
            SELECT
                pointID,
                pointName,
                distance_m,
                altitude,
                latitude,
                longitude
            FROM transect_points
            WHERE transectID=?
            """,
            (transectID,)
        )


        points = [
            tuple(p) for p in cur.fetchall()
        ]


        if points:


            point_choice = st.selectbox(
                "Select transect point",
                points,
                format_func=lambda x:
                f"{x[1]} - {x[2]} m - {x[3]} m altitude"
            )


            transectPointID = point_choice[0]

            default_altitude = point_choice[3]

            default_latitude = point_choice[4]

            default_longitude = point_choice[5]


            st.session_state.transect_coordinates = (
                default_latitude,
                default_longitude
            )


    else:

        st.warning(
            "No transect available."
        )



# =====================================================
# GPS
# =====================================================

if "latitude" not in st.session_state:

    st.session_state.latitude = 0.0


if "longitude" not in st.session_state:

    st.session_state.longitude = 0.0



if "transect_coordinates" in st.session_state:


    lat, lon = st.session_state.transect_coordinates

    st.session_state.latitude = lat

    st.session_state.longitude = lon

    del st.session_state.transect_coordinates



st.session_state.country = country

st.session_state.province = province

st.session_state.territory = territory

st.session_state.locality = locality



def find_gps():

    lat_auto, lon_auto = get_coordinates(
        st.session_state.country,
        st.session_state.province,
        st.session_state.territory,
        st.session_state.locality
    )


    if lat_auto is not None and lon_auto is not None:


        st.session_state.new_coordinates = (
            lat_auto,
            lon_auto
        )


    else:

        st.warning(
            "Location not found. Enter coordinates manually."
        )



def clear_coordinates():

    st.session_state.latitude = 0.0

    st.session_state.longitude = 0.0



st.button(
    "🔎 Find GPS from locality",
    on_click=find_gps
)


st.button(
    "🗑️ Clear coordinates",
    on_click=clear_coordinates
)



if "new_coordinates" in st.session_state:


    lat, lon = st.session_state.new_coordinates

    st.session_state.latitude = lat

    st.session_state.longitude = lon

    del st.session_state.new_coordinates



latitude = st.number_input(
    "Latitude",
    format="%.6f",
    value=st.session_state.latitude,
    key="latitude"
)


longitude = st.number_input(
    "Longitude",
    format="%.6f",
    value=st.session_state.longitude,
    key="longitude"
)


altitude = st.number_input(
    "Altitude (m)",
    min_value=0.0,
    value=default_altitude
)
# =====================================================
# SPECIES AUTOCOMPLETE SEARCH
# =====================================================

st.subheader("🌿 Taxon")


def search_function(text):

    if not text:
        return []

    results = search_species(text)

    return results["species"].tolist()


selected_species = st_searchbox(
    search_function,
    label="🔎 Search existing species"
)


taxon = None
new_species_name = None


if selected_species:

    taxon = get_species(selected_species)


# Si aucune sélection n'est faite,
# permettre une nouvelle espèce

new_species_name = st.text_input(
    "🆕 Or enter a new species name"
)


if new_species_name and taxon is None:

    st.info(
        f"New species to be created: {new_species_name}"
    )

    add_new = True

else:

    add_new = False

# =====================================================
# NEW SPECIES FORM
# =====================================================

if add_new:

    st.subheader("➕ New species information")


    new_scientificName = new_species_name


    new_kingdom = st.text_input(
        "Kingdom"
    )


    new_phylum = st.text_input(
        "Phylum"
    )


    new_class = st.text_input(
        "Class"
    )


    new_order = st.text_input(
        "Order"
    )


    new_family = st.text_input(
        "Family"
    )


    new_genus = st.text_input(
        "Genus"
    )


    st.text_input(
        "Species",
        value=new_scientificName,
        disabled=True
    )


    st.subheader("🌱 Biological information")


    new_establishmentMeans = st.text_input(
        "Establishment means"
    )


    new_organismRemarks = st.text_input(
        "Organism remarks"
    )


    new_nativeRange = st.text_input(
        "Native range"
    )


    new_iucn = st.text_input(
        "IUCN Red List Category"
    )


    new_vernacularName = st.text_input(
        "Vernacular name"
    )


    new_observationStatus = st.text_input(
        "Observation status"
    )


    new_primaryUse = st.text_input(
        "Primary use"
    )

# =====================================================
# AUTOMATIC TAXON INFORMATION
# =====================================================

if taxon is not None:

    st.subheader("🌿 Taxonomic information")


    col1, col2 = st.columns(2)


    with col1:

        st.text_input(
            "Kingdom",
            taxon["kingdom"],
            disabled=True
        )

        st.text_input(
            "Phylum",
            taxon["phylum"],
            disabled=True
        )

        st.text_input(
            "Class",
            taxon["class"],
            disabled=True
        )

        st.text_input(
            "Order",
            taxon["order_name"],
            disabled=True
        )


        st.text_input(
            "Family",
            taxon["family"],
            disabled=True
        )


    with col2:

        st.text_input(
            "Genus",
            taxon["genus"],
            disabled=True
        )


        st.text_input(
            "Species",
            taxon["species"],
            disabled=True
        )


        st.text_input(
            "Taxon ID",
            taxon["taxonID"],
            disabled=True
        )


    st.subheader("🌱 Biological information")


    establishmentMeans = st.text_input(
        "Establishment means",
        taxon["establishmentMeans"]
    )


    organismRemarks = st.text_input(
        "Organism remarks",
        taxon["organismRemarks"]
    )


    nativeRange = st.text_input(
        "Native range",
        taxon["nativeRange"]
    )


    iucnRedListCategory = st.text_input(
        "IUCN Red List Category",
        taxon["iucnRedListCategory"]
        if pd.notna(taxon["iucnRedListCategory"])
        else ""
    )


    vernacularName = st.text_input(
        "Vernacular name",
        taxon["vernacularName"]
        if pd.notna(taxon["vernacularName"])
        else ""
    )


    observationStatus = st.text_input(
        "Observation status",
        taxon["observationStatus"]
    )


    primaryUse = st.text_input(
        "Primary use",
        taxon["primaryUse"]
    )

description = st.text_area(
    "Plant description"
)


remarks = st.text_area(
    "Remarks"
)
phenology = st.selectbox(
    "Phenology",
    [
        "",
        "Vegetative",
        "Flowering",
        "Fruiting",
        "Flowering & Fruiting"
    ]
)

individualCount = st.number_input(
    "Number of individuals observed",
    min_value=0,
    value=0
)

specimenCount = st.number_input(
    "Number of specimens collected",
    min_value=0,
    value=0
)
st.subheader("📏 Plant measurements")

dbh = st.number_input(
    "DBH (cm)",
    min_value=0.0,
    value=0.0,
    step=0.1,
    help="Diameter at Breast Height (1.30 m above ground)"
)

height = st.number_input(
    "Plant height (m)",
    min_value=0.0,
    value=0.0,
    step=0.1
)
# =====================================================
# PHOTOS
# =====================================================

st.subheader("📷 Plant photographs")


uploaded_photos = st.file_uploader(
    "Upload plant photos",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)


camera_photo = st.camera_input(
    "📸 Take a photo with camera"
)


photo_type = st.selectbox(
    "Photo type",
    [
        "Habit",
        "Leaf",
        "Flower",
        "Fruit",
        "Bark",
        "Seed",
        "Herbarium specimen",
        "Other"
    ]
)
# ================================
# PHOTO PREVIEW
# ================================

if uploaded_photos:

    st.subheader("🔍 Photo preview")

    cols = st.columns(3)

    for i, photo in enumerate(uploaded_photos):

        with cols[i % 3]:

            st.image(
                photo,
                caption=photo.name,
                use_container_width=True
            )

# =====================================================
# SAVE
# =====================================================

if st.button("💾 Save observation"):
    if habitat == "➕ Add new habitat":
        st.error("Please save and select the new habitat before saving the observation.")
        st.stop()

    if observer == "":

        st.error("Please enter collector name.")
        st.stop()


    if locality == "":

        st.error("Please enter locality.")
        st.stop()


    if selected_species is None and new_species_name == "":

        st.error("Please select or enter a species.")
        st.stop()
    # ==========================================
    # CAS 1 : NOUVELLE ESPECE
    # ==========================================

    if add_new:


        cur.execute(
            """
            SELECT COUNT(*) 
            FROM species
            """
        )

        count = cur.fetchone()[0] + 1


        taxonID = f"NEW{count:06d}"


        cur.execute(
            """
            INSERT INTO species
            (
            taxonID,
            scientificName,
            kingdom,
            phylum,
            class,
            order_name,
            family,
            genus,
            species,
            taxonomicStatus,
            establishmentMeans,
            organismRemarks,
            nativeRange,
            iucnRedListCategory,
            vernacularName,
            observationStatus,
            primaryUse
            )

            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,

            (
            taxonID,
            new_species_name,
            new_kingdom,
            new_phylum,
            new_class,
            new_order,
            new_family,
            new_genus,
            new_species_name,
            "UNKNOWN",
            new_establishmentMeans,
            new_organismRemarks,
            new_nativeRange,
            new_iucn,
            new_vernacularName,
            new_observationStatus,
            new_primaryUse
            )
        )


        selected_species = new_species_name



    # ==========================================
    # CAS 2 : ESPECE EXISTANTE
    # ==========================================


    else:

        if taxon is None:

            st.error(
                "Please select an existing species or enter a new species name."
            )

            st.stop()

        taxonID = taxon["taxonID"]



    
    # ==========================================
    # SAVE LOCATION
    # ==========================================

    latitude = st.session_state.latitude
    longitude = st.session_state.longitude

    locationID = save_location(
        country,
        province,
        territory,
        locality,
        latitude,
        longitude,
        altitude
    )
    st.write("DEBUG LOCATION ID:", locationID)
    st.write("DEBUG GPS:", latitude, longitude, altitude)

    # ==========================================
    # ENREGISTREMENT OBSERVATION
    # ==========================================

    cur.execute(
        """
        INSERT INTO field_notes
        (
        date,
        time,
        observer,
        latitude,
        longitude,
        altitude,
        habitat,
        collectorNumber,
        specimenCount,
        individualCount,
        phenology,
        localityDescription,
        locationID,
        taxonID,
        species,
        description,
        remarks,
        dbh,
        height,
        designID,
        samplingUnitID,
        transectPointID,
        plotID,
        subplotID,
        quadratID,
        transectID
)

        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,

        (
        date,
        time,
        observer,
        latitude,
        longitude,
        altitude,
        habitat,
        collectorNumber,
        specimenCount,
        individualCount,
        phenology,
        localityDescription,
        locationID,
        taxonID,
        selected_species,
        description,
        remarks,
        dbh,
        height,
        designID,
        samplingUnitID,
        transectPointID,
        plotID,
        subplotID,
        quadratID,
        transectID
)
    )   

 # récupérer l'identifiant de l'observation créée

    noteID = cur.lastrowid


    # =====================================================
    # SAVE PHOTOS
    # =====================================================

    photos_to_save = []

    if uploaded_photos:
        photos_to_save.extend(uploaded_photos)

    if camera_photo:
        photos_to_save.append(camera_photo)


    if len(photos_to_save) > 0:

        PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

        photos_folder = PROJECT_DIR / "Database" / "Photos"

        photos_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        for photo in photos_to_save:

            exif = get_exif_data(photo)

            photo.seek(0)

            photo_datetime = exif.get(
                "DateTimeOriginal",
                exif.get("DateTime", "")
            )


            original_name = getattr(
                photo,
                "name",
                f"camera_photo_{uuid4()}.jpg"
            )


            filename = f"{uuid4()}_{original_name}"


            file_path = photos_folder / filename


            with open(file_path, "wb") as f:

                f.write(
                    photo.getbuffer()
                )


            cur.execute(
                """
                INSERT INTO photos
                (
                observation_id,
                filename,
                photo_type,
                photo_datetime
                )

                VALUES (?,?,?,?)
                """,

                (
                noteID,
                filename,
                photo_type,
                photo_datetime
                )
            )


    conn.commit()

    conn.close()

    st.success(
    "✅ Observation saved successfully!"
)