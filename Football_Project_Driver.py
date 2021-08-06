'''
    DS2000
    Jeremy Epstein and Kevin Largey
    Fantasy Football Project
    Driver
'''

from Football_Project_functions import *

def main():    
    # read draft data
    draft_header_2019, draft_2019 = read_football_data(
        "Fantasy_Draft_Data_2019.csv")
    draft_header_2018, draft_2018 = read_football_data(
        "Fantasy_Draft_Data_2018.csv")
    draft_header_2017, draft_2017 = read_football_data(
        "Fantasy_Draft_Data_2017.csv")

    # read performance results
    results_header_2019, results_2019 = read_football_data(
        "Actual_Results_2019.csv")
    results_header_2018, results_2018 = read_football_data(
        "Actual_Results_2018.csv")
    results_header_2017, results_2017 = read_football_data(
        "Actual_Results_2017.csv")

    # gets player names
    players_2017 = get_players(draft_header_2017, draft_2017)
    # gets corresponding draft data
    adp_2017 = get_adp(draft_header_2017, draft_2017)
    # gets corresponding position data
    positions_2017 = get_positions(draft_header_2017, draft_2017)
    
    players_2018 = get_players(draft_header_2018, draft_2018)
    adp_2018 = get_adp(draft_header_2018, draft_2018)
    positions_2018 = get_positions(draft_header_2018, draft_2018)
    
    players_2019 = get_players(draft_header_2019, draft_2019)
    adp_2019 = get_adp(draft_header_2019, draft_2019)
    positions_2019 = get_positions(draft_header_2019, draft_2019)

    # data in a given year
    player_pos_adp_vbd_2017 = match_vbd(players_2017,
                                        adp_2017, positions_2017,
                                        results_header_2017,
                                        results_2017)
    player_pos_adp_vbd_2018 = match_vbd(players_2018,
                                        adp_2018,
                                        positions_2018,
                                        results_header_2018,
                                        results_2018)
    player_pos_adp_vbd_2019 = match_vbd(players_2019,
                                        adp_2019,
                                        positions_2019,
                                        results_header_2019,
                                        results_2019)

    # data for all years
    all_years = make_one_list([player_pos_adp_vbd_2017,
                 player_pos_adp_vbd_2018,
                 player_pos_adp_vbd_2019])
    
    # data for a position in a given year
    qbs_2017 = get_quarterbacks(player_pos_adp_vbd_2017)
    qbs_2018 = get_quarterbacks(player_pos_adp_vbd_2018)
    qbs_2019 = get_quarterbacks(player_pos_adp_vbd_2019)
    all_qbs = make_one_list([qbs_2019, qbs_2018, qbs_2017])

    wrs_2017 = get_wide_receivers(player_pos_adp_vbd_2017)
    wrs_2018 = get_wide_receivers(player_pos_adp_vbd_2018)
    wrs_2019 = get_wide_receivers(player_pos_adp_vbd_2019)
    all_wrs = make_one_list([wrs_2019, wrs_2018, wrs_2017])

    rbs_2017 = get_running_backs(player_pos_adp_vbd_2017)
    rbs_2018 = get_running_backs(player_pos_adp_vbd_2018)
    rbs_2019 = get_running_backs(player_pos_adp_vbd_2019)
    all_rbs = make_one_list([rbs_2019, rbs_2018, rbs_2017])


    tes_2017 = get_tight_ends(player_pos_adp_vbd_2017)
    tes_2018 = get_tight_ends(player_pos_adp_vbd_2018)
    tes_2019 = get_tight_ends(player_pos_adp_vbd_2019)
    all_tes = make_one_list([tes_2019, tes_2018, tes_2017])

    # SCATTERPLOTS
    # plot of all players
    all_title = 'Production as a result of Draft Position \n 2017-2019 seasons'
    plot_from_list(all_years, all_title, True)

    # plot of QBs
    title = 'QB Productions as a result of Draft Position \n 2017-2019 seasons'
    plot_from_list(all_qbs, title, False)

    # plot of WRs
    title = 'WR Productions as a result of Draft Position \n 2017-2019 seasons'
    plot_from_list(all_wrs, title, False)

    # plot of RBs
    title = 'RB Productions as a result of Draft Position \n 2017-2019 seasons'
    plot_from_list(all_rbs, title, False)

    # plot of TEs
    title = 'TE Productions as a result of Draft Position \n 2017-2019 seasons'
    plot_from_list(all_tes, title, False)


    # CORRELATION COEFFICIENT
    # find correlation coefficient of all data
    print('Correlation coefficient of all data:')
    print(compute_correlation(all_years))

    # find correlation coefficient of quarterback position
    print()
    print('Correlation coefficient of Quarterbacks:')
    print(compute_correlation(all_qbs))

    # find correlation coefficient of Wide Receivers
    print()
    print('Correlation coefficient of Wide Receivers:')
    print(compute_correlation(all_wrs))

    # find correlation coefficient of Running Backs
    print()
    print('Correlation coefficient of Running Backs:')
    print(compute_correlation(all_rbs))

    # find correlation coefficient of Tight ends
    print()
    print('Correlation coefficient of Tight Ends:')
    print(compute_correlation(all_tes))
   
main()


