'''
Main src file to run the lenex to excel program locally
'''

from settings import Settings
from lib.club_management import Club
from lib.meet_management import SwimMeet, LenexHelper
from lib.registration_excel import RegistrationExcel

def main() -> None:
    '''Main to load setting, create a club, load in the competition and create the excel'''
    # Load or create the settings
    settings = Settings.init_settings()
    log = Settings.get_logger()

    # Create a club using the provided mdb
    club = Club(log, settings.club_name)
    club.fill_using_team_manager_mdb(settings.mdb_path)

    # Load in the competition lenex and extract the xml
    lenex = LenexHelper(log, settings.default_competition_path)
    lenex.load_lenex()
    lenex.extract_lef_from_lenex()
    lenex.load_xml_from_lef()

    # Construct a swim meet from the xml
    meet = SwimMeet(log)
    meet.load_from_xml(lenex.xml_root)

    # Create the registration excel
    excel = RegistrationExcel(log, meet.meet_name, settings.club_logo_path)
    excel.add_overview_registration_sheet(meet, club)
    excel.add_summary_sheet(meet, club)
    excel.add_valid_events_sheet(meet, club)
    excel.close()


if __name__ == "__main__":
    main()
