'''
    DS2000
    Jeremy Epstein and Kevin Largey
    Fantasy Football Project
    Functions
'''

import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from scipy import stats
from Football_Project_functions import *

##############################################################################
# Indices for complete rows
POSITION_INDEX = 1
ADP_INDEX = 2
VBD_INDEX = 3

# colors for each position
QB_COLOR = "yellow"
WR_COLOR = "tab:green"
RB_COLOR = "tab:red"
TE_COLOR = "tab:purple"

plt.rcParams['axes.facecolor'] = 'gainsboro'

def read_football_data(filename):
    ''' function: read_football_data
        input: filename (string)
        returns: tuple (header, football_data)
                 header is a list of the header row
                 football_data is list of lists

        Function reads in csv files into lists of list
        Also extracts header
    '''
    first = True
    football_data = []
    # data is read into program from csv and placed in football_data
    with open(filename,encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # header row is located and placed into header list
        for row in csv_reader:
            if first:
                header=row
                first = False
                continue
            # each row of csv is placed into football_data
            football_data.append(row)
    return (header, football_data)

def get_players(draft_header, draft_data):
    ''' function: get_players
        input: draft_header (list), draft_data(list of lists)
        returns: players, list of players names

        This function will make a separate list of all the names
        in the fantasy draft data
    '''
    # Player column index is located in header
    for name in range(len(draft_header)):
        if draft_header[name] == ('Player'):
            player_index = name
            
    # Player list is initialized and filled with names
    players = []
    for row in draft_data:
        players.append(row[player_index])     

    return players

def get_adp(draft_header, draft_data):
    ''' function: get_adp
        input: draft_header (list), draft_data(list of lists)
        returns: adp, list of players average draft position

        This function will make a separate list of all the avg
        draft positions from the fantasy draft data

        Since the players in the csv are sorted by descending adp,
        the indices in the players list will match with their adps
        in the list created in this function
    '''
    # Average draft position column index is located in header
    for name in range(len(draft_header)):
        if draft_header[name] == ('AVG'):
            adp_index = name
    # adp list is initialized and filled with adp values
    adp = []
    for row in draft_data:
        adp.append(row[adp_index])
        
    return adp

def get_positions(draft_header, draft_data):
    ''' function: get_positions
        input: draft_header (list), draft_data(list of lists)
        returns: positions, list of players' positions

        This function will make a separate list of all the
        positions each player plays

        Since the players and their positions in the csv are
        sorted by descending adp, the indices in the players
        list will match with their positions in the list
        created in this function
    '''
   
    for name in range(len(draft_header)):
        if draft_header[name] == ('POS'):
            position_index = name

    positions = []
    for row in draft_data:
        positions.append(row[position_index])

    return positions


def scrub_names(player_names):
    ''' function: scrub_names
        input: player_names(list)
        returns: scrubbed_names, new list of names
    
        This function will take the list of names from either
        the fantasy draft list of names or the actual results
        list of names and remove any symbols that will prevent
        the names from being matched later on
    '''

    # new names list is initialized
    scrubbed_names = []
    # old list of names is traversed, unwanted symbols are removed
    for name in player_names:
        name = name.replace("+","")
        name = name.replace("*","")
        name = name.replace("'","")
        name = name.replace(".","")
        name = name.upper()
        scrubbed_names.append(name)
        
    return scrubbed_names
    
    
def match_vbd(draft_names, adp, positions, results_header, results_data):
    
    ''' function: get_results
        input: draft_names (list of names in the draft), positions (list of player's
               positions, adp (descending list of average draft position by player),
               results_header (list), results_data (list of lists)
        returns: player_adp_results (list of tuples providing the player, position,
                 his adp, and his vbd)

        This function takes the list of names from the draft and matches them to
        their VBD value in the results VBD. Since the draft names arleady correspond
        to the players'  position and ADP value, all that needs to be done is attach
        his VBD value
    '''

    # Player column index is located in results header
    for name in range(len(results_header)):
        if results_header[name] == ('Player'):
            player_index = name
        
    # VBD column index is located in header        
    for name in range(len(results_header)):
        if results_header[name] == ('VBD'):
            vbd_index = name

            
    # list of names from results and list of vbd initialized
    result_names = []
    vbd = []

    # results csv traversed, fills the two lists
    for row in results_data:
        result_names.append(row[player_index])
        vbd.append(row[vbd_index])
        
    # list of names from draft and from results is scrubbed
    draft_names = scrub_names(draft_names)
    result_names = scrub_names(result_names)

    # list to put all three together is initialized
    player_adp_vbd = []
    
    # count increments with the names so adp and position lists may also be traversed
    draft_count = 0

    ''' For each name in the list of draft names, the name is compared to every
        name in the results list. Once the name is matched, the vbd from that index
        is extracted and is paired with that player's name, ADP and VBD. This information
        is put into a list as a tuple (name, adp, vbd)
    '''
    for draft_name in draft_names:
        result_count = 0
        for result_name in result_names:
            if draft_name == result_name:
                player_adp_vbd.append((draft_name,positions[draft_count],adp[draft_count],vbd[result_count]))
            result_count+=1
        draft_count+=1
    return player_adp_vbd




def get_quarterbacks(player_pos_adp_vbd):
    ''' function: get_quarterbacks
        input: player_pos_adp_vbd
        returns: quarterbacks, list of tuples of all QBs
        including their names, positions, adp and vbd

        The purpose of the next five functions is to separate
        the player data by position so we can observe how the
        valuation of players might differ based on the position
        they play
    '''

    # list of quarterbacks initialized
    quarterbacks = []
    # if POS is QB, the tuple is added to the list
    for row in player_pos_adp_vbd:
        if "QB" in row[1]:
            quarterbacks.append(row)
        
    return quarterbacks

def get_wide_receivers(player_pos_adp_vbd):
    ''' function: get_wide_receivers
        input: player_pos_adp_vbd
        returns: wide_receivers, list of tuples of all WRs
        including their names, positions, adp and vbd
    '''

    # list of wide receivers initialized
    wide_receivers = []
    # if POS is WR, the tuple is added to the list
    for row in player_pos_adp_vbd:
        if "WR" in row[1]:
            wide_receivers.append(row)
        
    return wide_receivers

def get_running_backs(player_pos_adp_vbd):
    ''' function: get_running_backs
        input: player_pos_adp_vbd
        returns: running_backs, list of tuples of all RBs
        including their names, positions, adp and vbd
    '''
    
    # list of running backs initialized
    running_backs = []
    # if POS is RB, the tuple is added to the list
    for row in player_pos_adp_vbd:
        if "RB" in row[1]:
            running_backs.append(row)
        
    return running_backs

def get_tight_ends(player_pos_adp_vbd):
    ''' function: get_tight_ends
        input: player_pos_adp_vbd
        returns: tight_ends, list of tuples of all TEs
        including their names, positions, adp and vbd
    '''
    
    # list of tight ends initialized
    tight_ends = []
    # if POS is TE, the tuple is added to the list
    for row in player_pos_adp_vbd:
        if "TE" in row[1]:
            tight_ends.append(row)
        
    return tight_ends

def get_kickers(player_pos_adp_vbd):
    ''' function: get_kickers
        input: player_pos_adp_vbd
        returns: kickers, list of tuples of all Ks
        including their names, positions, adp and vbd
    '''

    # list of kickers initialized
    kickers = []
    # if POS is K, the tuple is added to the list
    for row in player_pos_adp_vbd:
        if "K" in row[1]:
            kickers.append(row)
        
    return kickers

def plot_from_list(player_data, title, legend):
    '''
    Parameters: a list of player data matrices. each matrix consists of a list
        of player info: name, position, ADP, VBD
        A string (the title), a string (x label), a string (y label)
    Returns: an image (graph)
    Does: graphs the results of a series of player lists
    '''
    # make list of x coordinates (ADP)
    x = []
    
    # make list of y coordinates (VBD)
    y = []

    # colors according to position
    colors = []

    # iterate through list, storing info for each
    for each in player_data:
        x.append(each[ADP_INDEX])
        y.append(each[VBD_INDEX])
        colors.append(get_color(each[POSITION_INDEX]))

    x = as_floats(x)
    y = as_floats(y)

    # legend elements
    if legend:
        qbs = mpatches.Patch(color = QB_COLOR, label='Quarterbacks')
        rbs = mpatches.Patch(color = RB_COLOR, label='Running Backs')
        wrs = mpatches.Patch(color = WR_COLOR, label='Wide Receivers')
        tes = mpatches.Patch(color = TE_COLOR, label='Tight Ends')

        plt.legend(handles = [qbs, rbs, wrs, tes])

    plt.scatter(x, y,
                s = 20, c = colors)
    # labels and titles
    plt.title(title)
    plt.xlabel('ADP')
    plt.ylabel('VBD')
    plt.ylim(-300, 300)
    plt.xlim(0, 200)
    
    
    plt.show()

def as_floats(alist):
    '''
    Parameters: a list
    Returns: a list of floats
    Does: converts all elements into floats
    '''
    # initialize
    result = []

    # turn each value of input into a float
    for each in alist:
        if each == '':
            result.append(0.0)
        else:
            result.append(float(each))
    return result
    

def get_list_at_index(list_of_matrices, index):
    '''
    Parameters: (1) list of list of lists (2) index of each row to extract
        from
    Returns: a list
    Does: extracts from a list of lists data at one given row
    '''
    # the result which will store data from each row
    result = []

    # iterate through matrix
    for matrix in list_of_matrices:
        # iterate through each row
        for row in matrix:
            result.append(row[index])
    return result

def make_one_list(list_of_lists):
    '''
    Parameters: a list of lists
    Returns: a list
    Does: appends all lists within input into a single list
    '''
    # initialize result
    result = list_of_lists[0].copy()

    # attach each in list of lists to the end of the result
    # first is already in result, ignore it
    first = True
    
    # for each list in the input
    for each_list in list_of_lists:
        if (not first):
            for element in each_list:
                result.append(element)
        first = False
    return result

def get_color(position):
    '''
    Parameters: a string (abbreviation of player's position)
    Returns: a string (color name)
    Does: returns the color associated with given position
    '''
    # read only first 2 characters
    position = position[:2]

    # assign color as position dictates
    if position == "QB":
        return QB_COLOR
    elif position == "WR":
        return WR_COLOR
    elif position == "RB":
        return RB_COLOR
    elif position == "TE":
        return TE_COLOR
    else:
        return "black"
        #print(position)
        #return 0/0


def compute_correlation(player_pos_adp_vbd):
    '''
    Parameters: a list of lists going name, position, adp, vbd
    Returns: a float on [-1, 1]
    Does: finds the correlation between 2 variables
    '''
    adp = []
    vbd = []
    
    # iterate through all rows
    for row in player_pos_adp_vbd:
        adp.append(row[ADP_INDEX])
        vbd.append(row[VBD_INDEX])

    # convert to floats
    adp = as_floats(adp)
    vbd = as_floats(vbd)

    # find correlation coefficient of all data
    return stats.pearsonr(adp, vbd)

    
    
