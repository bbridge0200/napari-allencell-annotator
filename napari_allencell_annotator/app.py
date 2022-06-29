import sys

from PyQt5.QtWidgets import QApplication

from napari_allencell_annotator.controller.images_controller import ImagesController
from napari_allencell_annotator.controller.annotator_controller import AnnotatorController

class App(QApplication):
    """
    A class used to initialize the image annotator controller.
    """
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        MainController()



if __name__ == '__main__':
    app = App(sys.argv)

    sys.exit(app.exec_())

