
class Configuration:
    def __init__(self):
        # paths to input files
        self.path_to_map = 'input_BurningSkies_Normandy/stitched.png'
        self.path_to_landmarks = 'input_BurningSkies_Normandy/landmarks.txt'
        self.path_to_connections = 'input_BurningSkies_Normandy/connections_all.txt'

        # where to store output files
        self.output_dir = 'out_BS_Normandy_slides'

        # input image scale, kilometers per one pixel
        self.scaleKilometersPerPixel = 0.04846

        # kneeboard slides size and positions
        self.slide_extraction_size = (1800, 2700)
        self.slide_topleft_XYs = [[93, 117], [1313, 117], [2457, 117], [3537, 117]]
        self.slide_output_size = (683, 1024)
