
class DisplaySettings:
    def __init__(self):
        self.outputDPI = 600                            # Digits Per Inch, controls resolution of the output large image
        self.imageBrightnessAndContrast = (-40., 1.5)   # out = in * contrast + brightness
        self.scale = 0.7                                # makes all outputs smaller/bigger

        # sizes of fonts and elements
        self.landmarkFontSize = 12
        self.distanceFontSize = 6
        self.connectionMargin = 20
        self.distanceRectangleWidth = 80
        self.distanceRectangleHeight = 45
        self.angleRectangleWidth = 60
        self.angleRectangleHeight = 23
        self.connectionWidth = 1.5

        self.connectionColor = 'y'      # color of the connection lines
        self.radiusMultiplier = 1.0     # affects all the radii
        self.minConnCenterDistKm = 10   # minimum distance for the connection info to be drawn

        # scaling operations
        scale = self.scale
        self.landmarkFontSize = round(self.landmarkFontSize * scale)
        self.distanceFontSize = round(self.distanceFontSize * scale)
        self.connectionMargin = round(self.connectionMargin * scale)
        self.distanceRectangleWidth = round(self.distanceRectangleWidth * scale)
        self.distanceRectangleHeight = round(self.distanceRectangleHeight * scale)
        self.angleRectangleWidth = round(self.angleRectangleWidth * scale)
        self.angleRectangleHeight = round(self.angleRectangleHeight * scale)
        self.connectionWidth = self.connectionWidth * scale
        self.radiusMultiplier = self.radiusMultiplier * scale

