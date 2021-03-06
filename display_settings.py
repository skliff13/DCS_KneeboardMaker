import os


class DisplaySettings:
    def __init__(self):
        self.imageBrightnessAndContrast = (-40., 1.5)   # out = in * contrast + brightness
        self.scale = 3                                # makes all outputs smaller/bigger

        # sizes of fonts and elements
        self.landmarkFontSize = 12
        self.distanceFontSize = 4
        self.connectionMargin = 1
        self.distanceRectangleWidth = 15
        self.distanceRectangleHeight = 10
        self.angleRectangleWidth = 8
        self.angleRectangleHeight = 3.5
        self.connectionWidth = 1.5
        self.slidesColor = 'white'
        self.font_path = 'fonts/calibri.ttf' if os.name == 'nt' else 'font/Ubuntu-B.ttf'

        self.connectionColor = 'orange'      # color of the connection lines
        self.radiusMultiplier = 1.0     # affects all the radii
        self.minConnCenterDistKm = 10   # minimum distance for the connection info to be drawn
        self.export_upsize = 2
        self.export_interpolation_order = 3

        # scaling operations
        scale = self.scale
        self.landmarkFontSize = int(round(self.landmarkFontSize * scale))
        self.distanceFontSize = int(round(self.distanceFontSize * scale))
        self.connectionMargin = int(round(self.connectionMargin * scale))
        self.distanceRectangleWidth = int(round(self.distanceRectangleWidth * scale))
        self.distanceRectangleHeight = int(round(self.distanceRectangleHeight * scale))
        self.angleRectangleWidth = int(round(self.angleRectangleWidth * scale))
        self.angleRectangleHeight = int(round(self.angleRectangleHeight * scale))
        self.connectionWidth = int(self.connectionWidth * scale)
        # self.radiusMultiplier = self.radiusMultiplier * scale

