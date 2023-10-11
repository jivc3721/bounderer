
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
error_message[101] = "Error 101 Only one Setting per row is allowed"
error_message[102] = "Error 102 Following and Enhancing are not compatible with Setting in the same row"

error_message[201] = "Error 201 A Non Setting cannot have more than one predecessor"
error_message[202] = "Error 202 Any action can have multiple Settings as childs, but only one Non Setting successor"
error_message[204] = "Error 204 You cannot connect two icons belonging to the same row"

error_message[205] = "Error 205 Setting has to be connected to the  last immediate action of the parent flow"
error_message[206] = "Error 206 Link produces a Setting not connected to the last immediate action of a parent flow"

## not needed  error_message[207] = "Error 207 Link produces a Setting connected to the same flow in two points"

error_message[301] = "Error 301 Moving a Setting to a row with an already present Setting"
error_message[302] = "Error 302 Moving a Setting, Following or Enhancing to row with an already present Setting"

error_message[305] = "Error 305 Move produces an Setting not connected to the last immediate action of a parent flow"
error_message[306] = "Error 306 Moving the icon disrupts previously established sequence. Delete links before moving"
error_message[307] = "Error 307 Moving a Setting out of enclosing Settings"
error_message[308] = "Error 308 Moving a Non Setting out of enclosing Non Settings"

error_message[401] = "Error 401 Before erasing the icon, erase the links to it"

error_message[501] = "Error 501 Forbidden to have another SETTING in a row with an already present SETTING"
error_message[502] = "Error 502 Change produces a combination of icons not allowed"
error_message[511] = "Error 511 Change produces a NON-SETTING with multiple parents"

error_message[601] = "Error 601 before erasing the current row, move or erase the icons on the row"


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
## flow_color : in case of non-orphan flows, this will be the color
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
        # the same flow. Same flow here is number of flow is the same or the number is unconnected (flow <0).
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
        #it looks through the links of this icon, and creates a list of those links that lead to next icon in the
        # the same flow
        tmp = [lnk for lnk in self.links if action_icon[link[lnk][0]].flow == self.flow and
               action_icon[link[lnk][0]] != self]
        if tmp:
            # the link is a tuple with a pair of actionsID (numbers). The second one is the action that
            # is connected with the icon of the parameter
            return link[tmp[0]][0]
        else:
            return 0

    # list of ID icons in the flow previous to the current one
    def previous_list(self):
        previous = self.previous_inflow()
        list_p = []
        while previous:
            list_p.insert(0, previous)
            previous = action_icon[previous].previous_inflow()
        return list_p

    # list of ID icons in the flow after the current one
    def upcoming_list(self):
        n = self.next_inflow()
        list_p = []
        while n:
            list_p.append(n)
            n = action_icon[n].next_inflow()
        return list_p

    # returns a list with all the actions in the flow
    def items_flow(self, current):
        p_flow = []
        p_flow = self.previous_list()
        p_flow.append(current)
        for icon in self.upcoming_list():
            p_flow.append(icon)
        return p_flow

    # returns the iconID of the first icon of the flow
    def first_inflow(self):
        previous = self.previous_inflow()
        safe = previous
        while previous:
            safe = previous
            previous = self.previous_inflow()

        return safe

    def enclosing_settings(self):
        d_past = self.row + 1
        d_later = len(coding_sheet) + 1
        past = 0
        later = 0
        for icon in action_icon:
            if action_icon[icon].action == SETTING and action_icon[icon].row < self.row:
                d = self.row - action_icon[icon].row
                if d < d_past:
                    past = icon
                    d_past = d
            if action_icon[icon].action == SETTING and action_icon[icon].row > self.row:
                d = self.row - action_icon[icon].row
                if d < d_later:
                    later = icon
                    d_later = d
        return past, later

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
                d = self.row - action_icon[icon].row
                if d < d_later:
                    later = icon
                    d_later = d
        return past, later



    # takes the current (IconID) flow number, and disseminate the number with a color an an orphan state
    # also it reurns the links connecting the icons implied, also with the terminations of those connection where
    # new flows start
    def disseminate_toicons(self, current, new_color, orphan_state):
        f_number = action_icon[current].flow
        icons_tochange = self.items_flow(current)
        lnk_toreturn = []
        for item in icons_tochange:  # find the flows of these icons to be colored
            action_icon[item].flow = f_number
            action_icon[item].flow_color = new_color
            action_icon[item].orphan = orphan_state
            lnks = [lnk for lnk in action_icon[item].links if action_icon[link[lnk][0]].flow == f_number]
            for lk in lnks:
                lnk_toreturn.append(lk)
        return lnk_toreturn



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
