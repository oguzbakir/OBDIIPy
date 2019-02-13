# /***************************************************************************/
# /* ELM327 OBDII CAN BUS Diagnostic Software.                               */
# /*                                                                         */
# /*                                                                         */
# /* Class: Display                                                          */
# /* Look after a hierarchy of objects to be displayed.                      */
# /***************************************************************************/


import os
import subprocess
import pygame
import Visual
import Button
import Gadget
import Plot

DEBUG = "OFF"


class Display:
    # List of meters to be displayed on the Meters tab.
    Meters = {}
    Meters["NAME"] = "METERS"

    # List of frame data to be displayed on the frame data tab.
    FrameData = {}
    FrameData["NAME"] = "FRAME_DATA"

    # List of freeze frame data to be displayed on the freeze frame data tab.
    FreezeFrameData = {}
    FreezeFrameData["NAME"] = "FREEZE_FRAME_DATA"

    # List of plots to be displayed on the plots tab.
    Plots = {}
    Plots["NAME"] = "PLOTS"

    # List of trouble code info to be displayed on the vehicle info tab.
    TroubleInfo = {}
    TroubleInfo["NAME"] = "TROUBLE_INFO"

    # List of vehicle info to be displayed on the vehicle info tab.
    VehicleInfo = {}
    VehicleInfo["NAME"] = "VEHICLE_INFO"

    # List of ELM327 info to be displayed on the ELM327 info tab.
    ELM327Info = {}
    ELM327Info["NAME"] = "ELM327_INFO"

    def __init__(self):
        # Initialise PyGame environment for graphics and sound.
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        res = subprocess.run("./activescreen", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if (res.returncode == 0):
            wh = res.stdout.split(b' ')
            screenw = int(wh[0])
            screenh = int(wh[1])
            self.ThisSurface = pygame.display.set_mode((screenw, screenh), pygame.NOFRAME)
        else:
            print("No screens detected")
            exit(1)
        #self.ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        # Hide mouse pointer, using a touch screen for click events.
        #		pygame.mouse.set_visible(False)

        # Get the dimensions of the surface to draw the visual object onto.
        (self.DisplayXLen, self.DisplayYLen) = pygame.Surface.get_size(self.ThisSurface)
        if DEBUG == "ON":
            print("DISPLAY: " + str(self.DisplayXLen) + " x " + str(self.DisplayYLen))

        self.SurfaceXLen = pygame.display.Info().current_w
        self.SurfaceYLen = pygame.display.Info().current_h

        # Scale gadget sizes to a preportion of the display surface.
        self.GadgetWidth = int(self.SurfaceXLen / 3)
        self.GadgetHeight = int((self.SurfaceYLen - Visual.BUTTON_HEIGHT) / 1.4)
        self.ButtonWidth = int(self.SurfaceXLen / 12)

        # Define the buttons to be displayed on the background.
        self.Buttons = {
            "METERS": Button.Button(self.ThisSurface, "METERS", Visual.PRESS_LATCH, 2 * self.ButtonWidth, 0,
                                    self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Meters.png"),
            "FRAME": Button.Button(self.ThisSurface, "FRAME", Visual.PRESS_LATCH, 3 * self.ButtonWidth, 0,
                                   self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Frame.png"),
            "FREEZE": Button.Button(self.ThisSurface, "FREEZE", Visual.PRESS_LATCH, 4 * self.ButtonWidth, 0,
                                    self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/FreezeFrame.png"),
            "PLOTS": Button.Button(self.ThisSurface, "PLOTS", Visual.PRESS_LATCH, 5 * self.ButtonWidth, 0,
                                   self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Plots.png"),
            "TROUBLE": Button.Button(self.ThisSurface, "TROUBLE", Visual.PRESS_LATCH, 6 * self.ButtonWidth, 0,
                                     self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Trouble.png"),
            "VEHICLE": Button.Button(self.ThisSurface, "VEHICLE", Visual.PRESS_LATCH, 7 * self.ButtonWidth, 0,
                                     self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Vehicle.png"),
            "ELM327": Button.Button(self.ThisSurface, "ELM327", Visual.PRESS_LATCH, 8 * self.ButtonWidth, 0,
                                    self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/OBDII.png"),
            "BUSY": Button.Button(self.ThisSurface, "BUSY", Visual.PRESS_DOWN, self.DisplayXLen - 2 * self.ButtonWidth,
                                  0, self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Busy.png"),
            "EXIT": Button.Button(self.ThisSurface, "EXIT", Visual.PRESS_DOWN, self.DisplayXLen - self.ButtonWidth, 0,
                                  self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Exit.png"),

            "MIL": Button.Button(self.ThisSurface, "MIL", Visual.PRESS_DOWN, 0, Visual.BUTTON_HEIGHT, self.ButtonWidth,
                                 Visual.BUTTON_HEIGHT, "IMAGE:icons/MIL_Off.png", DownText="IMAGE:icons/MIL_On.png"),
            "SAVE": Button.Button(self.ThisSurface, "SAVE", Visual.PRESS_DOWN, self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                  self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Save.png"),
            "PRINT": Button.Button(self.ThisSurface, "PRINT", Visual.PRESS_DOWN, 2 * self.ButtonWidth,
                                   Visual.BUTTON_HEIGHT, self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                   "IMAGE:icons/Print.png"),
            "DATE": Button.Button(self.ThisSurface, "DATE", Visual.PRESS_NONE, 4 * self.ButtonWidth,
                                  Visual.BUTTON_HEIGHT, 2 * self.ButtonWidth, Visual.BUTTON_HEIGHT, "DATE"),
            "TIME": Button.Button(self.ThisSurface, "TIME", Visual.PRESS_NONE, 6 * self.ButtonWidth,
                                  Visual.BUTTON_HEIGHT, 2 * self.ButtonWidth, Visual.BUTTON_HEIGHT, "TIME"),
        }

        # Define the meters tab area for the display.
        self.Meters["LOCK"] = Button.Button(self.ThisSurface, "LOCK", Visual.PRESS_TOGGLE, 0, 0, self.ButtonWidth,
                                            Visual.BUTTON_HEIGHT, "IMAGE:icons/Lock_Off.png",
                                            DownText="IMAGE:icons/Lock_On.png")
        self.Meters["ADD"] = Button.Button(self.ThisSurface, "ADD", Visual.PRESS_DOWN, self.ButtonWidth, 0,
                                           self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Add.png")
        self.Meters["GO_STOP"] = Button.Button(self.ThisSurface, "GO_STOP", Visual.PRESS_TOGGLE,
                                               self.DisplayXLen - 3 * self.ButtonWidth, 0, self.ButtonWidth,
                                               Visual.BUTTON_HEIGHT, "IMAGE:icons/Go.png",
                                               DownText="IMAGE:icons/Stop.png")

        # Define the frame data tab area for the display.
        self.FrameData["INFO"] = Button.Button(self.ThisSurface, "INFO", Visual.PRESS_NONE, 0, 2 * Visual.BUTTON_HEIGHT,
                                               self.DisplayXLen, self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "",
                                               Visual.ALIGN_TEXT_LEFT)
        self.FrameData["RELOAD"] = Button.Button(self.ThisSurface, "RELOAD", Visual.PRESS_DOWN,
                                                 self.DisplayXLen - self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                 self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Reload.png")

        # Define the freeze frame data tab area for the display.
        self.FreezeFrameData["INFO"] = Button.Button(self.ThisSurface, "INFO", Visual.PRESS_NONE, 0,
                                                     2 * Visual.BUTTON_HEIGHT, self.DisplayXLen,
                                                     self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "",
                                                     Visual.ALIGN_TEXT_LEFT)
        self.FreezeFrameData["RELOAD_FREEZE"] = Button.Button(self.ThisSurface, "RELOAD_FREEZE", Visual.PRESS_DOWN,
                                                              self.DisplayXLen - self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                              self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                              "IMAGE:icons/Reload.png")

        # Define the plot tab area for the display.
        self.Plots["PLOT"] = Plot.Plot(self.ThisSurface, "PLOT", Visual.PRESS_NONE, 0, 2 * Visual.BUTTON_HEIGHT,
                                       self.DisplayXLen, self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "")
        self.Plots["GO_STOP"] = Button.Button(self.ThisSurface, "GO_STOP", Visual.PRESS_TOGGLE,
                                              self.DisplayXLen - 3 * self.ButtonWidth, 0, self.ButtonWidth,
                                              Visual.BUTTON_HEIGHT, "IMAGE:icons/Go.png",
                                              DownText="IMAGE:icons/Stop.png")
        self.Plots["PLOT_1"] = Button.Button(self.ThisSurface, "PLOT_1", Visual.PRESS_DOWN,
                                             self.DisplayXLen - 4 * self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                             self.ButtonWidth, Visual.BUTTON_HEIGHT, "[1]")
        self.Plots["PLOT_2"] = Button.Button(self.ThisSurface, "PLOT_2", Visual.PRESS_DOWN,
                                             self.DisplayXLen - 3 * self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                             self.ButtonWidth, Visual.BUTTON_HEIGHT, "[2]")
        self.Plots["PLOT_3"] = Button.Button(self.ThisSurface, "PLOT_3", Visual.PRESS_DOWN,
                                             self.DisplayXLen - 2 * self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                             self.ButtonWidth, Visual.BUTTON_HEIGHT, "[3]")
        self.Plots["RESET"] = Button.Button(self.ThisSurface, "RESET", Visual.PRESS_DOWN,
                                            self.DisplayXLen - self.ButtonWidth, Visual.BUTTON_HEIGHT, self.ButtonWidth,
                                            Visual.BUTTON_HEIGHT, "IMAGE:icons/Reset.png")

        # Define the trouble tab area for the display.
        self.TroubleInfo["INFO"] = Button.Button(self.ThisSurface, "INFO", Visual.PRESS_NONE, 0,
                                                 2 * Visual.BUTTON_HEIGHT, self.DisplayXLen,
                                                 self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "",
                                                 Visual.ALIGN_TEXT_LEFT)
        self.TroubleInfo["REFRESH"] = Button.Button(self.ThisSurface, "REFRESH", Visual.PRESS_DOWN,
                                                    9 * self.ButtonWidth, Visual.BUTTON_HEIGHT, self.ButtonWidth,
                                                    Visual.BUTTON_HEIGHT, "IMAGE:icons/Refresh.png")
        self.TroubleInfo["CLEAR"] = Button.Button(self.ThisSurface, "CLEAR", Visual.PRESS_DOWN,
                                                  self.DisplayXLen - self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                  self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Clear.png")

        # Define the vehicle tab area for the display.
        self.VehicleInfo["INFO"] = Button.Button(self.ThisSurface, "INFO", Visual.PRESS_NONE, 0,
                                                 2 * Visual.BUTTON_HEIGHT, self.DisplayXLen,
                                                 self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "",
                                                 Visual.ALIGN_TEXT_LEFT)

        # Define the ELM327 tab area for the display.
        self.ELM327Info["INFO"] = Button.Button(self.ThisSurface, "INFO", Visual.PRESS_NONE, 0,
                                                2 * Visual.BUTTON_HEIGHT, self.DisplayXLen,
                                                self.DisplayYLen - 2 * Visual.BUTTON_HEIGHT, "", Visual.ALIGN_TEXT_LEFT)
        self.ELM327Info["CONFIG"] = Button.Button(self.ThisSurface, "CONFIG", Visual.PRESS_DOWN, 9 * self.ButtonWidth,
                                                  Visual.BUTTON_HEIGHT, self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                  "IMAGE:icons/Config.png")
        self.ELM327Info["CONNECT"] = Button.Button(self.ThisSurface, "CONNECT", Visual.PRESS_DOWN,
                                                   self.DisplayXLen - self.ButtonWidth, Visual.BUTTON_HEIGHT,
                                                   self.ButtonWidth, Visual.BUTTON_HEIGHT, "IMAGE:icons/Connect.png")

        # Currently selected tab, default meters.
        self.CurrentTab = self.ELM327Info
        self.Buttons["ELM327"].SetDown(True)
        self.Buttons["BUSY"].SetVisible(False)

    # /****************************************************/
    # /* Perform required tasks when closing the display. */
    # /****************************************************/
    def Close(self):
        # Show mouse pointer before ending application.
        pygame.mouse.set_visible(True)

    # /************************************/
    # /* Return the width of the display. */
    # /************************************/
    def GetDisplayWidth(self):
        return self.DisplayXLen

    # /*************************************/
    # /* Return the height of the display. */
    # /*************************************/
    def GetDisplayHeight(self):
        return self.DisplayYLen

    # /*******************************************/
    # /* Load gadgets onto meters tab from disk. */
    # /*******************************************/
    def LoadMetersTab(self, ValidPIDs):
        try:
            if os.path.isfile("config/meters.cfg"):
                File = open("config/meters.cfg", 'r')
                xPos = 0
                Name = ""
                TextLine = "."
                while TextLine != "":
                    TextLine = File.readline()
                    TextLine = TextLine.replace("\n", "")
                    TextElements = TextLine.split('|')
                    for ThisElement in TextElements:
                        if ThisElement[:5] == "Name=":
                            Name = str(ThisElement[5:])
                            self.Meters[Name] = Gadget.Gadget(self.ThisSurface, Name, Visual.PRESS_NONE, 0,
                                                              2 * Visual.BUTTON_HEIGHT, self.GadgetWidth,
                                                              self.GadgetHeight, "NEW")
                        elif ThisElement[:5] == "xPos=":
                            xPos = float(ThisElement[5:])
                        elif ThisElement[:5] == "yPos=":
                            self.Meters[Name].SetPos(xPos, float(ThisElement[5:]))
                        elif ThisElement[:6] == "Style=":
                            self.Meters[Name].SetStyle(float(ThisElement[6:]))
                        elif ThisElement[:4] == "PID=":
                            ThisPID = str(ThisElement[4:])
                            ThisPidDescription = ""
                            if ThisPID in ValidPIDs:
                                ThisPidDescription = ValidPIDs[ThisPID]
                            self.Meters[Name].SetPID(ThisPID, ThisPidDescription)
                File.close()

                # Hide buttons on meteres, default locked.
                self.Meters["LOCK"].SetDown(True)
                self.Meters["ADD"].SetVisible(False)
                for ThisGadget in self.Meters:
                    if type(self.Meters[ThisGadget]) is not str and type(self.Meters[ThisGadget]) is not Button.Button:
                        for ThisButton in self.Meters[ThisGadget].Buttons:
                            self.Meters[ThisGadget].Buttons[ThisButton].SetVisible(False)
        except:
            # On fail remove all loaded gadgets.
            for ThisGadget in self.Meters:
                if type(self.Meters[ThisGadget]) is not str and type(self.Meters[ThisGadget]) is not Button.Button:
                    self.Meters.pop([ThisGadget], None)

    # /*****************************************/
    # /* Save gadgets from meters tab to disk. */
    # /*****************************************/
    def SaveMetersTab(self):
        if len(self.Meters) > 1:
            File = open("config/meters.cfg", 'w')
            for ThisGadget in self.Meters:
                if type(self.Meters[ThisGadget]) is not str and type(self.Meters[ThisGadget]) is not Button.Button:
                    Data = "Name=" + str(self.Meters[ThisGadget].GetName())
                    Data += "|xPos=" + str(self.Meters[ThisGadget].GetXPos())
                    Data += "|yPos=" + str(self.Meters[ThisGadget].GetYPos())
                    Data += "|Style=" + str(self.Meters[ThisGadget].GetStyle())
                    Data += "|PID=" + str(self.Meters[ThisGadget].GetPID())
                    File.write(Data + "\n")
            File.close()

    # /***********************************************************/
    # /* Check if an event occurred on the display. Perform any  */
    # /* required actions and let the caller know if the display */
    # /* area was touched.                                       */
    # /***********************************************************/
    def IsEvent(self, EventType, xPos, yPos, PointerButton, xOffset=0, yOffset=0):
        Result = False

        # Check for gadget touches on the currently selected tab only, in the correct Z order.
        for ThisVisual in reversed(Visual.VisualZOrder):
            for ThisGadget in self.CurrentTab:
                if type(self.CurrentTab[ThisGadget]) is not str and self.CurrentTab[ThisGadget] == ThisVisual:
                    Result = self.CurrentTab[ThisGadget].IsEvent(EventType, xPos, yPos, PointerButton, xOffset, yOffset)
                    if Result != False:
                        if EventType == Visual.EVENT_MOUSE_DOWN:
                            # When a gadget is clicked, bring it to the front of other gadgets.
                            TopGadgetIndex = len(Visual.VisualZOrder) - 1
                            ThisGadgetIndex= Visual.VisualZOrder.index(self.CurrentTab[ThisGadget])
                            Visual.VisualZOrder[TopGadgetIndex] = Visual.VisualZOrder[ThisGadgetIndex]
                            for MoveGadgetIndex in range(ThisGadgetIndex, TopGadgetIndex):
                                Visual.VisualZOrder[MoveGadgetIndex] = Visual.VisualZOrder[MoveGadgetIndex + 1]
                            # If a gadget close button was pressed, remove the gadget.
                            if DEBUG == "ON":
                                print(str(Result))
                            if Result["BUTTON"] == "CLOSE":
                                self.CurrentTab.pop(ThisGadget, None)
                        break
            if Result != False:
                break

        # If no gadgets were touched, check for button touches.
        if Result == False:
            for ThisButton in self.Buttons:
                Result = self.Buttons[ThisButton].IsEvent(EventType, xPos, yPos, PointerButton, xOffset, yOffset)
                if Result != False:
                    if EventType == Visual.EVENT_MOUSE_DOWN:
                        # Switch tabs when a tab button is pressed.
                        if Result["BUTTON"] == "METERS":
                            self.CurrentTab = self.Meters
                        elif Result["BUTTON"] == "FRAME":
                            self.CurrentTab = self.FrameData
                        elif Result["BUTTON"] == "FREEZE":
                            self.CurrentTab = self.FreezeFrameData
                        elif Result["BUTTON"] == "PLOTS":
                            self.CurrentTab = self.Plots
                        elif Result["BUTTON"] == "TROUBLE" or Result["BUTTON"] == "MIL":
                            self.CurrentTab = self.TroubleInfo
                        elif Result["BUTTON"] == "VEHICLE":
                            self.CurrentTab = self.VehicleInfo
                        elif Result["BUTTON"] == "ELM327":
                            self.CurrentTab = self.ELM327Info
                    break

            # If a button was touched, highlight only the current tab.
            if Result != False:
                if self.CurrentTab != self.Meters:
                    self.Buttons["METERS"].SetDown(False)
                if self.CurrentTab != self.FrameData:
                    self.Buttons["FRAME"].SetDown(False)
                if self.CurrentTab != self.FreezeFrameData:
                    self.Buttons["FREEZE"].SetDown(False)
                if self.CurrentTab != self.Plots:
                    self.Buttons["PLOTS"].SetDown(False)
                if self.CurrentTab != self.TroubleInfo:
                    self.Buttons["TROUBLE"].SetDown(False)
                if self.CurrentTab != self.VehicleInfo:
                    self.Buttons["VEHICLE"].SetDown(False)
                if self.CurrentTab != self.ELM327Info:
                    self.Buttons["ELM327"].SetDown(False)

        return Result

    # /***********************************************/
    # /* Set the text on the gadget or button of the */
    # /* specified name on the specified tab.        */
    # /***********************************************/
    def SetVisualText(self, Tab, VisualName, NewText, Append=False, DataValue=0):
        for ThisGadget in Tab:
            if type(Tab[ThisGadget]) is not str:
                if Tab[ThisGadget].GetName() == VisualName:
                    Tab[ThisGadget].SetText(NewText, Append, DataValue)

        for ThisButton in self.Buttons:
            if self.Buttons[ThisButton].GetName() == VisualName:
                self.Buttons[ThisButton].SetText(NewText, Append, DataValue)

    # /*****************************************************/
    # /* Draw buttons and gadgets on the provided surface. */
    # /*****************************************************/
    def Display(self):
        # Erase the surface.
        self.ThisSurface.fill((0x00, 0x00, 0x00))

        # Display all buttons on the background.
        for ThisButton in self.Buttons:
            self.Buttons[ThisButton].Display(self.ThisSurface)

        # Display all gadgets on the selected tab in the correct Z order.
        for ThisVisual in Visual.VisualZOrder:
            for ThisGadget in self.CurrentTab:
                if type(self.CurrentTab[ThisGadget]) is not str and self.CurrentTab[ThisGadget] == ThisVisual:
                    self.CurrentTab[ThisGadget].Display(self.ThisSurface)

        # Update the display.
        pygame.display.flip()
