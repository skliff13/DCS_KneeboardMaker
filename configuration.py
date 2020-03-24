
class Configuration:
    def __init__(self):
        # paths to input files
        self.path_to_map = 'input_LFDM_server/stitched.jpg'
        self.path_to_landmarks = 'input_LFDM_server/landmarks.txt'
        self.path_to_connections = 'input_LFDM_server/connections_all.txt'

        # where to store output files
        self.output_dir = 'out_LFDM'

        # input image scale, kilometers per one pixel
        self.scaleKilometersPerPixel = 0.06425
        self.draw_landmarks = False
        self.draw_connections = True

        # kneeboard slides size and positions
        self.slide_extraction_size = (683, 1024)
        self.slide_topleft_XYs = [[93, 117]]
        self.slide_output_size = (683, 1024)
