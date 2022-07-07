from PyQt5.QtWidgets import QWidget, QVBoxLayout

from napari_allencell_annotator.controller.images_controller import ImagesController

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
import napari


class MainController(QWidget):
    """
        A class used to combine/communicate between AnnotatorController and ViewController.

        Methods
        -------
        start_annotating()
            Enters annotating mode if files have been added.
        next_image()
            Moves to the next image for annotating.
        prev_image()
            Moves to the previous image for annotating.
        """

    def __init__(self):
        super().__init__()
        self.napari = napari.Viewer()
        self.layout = QVBoxLayout()
        self.images = ImagesController(self.napari)
        self.annots = AnnotatorController(self.napari)
        self.layout.addWidget(self.images.view, stretch=1)
        self.layout.addWidget(self.annots.view, stretch=2)
        self.setLayout(self.layout)
        self.show()
        self.napari.window.add_dock_widget(self, area="right")
        self._connect_slots()

    def _connect_slots(self):
        """Connects annotator view buttons start, next, and prev to slots"""
        self.annots.view.start_btn.clicked.connect(self.start_annotating)
        self.annots.view.next_btn.clicked.connect(self.next_image)
        self.annots.view.prev_btn.clicked.connect(self.prev_image)


    def start_annotating(self):
        """
        Enter annotating mode if files have been added.

        Alerts user if there are no files added. Hides the file
        viewer and starts the annotating process.
        """
        if self.images.get_num_files() is None or self.images.get_num_files() < 1:
            self.images.view.alert("Can't Annotate Without Adding Images")
        else:
            self.layout.removeWidget(self.images.view)
            self.images.view.hide()
            self.images.start_annotating()
            self.annots.start_annotating(self.images.get_num_files())
            self.annots.set_curr_img(self.images.curr_img_dict())

    def next_image(self):
        """
        Move to the next image for annotating.

        If the last image is being annotated, write to csv. If the second
        image is being annotated, enable previous button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()['File Path'])
        if self.annots.view.next_btn.text() == "Save and Export":
            self.annots.write_to_csv()
        else:
            self.images.next_img()
            self.annots.set_curr_img(self.images.curr_img_dict())
            if self.images.curr_img_dict()["Row"] == "1":
                self.annots.view.prev_btn.setEnabled(True)

    def prev_image(self):
        """
        Move to the previous image for annotating.

        If the first image is being annotated, disable button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()['File Path'])
        self.images.prev_img()
        self.annots.set_curr_img(self.images.curr_img_dict())
        if self.images.curr_img_dict()["Row"] == "0":
            self.annots.view.prev_btn.setEnabled(False)
