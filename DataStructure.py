
MOVE_COLUMN          = 0
TIME_COLUMN          = 1
ACTOR_COLUMN         = 2
ACTIONS_COLUMN       = 3
COMMUNICATION_COLUMN = 4
NOTES_COLUMN         = 5

CELL_GAP_X = 20
CELL_GAP_Y = 10

## Boundary Actions

SETTING     = 0
FOLLOWING   = 1
WANDERING   = 2
PROBING     = 3
CHALLENGING = 4
ENHANCING   = 5

ICON_NAME = ["Setting", "Following", "Wandering", "Probing", "Challenging", "Enhancing"]

NO_ICON     = -1

UNCONNECTED      = -1
UNCONNECTED_DASH = (1,1)
CONNECTED_DASH   = ()

SETTING_COMPATIBLE = {SETTING, CHALLENGING, WANDERING, PROBING}

error_message = {}
error_message[1]   = "Error 1 Area not available for dropping Icons"

# Errors placing icons
error_message[101] = "Error 101 Only one Setting per row is allowed"
error_message[102] = "Error 102 Following and Enhancing are not compatible with Setting in the same row"

# errors creating links
error_message[201] = "Error 201 A Non Setting cannot have more than one predecessor"
error_message[202] = "Error 202 Any action can have multiple Settings as children, but only one Non Setting successor"
error_message[204] = "Error 204 You cannot connect two icons belonging to the same row"

error_message[205] = "Error 205 Setting has to be connected to the  last immediate action of the parent flow"
error_message[206] = "Error 206 Link produces a Setting not connected to the last immediate action of a parent flow"

## not needed  error_message[207] = "Error 207 Link produces a Setting connected to the same flow in two points"

# Errors moving icons
error_message[301] = "Error 301 Moving a Setting to a row with an already present Setting"
error_message[302] = "Error 302 Moving a Setting, Following or Enhancing to row with an already present Setting"

error_message[305] = "Error 305 The Setting moved has to be connected to the last immediate action of a parent flow"
error_message[306] = "Error 306 Moving the icon disrupts previously established sequence. Delete links before moving"
error_message[307] = "Error 307 Moving a Setting out of enclosing Settings"
error_message[308] = "Error 308 Moving a Non Setting out of enclosing Non Settings"
# error 315 and 305 are related....I thought about making them the same error
error_message[315] = "Error 315 This move produces Setting(s) not connected to the last immediate action of a parent flow"

# Errors erasing
error_message[401] = "Error 401 Before erasing the icon, erase the links to it"

# Errors changing an icon for another
error_message[501] = "Error 501 Forbidden to have another SETTING in a row with an already present SETTING"
error_message[502] = "Error 502 Change produces a combination of icons not allowed"
error_message[511] = "Error 511 Change produces a NON-SETTING with multiple parents"
error_message[512] = "Error 512 Change branches two Non-Setting flows for a previous action"

error_message[601] = "Error 601 before erasing the current row, move or erase the icons on the row"

# Errors in file management
error_message[701] = "Without a name, no PostScrip generated"


action_icon = {}
## Intended use: a dictionary of class action items
## each key points to a class action item and, corresponds to the ID of the image on the canvas

link = {}
## Intended use: hold the links connecting the icons as a dictionary of key:tuples.
## The key of the dictionary is the LineId accordingly to the canvas
## The tuple will have len =2.
## The number at [0] will be the number of the first icon, the one in a previous row
## The number at [1] will be the number of the second icon to be connected

class excel_field :
 # This initialization takes the values referenced by coding_sheet but some values in relation to icons are left empty
    def __init__(self):
        # def __init__(self, k_row=0, k_icon=0, k_parent=0, flow=0, time="", actor="", transcription="", comment=""):

        self.k_row = 0
        self.k_icon = None
        self.k_flow = None
        self.k_parent = None
        self.time = ""
        self.actor = ""
        self.transcription = ""
        self.comment = ""
        self.icon_note = ""

#    Icon comment????????

class action :
    def __init__(self, row=0, flow=None, action=0, delta_x=0, links=(),
                 note="", graph_x=0, flow_color=0, orphan=True):
        self.row = row
        self.flow = flow
        self.action = action
        self.delta_x = delta_x
        self.links = links
        self.note = note
        self.graph_x = graph_x
        self.flow_color = flow_color
        self.orphan = orphan
######## perhaps a flag_flow to know if we are connected or not.

## row        : number of the row as in the coding_sheet,
## flow       : the flow as in boundary games to which this action belongs
## action     : specifies the action: setting, following, etc, accordingly to constants above
## delta_x    : the x position of the icon (basically because user can move icons
## links      : a tuple with the lineIDs that connect to other icons
## note       : notes enter by the user about a particular icon
## graph_x "  : if the icon is a Setting, this will represent the position in X of this flow on the graph_view
## flow_color : color of the flow. if orphan the line is dotted keeping the color
## orphan     : when false, the flow is connected to another flow that starts with a Setting.
##                  when true, the flow does not start with a Setting or that initial Setting is
##                  disconnected from a Setting. Only exception Setting at 0.
## important note: flow and orphan can be seen too similar in many cases. But there are cases in which a flow
## can have a number because there is a parent SETTING to that flow, nevertheless that SETTING is not connected with
## a flow with parent, so it is an orphan


    # sort by flow
    # Used to define the sort key for constructing the tree
    def sort_byflow(self, item):
        return item.flow

    # it returns a link that connects the self invoking with the icon in the parameter.
    def link_connecting(self, icon):
        for lnk in self.links:
            if lnk in action_icon[icon].links:
                return lnk
        return 0

    # it returns a list of links to orphan predecesors
    def unconnected_predecessors(self):
        if self.action == SETTING and self.row == 0:
            return []
        # basically from the self(current node) return those lnk that are unconnected, that is to say
        # the predecesor [lnk][0] is unconnected and is connected to the current, but becasue the predecessor
        # is unconnected this also is unconnected.
        return [lnk for lnk in self.links if action_icon[link[lnk][1]] == self and
                action_icon[link[lnk][0]].flow < 0]

    # returns a lnk number that connects this icon to the one up in the flow specified by parameter flow
    def flowup_tolink(self, flow):
        for lnk in self.links:
            if action_icon[link[lnk][0]] != self and action_icon[link[lnk][0]].flow == flow :
                return lnk
        return None

    def flowdwn_tolink(self, flow):
        for lnk in self.links:
            if action_icon[link[lnk][1]] != self and action_icon[link[lnk][1]].flow == flow :
                return lnk
        return None

    # return the flow number of the parents of the action
    def flow_parents(self):
        predecessors = [lnk for lnk in self.links if action_icon[link[lnk][0]] != self]
        parents = []
        for p in predecessors:
            parents.append(action_icon[link[p][0]].flow)
        return parents

    def flow_descendents(self):
        succesors = [lnk for lnk in self.links if action_icon[link[lnk][1]] != self]
        descendents = []
        for p in succesors:
            descendents.append(action_icon[link[p][1]].flow)
        return descendents

    # return the ID numbers of the icons parents to this action
    def icon_parents(self):
        predecessors = [lnk for lnk in self.links if action_icon[link[lnk][0]] != self]
        parents = []
        for p in predecessors:
            parents.append(link[p][0])
        return parents

    def icon_children(self):
        children_links = [lnk for lnk in self.links if action_icon[link[lnk][1]] != self]
        children = []
        for child in children_links:
            children.append(link[child][1])
        return children
#

    # returns the number of the closest row upwards where this action is connected with another icon
    # if not connection is available, it says that the row is -1
    def closest_rowup(self):
        base_row = -1
        for lnk in self.links:
            if (action_icon[link[lnk][0]].row) < self.row and (action_icon[link[lnk][0]].row > base_row):
                base_row = action_icon[link[lnk][0]].row
            if (action_icon[link[lnk][1]].row) < self.row and (action_icon[link[lnk][1]].row > base_row):
                base_row = action_icon[link[lnk][1]].row
        return base_row

    def closest_rowdown(self):
        base_row = 100000 # I am assuming we will never get 1000000 rows!!! warning
        for lnk in self.links:
            if (action_icon[link[lnk][0]].row) > self.row and (action_icon[link[lnk][0]].row < base_row):
                base_row = action_icon[link[lnk][0]].row
            if (action_icon[link[lnk][1]].row) > self.row and (action_icon[link[lnk][1]].row < base_row):
                base_row = action_icon[link[lnk][1]].row
        if base_row == 100000:
            return -1
        else:
            return base_row

    # returns the ID number of the icon next to this in the same flow. returns 0 if there is none
    def next_inflow(self):
        #it looks through the links of this icon, and creates a list of those links that lead to next icon in the
        # the "same" flow. the criteria for next is not the flow number. It is basically that the icon of destiny
        # is not self, that menas self is a point of origen, so the icon at the other end is next. The only
        # exceptions is if we find a Setting, that means decisively the next icon is not from this flow, so we return 0.
        tmp = [lnk for lnk in self.links if action_icon[link[lnk][1]] != self and
               action_icon[link[lnk][1]].action != SETTING]
        if tmp:
            # the link is a tuple with a pair of actionsID (numbers). The second one is the action that
            # is connected with the icon of the parameter
            return link[tmp[0]][1]
        else:
            return 0

    def next_inflow_old(self):
        #it looks through the links of this icon, and creates a list of those links that lead to next icon in the
        # the same flow. Same flow here is number of flow is the same or the number is unconnected (flow <0).
        tmp = [lnk for lnk in self.links if (action_icon[link[lnk][1]].flow == self.flow or
                                             action_icon[link[lnk][1]].flow < 0) and
               action_icon[link[lnk][1]] != self]
        if tmp:
            # the link is a tuple with a pair of actionsID (numbers). The second one is the action that
            # is connected with the icon of the parameter
            return link[tmp[0]][1]
        else:
            return 0



    # returns the ID number of the icon previous to this in the same flow. returns 0 if there is none
    def previous_inflow(self):
        #it looks through the links of this icon, and creates a list of those links that lead to previous icon in the
        # the same flow.... [lnl][0] refers to the origen of the link, and that link has as flow number the same
        # as the icon in self, and the origen is not self....that imply self is the destiny.
        tmp = [lnk for lnk in self.links if action_icon[link[lnk][0]].flow == self.flow and
               action_icon[link[lnk][0]] != self]
        if tmp:
            # the link is a tuple with a pair of actionsID (numbers). The second one is the action that
            # is connected with the icon of the parameter
            return link[tmp[0]][0]
        else:
            return 0

    # list of ID icons in the flow previous to the current one (current one not included)
    # the list is ordered. in [0] we find the first iconID of the flow
    def previous_list(self):
        list_p = []
        previous = self.previous_inflow()
        while previous:
            list_p.insert(0, previous)
            previous = action_icon[previous].previous_inflow()
        return list_p

    # list of ID icons in the flow after the current one (current one not included)
    # the list is ordered in [-1] we find the last IconID of the flow
    def upcoming_list(self):
        list_p = []
        n = self.next_inflow()
        while n:
            list_p.append(n)
            n = action_icon[n].next_inflow()
        return list_p

    # returns a list with all the icons in the flow...dirty trick...the current one is pass as argument
    # the list is ordered from the first icon of the flow [0] to the last one in [-1]
    def items_flow(self, current):
        p_flow = []
        p_flow = self.previous_list()
        p_flow.append(current)
        for icon in self.upcoming_list():
            p_flow.append(icon)
        return p_flow

    # returns the iconID of the first icon of the flow
    def first_inflow(self, current):
        safe = current
        previous = self.previous_inflow()
        while previous:
            safe = previous
            previous = self.previous_inflow()
        return safe

    def enclosing_settings(self):
        d_past = self.row + 1
        d_later = len(coding_sheet) + 1
        past = None
        later = None
        for icon in action_icon:
            if action_icon[icon].action == SETTING and action_icon[icon].row < self.row:
                d = self.row - action_icon[icon].row
                if d < d_past:
                    past = icon
                    d_past = d
            if action_icon[icon].action == SETTING and action_icon[icon].row > self.row:
                d = abs(self.row - action_icon[icon].row)
                if d < d_later:
                    later = icon
                    d_later = d
        return past, later

# here the routine gives the ID of the icons surronding the icon in focus. If there are no icon behind or forward
    # it will return None in the variables past and later. The rutine works by calculating the distance of Settings to
    # this Setting. The ones with the smaller distance are the ones enclosing the Setting in focus. Note that for
    # calculating the distance of the later icons I sued ABS to avoid the problem of big distances being negative
    def enclosing_nonsettings(self):
        d_past = self.row + 1
        d_later = len(coding_sheet) + 1
        past = 0
        later = 0
        for icon in action_icon:
            if action_icon[icon].action != SETTING and action_icon[icon].row < self.row and \
                not action_icon[icon].previous_list():
                d = self.row - action_icon[icon].row
                if d < d_past:
                    past = icon
                    d_past = d
            if action_icon[icon].action != SETTING and action_icon[icon].row > self.row and \
                not action_icon[icon].previous_list():
                d = abs(self.row - action_icon[icon].row)
                if d < d_later:
                    later = icon
                    d_later = d
        return past, later



    # takes the current (IconID) flow number, and disseminate that number plus color and orphan state to
    # the connected icons to this flow (notice that sometimes the number of the flow is changing in some icons
    # so we rely in the links connecting the icons to figure out that they are on the same flow....
    # also it returns the links connecting the icons implied, including the terminations of those connections where
    # new flows start
    def disseminate_toicons(self, current, new_color, orphan_state):
        f_number = action_icon[current].flow
        icons_tochange = self.items_flow(current)
        lnk_toreturn = []
        for item in icons_tochange:  # find the flows of these icons to be colored
            action_icon[item].flow = f_number
            action_icon[item].flow_color = new_color
            action_icon[item].orphan = orphan_state
            # gets the lnks in which the node of origen is the one specified by the item....if not is not part of
            # the flow because the items of the flow were selected by items_flow....need to check!!
            lnks = [lnk for lnk in action_icon[item].links if action_icon[link[lnk][0]].flow == f_number]
            for lk in lnks:
                lnk_toreturn.append(lk)
        return lnk_toreturn
#perhaps this is a better condition? basically the link points forward...
#   lnks = [lnk for lnk in action_icon[item].links if link[lnk][0] == item

coding_sheet = [] # the structure pointing to the widgets, the "spreadsheet" [rows][columns]
sheet_description = []  # describes the properties of each column
sheet_description.append({"field_name": "Move",
                          "type_of_field": "no_editable",
                          "size": 0.05,
                          "enter_behaviour": "none"})
sheet_description.append({"field_name": "Time",
                          "type_of_field": "editable",
                          "size": 0.06,
                          "enter_behaviour": "new_row"})
sheet_description.append({"field_name": "Actor",
                           "type_of_field": "editable",
                          "size": 0.09,
                          "enter_behaviour": "new_row"})
sheet_description.append({"field_name": "Actions",
                          "type_of_field": "graph",
                          "size": 0.3,
                          "enter_behaviour": "none"})
sheet_description.append({"field_name": "Communication",
                          "type_of_field": "editable",
                          "size": 0.25,
                          "enter_behaviour": "break_field"})
sheet_description.append({"field_name": "Notes",
                          "type_of_field": "editable",
                          "size": 0.25,
                          "enter_behaviour": "in_field"})


current_row = 0  # on the coding_sheet
current_column = 0  # on the coding_sheet

number_of_columns = len(sheet_description)
