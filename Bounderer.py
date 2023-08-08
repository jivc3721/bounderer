

# with import we use the name of the module or alias to invoke contents
# with from... we can bypass the name of the module when invoking
import tkinter as tk
import tkinter.font as tkf
from tkinter import ttk
from DataStructure import *
from tkinter import filedialog
from tkinter import messagebox

import os

from docx import Document
import xlsxwriter

#for printing
# import tempfile
#import win32api
#import win32print

#prueba

# colors of the interface
REC_WRITING = "#0B0"  # a light green
REC_CODING = "#BBD"  # lither green "#ADA"
REC_HOVERING = "#BBB"  # a soft gray
REC_INACTIVE = "white"

TXT_WRITING = "black"
TXT_HOVERING = "blue"
TXT_INACTIVE = "black"

LINE_COLOR = "#DDD"     # divides rows.   softer gray (than the rectangle)
# LINK_COLOR = "#D77"     # a red similar to the first illustrations of boundary games
# ORPHAN_LINKCOLOR = "#999" # a gray a little darker than the separation lines
ACTIVE_LINKCOLOR = "#5E7FD9"  # the idea is a blue similar to menus. You are choosing to do something with the link

LK_DEFAULTCOLOR =  0       # a red similar to the first illustrations of boundary games
ORPHAN_LINKCOLOR = 8  # a gray a little darker than the separation lines

LEAF_COLOR = "#5000a0"  # for the tree/structure view a kind of dark purple


GAP_FOR_ICON = 3  # the idea is that the icon takes 2 pixels more before and after the rectangle
GAP_FOR_LINE = 5  # here the line is placed at middle way between two cells and the gap between them is 10, so the half

LINK_COLOR_V = []
LINK_COLOR_V.append("#aa0000")  # Red
LINK_COLOR_V.append("#fa7818")  # Orange
LINK_COLOR_V.append("#0000b3")  # Blue
LINK_COLOR_V.append("#12a0fe")  # Cyan
LINK_COLOR_V.append("#7df600")  # LemonGreen
LINK_COLOR_V.append("#129200")  # GrassGreen
LINK_COLOR_V.append("#000000")  # Black
LINK_COLOR_V.append("#959595")  # Gray
LINK_COLOR_V.append("#a600f6")  # Purple

# LINK_COLOR_V[LINK_COLOR]
# LINK_COLOR_V[ORPHAN_LINKCOLOR]

#Constants for invisibility. Color and manage swith ON-OFF UP and DOWN
INVISIBLE_MARKCOLOR = "#FF2424"
ON   = 1
OFF  = 0
UP   = 1
DOWN = 0


############### TAGS #####################################
## Different visual element on a canvas have a tag, that speed up recognition
## of elements or facilitates selecting some of then for
## actualizing the visualization
##
##  "highlight" : to highlight the tk.rectangles behind text
##  "bg"        : shows that is a BackGround rectangle behind text
##
##  "icon_frame" : It is a rectangle behind the icons
##  "icon"       : an tk.PhotoImage of an icon
##  "link"       : line linking two icons
##  "info_window": used to mark the text and the rectangle giving information about an icon.
##                 it facilitates to erase all the elements of the window later.
##
##  "field"      : to identify text elements
##
##  "move"       : to mark elements for moving
##  "exclude"    : to exclude some element from the "move"
##
##  "erase"      : to erase all the items (e.g when loading a new file)

class CodingCanvas(tk.Canvas):

    def __init__(self, root, **options):
        global current_row, current_column
        tk.Canvas.__init__(self, root, options)

        # ICONS FOR CODING
        self.ICONS = []
        self.ICONS.append(tk.PhotoImage(file="setting.ppm"))
        self.ICONS.append(tk.PhotoImage(file="following.ppm"))
        self.ICONS.append(tk.PhotoImage(file="wandering.ppm"))
        self.ICONS.append(tk.PhotoImage(file="probing.ppm"))
        self.ICONS.append(tk.PhotoImage(file="challenging.ppm"))
        self.ICONS.append(tk.PhotoImage(file="enhancing.ppm"))
        # ICONS FOR LINKING
        self.ICONS.append(tk.PhotoImage(file="settingNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="followingNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="wanderingNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="probingNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="challengingNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="enhancingNEG.ppm"))
        # ICONS FOR CONTEXTUAL MENU
        self.ICONS.append(tk.PhotoImage(file="settingSmall.ppm"))
        self.ICONS.append(tk.PhotoImage(file="followingSmall.ppm"))
        self.ICONS.append(tk.PhotoImage(file="wanderingSmall.ppm"))
        self.ICONS.append(tk.PhotoImage(file="probingSmall.ppm"))
        self.ICONS.append(tk.PhotoImage(file="challengingSmall.ppm"))
        self.ICONS.append(tk.PhotoImage(file="enhancingSmall.ppm"))
        # ICONS FOR CODING - WARNINGS
        self.ICONS.append(tk.PhotoImage(file="settingSmallNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="followingSmallNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="wanderingSmallNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="probingSmallNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="challengingSmallNEG.ppm"))
        self.ICONS.append(tk.PhotoImage(file="enhancingSmallNEG.ppm"))

        # ICONS FOR SELECTING THE COLOR OF A FLOW
        self.FLOW_COLORS = []
        self.FLOW_COLORS.append(tk.PhotoImage(file="Red.ppm"))  # aa0000
        self.FLOW_COLORS.append(tk.PhotoImage(file="Orange.ppm"))  # fa7818
        self.FLOW_COLORS.append(tk.PhotoImage(file="Blue.ppm"))  # 0000b3
        self.FLOW_COLORS.append(tk.PhotoImage(file="Cyan.ppm"))  # 12a0fe
        self.FLOW_COLORS.append(tk.PhotoImage(file="LemonGreen.ppm"))  # 7df600
        self.FLOW_COLORS.append(tk.PhotoImage(file="GrassGreen.ppm"))  # 129200
        self.FLOW_COLORS.append(tk.PhotoImage(file="Black.ppm"))  # 000000
        self.FLOW_COLORS.append(tk.PhotoImage(file="Gray.ppm"))  # 774a4a




        # Contextual menu for boundary actions
        self.boundarymenu = tk.Menu(self, tearoff=0)
        self.boundarymenu.add_command(label=" setting", image=self.ICONS[12],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(SETTING))
        self.boundarymenu.add_command(label=" following", image=self.ICONS[13],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(FOLLOWING))
        self.boundarymenu.add_command(label=" wandering", image=self.ICONS[14],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(WANDERING))
        self.boundarymenu.add_command(label=" probing", image=self.ICONS[15],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(PROBING))
        self.boundarymenu.add_command(label=" challenging", image=self.ICONS[16],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(CHALLENGING))
        self.boundarymenu.add_command(label=" enhancing", image=self.ICONS[17],
                                      compound=tk.LEFT, command=lambda: self.draw_icon(ENHANCING))

        # Contextual menu for changing action
        self.changingmenu = tk.Menu(self, tearoff=0, bg="black", fg="white")
        self.changingmenu.add_command(label="change to ", image=self.ICONS[18],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(SETTING))
        self.changingmenu.add_command(label="change to ", image=self.ICONS[19],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(FOLLOWING))
        self.changingmenu.add_command(label="change to ", image=self.ICONS[20],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(WANDERING))
        self.changingmenu.add_command(label="change to ", image=self.ICONS[21],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(PROBING))
        self.changingmenu.add_command(label="change to ", image=self.ICONS[22],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(CHALLENGING))
        self.changingmenu.add_command(label="change to ", image=self.ICONS[23],
                                      compound=tk.RIGHT, command=lambda: self.change_icon(ENHANCING))


        # Contextual menu for links
        self.linkmenu = tk.Menu(self, tearoff=0)
        self.linkmenu.add_command(label="- Erase link -", command=self.delete_link)

        # Contextual menu for editing boundary actions
        self.edit_actionMenu = tk.Menu(self, tearoff=0)
        #     Checkboxes for flows in menu
        self.predeccesorMenu = tk.Menu(self.edit_actionMenu, tearoff=0)
        self.succesorMenu = tk.Menu(self.edit_actionMenu, tearoff=0)
        self.edit_actionMenu.add_cascade(label=" Predeccesors", menu=self.predeccesorMenu)
        self.edit_actionMenu.add_cascade(label=" Sucessors", menu=self.succesorMenu)
        self.edit_actionMenu.add_command(label=" Edit ", command=self.edit_action)
        self.edit_actionMenu.add_separator()
        self.edit_actionMenu.add_command(label=" Erase ", command=self.delete_icon)


        # calculating screen positions
        x1 = 0
        screen_x = root.winfo_screenwidth()
        for field in sheet_description:
            field["x1"] = x1
            field["width"] = int(screen_x*field["size"])-CELL_GAP_X
            x1 += int(screen_x*field["size"])

        # variables to trap event x and y for drawing icons
        self.click_x = 0
        self.click_y = 0
        self.icon_row = 0

        # variables for moving icons
        self.icon_dx = 0
        self.icon_dy = 0
        self.click_on_icon = 0

        # variables for information window for icons
        self.info_window_on = False

        # variables for window for icon data entry
        self.canvas_window = 0

        # variables for linking icons
        self.first_icon = 0
        self.ready_forlink = False

        # variables to idenfy which itemID (link or icon) is edited(erased?)
        self.link_to_edit = 0
        self.icon_to_edit = 0

        # dirty trick to put an item as reference of the first item item 1
        # it will never be touched by any operation so is an unmovable reference point
        # to put all the "icon_frame" below this and the icon will be always on top of this
        self.baseline = self.create_line(0, -10, 10, -10)

        # Drawing first row
        self.new_row(0)
        current_column = TIME_COLUMN
        self.focus_set()  # move focus to canvas
        self.focus(coding_sheet[current_row][current_column])  # set focus to text item
        self.index(coding_sheet[current_row][current_column], tk.END)
        self.highlight(coding_sheet[current_row][current_column])

        # events bindings
        self.tag_bind("field", "<Button-1>", self.mvinsertion_cursor)

        self.tag_bind("icon", "<Button-1>", self.info_window_i)
        self.tag_bind("link", "<Button-1>", self.info_window_lnk)

        self.tag_bind("icon", "<B1-ButtonRelease>", self.close_info_window)
        self.tag_bind("link", "<B1-ButtonRelease>", self.close_info_window)

        self.bind("<Double-Button-1>", self.double_click)

        self.tag_bind("icon_frame", "<Button-3>", self.menu_boundaryaction)

        self.tag_bind("icon", "<Shift-Button-3>", self.menu_change)
        self.tag_bind("icon", "<Button-3>", self.menu_icon)
        self.tag_bind("link", "<Button-3>", self.menu_link)

        self.bind("<Key>", self.handle_key)
        self.bind("<Shift-KeyPress-Tab>", self.shift_tab)

        self.tag_bind("icon", "<Shift-Button-1>", self.icon_to_move)
        self.tag_bind("icon", "<Shift-B1-Motion>", self.move_icon)
        self.tag_bind("icon", "<Shift-B1-ButtonRelease>", self.icon_restplace)

    def has_focus(self):
        return self.focus()

    # finds the maximun height (Y) for a cell in a row (considering the text fields)
    def maxy_row(self, row):
        if row < 0 or row >= len(coding_sheet):
            return 0
        else:
            y = 0
            for i in range(number_of_columns):
                if i != ACTIONS_COLUMN:
                    y = max([y, self.fit_box(coding_sheet[row][i])[3]])
        return y

    # finds the maximun height (Y) for the boxes below the text
    def maxy_row_box(self, row):
        if row < 0 or row >= len(coding_sheet):
            return 0
        else:
            y = 0
            for i in range(number_of_columns):
                if i != ACTIONS_COLUMN:
                    below = self.find_below(coding_sheet[row][i])
                    if below:
                        y = max([y, self.fit_box(below)[3]])
        return y

    def fit_box_text(self, row):
        if 0 <= row <= len(coding_sheet):
            for i in range(number_of_columns):
                if i != ACTIONS_COLUMN:
                    box = self.find_below(coding_sheet[row][i])
                    x1, y1, x2, y2 = self.fit_box(coding_sheet[row][i])
                    c = sheet_description[i]
                    self.coords(box, c["x1"], y1, c["x1"] + c["width"], y2)

    # takes an item tag number and loos for the equivalent row and column on the coding_sheet
# the idea is to take a mouse event and translate the coordinates to ones on the sheet

    def item_to_coding_grid(self, item):  # it works with item id no tag
        x1, y1 = self.coords(item)
        ref = self.find_closest(sheet_description[0]["x1"], y1)
        row = int(self.itemcget(ref, "text"))
        column = 0
        f = self.find_withtag(item)[0]
        while coding_sheet[row][column] != f:
            column += 1
        return column, row

    def move_to_visibility(self, item):
        # returns 0 if you are visible. 1 if your are after the end of the window
        #    and -1 if you are before the top part of the window
        x1, y1, x2, y2 = self.bbox(item)
        window_height = self.config("height")[4]
        currentIndx = self.index(item, tk.INSERT)
        t_y = y1
        while t_y < y2:
            t_y += 1
            tIndex = self.index(item, "@%d,%d" % (x1, t_y))
        if currentIndx < tIndex:
            t_y -= 10
        if t_y <= self.canvasy(0):
            return -1
        elif t_y > self.canvasy(int(window_height)):
            return 1
        else:
            return 0

    def action_tkcolor(self, c):
        return LINK_COLOR_V[c]

##########################   Actualising Adapting Visualization
####################################################################

    def redraw_links(self):
        for ln in link:
            icon1 = link[ln][0]
            icon2 = link[ln][1]
            x1, y1 = self.icon_center(icon1)
            x2, y2 = self.icon_center(icon2)
            lx1, ly1, sx, sy, lx2, ly2 = self.coords(ln)
            if x1 != lx1 or y1 != ly1 or x2 != lx2 or y2 != ly2:
                sx = x2
                sy = ((max(y1, y2) - min(y1, y2))/2) + min(y1, y2)
                self.coords(ln, x1, y1, sx, sy, x2, y2)
    
    def fix_graph(self, row):
        maxy = 0
        for i in range(number_of_columns):
            if i != ACTIONS_COLUMN:
                maxy = max([maxy, self.fit_box(coding_sheet[row][i])[3]])
        x1, y1, x2, y2 = self.coords(coding_sheet[row][ACTIONS_COLUMN])
        old_middle_y = int((y2-y1-25)/2)

        self.coords(coding_sheet[row][ACTIONS_COLUMN], x1, y1, x2, maxy)
        new_middle_y = int((maxy-y1-25)/2)  # for centring the icon on y axis
        self.addtag_overlapping("move", x1+1, y1+1, x2-1, maxy-1)  # a circumscribed rectangle
        self.dtag(coding_sheet[row][ACTIONS_COLUMN], "move")
        self.move("move", 0, new_middle_y - old_middle_y)
        self.dtag("move", "move")
        self.redraw_links()

    def fit_box(self, item):
        x1, y1, x2, y2 = self.bbox(item)
        if self.type(item) == "text":
            y1 -= 1
        return x1+1, y1+1, x2-1, y2-1

    def print_state(self, item):
        global current_row, current_column
        print("currentRow-Colummn", current_row, current_column)
        print("boxall:", self.bbox('all'))
        print("box item, type", self.bbox(item), self.type(item))
        parameters = self.config()
        print("scrollregion", parameters["scrollregion"])
        print("------------------------------------------------")

    def highlight(self, item):  # it seems that the bbox of item and rectangle differ in 1 pixel
        global current_row, current_column

        old_rectangle = self.find_withtag("highlight")
        rectangle = self.find_below(item)
        if not old_rectangle:  # no previous selection then put a selection?
            self.addtag_withtag("highlight", rectangle)  # put highlight tag to rectangle below
            self.itemconfig(rectangle, fill=REC_WRITING, activefill=REC_WRITING)  # config. color rectangle on
            self.itemconfig(item, fill=TXT_WRITING)
        else:  # there is a previous highlight
            if old_rectangle != rectangle:
                self.itemconfig(old_rectangle, fill=REC_INACTIVE, activefill=REC_HOVERING)
                txt = self.find_above(old_rectangle)
                self.itemconfig(txt, fill=TXT_INACTIVE)
                self.dtag(old_rectangle, "highlight")
                self.addtag_below("highlight", item)
                self.itemconfig(item, fill=TXT_WRITING)
                self.itemconfig(rectangle, fill=REC_WRITING, activefill=REC_WRITING)

        max_text = self.maxy_row(current_row)
        max_box = self.maxy_row_box(current_row)
        if max_text != max_box:
            limit_y2 = max_box+6 if current_row == len(coding_sheet)-1 \
                else self.maxy_row(len(coding_sheet)-1)+LINE_SPACE
            self.addtag_overlapping("move", -1, max_box+4, 1367, limit_y2)
            self.addtag_overlapping("exclude", -1, self.coords(item)[1], 1367, max_box)
            self.dtag("exclude", "move")
            diff = max_text - max_box
            self.move("move", 0, diff)
            self.dtag("move", "move")
            self.dtag("exclude", "exclude")
            # Old division
            self.fit_box_text(current_row)
            self.fix_graph(current_row)
            self.update_idletasks()
            bx1, by1, bx2, by2 = self.bbox('all')
            self.print_state(item)
            scrollregion = self.cget("scrollregion")
            sx1, sy1, sx2, sy2 = map(float, scrollregion.split())
            if sy2 != by2 :
                self.configure(scrollregion=(0, 0, 1366, by2))
                self.print_state(item)
                self.yview_scroll(0, tk.UNITS)

##___________________________End Actualising Adapting Visualization
##_________________________________________________________________

############################## Single and Double Click Management
####################################################################
            
    def icon_center(self, icon):
        x1, y1, x2, y2 = self.bbox(icon)
        return x1+int((x2-x1)/2), y1+int((y2-y1)/2)

    # I think that for actualize_flow I was assuming that this function here was copying information about the
    # flow from the icon1 to the icon2....SETTING in icon2 is special becasue in that case info of the flow
    # do not down.
    def create_link(self, icon1, icon2):
        global link, action_icon
        lx1, ly1 = self.icon_center(icon1)
        lx2, ly2 = self.icon_center(icon2)

        sx = lx2
        sy = ((max(ly1, ly2) - min(ly1, ly2))/2) + min(ly1, ly2)
        lnkcolor = action_icon[icon1].flow_color
        lkdash = UNCONNECTED_DASH if action_icon[icon1].orphan else CONNECTED_DASH

        lnk = self.create_line(lx1, ly1, sx, sy, lx2, ly2, smooth=True, width=3,
                               fill=self.action_tkcolor(lnkcolor), activewidth=5,
                               activefill=ACTIVE_LINKCOLOR, dash=lkdash, tag="link", state=tk.NORMAL)
        self.tag_raise(icon1, lnk)
        self.tag_raise(icon2, lnk)
        link[lnk] = (icon1, icon2)

        action_icon[icon1].links = action_icon[icon1].links + (lnk,)
        action_icon[icon2].links = action_icon[icon2].links + (lnk,)

    def error_link(self, icon1, icon2):  # look dictionary of errors on DataStructure.py
        # Error 201 only one predecessor for NON-Settings
        if action_icon[icon2].action != SETTING:
            if [lnk for lnk in action_icon[icon2].links if link[lnk][1] == icon2]:
                return 201

        # Error 202 "A Boundary-Action can have multiple child Settings, but only one Non Setting successor"
        if action_icon[icon2].action != SETTING:
            for lnk in action_icon[icon1].links:
                if action_icon[link[lnk][0]] == action_icon[icon1] and action_icon[link[lnk][1]].action != SETTING:
                    return 202

        # Error 204 no horizontal connections
        if action_icon[icon1].row == action_icon[icon2].row:
            return 204

        # Error 205 "A Setting only can be connected to the last previous Action of the
        #            parent flow" (((???? perhasp this is any action instead of only setting?)
        if action_icon[icon2].action == SETTING:
            # next_icon = self.next_inflow(icon1)
            next_icon = action_icon[icon1].next_inflow()
            if next_icon:
                # if the row of the next icon is less than the setting at icon2
                # you should not connect to icon1 but to a later one
                if action_icon[next_icon].row < action_icon[icon2].row:
                    return 205

        # Error 206 Link produces a Setting not connected to the last immediate action of the parent flow
        if action_icon[icon2].action != SETTING:
            row2 = action_icon[icon2].row
            l_previous = action_icon[icon1].previous_list()
            l_previous.insert(0, icon1)
            for icon in l_previous:
                for lnk in action_icon[icon].links:
                    if action_icon[link[lnk][1]].action == SETTING and action_icon[link[lnk][1]].row > row2:
                        return 206

        # Error 207 The connection produces a Setting connected to the same parent Setting in two points
        # flow = action_icon[icon1].flow
        # next_setting2 = icon2
        # if flow != UNCONNECTED:
        #     if action_icon[icon2].action != SETTING:
        #         next_setting2 = self.find_nextsetting(icon2)
        #     if next_setting2 != 0:
        #         tmp = [lnk for lnk in action_icon[next_setting2].links if action_icon[link[lnk][0]].flow == flow]
        #         if tmp:
        #             return 207
        # return 0

# single click on a field of text to move insertion cursor
    def mvinsertion_cursor(self, event):
        # translate to the canvas coordinate system
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        # move insertion cursor
        item = self.has_focus()
        if not item:
            return  # or do something else
        self.icursor(item, "@%d,%d" % (x, y))
        self.select_clear()

    def info_window_lnk(self, event):
        # translate to the canvas coordinate system
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        lnk = self.find_withtag(tk.CURRENT)[0]
        icon1 = link[lnk][0]
        icon2 = link[lnk][1]
        label = "flow  : " + str(action_icon[icon1].flow) + "\n" + \
                ICON_NAME[action_icon[icon1].action] + " : " + action_icon[icon1].note + "\n" + \
                "row   : " + str(action_icon[icon1].row) + "\n" + \
                "»»»»»»»»»»»»»»»»" + "\n" + \
                "flow  : " + str(action_icon[icon2].flow) + "\n" + \
                ICON_NAME[action_icon[icon2].action] + " :  " + action_icon[icon2].note + "\n" + \
                "row   : " + str(action_icon[icon2].row)

        text = self.create_text(x, y, justify=tk.LEFT, width=250, text=label, tags="info_window", anchor=tk.N)
        x1, y1, x2, y2 = self.bbox(text)
        rect = self.create_rectangle(x1-3, y1-3, x2+3, y2+3, fill="Cyan", tags="info_window", width=2)
        self.tag_lower(rect, text)
        # create multiple elements for the window with a tag "info_window" so when erased just erase all
        # with the tag
        # perhaps create first the text and then make rectangle as big as text(just as when loading file)
        self.info_window_on = True

#single click on an icon to display info window
    def info_window_i(self, event):
        # translate to the canvas coordinate system
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        icon = self.find_withtag(tk.CURRENT)[0]
        # location = self.bbox(icon)
        label = ICON_NAME[action_icon[icon].action] + "»»»»»»»»" + "\n" + \
                "flow  : " + str(action_icon[icon].flow) + "\n" + \
                "note  : " + (action_icon[icon].note) + "\n" + \
                "\n"
                # "row   : " + str(action_icon[icon].row) + \
                # "IconID: " + str(icon)
        # "Orphan: " + str(action_icon[icon].orphan) + "\n" +   \
        #         "tag   : " + self.gettags(icon)[0] + "\n" + \
        #         "location: " + str(location[0]) + "," + str(location[1]) + "," + \
        #         str(location[2]) + "," + str(location[3]) + "\n" + \

        text = self.create_text(x, y, justify=tk.LEFT, width=250, text=label, tags="info_window", anchor=tk.N)
        x1, y1, x2, y2 = self.bbox(text)
        rect = self.info_window_ID = self.create_rectangle(x1-3, y1-3, x2+3, y2+3, fill="yellow", tags="info_window", width=2)
        self.tag_lower(rect, text)
        # create multiple elements for the window with a tag "info_window" so when erased just erase all
        # with the tag
        # perhaps create first the text and then make rectangle as big as text(just as when loading file)
        self.info_window_on = True

# click release to close info window
    def close_info_window(self, event):
        if self.info_window_on:
            self.delete("info_window")
            self.info_window_on = False

    def double_click(self, event):  # set_focus
        global current_row, current_column
        tags = self.gettags(tk.CURRENT)
        if self.ready_forlink:
            if self.type(tk.CURRENT) == "image":
                second_icon = self.find_withtag(tk.CURRENT)[0]
                icon1, icon2 = self.first_icon, second_icon
                if action_icon[icon1].row > action_icon[icon2].row:
                    icon1, icon2 = icon2, icon1
                if not (error_number := self.error_link(icon1, icon2)):
                    old_flow = action_icon[icon2].flow
                    self.create_link(icon1, icon2)
                    self.actualize_flow(icon1)
                    if action_icon[icon2].action != SETTING:
                        # now we have a hole in the numbering....so fix
                        for icon in action_icon.keys():
                            action_icon[icon].flow = action_icon[icon].flow + 1 \
                                if action_icon[icon].flow < old_flow and action_icon[icon].flow < 0  \
                                else action_icon[icon].flow
                    self.itemconfigure(self.first_icon, state=tk.NORMAL)
                    self.config(cursor="arrow")
                    self.ready_forlink = False
                else:
                    self.error_message(error_number)  # perhaps a warning message
            else:
                self.itemconfigure(self.first_icon, state=tk.NORMAL)
                self.config(cursor="arrow")
                self.ready_forlink = False
            return
        if "bg" in tags:  # click on the rectangle
            self.focus_set()
            fx = self.find_above(tk.CURRENT)
            self.focus(fx)
            self.highlight(fx)
            current_column, current_row = self.item_to_coding_grid(fx)
        elif self.type(tk.CURRENT) == "text":  # click on text
            fx = self.find_withtag(tk.CURRENT)
            self.focus_set()  # move focus to canvas
            self.focus(fx[0])  # set focus to text item
            self.highlight(fx[0])
            current_column, current_row = self.item_to_coding_grid(fx[0])
        elif "icon" in tags:
            self.first_icon = self.find_withtag(tk.CURRENT)[0]
            self.itemconfigure(self.first_icon, state=tk.DISABLED)
            self.config(cursor="target")
            self.ready_forlink = True

##________________________________ Single and Double Click Management
##___________________________________________________________________

########################  Menus and operations for drawing boundary icons       
############################################################################

    def delete_icon(self):
        if not action_icon[self.icon_to_edit].links:
            if action_icon[self.icon_to_edit].action == SETTING:
                for icon in action_icon:
                    action_icon[icon].flow = action_icon[icon].flow \
                        if action_icon[icon].flow <= action_icon[self.icon_to_edit].flow or \
                           action_icon[icon].flow == UNCONNECTED else action_icon[icon].flow-1
            else:
                for icon in action_icon:
                    action_icon[icon].flow = action_icon[icon].flow \
                        if action_icon[icon].flow > action_icon[self.icon_to_edit].flow \
                        else action_icon[icon].flow+1
            del action_icon[self.icon_to_edit]
            self.delete(self.icon_to_edit)
        else:
            self.error_message(401) # do not erase if this have links

    def put_mark_invisibility(self, icon, state=ON, up_down=UP):
        x1, y1, x2, y2 = self.bbox(icon)

        # to find if there are marks, you find objects in the space of the icon that have special tags
        objects = self.find_enclosed(x1-1, y1-1, x2+1, y2+1)
        mark_up = [obj for obj in objects if "invisible_up" in self.itemcget(obj, "tag")]
        mark_dwn = [obj for obj in objects if "invisible_down" in self.itemcget(obj, "tag")]

        if state == ON:
            if up_down == UP:
                if not mark_up:
                    self.create_oval(x2 - 10, y1, x2, y1 + 10, fill=INVISIBLE_MARKCOLOR, tag="invisible_up")
            elif not mark_dwn:
                self.create_oval(x1, y2 - 10, x1 + 10, y2, fill=INVISIBLE_MARKCOLOR, tag="invisible_down")
        else:
            if up_down == UP and mark_up:
                self.delete(mark_up[0])
            elif up_down == DOWN and mark_dwn:
                self.delete(mark_dwn[0])

    # Odd plce for this function. It is used when moving an icon. The idea is to turn off the
    # invisibility marks wothout questions and the once the icon is in the new place if ask if there are
    # invisible links in order to put the mark again
    def invisible_links(self, icon, up_down=UP):
        link_list = []
        link_list.clear()
        if up_down == UP:
            link_list = [lnk for lnk in action_icon[icon].links if link[lnk][0] != icon]
        else:
            link_list = [lnk for lnk in action_icon[icon].links if link[lnk][1] != icon]
        if not link_list:
            return False
        for lnk in link_list:
            if self.itemcget(lnk, "state") == tk.HIDDEN:
                return True
        return False

    def toggle_lnkupvisibility(self, flow):
        lnk = action_icon[self.icon_to_edit].flowup_tolink(flow)
        icon2 = link[lnk][0]
        chkb_state = tk.HIDDEN if self.itemcget(lnk, "state") == tk.NORMAL else tk.NORMAL
        self.itemconfigure(lnk, state=chkb_state)
        if chkb_state == tk.HIDDEN:
            self.put_mark_invisibility(self.icon_to_edit, state=ON, up_down=UP)
            self.put_mark_invisibility(icon2, state=ON, up_down=DOWN)
        elif not self.invisible_links(self.icon_to_edit, up_down=UP):
            self.put_mark_invisibility(self.icon_to_edit, state=OFF, up_down=UP)
            self.put_mark_invisibility(icon2, state=OFF, up_down=DOWN)

    def toggle_lnkdwnvisibility(self, flow):
        lnk = action_icon[self.icon_to_edit].flowdwn_tolink(flow)
        icon2 = link[lnk][1]
        chkb_state = tk.HIDDEN if self.itemcget(lnk, "state") == tk.NORMAL else tk.NORMAL
        self.itemconfigure(lnk, state=chkb_state)
        if chkb_state == tk.HIDDEN:
            self.put_mark_invisibility(self.icon_to_edit, state=ON, up_down=DOWN)
            self.put_mark_invisibility(icon2, state=ON, up_down=UP)
        elif not self.invisible_links(self.icon_to_edit, up_down=UP):
            self.put_mark_invisibility(self.icon_to_edit, state=OFF, up_down=DOWN)
            self.put_mark_invisibility(icon2, state=OFF, up_down=UP)

    def menu_icon(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        self.icon_to_edit = self.find_withtag(tk.CURRENT)[0]

        # Actualize Menus predeccesors, suceesors, that is first knowing if there are items from previous run
        #  abd then erase them. also clearing the list of control IntVar fro the checkboxes
        p_checkbox_var = []
        itemsPre = self.predeccesorMenu.index(tk.END)
        if itemsPre != None:
            self.predeccesorMenu.delete(0, itemsPre)
        cb_predeccesors = action_icon[self.icon_to_edit].flow_parents()
        cb_predeccesors.sort()
        for flow in cb_predeccesors:
            p_checkbox_var.append(tk.IntVar())
            self.predeccesorMenu.add_checkbutton(label=str(flow), variable=p_checkbox_var[-1],
                                                 command=lambda flow=flow: self.toggle_lnkupvisibility(flow))
            lnk = action_icon[self.icon_to_edit].flowup_tolink(flow)
            chkb_state = 1 if self.itemcget(lnk, "state") == tk.NORMAL else 0
            p_checkbox_var[-1].set(chkb_state)

        s_checkbox_var = []
        itemsSucc = self.succesorMenu.index(tk.END)
        if itemsSucc != None:
            self.succesorMenu.delete(0, itemsSucc)
        cb_succesors = action_icon[self.icon_to_edit].flow_descendents()
        cb_succesors.sort()
        for flow in cb_succesors:
            s_checkbox_var.append(tk.IntVar())
            self.succesorMenu.add_checkbutton(label=str(flow), variable=s_checkbox_var[-1],
                                                 command=lambda flow=flow: self.toggle_lnkdwnvisibility(flow))
            lnk = action_icon[self.icon_to_edit].flowdwn_tolink(flow)
            chkb_state = 1 if self.itemcget(lnk, "state") == tk.NORMAL else 0
            s_checkbox_var[-1].set(chkb_state)

        self.edit_actionMenu.post(event.x_root, event.y_root)

    def error_change(self, icon_id, new_action):
        if action_icon[icon_id].action != new_action:
            actions_in_row = set()
            iconsrow = self.icons_in_row(action_icon[icon_id].row)
            for a in iconsrow:
                actions_in_row.add(action_icon[a].action)
            # Error 501 Forbidden to have another SETTING in a row with an already present SETTING
            if SETTING in actions_in_row and new_action == SETTING:
                return 501

            # Error 502 Change produces a combination of icons not allowed
            if SETTING in actions_in_row or new_action == SETTING:
                actions_in_row.add(new_action)
                actions_in_row.remove(action_icon[icon_id].action)
                if {SETTING}.issubset(actions_in_row):
                    if not actions_in_row.issubset(SETTING_COMPATIBLE):
                        return 502

            # Error 511 Change produces a NON-SETTING with multiple parents
            parents = action_icon[icon_id].flow_parents()
            if new_action != SETTING and len(parents) > 1:
                return 511

        return 0

    def change_icon(self, new_action):
        if not (error := self.error_change(self.icon_to_edit, new_action)):
            self.itemconfigure(self.icon_to_edit, image=self.ICONS[new_action])
            parents = action_icon[self.icon_to_edit].icon_parents()
            if action_icon[self.icon_to_edit].action == SETTING:
                old_flow = action_icon[self.icon_to_edit].flow
                action_icon[self.icon_to_edit].action = new_action
                if parents: # because is ok the change there will be only one parent
                    self.actualize_flow(parents[0])
                    # now renumber Settings....
                for icon in action_icon:
                    action_icon[icon].flow = action_icon[icon].flow -1\
                        if old_flow < action_icon[icon].flow else action_icon[icon].flow
            else:
                pass
        else:
            self.error_message(error)





    def menu_change(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        self.icon_to_edit = self.find_withtag(tk.CURRENT)[0]
        self.changingmenu.post(event.x_root, event.y_root)


    def menu_boundaryaction(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        rect = self.find_withtag(tk.CURRENT)[0]
        ref = self.find_closest(sheet_description[0]["x1"], self.coords(rect)[1])
        self.icon_row = int(self.itemcget(ref, "text"))
        self.click_x = x
        self.click_y = y
        self.boundarymenu.post(event.x_root, event.y_root)

    def draw_icon(self, type_icon):
        global action_icon

        if not (error := self.error_icon(type_icon, self.icon_row)):
            rx1, ry1, rx2, ry2 = self.bbox(coding_sheet[self.icon_row][ACTIONS_COLUMN])
            delta_y = (ry2-ry1-25)/2  # for centring the icon on y axis
            item = self.create_image(self.click_x, ry1 + delta_y, anchor=tk.NW, image=self.ICONS[type_icon],
                                     tags="icon", disabledimage=self.ICONS[type_icon+6])
            action_icon[item] = action(row=self.icon_row, flow=UNCONNECTED,
                                   action=type_icon, delta_x=self.click_x)
            if type_icon == SETTING:
                self.numbering_new_setting(item)
            else:
                prev_flow = self.get_previous_nonSetting(item)
                action_icon[item].flow = prev_flow - 1
                self.renumbering_non_settings(item)
        else:
            self.error_message(error)

    def error_message(self, errorcode):
        messagebox.showerror("Boundary Games Syntax Error", error_message[errorcode])

    def error_icon(self, icon, icon_row):
        # error 101 no more than one Setting per row
        if icon == SETTING:
            if self.setting_in_row(icon_row):
                return 101

        # error 102
        actions_in_row = set()
        iconsrow = self.icons_in_row(icon_row)
        for a in iconsrow:
            actions_in_row.add(action_icon[a].action)
        if SETTING in actions_in_row or icon == SETTING:
            actions_in_row.add(icon)
            if not actions_in_row.issubset(SETTING_COMPATIBLE) :
                return 102
        return 0

    def redraw_iconlinks(self, icon):
        for i in action_icon[icon].links:
            icon1 = link[i][0]
            icon2 = link[i][1]

            lx1, ly1 = self.icon_center(icon1)
            lx2, ly2 = self.icon_center(icon2)
            sx = lx1 if ly1 > ly2 else lx2
            sy = ((max(ly1, ly2) - min(ly1, ly2))/2) + min(ly1, ly2)
            self.coords(i, lx1, ly1, sx, sy, lx2, ly2)
            if ly1 > ly2:
                link[i] = (icon2, icon1)

    def to_thefront(self, icon):
        ref = self.create_line(50, -10, 51, -10)
        self.tag_raise(icon, ref)
        self.delete(ref)

    def icon_to_move(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        icon = self.find_withtag(tk.CURRENT)[0]
        item_tags = self.gettags(icon)
        print(item_tags)
        if "icon" in item_tags:
            #         turn off the markings of invisibility before moving
            icon = self.find_withtag(tk.CURRENT)[0]
            print("icon::::::::", icon)
            self.put_mark_invisibility(icon, state=OFF, up_down=UP)
            self.put_mark_invisibility(icon, state=OFF, up_down=DOWN)

            self.to_thefront(tk.CURRENT)
            coords = self.coords(tk.CURRENT)
            self.icon_dx = x - coords[0]
            self.icon_dy = y - coords[1]

    def move_icon(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        coords = self.bbox(tk.CURRENT)
        icon = self.find_withtag(tk.CURRENT)[0]
        if len(coords):
            self.coords(tk.CURRENT, x-self.icon_dx, y-self.icon_dy)
            self.redraw_iconlinks(icon)

    def error_move(self, icon_ID, to_row):
        # error 301 no more than one Setting per row
        if action_icon[icon_ID].action == SETTING:
            count = 0
            icons = self.icons_in_row(to_row)
            for i in icons:
                if action_icon[i].action == SETTING:
                    count += 1
            if count > 1:
                return 301

        # error 302 Moving a Setting, Following or Enhancing to row with an already present Setting
        setting_compatible = {SETTING, CHALLENGING, WANDERING, PROBING}
        actions_in_row = set()
        iconsrow = self.icons_in_row(to_row)
        for a in iconsrow:
            actions_in_row.add(action_icon[a].action)
        actions_in_row.add(action_icon[icon_ID].action)
        if SETTING in actions_in_row or action_icon[icon_ID].action == SETTING:
            actions_in_row.add(action_icon[icon_ID].action)
            if not actions_in_row.issubset(setting_compatible) :
                return 302

        # error 305 Move produces an Setting not connected to the last immediate action of a parent flow
        if action_icon[icon_ID].action == SETTING:
            predecessors = action_icon[icon_ID].icon_parents()
            succesors = []
            for p in predecessors:
                s = action_icon[p].next_inflow()
                if s:
                    succesors.append(action_icon[s].row)
                if succesors:
                    succesors.sort()
                    if to_row >= succesors[0]:
                        return 305

        # error 306 Moving the icon disrupts previously established sequence. Delete links before moving
        closest_up = action_icon[icon_ID].closest_rowup()
        closest_down = action_icon[icon_ID].closest_rowdown()
        if (to_row <= closest_up != -1) or (to_row >= closest_down != -1):
            return 306

        # error 307 Moving a Setting out of enclosing Settings
        if action_icon[icon_ID].action == SETTING:
            past, later = action_icon[icon_ID].enclosing_settings()
            if past:
                if action_icon[past].row > to_row:
                    return 307
            if later:
                if to_row > action_icon[later].row:
                    return 307

        return 0

    def icon_restplace(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        icon_id = self.find_withtag(tk.CURRENT)[0]
        overlapping = self.find_overlapping(x, y, x, y)
        rectangle = [item for item in overlapping if self.type(item) == "rectangle"]
        error_move = 1
        if rectangle and "icon_frame" in self.gettags(rectangle):
            rect = rectangle[0]
            ref = self.find_closest(sheet_description[0]["x1"], self.coords(rect)[1])
            icon_row = int(self.itemcget(ref, "text"))

            if not (error_move := self.error_move(icon_id, icon_row)):
                rx1, ry1, rx2, ry2 = self.bbox(rect)
                delta_y = (ry2-ry1-25)/2  # for centring the icon on y axis

                self.coords(tk.CURRENT, x-self.icon_dx, ry1+delta_y)
                action_icon[self.find_withtag(tk.CURRENT)[0]].delta_x = x-self.icon_dx
                icon_oldrow = action_icon[self.find_withtag(tk.CURRENT)[0]].row
                action_icon[self.find_withtag(tk.CURRENT)[0]].row = icon_row

# Special case in which a Setting is move to row 0 and becomes prime SETTING
                if action_icon[icon_id].action == SETTING and icon_row == 0:
                    action_icon[icon_id].orphan = False
                    self.actualize_flow(icon_id)
# special case Setting when moved it loses Prime status

                if action_icon[icon_id].action == SETTING and icon_oldrow == 0 and icon_row > 0:
                    action_icon[icon_id].orphan = True
                    self.actualize_flow(icon_id)

        if error_move:
            rx1, ry1, rx2, ry2 = self.bbox(coding_sheet[action_icon[icon_id].row][ACTIONS_COLUMN])
            delta_y = (ry2-ry1-25)/2  # for centring the icon on y axis
            self.coords(tk.CURRENT, action_icon[icon_id].delta_x, ry1 + delta_y)
            self.error_message(error_move)
        self.redraw_iconlinks(icon_id)

        # re-establishing invisibility marks
        if self.invisible_links(icon_id, up_down=UP):
            self.put_mark_invisibility(icon_id, state=ON, up_down=UP)
        if self.invisible_links(icon_id, up_down=DOWN):
            self.put_mark_invisibility(icon_id, state=ON, up_down=DOWN)

    def menu_link(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        self.link_to_edit = self.find_withtag(tk.CURRENT)[0]
        self.linkmenu.post(event.x_root, event.y_root)

    def delete_link(self):
        icon1, icon2 = link[self.link_to_edit][0], link[self.link_to_edit][1]

        # erase link from icon1 list of links
        links_list = list(action_icon[icon1].links)
        links_list.remove(self.link_to_edit)
        action_icon[icon1].links = tuple(links_list)

        # erase link from icon2 list of links
        links_list = list(action_icon[icon2].links)
        links_list.remove(self.link_to_edit)
        action_icon[icon2].links = tuple(links_list)

        # erase the link from the link dictionary and link_to edit that is really a list with only
        # one element
        del link[self.link_to_edit]
        self.delete(self.link_to_edit)

        # bit to correct....the idea is to check if there are more line lines to keep it connected.
        if action_icon[icon2].action != SETTING:
            # action_icon[icon2].flow = UNCONNECTED
            # action_icon[icon2].orphan = True
            action_icon[icon2].flow = self.get_previous_nonSetting(icon2) - 1
            action_icon[icon2].orphan = True
            self.renumbering_non_settings(icon2)
        else:
            unconnected_links = action_icon[icon2].unconnected_predecessors()
            if not unconnected_links and action_icon[icon2].flow_parents():
                action_icon[icon2].orphan = False
            else:
                action_icon[icon2].orphan = True
        self.actualize_flow(icon2)

               
##______________________________ Menus and operations for drawing boundary icons
##____________________________________________________________________________



################################# Validations-Rules-Boundary Games "Grammar"
############################################################################

    # return a list of iconsID on the row
    def icons_in_row(self, row):
        x1, y1, x2, y2 = self.bbox(coding_sheet[row][ACTIONS_COLUMN])
        overlapping_items = self.find_overlapping(x1, y1, x2, y2)
        return [icon for icon in overlapping_items if self.type(icon) == "image"]

    def setting_in_row(self, row):
        # returns the iconID is there is already a Setting on the row
        # get the items overlapping cell of icons in that row
        icons = self.icons_in_row(row)
        for icon in icons:
            if action_icon[icon].action == SETTING:
                return icon
        return 0

    def numbering_new_setting(self, iconID):
        # First it will assign a new number to the Setting
        # then it will fix numeration for all the other Settings
        row = action_icon[iconID].row - 1
        setting_found = False
        # going back to look for a previous Settings
        while row >= 0:
            l_icons = self.icons_in_row(row)
            if previous_setting := self.setting_in_row(row):
                setting_found = True
                break
            row -= 1
        if setting_found:
            action_icon[iconID].flow = action_icon[previous_setting].flow + 1 # numbering the setting
            action_icon[iconID].graph_x = (action_icon[previous_setting].graph_x + 10) % 1200 # for the graph view
        else:
            action_icon[iconID].flow = 0
            action_icon[iconID].graph_x = 20  # initial place for icon in graph view...better a constant?
            # go to the whole list of icons renumbering the settings
        for icon in action_icon.keys():
            if action_icon[icon].action == SETTING and action_icon[icon].row == 0:
                action_icon[icon].orphan = False
            if (action_icon[icon].flow < action_icon[iconID].flow) or (icon == iconID):
                action_icon[icon].flow = action_icon[icon].flow
            else:
                action_icon[icon].flow = action_icon[icon].flow + 1

    def get_previous_nonSetting(self, icon_id):
        row = action_icon[icon_id].row
        while row >= 0:
            icons = self.icons_in_row(row)
            non_settings = [icon for icon in icons if action_icon[icon].action != SETTING and icon != icon_id]
            if non_settings:
                candidates = [icon for icon in non_settings if not action_icon[icon].flow_parents()]
                if candidates:
                    min_flow = -1
                    for c in candidates:
                        min_flow = action_icon[c].flow if action_icon[c].flow < min_flow else min_flow
                    return min_flow
            row -= 1
        return 0

    def renumbering_non_settings(self, icon_id):
        for icon in action_icon.keys():
            action_icon[icon].flow = action_icon[icon].flow-1 if \
                action_icon[icon].flow <= action_icon[icon_id].flow \
                and action_icon[icon].row > action_icon[icon_id].row else action_icon[icon].flow


##_______________________________ Validations-Rules-Boundary Games "Grammar"
##__________________________________________________________________________


################################# Orphans and not Orphan Flows Visualization
############################################################################


    def actualize_flow(self, icon1):
        color = action_icon[icon1].flow_color
        orphan_st = action_icon[icon1].orphan
        flow_dash = UNCONNECTED_DASH if orphan_st else CONNECTED_DASH
        lnks = action_icon[icon1].disseminate_toicons(icon1, color, orphan_st)
        for lk in lnks:
            self.itemconfigure(lk, fill=self.action_tkcolor(color), dash=flow_dash)
            if action_icon[link[lk][1]].action == SETTING:
                sblnk_color = self.action_tkcolor(action_icon[link[lk][1]].flow_color)
                # if the sublink is currently orphan, but the parent flow is not orphan
                # and all the predecessors are connected change the sublink to not orphan
                if (not orphan_st) and action_icon[link[lk][1]].orphan and \
                        (not action_icon[link[lk][1]].unconnected_predecessors()):
                    sublnk = action_icon[link[lk][1]].disseminate_toicons\
                        (link[lk][1], action_icon[link[lk][1]].flow_color, False)
                    for sl in sublnk:
                        self.itemconfigure(sl, fill=sblnk_color, dash=CONNECTED_DASH)
                # if the parent flow is orphan and the sublink is not orphan, we need to put the sublink as orphan
                elif orphan_st and (not action_icon[link[lk][1]].orphan):
                    sublnk = action_icon[link[lk][1]].disseminate_toicons(link[lk][1],
                                                                          action_icon[link[lk][1]].flow_color, True)
                    for sl in sublnk:
                        self.itemconfigure(sl, fill=sblnk_color, dash=UNCONNECTED_DASH)


##_______________________________ Orphans and not Orphan Flows Visualization
##__________________________________________________________________________



################################# Contextual Menu for icons and links
#####################################################################

    def edit_window_cancel(self):
        self.delete(self.canvas_window)

    def edit_window_ok(self):
        action_icon[self.icon_to_edit].note = self.icon_note.get()
        action_icon[self.icon_to_edit].flow_color = self.flow_color.get()
        self.actualize_flow(self.icon_to_edit)

        self.delete(self.canvas_window)

    def edit_action(self):
        x1, y1, x2, y2 = self.bbox(self.icon_to_edit)

        edit_window = ttk.Frame(coding_view, borderwidth=5, relief="ridge")
        edit_window['padding'] = 5
        self.icon_note = tk.StringVar(value=action_icon[self.icon_to_edit].note)
        self.flow_color = tk.IntVar(value=action_icon[self.icon_to_edit].flow_color)

        l1 = ttk.Label(edit_window, text="Icon memo : ")
        e1 = ttk.Entry(edit_window, textvariable=self.icon_note, width=45)
        l2 = ttk.Label(edit_window, text="Flow color->")

        rb0 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=0, image=self.FLOW_COLORS[0])
        rb1 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=1, image=self.FLOW_COLORS[1])
        rb2 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=2, image=self.FLOW_COLORS[2])
        rb3 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=3, image=self.FLOW_COLORS[3])
        rb4 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=4, image=self.FLOW_COLORS[4])
        rb5 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=5, image=self.FLOW_COLORS[5])
        rb6 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=6, image=self.FLOW_COLORS[6])
        rb7 = ttk.Radiobutton(edit_window, variable=self.flow_color, value=7, image=self.FLOW_COLORS[7])



        b1 = ttk.Button(edit_window, text="Ok", command=self.edit_window_ok)
        b2 = ttk.Button(edit_window, text="Cancel", command=self.edit_window_cancel)

        l1.grid(row=0, column=0)
        e1.grid(row=0, column=1, columnspan=3)
        l2.grid(row=1)

        if self.flow_color.get() != ORPHAN_LINKCOLOR:
            rb0.grid(row=2, column=0)  # red
            rb1.grid(row=3, column=0)  # orange
            rb2.grid(row=2, column=1)  # blue
            rb3.grid(row=3, column=1)  # cyan
            rb4.grid(row=2, column=2)  # lemongreen
            rb5.grid(row=3, column=2)  # grassgreen
            rb6.grid(row=2, column=3)  # black
            rb7.grid(row=3, column=3)  # gray

        b1.grid(row=4, column=1)
        b2.grid(row=4, column=2)
        self.canvas_window = self.create_window(x2, y2, window=edit_window)
        edit_window.mainloop()


##_______________________________ Contextual Menu for icons and links
##_____________________________________________________________________

################################# Keys and creation of rows
##########################################################            
    
    def handle_key(self, event):
        # widget-wide key dispatcher
        item = self.has_focus()
        if not item:
            return
        insert = self.index(item, tk.INSERT)
        
        if event.keysym == "Return" and sheet_description[current_column]["enter_behaviour"] == "break_field":
            self.break_field(current_row)    
        if event.keysym == "Return" and sheet_description[current_column]["enter_behaviour"] == "new_row":
            self.insert_row(current_row+1)
        elif event.char >= " " or (event.keysym == "Return" and
                                   sheet_description[current_column]["enter_behaviour"] == "in_field"):
            # printable character
            if self.select_item():  # this if not because there will no be selection
                self.dchars(item, tk.SEL_FIRST, tk.SEL_LAST)
                self.select_clear()
            self.insert(item, "insert", event.char)
            self.highlight(item)

        elif event.keysym == "BackSpace":
            if self.select_item():
                self.dchars(item, tk.SEL_FIRST, tk.SEL_LAST)
                self.select_clear()
            else:
                if insert > 0:
                    self.dchars(item, insert-1, insert)
                elif current_column == COMMUNICATION_COLUMN and current_row > 0 :
                    self.transcript_bs()
                    item = self.has_focus()
            self.highlight(item)

        # navigation
        elif event.keysym == "Home":
            self.icursor(item, 0)
            self.select_clear()
        elif event.keysym == "End":
            self.icursor(item, tk.END)
            self.select_clear()
        elif event.keysym == "Right":
            self.icursor(item, insert+1)
            self.select_clear()
        elif event.keysym == "Left":
            self.icursor(item, insert-1)
            self.select_clear()
        elif event.keysym == "Tab":
            self.next_cell()
        else:
            pass
        self.update_idletasks()
        m = self.move_to_visibility(item)
        while m != 0:
            self.yview(tk.SCROLL, m, tk.UNITS)
            m = self.move_to_visibility(item)

    def shift_tab(self, event):
        item = self.has_focus()
        if not item:
            return
        self.prev_cell()
        self.yview(tk.SCROLL, self.move_to_visibility(item), tk.UNITS)

    def prev_cell(self):
        global current_row, current_column
        c = current_column-1
        if sheet_description[c]["type_of_field"] in ["graph", "no_editable"]:
            c -= 1
        if c < 0:
            if current_row > 0:
                current_row -= 1
                c = number_of_columns-1
            else:
                c = TIME_COLUMN
        current_column = c
        self.focus_set()  # move focus to canvas
        self.focus(coding_sheet[current_row][current_column])  # set focus to text item
        self.index(coding_sheet[current_row][current_column], tk.END)
        self.highlight(coding_sheet[current_row][current_column])
    
    def next_cell(self):
        global current_row, current_column

        current_column += 1
        if current_column >= number_of_columns:
            if current_row == len(coding_sheet)-1:
                self.new_row(current_row+1)
                current_row += 1
                current_column = TIME_COLUMN
            else:
                current_row += 1
                current_column = TIME_COLUMN
        elif sheet_description[current_column]["type_of_field"] in ["graph", "no_editable"]:
            current_column += 1
                
        self.focus_set()  # move focus to canvas
        self.focus(coding_sheet[current_row][current_column])  # set focus to text item
        self.index(coding_sheet[current_row][current_column], tk.END)
        self.highlight(coding_sheet[current_row][current_column])

    def delete_row(self, row):
        # measure fields to delete and to move
        dy1 = self.fit_box(coding_sheet[row][0])[1]
        dy2 = self.maxy_row_box(row)
        my1 = dy2 + GAP_FOR_LINE +1
        my2 = self.maxy_row_box(len(coding_sheet)-1) + GAP_FOR_LINE + 1

        # mark areas to delete (we have to exclude some because overlapping goes too far) and to move
        self.addtag_overlapping("delete", 0, dy1, 1367, dy2 + GAP_FOR_LINE)
        self.addtag_overlapping("exclude", -1, self.fit_box(coding_sheet[row-1][0])[1],
                                1367, self.fit_box(coding_sheet[row-1][0])[3])
        self.dtag("exclude", "delete")

        self.addtag_overlapping("move", 0, my1, 1367, my2)

        # delte from canvas
        self.delete("delete")

        # renumber rows and icons because we have things to move and renumber
        if row < len(coding_sheet)-1:
#            dy_shift = dy2 - my2 + GAP_FOR_LINE +1
            dy_shift = (dy2 - dy1 + (GAP_FOR_LINE * 2)) * (- 1)

            self.move("move", 0, dy_shift)

            for i in range(row, len(coding_sheet)):
                move_to_renumber = coding_sheet[i][0]
                self.itemconfigure(move_to_renumber, text=str(i - 1))
            for i in action_icon:
                action_icon[i].row = action_icon[i].row -1 if action_icon[i].row >= row \
                    else action_icon[i].row

        self.dtag("exclude", "exclude")
        self.dtag("move", "move")
        # delete logically
        del coding_sheet[row]
        self.fix_graph(row-1)


    def transcript_bs(self):
        global current_row
        if not self.icons_in_row(current_row):
            # get the sources text from transcript and notes

            comm_down_text = self.itemcget(coding_sheet[current_row][COMMUNICATION_COLUMN], "text")
            note_down_text = self.itemcget(coding_sheet[current_row][NOTES_COLUMN], "text")

            #move text to the row above
            current_row -= 1
            # get the target text from transcript and notes
            comm_up_text = self.itemcget(coding_sheet[current_row][COMMUNICATION_COLUMN], 'text')
            note_up_text = self.itemcget(coding_sheet[current_row][NOTES_COLUMN], 'text')

            self.itemconfigure(coding_sheet[current_row][COMMUNICATION_COLUMN], text=comm_up_text + " " + comm_down_text)
            self.itemconfigure(coding_sheet[current_row][NOTES_COLUMN], text=note_up_text + " " + note_down_text)

            # move field up
            self.focus_set()
            self.focus(coding_sheet[current_row][COMMUNICATION_COLUMN])  # set focus to text item
            self.index(coding_sheet[current_row][COMMUNICATION_COLUMN], tk.END)
            self.icursor(coding_sheet[current_row][COMMUNICATION_COLUMN], tk.END)
            self.highlight(coding_sheet[current_row][COMMUNICATION_COLUMN])

            self.delete_row(current_row+1)


        else:
            self.error_message(601)

    def break_field(self, row):
        item = self.has_focus()
        if not item:
            return
        insert = self.index(item, tk.INSERT)
        if insert == 0:
            self.insert_row(row)
        else:
            text = self.itemcget(item, 'text')
            textabove = text[:insert]
            textbelow = text[insert:]
            self.itemconfigure(item, text=textabove)
            self.highlight(coding_sheet[current_row][current_column])

            self.insert_row(row+1, ["", "", "", "", textbelow, ""])

            self.focus_set()  # move focus to canvas
            self.focus(coding_sheet[current_row][current_column])  # set focus to text item
            self.index(coding_sheet[current_row][current_column], tk.END)
            self.highlight(coding_sheet[current_row][current_column])

    def insert_row(self, row, contents=[]):
        global current_row, current_column
        # Setting in the first row lose the prime Setting status when moved downwards
        setting_icon = self.setting_in_row(row)
        if setting_icon and row == 0:
            action_icon[setting_icon].orphan = True
            self.actualize_flow(setting_icon)

        if row < len(coding_sheet):  # if we insert before last line, we need to select lines to push down
            self.addtag_overlapping("move", 0, self.maxy_row(row-1) + CELL_GAP_Y-1, 1367,
                                        self.maxy_row(len(coding_sheet) - 1) + GAP_FOR_LINE)
            # change numeration for rows....and change rows for shifted icons
            for i in range(row, len(coding_sheet)):
                move_to_renumber = coding_sheet[i][0]
                self.itemconfigure(move_to_renumber, text=str(i + 1))
            for i in action_icon:
                action_icon[i].row = action_icon[i].row + 1 if action_icon[i].row >= row \
                    else action_icon[i].row
            self.new_row(row, contents)
            current_row += 1

            shift_y = self.maxy_row(row) - self.fit_box(coding_sheet[row][0])[1] + CELL_GAP_Y
            self.move("move", 0, shift_y)
            self.dtag("move", "move")
        else:
            self.new_row(row, contents)
            current_row += 1

       # focus the new cell
        self.focus_set()  # move focus to canvas
        self.focus(coding_sheet[current_row][current_column])  # set focus to text item
        self.index(coding_sheet[current_row][current_column], tk.END)
        self.highlight(coding_sheet[current_row][current_column])

    def new_row(self, row, contents=[]):
        global current_row, current_column
        
        y = self.maxy_row(row-1)+CELL_GAP_Y
        coding_sheet.insert(row, [])
        column = 0
        for i in sheet_description:
            if i["type_of_field"] == "graph":
                item = self.create_rectangle(i["x1"], y, i["x1"] + i["width"], y + LINE_SPACE - 1, fill=REC_INACTIVE,
                                             outline="", activefill=REC_CODING, width=8, tags="icon_frame")
                self.tag_lower(item, self.baseline)
            else:
                label = ""
                field_state = tk.NORMAL
                rec_fill = REC_INACTIVE
                txt_fill = TXT_INACTIVE
                if contents:
                    label = contents[column]
                if i["field_name"] == "Move":
                    label = str(row)
                    field_state = tk.DISABLED
                    rec_fill = "black"
                    txt_fill = "white"
                item = self.create_text(i["x1"], y, justify=tk.LEFT, width=i["width"], state=field_state, text=label,
                                        anchor=tk.NW, fill=txt_fill, activefill=TXT_HOVERING, tags="field")
                ix1, iy1, ix2, iy2 = self.fit_box(item)
                rectangle = self.create_rectangle(i["x1"], y, i["x1"] + i["width"], iy2, state=field_state,
                                                  fill=rec_fill, outline="", activefill=REC_HOVERING, tags="bg")
                self.tag_lower(rectangle, item)
            coding_sheet[row].append(item)
            column += 1

        # fixing the height of ACTION_COLUMN accordingly to maximum height in the row
        maxy = 0
        for i in range(number_of_columns):
            if i != ACTIONS_COLUMN:
                maxy = max([maxy, self.fit_box(coding_sheet[row][i])[3]])
        x1, y1, x2, y2 = self.coords(coding_sheet[row][ACTIONS_COLUMN])
        self.coords(coding_sheet[row][ACTIONS_COLUMN], x1, y1, x2, maxy)

        line_y = self.maxy_row(row) + GAP_FOR_LINE
        self.redraw_links()
        self.create_line(0, line_y, 1366, line_y, fill=LINE_COLOR, width=1)
#        self.configure(scrollregion=self.bbox("all"))

##_______________________________________ Key and creation of rows
##________________________________________________________________            

    def identify_icon(self, row, action, delta_x):
        # meant to work with files. The information of the file need to be inferred to re-create the original diagram
        # for link, the file contains some characteristics of what is required from the link.
        # it should connect a certain icon, in certain part of the screen with another
        # so we need to look on the current icons which one fit the description in order to create the link
        rx1, ry1, rx2, ry2 = self.bbox(coding_sheet[row][ACTIONS_COLUMN])
        candidates = self.find_overlapping(rx1, ry1, rx2, ry2)
        for c in candidates:
            if c in action_icon:
                if action_icon[c].action == action and action_icon[c].delta_x == delta_x:
                    return c
        return 0
                
##_________________________________________________________________________            
######### End of class CanvasText #########################
##_________________________________________________________________________            


####################################################################
############################## TreeCanvas
####################################################################


class TreeCanvas(tk.Canvas):
    def __init__(self, root, **options):
        tk.Canvas.__init__(self, root, options)

        self.t_matrix = []
        self.leafs = []

        self.BASE_Y = 50
        self.GAP_Y = 20
        self.ref = 0

        self.info_window_on = False
        self.bind("<Button-1>", self.show_info)
        self.bind("<B1-ButtonRelease>", self.close_info_window)


        self.x1 = 0
        self.bg_tomove = 0
        self.moving = False
        self.leaf_moved = 0

        self.bind("<Shift-Button-1>", self.icon_to_move)
        self.bind("<Shift-B1-Motion>", self.move_icon)
        self.bind("<Shift-B1-ButtonRelease>", self.icon_restplace)





      # self.bind("<Double-Button-1>", self.double_click)
      # self.bind("<Button-3>", self.menu_boundaryaction)
      #

    def load_data(self):
        self.leafs = [flow for flow in action_icon.values() if flow.action == SETTING]
        if self.leafs:
            self.leafs.sort(key=self.leafs[0].sort_byflow)
            graphsize = len(self.leafs)
            self.t_matrix = [[0 for y in range(graphsize)] for x in range(graphsize)]
        for leaf in self.leafs:
            lnk = leaf.flow_parents()
            for l in lnk :
                self.t_matrix[leaf.flow][l] = 1

    def paint(self):
        self.ref = self.create_line(50, -10, 51, -10)
        for leaf in self.leafs:
            leaf_tags = (str(leaf.flow), "leaf")
            t = self.create_text(leaf.graph_x, self.BASE_Y+(leaf.flow*self.GAP_Y), fill="white",
                                 text=str(leaf.flow), tags=leaf_tags)
            x1, y1, x2, y2 = self.bbox(t)
            print ("coordinates:", leaf.flow, self.coords(t))
            o = self.create_oval(x1-5, y1, x2 + 5, y2, fill=LEAF_COLOR, tags=str(leaf.flow))
            self.tag_lower(o, t)
        self.draw_links()

    def draw_links(self):
        for y in range(len(self.leafs)):
            for x in range (len(self.leafs)):
                if self.t_matrix[y][x] > 0:
                    i1x = self.leafs[y].graph_x
                    i1y = self.BASE_Y+ (y*self.GAP_Y)
                    i2x = self.leafs[x].graph_x
                    i2y = self.BASE_Y+ (x*self.GAP_Y)
                    l = self.create_line(i1x, i1y, i2x, i2y,
                                         fill=c.action_tkcolor(self.leafs[x].flow_color), width=3)
                    self.tag_lower(l, self.ref)
                    self.t_matrix[y][x] = l

    def show_info(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        if self.type(tk.CURRENT) == "text":
            leaf = int(self.itemcget(tk.CURRENT, "text"))
            label = "------------------------------" + "\n" + \
                    "flow  : " + str(self.leafs[leaf].flow) + "\n" + \
                    "note  : " + (self.leafs[leaf].note)
            info = self.create_text(x, y, justify=tk.LEFT, width=250, text=label, tags="info_window", anchor=tk.NW)
            x1, y1, x2, y2 = self.bbox(info)
            rect = self.info_window_ID = self.create_rectangle(x1 - 3, y1 - 3, x2 + 3, y2 + 3,
                                                               fill="yellow", tags="info_window",  width=2)
            self.tag_lower(rect, info)
            # create multiple elements for the window with a tag "info_window" so when erased just erase all
            # with the tag
            # perhaps create first the text and then make rectangle as big as text(just as when loading file)
            self.info_window_on = True

    def close_info_window(self, event):
        if self.info_window_on:
            self.delete("info_window")
            self.info_window_on = False

    def to_thefront(self, icon):
        ref = self.create_line(50, -10, 51, -10)
        self.tag_raise(icon, ref)
        self.delete(ref)

    def redraw_link(self, leaf):
        if leaf > 0:
            for i in range(leaf):
                lnk = self.t_matrix[leaf][i]
                if lnk:
                    i1x = self.leafs[leaf].graph_x + 5
                    i1y = self.BASE_Y+ (leaf*self.GAP_Y)
                    i2x = self.leafs[i].graph_x + 5
                    i2y = self.BASE_Y+ (i*self.GAP_Y)
                    self.coords(lnk, i1x, i1y, i2x, i2y)
        if leaf < len(self.t_matrix):
            for i in range(leaf, len(self.t_matrix)):
                lnk = self.t_matrix[i][leaf]
                if lnk:
                    i1x = self.leafs[leaf].graph_x + 5
                    i1y = self.BASE_Y + (leaf * self.GAP_Y)
                    i2x = self.leafs[i].graph_x + 5
                    i2y = self.BASE_Y + (i * self.GAP_Y)
                    self.coords(lnk, i1x, i1y, i2x, i2y)

    def icon_to_move(self, event):
        x = self.canvasx(event.x)
        if "leaf" in self.gettags(tk.CURRENT):
            self.leaf_moved = int(self.gettags(tk.CURRENT)[0])
            self.bg_tomove = self.find_below(tk.CURRENT)
            self.moving = True

    def move_icon(self, event):
        if self.moving:
            x = self.canvasx(event.x)
            self.x1, y1, x2, y2 = self.bbox(tk.CURRENT)
            self.move(tk.CURRENT, x-self.x1, 0)
            self.move(self.bg_tomove, x - self.x1, 0)
            self.leafs[self.leaf_moved].graph_x = x
            self.redraw_link(self.leaf_moved)

    def icon_restplace(self, event):
        if self.moving:
            x = self.canvasx(event.x)
            self.move(tk.CURRENT, x-self.x1, 0)
            self.move(self.bg_tomove, x - self.x1, 0)
            self.bg_tomove = 0
            self.leafs[self.leaf_moved].graph_x = x
            self.redraw_link(self.leaf_moved)
            self.moving = False

            leaf_to_actualize = [icon for icon in action_icon.values()
                                 if icon.action == SETTING and icon.flow ==self.leaf_moved][0]
            leaf_to_actualize.graph_x = x

##_________________________________________________________________________
######### End of class TreeCanvas #########################
##_________________________________________________________________________


def print_coding():
    c.postscript(file="print.ps", colormode="color")
    os.startfile("print.ps", "print")

    # # filename = tempfile.mktemp(".txt")
    # # open(filename, "w").write("This is a test")
    # win32api.ShellExecute(
    #     0,
    #     "printto",
    #     "print.ps",
    #     '"%s"' % win32print.GetDefaultPrinter(),
    #     ".",
    #     0
    # )



def nothing_to_do():
    pass

def import_file():
    global current_row, current_column, coding_sheet

    filename = filedialog.askopenfilename(title="Import Word Table File", defaultextension=".docx",
                                          filetypes=(("Word file", "*.docx"), ("all files", "*.*")))
    if filename:
        coding_sheet = []  # this and the following erase the previous information
        c.addtag_all("erase")
        c.delete("erase")
        c.baseline = c.create_line(0, -10, 10, -10)
        action_icon.clear()
        link.clear()
        current_row, current_column = 0, 0
        row_content = ["", "", "", "", "", ""]

        document = Document(filename)
        for table in document.tables:
            for row in table.rows:
                if current_row > 0:
                    row_content[TIME_COLUMN] = row.cells[0].text
                    row_content[ACTOR_COLUMN] = row.cells[1].text
                    row_content[COMMUNICATION_COLUMN] = row.cells[2].text
                    row_content[NOTES_COLUMN] = row.cells[3].text
                    c.new_row(current_row-1, contents=row_content)
                current_row+=1

        current_column = TIME_COLUMN
        current_row -= 1

        current_row = 0
        c.focus_set()  # move focus to canvas
        c.focus(coding_sheet[current_row][current_column])  # set focus to text item
        c.index(coding_sheet[current_row][current_column], tk.END)
        c.highlight(coding_sheet[current_row][current_column])


def open_file():
    global current_row, current_column, coding_sheet, codingfile
    filename = filedialog.askopenfilename(title="Open Coding", defaultextension=".bg",
                                          filetypes=(("boundary games coding", "*.bg"), ("all files", "*.*")))
    if filename:
        coding_sheet = []  # this and the following erase the previous information
        c.addtag_all("erase")
        c.delete("erase")
        c.baseline = c.create_line(0, -10, 10, -10)
        action_icon.clear()
        link.clear()
        current_row, current_column = 0, 0
        row_content = []
        f = open(filename, mode="r")
        text = ""
        current_row, current_column = 0, 0
        process_values = True
        file_section = 0
        for line in f:
            if line == "##icons##\n":
                file_section = 1
                continue
            if line == "##links##\n":
                file_section = 2
                continue
            if file_section == 0:
                if line == "#EF#\n":
                    row_content.append(text.rstrip())
                    text = ""
                    current_column += 1
                else:
                    text = text+line
                if current_column == number_of_columns:
                    c.new_row(current_row, contents=row_content)
                    row_content = []
                    current_column = 0
                    current_row += 1
            elif file_section == 1:
                if process_values:
                    str_data = line.split()
                    data = [int(float(d)) for d in str_data]
                    rx1, ry1, rx2, ry2 = c.bbox(coding_sheet[data[0]][ACTIONS_COLUMN])
                    delta_y = (ry2-ry1-25)/2  # for centring the icon on y axis
                    item = c.create_image(data[3], ry1 + delta_y, anchor=tk.NW, image=c.ICONS[data[2]], tags="icon",
                                          disabledimage=c.ICONS[data[2]+6])
                    action_icon[item] = action(row=data[0], flow=data[1], action=data[2], delta_x=data[3],
                                               graph_x=data[4], flow_color=data[5], orphan=bool(data[6]))
                    process_values = False
                    note = ""
                else:
                    if line == "#EF#\n":
                        process_values = True
                        action_icon[item].note = note.rstrip()
                    else:
                        note = note + line
            elif file_section == 2:
                str_data = line.split()
                data = [int(float(d)) for d in str_data]

                icon1 = c.identify_icon(data[0], data[1], data[2])
                icon2 = c.identify_icon(data[3], data[4], data[5])
                print("icons to link:", icon1, icon2)
                c.create_link(icon1, icon2)
            codingfile = filename
        f.close()
        root.title("Bounderer Vr. Alfa ::: " + filename)
        current_row = 0
        current_column = TIME_COLUMN

        c.focus_set()  # move focus to canvas
        c.focus(coding_sheet[current_row][current_column])  # set focus to text item
        c.index(coding_sheet[current_row][current_column], tk.END)
        c.highlight(coding_sheet[current_row][current_column])

def save_file():
    global codingfile
    codingfile = filedialog.asksaveasfilename(title="Save Coding As", defaultextension=".bg",
                                            initialfile=codingfile,
                                            filetypes=(("boundary games coding", "*.bg"), ("all files", "*.*")))
    if codingfile:
        f = open(codingfile, mode="w")
        for row in coding_sheet:
            for i in range(number_of_columns):
                if i != ACTIONS_COLUMN:
                    f.write(c.itemcget(row[i], 'text')+"\n")
                    print(c.itemcget(row[0], 'text'))
                f.write("#EF#\n")
        f.write("##icons##"+"\n")
        for icon in action_icon:  # saving the icons
            int_orphan = int(action_icon[icon].orphan)
            f.write(str(action_icon[icon].row) + " " +
                    str(action_icon[icon].flow) + " " +
                    str(action_icon[icon].action) + " " +
                    str(action_icon[icon].delta_x) + " " +
                    str(action_icon[icon].graph_x) + " " +
                    str(action_icon[icon].flow_color) + " " +
                    str(int_orphan) + "\n")
            f.write(action_icon[icon].note + "\n")
            f.write("#EF#\n")
        f.write("##links##"+"\n")
        for lnk in link:  # saving the links
            icon1 = link[lnk][0]
            icon2 = link[lnk][1]
            f.write(str(action_icon[icon1].row) + " " +
                    str(action_icon[icon1].action) + " " +
                    str(action_icon[icon1].delta_x) + " " +
                    str(action_icon[icon2].row) + " " +
                    str(action_icon[icon2].action) + " " +
                    str(action_icon[icon2].delta_x) + " " +
                    "\n")
        f.close()
        root.title("Bounderer Vr. Alfa ::: " + codingfile)


def mytrace():
    print("my trace:")
    print(c.has_focus())
    print("current_row: ", current_row, "current_column:", current_column)
    print(c.bbox(coding_sheet[current_row][current_column]))
    print(action_icon)
    print("links:", link)

def bring_coding_view():
    tc.addtag_all("erase")
    tc.delete("erase")
    tc.leafs.clear()
    tc.t_matrix.clear()
    coding_view.lift()


def bring_graph_view():
    tc.load_data()
    tc.paint()
    graph_view.lift()

def field_value(field):
    return c.itemcget(field, "text")

def write_excel_header(sheet):
    sheet.write(0, 1, "k_row")
    sheet.write(0, 2, "k_icon")
    sheet.write(0, 3, "k_delta_x")
    sheet.write(0, 4, "flow")
    sheet.write(0, 5, "icon_note")
    sheet.write(0, 6, "time")
    sheet.write(0, 7, "actor")
    sheet.write(0, 8, "transcription")
    sheet.write(0, 9, "comment")


def load_row_on_field(row, excelfield):
    excelfield.k_row = int(c.itemcget(coding_sheet[row][MOVE_COLUMN], 'text'))
    excelfield.time = c.itemcget(coding_sheet[row][TIME_COLUMN], 'text')
    excelfield.actor = c.itemcget(coding_sheet[row][ACTOR_COLUMN], 'text')
    excelfield.transcription = c.itemcget(coding_sheet[row][COMMUNICATION_COLUMN], 'text')
    excelfield.comment = c.itemcget(coding_sheet[row][NOTES_COLUMN], 'text')
    excelfield.k_icon = NO_ICON
    excelfield.k_delta_x = NO_ICON
    excelfield.k_flow = UNCONNECTED
    excelfield.icon_note = ""


def row_to_excel(sheet, excelrow, excel_field):
    sheet.write(excelrow, 1, excel_field.k_row)
    sheet.write(excelrow, 2, excel_field.k_icon)
    sheet.write(excelrow, 3, excel_field.k_delta_x)
    sheet.write(excelrow, 4, excel_field.flow)
    sheet.write(excelrow, 5, excel_field.icon_note)
    sheet.write(excelrow, 6, excel_field.time)
    sheet.write(excelrow, 7, excel_field.actor)
    sheet.write(excelrow, 8, excel_field.transcription)
    sheet.write(excelrow, 9, excel_field.comment)

def export_excel():
    filename = filedialog.asksaveasfilename(title="Export Coding to Excel", defaultextension=".xlsx",
                                            filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
    if filename:
        book = xlsxwriter.Workbook(filename)
        sheet = book.add_worksheet()
        write_excel_header(sheet)

        excelrow = 1
        old_excel = excel_field()
        new_excel = excel_field()
        for row in coding_sheet:
            load_row_on_field(int(field_value(row[MOVE_COLUMN])), new_excel)
            new_excel.time = old_excel.time if new_excel.time == "" else new_excel.time
            new_excel.actor = old_excel.actor if new_excel.actor == "" else new_excel.actor
            icons = c.icons_in_row(int(field_value(row[MOVE_COLUMN])))
            for icon in icons:
                new_excel.k_icon = action_icon[icon].action
                new_excel.k_delta_x = action_icon[icon].delta_x
                new_excel.flow = action_icon[icon].flow
                new_excel.icon_note = action_icon[icon].note
                flows = action_icon[icon].flow_parents()
                for link in flows:
                    new_excel.flow = link
                    row_to_excel(sheet, excelrow, new_excel)
                    excelrow += 1
                if not flows:
                    # no links in the icon # extract the flow from the flow in which the icon is
                    row_to_excel(sheet, excelrow, new_excel)
                    excelrow += 1
            if not icons:
                new_excel.k_icon = NO_ICON
                new_excel.flow = UNCONNECTED
                new_excel.k_delta_x = NO_ICON
                row_to_excel(sheet, excelrow, new_excel)
                excelrow+=1
            old_excel = new_excel
        book.close()

def export_graph():
    filename = filedialog.asksaveasfilename(title="Export Structure Tree to GraphML", defaultextension=".GRAPHML",
                                            filetypes=(("GraphML type", "*.GRAPHML"), ("all files", "*.*")))
    if filename:
        f = open(filename, mode="w")
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"\n")
        f.write("    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
        f.write("    xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns\n")
        f.write("     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">\n")
        f.write("    <key id =\"label\" for=\"node\" attr.name=\"label\" attr.type=\"string\" />")
        f.write("  <graph id=\"StructureTree\" edgedefault=\"directed\">\n")
        n_nodes = len(tc.t_matrix[0])
        for i in range(n_nodes):
            f.write("    <node id=\"" + str(i)+ "\">\n")
            f.write("      <data key=\"label\"" + ">Setting" + str(i) + "</data>\n")
            f.write("    </node>\n")
            for j in range(n_nodes):
                if tc.t_matrix[i][j] != 0:
                    f.write("    <edge source=\"" + str(j) + "\" target=\"" + str(i) + "\"/>\n")
        f.write("  </graph>\n")
        f.write("</graphml>\n")

        f.close()

def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to save the file before quitting?"):
        save_file()
        root.destroy()
    else:
        root.destroy()
# Perhaps improve this detecting if the file needs to be saved because there are changes. This requires
# a boolean on all the errors messages (if no error is that there was a change) add to this the delete icon that do not
#  have a separate function for error handling
# the other thing is handle_key with printable keys and enter, backspace to move the boolean.

###################################################################
###################################################################
###################################################################
        
# MAIN PROGRAM


root = tk.Tk()
root.title("Bounderer Vr. Alfa")
root.geometry("1366x400+0+0")
#print("new Screen size:", root.winfo_screenwidth())
#print("screen size y:", root.winfo_screenheight())

graph_view = tk.Frame(root)
coding_view = tk.Frame(root)

graph_view.place(relheight=1, relwidth=1)
coding_view.place(relheight=1, relwidth=1)

default_font = tkf.nametofont("TkDefaultFont")
default_font.configure(size=12)
LINE_SPACE = default_font.metrics("linespace")
# print("LineSpace:", LINE_SPACE)
txt_col = "Row" + (" "*9) + "Time"+(" "*11) +"Actor"+(" "*21) +"Coding"+(" "*90) +"Transcript" + (" "*68) + "Comment"
col_names = tk.Label(coding_view, text=txt_col, background="black", foreground="white", anchor=tk.NW)
scroll = tk.Scrollbar(coding_view, orient=tk.VERTICAL)
c = CodingCanvas(coding_view, bg="white", selectbackground="blue", confine=1,
               scrollregion=(0, 0, 1366, 100000), yscrollcommand=scroll.set)
scroll.config(command=c.yview)
col_names.pack(side=tk.TOP,fill=tk.X, pady=8)
c.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
scroll.pack(side=tk.LEFT, fill=tk.Y)


# fix the problem of scrolling afterwards
tc = TreeCanvas(graph_view, bg="white", selectbackground="blue", confine=1,
               scrollregion=(0, 0, 1366, 1000))
tc.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# print("req size scroll bar:", scroll.winfo_reqwidth())
# print("req size scroll bar:", scroll.winfo_reqheight())


menubar = tk.Menu(root)

menuFile = tk.Menu(menubar, tearoff=0)

menuExport = tk.Menu(menuFile, tearoff=0)
menuExport.add_command(label="PDF", command=print_coding)
menuExport.add_command(label="Excel", command=export_excel)

menuFile.add_command(label="New", command=nothing_to_do)
menuFile.add_command(label="Open", command=open_file)
menuFile.add_command(label="Save As...", command=save_file)
menuFile.add_command(label="Import", command=import_file)
menuFile.add_cascade(label="Export coding", menu=menuExport)
menuFile.add_command(label="Export Tree", command=export_graph)
menuFile.add_command(label="Exit", command=nothing_to_do)



menuView = tk.Menu(menubar, tearoff=0)
menuView.add_command(label="Coding", command=bring_coding_view)
menuView.add_command(label="Tree", command=bring_graph_view)

menuVerify = tk.Menu(menubar, tearoff=0)
menuVerify.add_command(label="Inconsistencies", command=mytrace)
menuVerify.add_command(label="Algo Mas", command=nothing_to_do)

menuSettings = tk.Menu(menubar, tearoff=0)
menuSettings.add_command(label="Colors", command=nothing_to_do)
menuSettings.add_command(label="cells sizes", command=nothing_to_do)
menuSettings.add_command(label="distances", command=nothing_to_do)

menubar.add_cascade(label="File", menu=menuFile)
menubar.add_cascade(label="View", menu=menuView)
# menubar.add_cascade(label="Verify", menu=menuVerify)
# menubar.add_cascade(label="Settings", menu=menuSettings)
menubar.add_command(label="About", command=nothing_to_do)
# menubar.add_command(label="Search", command=nothing_to_do)

codingfile = ""

root.configure(menu=menubar)

# bit to make the program ask for saving the file when quiting
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
