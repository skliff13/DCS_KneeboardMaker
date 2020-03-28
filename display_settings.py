
class DisplaySettings:
    def __init__(self):
        self.imageBrightnessAndContrast = (-40., 1.5)   # out = in * contrast + brightness
        self.scale = 4                                # makes all outputs smaller/bigger

        # sizes of fonts and elements
        self.landmarkFontSize = 12
        self.distanceFontSize = 4
        self.connectionMargin = 5
        self.distanceRectangleWidth = 20
        self.distanceRectangleHeight = 10
        self.angleRectangleWidth = 12
        self.angleRectangleHeight = 5
        self.connectionWidth = 1.5

        self.connectionColor = 'gold'      # color of the connection lines
        self.radiusMultiplier = 1.0     # affects all the radii
        self.minConnCenterDistKm = 10   # minimum distance for the connection info to be drawn

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

