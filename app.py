#!/usr/bin/env python3

import hashlib
import os
import time
import uuid
from collections import Counter
from datetime import datetime

import qrcode
import streamlit as st

st.set_page_config(layout="wide")


def setup_session():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
        os.makedirs("submissions", exist_ok=True)
        session_file = f"submissions/{st.session_state.session_id}"
        open(session_file, "a").close()


def show_qrcode():
    import io

    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data("https://survey-curation-kb5vthfywnfhq3momv9w6k.streamlit.app/")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Scan to access the survey", width=200)


def build_form():
    col1, col2 = st.columns(2)
    with col2:
        show_qrcode()
    with col1:
        st.write(
            "# Willing to help authors curate and publish their data for a Journal?"
        )
        st.write("# What do you need ?")

    scientific_field = st.selectbox(
        "Scientific field:",
        [
            "",
            "Other",
            "Agricultural and Food Sciences",
            "Anthropology",
            "Archaeology",
            "Architecture",
            "Art History",
            "Astronomy",
            "Biochemistry",
            "Biology",
            "Biotechnology",
            "Chemistry",
            "Classical Studies",
            "Computer Science",
            "Earth Sciences",
            "Ecology",
            "Economics",
            "Education Sciences",
            "Civil Engineering",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Engineering",
            "Environmental Sciences",
            "Evolutionary Biology",
            "Gender Studies",
            "History",
            "Law",
            "Linguistics and Literature",
            "Materials Science",
            "Mathematics",
            "Media and Communication Studies",
            "Medicine",
            "Microbiology",
            "Musicology",
            "Neurosciences",
            "Philosophy",
            "Physics",
            "Plant and Animal Biology",
            "Political Science",
            "Psychology",
            "Religious Studies",
            "Social and Cultural Geography",
            "Sociology",
            "Theology",
            "Veterinary Medicine",
        ],
    )

    other_field = ""
    if scientific_field == "Other":
        other_field = st.text_input("Please specify the scientific field:")

    features = st.text_area("Necessary features for a curation tool/framework:")
    submitted = st.button("Submit")
    if submitted:
        if not scientific_field:
            st.error("Please select a scientific field.")
        elif not features.strip():
            st.warning("Please enter at least one necessary feature.")
        else:
            display_field = (
                other_field if scientific_field == "Other" else scientific_field
            )
            os.makedirs("submissions", exist_ok=True)
            filename = f"submissions/{st.session_state.session_id}_answer.txt"
            with open(filename, "a") as f:
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Scientific field: {display_field}\n")
                f.write(f"Necessary features: {features}\n")
                f.write("-" * 40 + "\n")
            st.success(f"Your contribution was saved")
            # st.write("Scientific field:", display_field)
            # st.write("Necessary features:", features)


def show_progress():
    import matplotlib.pyplot as plt
    from wordcloud import STOPWORDS, WordCloud

    submissions_dir = "submissions"

    col1, col2 = st.columns(2)
    with col2:
        show_qrcode()
        if st.button("Clear Survey?"):
            import shutil

            shutil.rmtree(submissions_dir)
    with col1:
        st.write("# Submissions Progress")

    os.makedirs(submissions_dir, exist_ok=True)

    current_files = sorted(
        [f for f in os.listdir(submissions_dir) if f.endswith("_answer.txt")]
    )

    st.write(f"## Total submissions: {len(current_files)}")
    st.write("---")

    if not current_files:
        st.info("No submissions yet.")
    else:
        field_counts = Counter()
        all_features = []

        for filename in current_files:
            filepath = os.path.join(submissions_dir, filename)
            with open(filepath, "r") as f:
                content = f.read()
            for line in content.splitlines():
                if line.startswith("Scientific field: "):
                    field = line.replace("Scientific field: ", "").strip()
                    field_counts[field] += 1
                elif line.startswith("Necessary features: "):
                    features = line.replace("Necessary features: ", "").strip()
                    all_features.append(features)

        col1, col2 = st.columns(2)

        with col1:
            # Pie chart (cached by content hash)
            pie_hash = hashlib.md5(
                str(sorted(field_counts.items())).encode()
            ).hexdigest()
            pie_path = f"{submissions_dir}/piechart_{pie_hash}.png"

            st.subheader("Scientific Fields")
            if os.path.exists(pie_path):
                st.image(pie_path)
            else:
                labels, values = zip(*field_counts.items())
                fig, ax = plt.subplots()
                ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
                ax.axis("equal")
                st.pyplot(fig)
                fig.savefig(pie_path, bbox_inches="tight")
                plt.close(fig)

        with col2:
            # Word cloud (cached by content hash)
            text = " ".join(all_features)
            wc_hash = hashlib.md5(text.encode()).hexdigest()
            wc_path = f"{submissions_dir}/wordcloud_{wc_hash}.png"

            st.subheader("Features")
            if os.path.exists(wc_path):
                st.image(wc_path)
            else:
                stopwords = set(STOPWORDS)
                french_stopwords = {
                    "le",
                    "la",
                    "les",
                    "un",
                    "une",
                    "des",
                    "et",
                    "ou",
                    "de",
                    "du",
                    "en",
                    "a",
                    "au",
                    "aux",
                    "pour",
                    "par",
                    "sur",
                    "dans",
                    "avec",
                    "sans",
                    "sous",
                    "ce",
                    "cet",
                    "cette",
                    "ces",
                    "mon",
                    "ton",
                    "son",
                    "notre",
                    "votre",
                    "leur",
                    "que",
                    "qui",
                    "quoi",
                    "dont",
                    "où",
                    "mais",
                    "donc",
                    "or",
                    "ni",
                    "car",
                    "je",
                    "tu",
                    "il",
                    "elle",
                    "nous",
                    "vous",
                    "ils",
                    "elles",
                    "est",
                    "sont",
                    "être",
                    "avoir",
                    "faire",
                    "aller",
                    "pouvoir",
                    "vouloir",
                    "devoir",
                    "venir",
                    "voir",
                    "savoir",
                    "falloir",
                    "fallait",
                    "faut",
                    "plus",
                    "moins",
                    "très",
                    "tout",
                    "tous",
                    "toute",
                    "toutes",
                    "autre",
                    "autres",
                    "même",
                    "si",
                    "tant",
                    "tel",
                    "telle",
                    "tels",
                    "telles",
                    "comme",
                    "dont",
                    "ainsi",
                    "alors",
                    "ceci",
                    "cela",
                    "celui",
                    "celle",
                    "ceux",
                    "celles",
                    "y",
                    "en",
                    "là",
                }
                stopwords.update(french_stopwords)

                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color="white",
                    stopwords=stopwords,
                ).generate(text)

                fig2, ax2 = plt.subplots(figsize=(10, 5))
                ax2.imshow(wc, interpolation="bilinear")
                ax2.axis("off")
                st.pyplot(fig2)
                fig2.savefig(wc_path, bbox_inches="tight")
                plt.close(fig2)

        # for filename in current_files:
        #     filepath = os.path.join(submissions_dir, filename)
        #     with open(filepath, "r") as f:
        #         content = f.read()
        #     with st.expander(f"📄 {filename}"):
        #         st.text(content)

    # Auto-refresh every 2 seconds
    time.sleep(2)
    st.rerun()


def main():
    params = st.query_params
    if "progress" in params:
        show_progress()
    else:
        setup_session()
        build_form()


if __name__ == "__main__":
    main()
