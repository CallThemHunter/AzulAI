import wx
from Engine.Elements.board import Board


class AzulScoringApp(wx.Frame):
    board = Board()
    score = 0

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400, 300))
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.score_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.quote = wx.StaticText(self, label="Player Score: " + str(self.score), pos=(20, 30))
        self.score_sizer.Add(self.quote)

        self.wall_sizer = wx.GridSizer(5, gap=(1, 1))
        self.buttons = []
        for i in range(0, 25):
            self.buttons.append(wx.Button(self, id=i, label=""))
            self.wall_sizer.Add(self.buttons[i], 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.toggleButton, source=self.buttons[i])

        self.SetSizer(self.wall_sizer)
        self.SetAutoLayout(1)
        self.wall_sizer.Fit(self)

        self.main_sizer.Add(self.score_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.main_sizer.Add(self.wall_sizer, 0, wx.CENTER)
        self.Show()

    def toggleButton(self, event: wx.Button):
        id = event.Id
        row = id // 5
        col = id % 5
        score: int
        if event.EventObject.Label == "":
            event.EventObject.Label = "X"
            score = self.board.add_tile(row, col)
        else:
            event.EventObject.Label = ""
            score = self.board.remove_tile(row, col)
        self.quote.Label = "Player Score: " + str(score)
        self.quote.LabelText = "Player Score: " + str(score)


app = wx.App(False)

frame = AzulScoringApp(None, "Azul Scoring App")

frame.Show(True)
app.MainLoop()
