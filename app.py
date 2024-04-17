import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup
import requests
import re

# Create a Streamlit web app
st.set_page_config(page_title="LIVE CRICKET SCORE", page_icon="🏏")

# Define the CricketScore class
class CricketScore:

    # Scrapping the data from cricbuzz.com
    @staticmethod
    def scrap():
        URL = "https://www.cricbuzz.com/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="match_menu_container")
        scrap_results = results.find_all("li", class_="cb-match-card")
        return scrap_results

    # Load the cricket match details
    @staticmethod
    def match_details():
        details = CricketScore.scrap()
        live_match = {}
        for detail in details:
            live_team_details = {}
            summary = CricketScore.match_summary(detail)
            if summary is not None:
                match_header = CricketScore.match_header(detail).text
                teams = CricketScore.teams_name(detail)
                score_card = CricketScore.team_score(detail)
                live_team_details['summary'] = summary.text
                live_team_details['match_header'] = match_header
                live_team_details['score_card'] = score_card[0] + " :: " + score_card[1]
                live_match[teams[0] + " vs " + teams[1]] = live_team_details
        return live_match

    # Load match summary
    @staticmethod
    def match_summary(detail):
        return detail.find("div", class_="cb-mtch-crd-state")

    # Load match header
    @staticmethod
    def match_header(detail):
        return detail.find("div", class_="cb-mtch-crd-hdr")

    # Load teams' names
    @staticmethod
    def teams_name(detail):
        l = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text
        team1_index = re.search(r"\d", team1_details).start() if re.search(r"\d", team1_details) else len(team1_details)
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text
        team2_index = re.search(r"\d", team2_details).start() if re.search(r"\d", team2_details) else len(team2_details)
        l.append(team1_details[:team1_index])
        l.append(team2_details[:team2_index])
        return l

    # Load team score
    @staticmethod
    def team_score(detail):
        l = []
        team1_details = detail.find("div", class_="cb-hmscg-bat-txt").text
        team2_details = detail.find("div", class_="cb-hmscg-bwl-txt").text
        l.append(team1_details)
        l.append(team2_details)
        return l

    # Main function to display the Streamlit web app
    @staticmethod
    def main():
        st.title("LIVE CRICKET SCORE")
        #st.image(Image.open("cric.jpg"), width=800)

        # Adding live matches text to the app
        st.header("Live Matches")

        # Adding all live matches to a selection box
        matches = CricketScore.match_details()
        selected_match = st.selectbox("Select a live match:", list(matches.keys()))

        # Display match details
        if st.button("Check Score"):
            x = matches[selected_match]

            # Display team names and match header
            st.subheader(f"{selected_match} - {x['match_header']}")

            # Display score details
            st.write("Score Details:")
            st.write(x['score_card'])

            # Display match summary
            st.write("Summary:")
            st.write(x['summary'])

# Run the Streamlit app
if __name__ == "__main__":
    CricketScore.main()
