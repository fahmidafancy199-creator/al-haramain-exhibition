import streamlit as st
import sqlite3
import pandas as pd
import re
import os
from datetime import datetime, date


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Al Haramain Exhibition",
    page_icon="logo.png",
    layout="centered"
)

DATABASE_NAME = "al_haramain_exhibition.db"

COUNTRIES = [
    'Afghanistan',
    'Albania',
    'Algeria',
    'Andorra',
    'Angola',
    'Antigua and Barbuda',
    'Argentina',
    'Armenia',
    'Australia',
    'Austria',
    'Azerbaijan',
    'Bahamas',
    'Bahrain',
    'Bangladesh',
    'Barbados',
    'Belarus',
    'Belgium',
    'Belize',
    'Benin',
    'Bhutan',
    'Bolivia',
    'Bosnia and Herzegovina',
    'Botswana',
    'Brazil',
    'Brunei',
    'Bulgaria',
    'Burkina Faso',
    'Burundi',
    'Cabo Verde',
    'Cambodia',
    'Cameroon',
    'Canada',
    'Central African Republic',
    'Chad',
    'Chile',
    'China',
    'Colombia',
    'Comoros',
    'Congo (Republic of the Congo)',
    'Costa Rica',
    "Côte d'Ivoire",
    'Croatia',
    'Cuba',
    'Cyprus',
    'Czechia',
    'Democratic Republic of the Congo',
    'Denmark',
    'Djibouti',
    'Dominica',
    'Dominican Republic',
    'Ecuador',
    'Egypt',
    'El Salvador',
    'Equatorial Guinea',
    'Eritrea',
    'Estonia',
    'Eswatini',
    'Ethiopia',
    'Fiji',
    'Finland',
    'France',
    'Gabon',
    'Gambia',
    'Georgia',
    'Germany',
    'Ghana',
    'Greece',
    'Grenada',
    'Guatemala',
    'Guinea',
    'Guinea-Bissau',
    'Guyana',
    'Haiti',
    'Honduras',
    'Hungary',
    'Iceland',
    'India',
    'Indonesia',
    'Iran',
    'Iraq',
    'Ireland',
    'Israel',
    'Italy',
    'Jamaica',
    'Japan',
    'Jordan',
    'Kazakhstan',
    'Kenya',
    'Kiribati',
    'Kuwait',
    'Kyrgyzstan',
    'Laos',
    'Latvia',
    'Lebanon',
    'Lesotho',
    'Liberia',
    'Libya',
    'Liechtenstein',
    'Lithuania',
    'Luxembourg',
    'Madagascar',
    'Malawi',
    'Malaysia',
    'Maldives',
    'Mali',
    'Malta',
    'Marshall Islands',
    'Mauritania',
    'Mauritius',
    'Mexico',
    'Micronesia',
    'Moldova',
    'Monaco',
    'Mongolia',
    'Montenegro',
    'Morocco',
    'Mozambique',
    'Myanmar',
    'Namibia',
    'Nauru',
    'Nepal',
    'Netherlands',
    'New Zealand',
    'Nicaragua',
    'Niger',
    'Nigeria',
    'North Korea',
    'North Macedonia',
    'Norway',
    'Oman',
    'Pakistan',
    'Palau',
    'Palestine',
    'Panama',
    'Papua New Guinea',
    'Paraguay',
    'Peru',
    'Philippines',
    'Poland',
    'Portugal',
    'Qatar',
    'Romania',
    'Russia',
    'Rwanda',
    'Saint Kitts and Nevis',
    'Saint Lucia',
    'Saint Vincent and the Grenadines',
    'Samoa',
    'San Marino',
    'Sao Tome and Principe',
    'Saudi Arabia',
    'Senegal',
    'Serbia',
    'Seychelles',
    'Sierra Leone',
    'Singapore',
    'Slovakia',
    'Slovenia',
    'Solomon Islands',
    'Somalia',
    'South Africa',
    'South Korea',
    'South Sudan',
    'Spain',
    'Sri Lanka',
    'Sudan',
    'Suriname',
    'Sweden',
    'Switzerland',
    'Syria',
    'Taiwan',
    'Tajikistan',
    'Tanzania',
    'Thailand',
    'Timor-Leste',
    'Togo',
    'Tonga',
    'Trinidad and Tobago',
    'Tunisia',
    'Türkiye',
    'Turkmenistan',
    'Tuvalu',
    'Uganda',
    'Ukraine',
    'United Arab Emirates',
    'United Kingdom',
    'United States',
    'Uruguay',
    'Uzbekistan',
    'Vanuatu',
    'Vatican City',
    'Venezuela',
    'Vietnam',
    'Yemen',
    'Zambia',
    'Zimbabwe',
]

COUNTRY_DIAL_CODES = {
    'Afghanistan': '+93',
    'Albania': '+355',
    'Algeria': '+213',
    'Andorra': '+376',
    'Angola': '+244',
    'Antigua and Barbuda': '+1268',
    'Argentina': '+54',
    'Armenia': '+374',
    'Australia': '+61',
    'Austria': '+43',
    'Azerbaijan': '+994',
    'Bahamas': '+1242',
    'Bahrain': '+973',
    'Bangladesh': '+880',
    'Barbados': '+1246',
    'Belarus': '+375',
    'Belgium': '+32',
    'Belize': '+501',
    'Benin': '+229',
    'Bhutan': '+975',
    'Bolivia': '+591',
    'Bosnia and Herzegovina': '+387',
    'Botswana': '+267',
    'Brazil': '+55',
    'Brunei': '+673',
    'Bulgaria': '+359',
    'Burkina Faso': '+226',
    'Burundi': '+257',
    'Cabo Verde': '+238',
    'Cambodia': '+855',
    'Cameroon': '+237',
    'Canada': '+1',
    'Central African Republic': '+236',
    'Chad': '+235',
    'Chile': '+56',
    'China': '+86',
    'Colombia': '+57',
    'Comoros': '+269',
    'Congo (Republic of the Congo)': '+242',
    'Costa Rica': '+506',
    "Côte d'Ivoire": '+225',
    'Croatia': '+385',
    'Cuba': '+53',
    'Cyprus': '+357',
    'Czechia': '+420',
    'Democratic Republic of the Congo': '+243',
    'Denmark': '+45',
    'Djibouti': '+253',
    'Dominica': '+1767',
    'Dominican Republic': '+1809',
    'Ecuador': '+593',
    'Egypt': '+20',
    'El Salvador': '+503',
    'Equatorial Guinea': '+240',
    'Eritrea': '+291',
    'Estonia': '+372',
    'Eswatini': '+268',
    'Ethiopia': '+251',
    'Fiji': '+679',
    'Finland': '+358',
    'France': '+33',
    'Gabon': '+241',
    'Gambia': '+220',
    'Georgia': '+995',
    'Germany': '+49',
    'Ghana': '+233',
    'Greece': '+30',
    'Grenada': '+1473',
    'Guatemala': '+502',
    'Guinea': '+224',
    'Guinea-Bissau': '+245',
    'Guyana': '+592',
    'Haiti': '+509',
    'Honduras': '+504',
    'Hungary': '+36',
    'Iceland': '+354',
    'India': '+91',
    'Indonesia': '+62',
    'Iran': '+98',
    'Iraq': '+964',
    'Ireland': '+353',
    'Israel': '+972',
    'Italy': '+39',
    'Jamaica': '+1876',
    'Japan': '+81',
    'Jordan': '+962',
    'Kazakhstan': '+76',
    'Kenya': '+254',
    'Kiribati': '+686',
    'Kuwait': '+965',
    'Kyrgyzstan': '+996',
    'Laos': '+856',
    'Latvia': '+371',
    'Lebanon': '+961',
    'Lesotho': '+266',
    'Liberia': '+231',
    'Libya': '+218',
    'Liechtenstein': '+423',
    'Lithuania': '+370',
    'Luxembourg': '+352',
    'Madagascar': '+261',
    'Malawi': '+265',
    'Malaysia': '+60',
    'Maldives': '+960',
    'Mali': '+223',
    'Malta': '+356',
    'Marshall Islands': '+692',
    'Mauritania': '+222',
    'Mauritius': '+230',
    'Mexico': '+52',
    'Micronesia': '+691',
    'Moldova': '+373',
    'Monaco': '+377',
    'Mongolia': '+976',
    'Montenegro': '+382',
    'Morocco': '+212',
    'Mozambique': '+258',
    'Myanmar': '+95',
    'Namibia': '+264',
    'Nauru': '+674',
    'Nepal': '+977',
    'Netherlands': '+31',
    'New Zealand': '+64',
    'Nicaragua': '+505',
    'Niger': '+227',
    'Nigeria': '+234',
    'North Korea': '+850',
    'North Macedonia': '+389',
    'Norway': '+47',
    'Oman': '+968',
    'Pakistan': '+92',
    'Palau': '+680',
    'Palestine': '+970',
    'Panama': '+507',
    'Papua New Guinea': '+675',
    'Paraguay': '+595',
    'Peru': '+51',
    'Philippines': '+63',
    'Poland': '+48',
    'Portugal': '+351',
    'Qatar': '+974',
    'Romania': '+40',
    'Russia': '+7',
    'Rwanda': '+250',
    'Saint Kitts and Nevis': '+1869',
    'Saint Lucia': '+1758',
    'Saint Vincent and the Grenadines': '+1784',
    'Samoa': '+685',
    'San Marino': '+378',
    'Sao Tome and Principe': '+239',
    'Saudi Arabia': '+966',
    'Senegal': '+221',
    'Serbia': '+381',
    'Seychelles': '+248',
    'Sierra Leone': '+232',
    'Singapore': '+65',
    'Slovakia': '+421',
    'Slovenia': '+386',
    'Solomon Islands': '+677',
    'Somalia': '+252',
    'South Africa': '+27',
    'South Korea': '+82',
    'South Sudan': '+211',
    'Spain': '+34',
    'Sri Lanka': '+94',
    'Sudan': '+249',
    'Suriname': '+597',
    'Sweden': '+46',
    'Switzerland': '+41',
    'Syria': '+963',
    'Taiwan': '+886',
    'Tajikistan': '+992',
    'Tanzania': '+255',
    'Thailand': '+66',
    'Timor-Leste': '+670',
    'Togo': '+228',
    'Tonga': '+676',
    'Trinidad and Tobago': '+1868',
    'Tunisia': '+216',
    'Türkiye': '+90',
    'Turkmenistan': '+993',
    'Tuvalu': '+688',
    'Uganda': '+256',
    'Ukraine': '+380',
    'United Arab Emirates': '+971',
    'United Kingdom': '+44',
    'United States': '+1',
    'Uruguay': '+598',
    'Uzbekistan': '+998',
    'Vanuatu': '+678',
    'Vatican City': '+39',
    'Venezuela': '+58',
    'Vietnam': '+84',
    'Yemen': '+967',
    'Zambia': '+260',
    'Zimbabwe': '+263',
}

TEAM_MEMBERS = [
    'Mohammad Mahtabur Rahman',
    'Abdul Latheef Mappilakath',
    'Kalimuddin Nasiruddin Shaikh',
    'Pradip Kumar Sen',
    'Sanket Mukheshchandra Desai',
]

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]


# =====================================================
# DATABASE
# =====================================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return column_name in [row[1] for row in cursor.fetchall()]


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exhibitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exhibition_name TEXT NOT NULL,
            location TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            country TEXT NOT NULL,
            email TEXT NOT NULL,
            company_name TEXT,
            contacted_person TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Safe migrations for existing databases
    if not column_exists(cursor, "visitors", "phone"):
        cursor.execute("ALTER TABLE visitors ADD COLUMN phone TEXT")

    if not column_exists(cursor, "visitors", "exhibition_id"):
        cursor.execute("ALTER TABLE visitors ADD COLUMN exhibition_id INTEGER")

    conn.commit()
    conn.close()


def normalize_country(country):
    country = country.strip()
    key = country.lower().replace(".", "").replace(" ", "")
    if key in {"uae", "unitedarabemirates"}:
        return "United Arab Emirates"
    return country


def load_customers():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT
            v.*,
            e.exhibition_name,
            e.location AS exhibition_location,
            e.start_date AS exhibition_start_date,
            e.end_date AS exhibition_end_date
        FROM visitors v
        LEFT JOIN exhibitions e ON v.exhibition_id = e.id
        ORDER BY v.id DESC
    """, conn)
    conn.close()

    if "country" in df.columns:
        df["country"] = df["country"].fillna("").apply(normalize_country)

    return df


def get_exhibitions():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT *
        FROM exhibitions
        ORDER BY start_date DESC, id DESC
    """, conn)
    conn.close()
    return df


def get_active_exhibition():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, exhibition_name, location, start_date, end_date
        FROM exhibitions
        WHERE is_active = 1
        ORDER BY id DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return row


def create_exhibition(name, location, start_date, end_date, make_active=True):
    conn = get_connection()
    cursor = conn.cursor()

    if make_active:
        cursor.execute("UPDATE exhibitions SET is_active = 0")

    cursor.execute("""
        INSERT INTO exhibitions (
            exhibition_name,
            location,
            start_date,
            end_date,
            is_active,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name.strip(),
        location.strip(),
        start_date.isoformat(),
        end_date.isoformat(),
        1 if make_active else 0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def set_active_exhibition(exhibition_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE exhibitions SET is_active = 0")
    cursor.execute(
        "UPDATE exhibitions SET is_active = 1 WHERE id = ?",
        (int(exhibition_id),)
    )
    conn.commit()
    conn.close()


def save_customer(
    customer_name,
    country,
    phone,
    email,
    company_name,
    contacted_person,
    rating,
    review
):
    active = get_active_exhibition()
    exhibition_id = active[0] if active else None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO visitors (
            customer_name,
            country,
            phone,
            email,
            company_name,
            contacted_person,
            rating,
            review,
            created_at,
            exhibition_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_name.strip(),
        normalize_country(country),
        phone.strip(),
        email.strip().lower(),
        company_name.strip(),
        contacted_person,
        rating,
        review.strip(),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        exhibition_id
    ))

    conn.commit()
    conn.close()


# =====================================================
# VALIDATION
# =====================================================

def valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def clean_phone_number(value):
    return re.sub(r"[^0-9]", "", value or "")


# =====================================================
# APP STATE
# =====================================================

create_database()

if "page" not in st.session_state:
    st.session_state.page = "customer"

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if "selected_employee" not in st.session_state:
    st.session_state.selected_employee = TEAM_MEMBERS[0]


# =====================================================
# COMMON UI
# =====================================================

def show_logo():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=320)
    else:
        st.title("AL HARAMAIN")
        st.caption("PERFUMES")


# =====================================================
# CUSTOMER PAGE
# =====================================================

def customer_page():
    show_logo()

    if st.session_state.submitted:
        st.success("✅ Thank You!")
        st.header("Thank you for visiting Al Haramain Perfumes.")
        st.write("We truly appreciate your time and valuable feedback.")
        st.write("We look forward to staying connected with you.")

        if st.button("Register Next Visitor", use_container_width=True):
            st.session_state.submitted = False
            st.rerun()
        return

    active = get_active_exhibition()
    if active:
        _, ex_name, ex_location, ex_start, ex_end = active
        st.caption(
            f"Current Exhibition: {ex_name} • {ex_location} • "
            f"{ex_start} to {ex_end}"
        )

    st.header("Welcome to Al Haramain Perfumes")
    st.write(
        "Thank you for visiting us. "
        "Please share a few details so we can stay connected."
    )

    customer_name = st.text_input(
        "Your Name *",
        placeholder="Enter your name"
    )

    country = st.selectbox(
        "Country *",
        ["Select Country"] + COUNTRIES
    )

    dial_code = COUNTRY_DIAL_CODES.get(country, "")

    phone_col1, phone_col2 = st.columns([1, 3])
    with phone_col1:
        st.text_input(
            "Code",
            value=dial_code,
            disabled=True
        )
    with phone_col2:
        local_phone = st.text_input(
            "Phone Number *",
            placeholder="Enter phone number only"
        )

    email = st.text_input(
        "Email Address *",
        placeholder="example@company.com"
    )

    company_name = st.text_input(
        "Company Name",
        placeholder="Optional"
    )

    contacted_person = st.selectbox(
        "Who did you meet today? *",
        ["Select Team Member"] + TEAM_MEMBERS
    )

    st.subheader("How was your experience?")

    rating = st.radio(
        "Rating",
        [1, 2, 3, 4, 5],
        index=None,
        horizontal=True,
        format_func=lambda x: f"{x} ⭐",
        label_visibility="collapsed"
    )

    review = st.text_area(
        "Review / Comment",
        placeholder="Anything you would like to share? (Optional)",
        height=90
    )

    if st.button("SUBMIT", use_container_width=True):
        phone_digits = clean_phone_number(local_phone)

        if not customer_name.strip():
            st.error("Please enter your name.")
        elif country == "Select Country":
            st.error("Please select your country.")
        elif not phone_digits:
            st.error("Please enter your phone number.")
        elif len(phone_digits) < 6 or len(phone_digits) > 15:
            st.error("Please enter a valid phone number.")
        elif not email.strip():
            st.error("Please enter your email.")
        elif not valid_email(email):
            st.error("Please enter a valid email.")
        elif contacted_person == "Select Team Member":
            st.error("Please select the team member you met.")
        elif rating is None:
            st.error("Please select your rating.")
        else:
            full_phone = f"{dial_code}{phone_digits}"

            save_customer(
                customer_name,
                country,
                full_phone,
                email,
                company_name,
                contacted_person,
                rating,
                review
            )

            st.session_state.submitted = True
            st.rerun()

    st.divider()
    st.caption("Al Haramain Perfumes • Exhibition Visitor Registration")

    with st.expander("Admin Access"):
        if st.button("Open Admin Dashboard"):
            st.session_state.page = "admin"
            st.rerun()


# =====================================================
# ADMIN PAGE
# =====================================================

def admin_page():
    show_logo()

    # ENTER key submits this form
    if not st.session_state.admin_login:
        st.header("Admin Login")

        with st.form("admin_login_form"):
            password = st.text_input(
                "Admin Password",
                type="password"
            )
            login_submit = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_submit:
            if password == ADMIN_PASSWORD:
                st.session_state.admin_login = True
                st.rerun()
            else:
                st.error("Incorrect password.")

        if st.button("← Back to Customer Form"):
            st.session_state.page = "customer"
            st.rerun()
        return

    df = load_customers()
    exhibitions = get_exhibitions()

    st.header("Exhibition Dashboard")

    # -------------------------
    # Exhibition setup
    # -------------------------
    with st.expander("⚙ Exhibition Setup", expanded=False):
        st.markdown("**Create a new exhibition**")

        ex_name = st.text_input(
            "Exhibition Name",
            placeholder="e.g. Beautyworld USA"
        )

        ex_location = st.text_input(
            "Location",
            placeholder="e.g. Las Vegas, USA"
        )

        d1, d2 = st.columns(2)
        with d1:
            ex_start = st.date_input(
                "Start Date",
                value=date.today(),
                key="new_ex_start"
            )
        with d2:
            ex_end = st.date_input(
                "End Date",
                value=date.today(),
                key="new_ex_end"
            )

        if st.button(
            "Save & Set as Current Exhibition",
            use_container_width=True
        ):
            if not ex_name.strip() or not ex_location.strip():
                st.warning("Please enter exhibition name and location.")
            elif ex_end < ex_start:
                st.warning("End date cannot be before start date.")
            else:
                create_exhibition(
                    ex_name,
                    ex_location,
                    ex_start,
                    ex_end,
                    make_active=True
                )
                st.success("Exhibition saved and set as current.")
                st.rerun()

        if not exhibitions.empty:
            st.markdown("**Change current exhibition**")

            exhibition_labels = {
                f"{row['exhibition_name']} • {row['location']} • "
                f"{row['start_date']} to {row['end_date']}": row["id"]
                for _, row in exhibitions.iterrows()
            }

            active_choice = st.selectbox(
                "Select Exhibition",
                list(exhibition_labels.keys())
            )

            if st.button("Set Selected Exhibition as Current"):
                set_active_exhibition(exhibition_labels[active_choice])
                st.success("Current exhibition updated.")
                st.rerun()

    active = get_active_exhibition()
    if active:
        _, ex_name, ex_location, ex_start, ex_end = active
        st.caption(
            f"Current: {ex_name} • {ex_location} • "
            f"{ex_start} to {ex_end}"
        )
    else:
        st.warning(
            "No current exhibition is set. "
            "New visitors will be saved without an exhibition tag."
        )

    if df.empty:
        st.info("No visitors registered yet.")
    else:
        # -------------------------
        # Date + exhibition filter
        # -------------------------
        df["visit_date"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        ).dt.date

        filter_col1, filter_col2 = st.columns([1, 2])

        with filter_col1:
            selected_date = st.date_input(
                "Date",
                value=date.today(),
                key="dashboard_date"
            )

        with filter_col2:
            exhibition_options = ["All Exhibitions"]
            if "exhibition_name" in df.columns:
                exhibition_options += sorted(
                    [
                        x for x in df["exhibition_name"]
                        .dropna()
                        .astype(str)
                        .unique()
                        .tolist()
                        if x.strip()
                    ]
                )

            selected_exhibition = st.selectbox(
                "Exhibition",
                exhibition_options
            )

        filtered_df = df[df["visit_date"] == selected_date].copy()

        if selected_exhibition != "All Exhibitions":
            filtered_df = filtered_df[
                filtered_df["exhibition_name"] == selected_exhibition
            ]

        st.metric(
            f"Total Clients • {selected_date.strftime('%d %b %Y')}",
            len(filtered_df)
        )

        # -------------------------
        # Employee buttons
        # -------------------------
        st.markdown("### Team Members")

        cols = st.columns(len(TEAM_MEMBERS))
        for idx, member in enumerate(TEAM_MEMBERS):
            with cols[idx]:
                if st.button(
                    member,
                    key=f"employee_button_{idx}",
                    use_container_width=True
                ):
                    st.session_state.selected_employee = member

        selected_employee = st.session_state.selected_employee

        employee_df = filtered_df[
            filtered_df["contacted_person"] == selected_employee
        ].copy()

        st.markdown(
            f"### {selected_employee} — {len(employee_df)} Client(s)"
        )

        if employee_df.empty:
            st.info("No clients for this employee on the selected date/filter.")
        else:
            employee_df["created_at"] = pd.to_datetime(
                employee_df["created_at"],
                errors="coerce"
            ).dt.strftime("%d-%m-%Y %I:%M %p")

            columns = [
                "customer_name",
                "created_at",
                "country",
                "phone",
                "email",
                "company_name",
                "rating",
                "review",
                "exhibition_name"
            ]

            employee_view = employee_df[
                [c for c in columns if c in employee_df.columns]
            ].rename(
                columns={
                    "customer_name": "Customer Name",
                    "created_at": "Date & Time",
                    "country": "Country",
                    "phone": "Phone",
                    "email": "Email",
                    "company_name": "Company",
                    "rating": "Rating",
                    "review": "Review",
                    "exhibition_name": "Exhibition"
                }
            )

            st.dataframe(
                employee_view,
                use_container_width=True,
                hide_index=True,
                height=300
            )

        # -------------------------
        # Compact admin tools
        # -------------------------
        with st.expander("Admin Tools", expanded=False):
            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇ Download All Customer Data",
                data=csv,
                file_name="al_haramain_customers.csv",
                mime="text/csv",
                use_container_width=True
            )

            delete_options = {
                f"ID {row['id']} — {row['customer_name']} — {row['email']}": row["id"]
                for _, row in df.iterrows()
            }

            selected_visitor = st.selectbox(
                "Delete Visitor",
                ["Select Visitor"] + list(delete_options.keys())
            )

            confirm_delete = st.checkbox(
                "I confirm that I want to delete this visitor."
            )

            if st.button(
                "🗑 Delete Selected Visitor",
                use_container_width=True
            ):
                if selected_visitor == "Select Visitor":
                    st.warning("Please select a visitor.")
                elif not confirm_delete:
                    st.warning("Please confirm deletion first.")
                else:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "DELETE FROM visitors WHERE id = ?",
                        (delete_options[selected_visitor],)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Visitor deleted successfully.")
                    st.rerun()

    st.divider()

    nav1, nav2 = st.columns(2)

    with nav1:
        if st.button(
            "← Customer Form",
            use_container_width=True
        ):
            st.session_state.page = "customer"
            st.rerun()

    with nav2:
        if st.button(
            "Logout",
            use_container_width=True
        ):
            st.session_state.admin_login = False
            st.session_state.page = "customer"
            st.rerun()


# =====================================================
# RUN PAGE
# =====================================================

if st.session_state.page == "customer":
    customer_page()
else:
    admin_page()
