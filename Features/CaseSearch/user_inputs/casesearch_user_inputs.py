""""Contains test data that are used as user inputs across various areass used in Case Serach"""


class CaseSearchUserInput:
    """User Test Data"""

    """Domains"""
    casesearch = "casesearch"
    casesearch_1 = "casesearch-1"
    casesearch_2 = "casesearch-2"

    """App Names"""
    case_search_app_name = "Music App (Case Search & Claim)"
    french_app = "[French] Music App"

    """Users"""
    user_1 = 'automation-user-1'
    user_2 = 'automation-user-2'
    a_user = "a_user"
    kiran = "kiran"

    """Menus"""
    normal_menu = "Songs (Normal)"
    search_first_menu = "Songs (Search First)"
    see_more_menu = "Songs (See More)"
    skip_default_menu = "Songs (Skip to Default Search)"
    artist_menu = "Artist"
    exclude_property_from_case_search_menu = "Exclude property from case search"
    search_filter_menu = "Search Filter"
    search_setting_menu = "Songs - Case Search Settings"
    without_search_setting_menu = "Songs - Without Case Search Settings"
    inline_search_menu = "Songs Inline Case Search"
    multi_select_menu = "Songs Multi-Case List"
    display_only_forms_menu = "Play Song - Display Only Forms"
    shadow_menu = "Shadow Menu"
    musical_instruments_menu = "Musical Instruments (Performance)"
    mixed_case_type_menu = "Mixed Case Types"
    load_external_search_first_menu = "DR: Load external case into form (Search First)"
    smart_link_search_first_menu = "DR: Smart link to external domain (Search First)"
    smart_link_skip_default_menu = "DR: Smart link to external domain (Skip Default)"
    load_external_skip_default_menu = "DR: Load external case into form (Skip Default)"
    unrelated_case_load_external_menu = "Unrelated case id\'s property: Load from external domain."

    """Forms"""
    play_song_form = "Play Song"
    shows_form = "Shows"
    add_show_form = "Add Show"
    add_address_form = "Add Address"
    update_ratings_form = "Update Rating, Mood, or Energy"
    view_instruments_form = "View Instruments"
    update_song_form = "Update Song--> redirects to First Menu"

    """Pre=Configured Cases"""
    # Song-Cases

    song_automation_song = "Automation-Song-"
    song_automation_song_no_space = "AutomationSongNoSpace"
    song_automation_song_1 = "Automation-Song-1"
    song_automation_song_24 = "Automation-Song-24"
    song_automation_song_10 = "Automation-Song-10"
    song_automation_song_22 = "Automation-Song-22"
    song_case_on_casesearch2 = "Sept30_CS2"
    song_case_cs4_song_300 = "CS4 Song-300"
    song_case_on_casesearch_1 = "Bugs on casesearch-1"
    song_case_b_users_song = "b_users song"

    # Artist-Cases
    automation_artist_1 = "Automation-Artist-1"
    automation_artist_2 = "Automation-Artist-2"
    artist_no_space = "AutomationArtistNoSpace"
    artist_case_beach_boys = "Beach Boys"
    artist_case_arijit = "Arijit"

    # Show-Cases
    show_case_show1 = "Automation-Show1"
    show_case_casesearch_1 = "on casesearch-1"

    # Instruments-Cases
    instrument_case_guitar = "Guitar"

    case_with_unrelated_id = {"song_name": "Domain2_other7", "case_id": "fcc4c935-4f02-4a8c-86be-4e4cd833c3a0",
                              "rating": "5"}

    """Pre=Configured Values"""
    blank = ""
    default = "Default"
    # Rating
    one_star = "*"
    two_star = "**"
    three_star = "***"
    four_star = "****"
    five_star = "*****"
    mood_help_text = "Mood\'s Rating"
    date_2022_12_30 = "2022-12-30"
    date_30_12_2022 = "30/12/2022"
    date_12_30_2022 = "12/30/2022"
    dates = {"MM/DD/YYYY": '%m/%d/%Y', "YYYY-MM-DD": '%Y-%m-%d', "DD/MM/YYYY": "%d/%m/%Y"}
    full_home_address = "New Canada St., 3855 Brienz, Switzerland"
    full_work_address = "Avenida Benito Juárez, 77560 Alfredo V. Bonfil, Quintana Roo, Mexico"
    home_street_value = "New Canada St."
    home_city_value = "Brienz"
    work_city_value = "Alfredo V. Bonfil"
    home_country_value = "Switzerland"
    home_zipcode_value = "3855"
    home_country_belgium = "Belgium"
    required_msg = "Required"
    required_msg_if_rating_two = "This is only required if Rating = 2, otherwise not required."
    value_with_space = " es"
    validation_msg_no_spaces = "No spaces allowed!"
    validation_msg_invalid_respons = "Sorry, this response is invalid!"
    latin_music = "Latin music"
    latin_jazz = "Latin jazz"
    funk_metal = "Funk Metal"
    default_search_title = "Case Claim"
    search_title = "Song Detail"
    french_search_title = "Song Detail (French)"
    search_subtitle = "This page displays all the song properties for search"
    french_search_subtitle = "This page displays all the song properties for search (french)"
    incomplete_word_guitar = "Guit"
    acoustic_bass_guitar = "Acoustic bass guitar"
    id_with_hyphen = "1-2-3-4-5"
    id_without_hyphen = "12345"

    """Case Properties/Search Fields"""

    ratings = {one_star: '1', two_star: '2', three_star: '3', four_star: '4', five_star: '5'}
    song_name = "Song Name"
    name = "Name"
    mood = "Mood"
    energy = "Energy"
    date_opened = "Date Opened"
    rating = "Rating"
    home_street = "Home Street"
    home_country = "Home Country"
    search_home_address = 'Search Home Address'
    search_work_address = 'Search Work Address'
    artist = "Artist"
    song_release_date = "Song Release Date"
    show_date = "Show Date"
    subgenre = "SubGenre"
    genre = "Genre"
    parent_artist = "Parent Artist"
    rating_input = "Rating Input"
    instrument_name = "Instrument Name"
    song_id = "Song ID"

    # Case list columns
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"
    six = "6"
    seven = "7"
    eight = "8"
    rating_four_and_five = "#,#4#,#5"

    # Questions
    add_show_question = "Add a show in this city"
