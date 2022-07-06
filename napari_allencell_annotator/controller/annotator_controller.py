import json
from napari_allencell_annotator.view.annotator_view import AnnotatorView, AnnotatorViewMode
from napari_allencell_annotator.util.directories import Directories
import napari

from typing import Dict, List
import csv


class AnnotatorController:
    """
    A class used to control the model and view for annotations.

    Inputs
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used

    Methods
    -------
    start_annotating(num_images : int)
        Changes annotation view to annotating mode, opens a .csv file to write to.

    set_curr_img(curr_img : Dict[str, str])
        Sets the current image for view and changes next button if annotating the last image.

    write_image_csv(prev_img: Dict[str, str])
        Writes the outgoing images annotations and data to the csv.


    write_to_csv()
        Closes the csv writer.
    """

    def __init__(self, viewer: napari.Viewer):
        # 1 annotation
        path = str(Directories.get_assets_dir() / "sample3.json")
        # 4 annotations
        #path = str(Directories.get_assets_dir() / "sample.json")
        # 8 annotations
        # path: str = str(Directories.get_assets_dir() / "sample2.json")
        self.annot_data: Dict[str, Dict[str, str]] = json.load(open(path))
        # open in add mode
        # self.view = AnnotatorView(napari.Viewer(), data)
        # open in view mode
        self.view: AnnotatorView = AnnotatorView(viewer, self, mode=AnnotatorViewMode.VIEW)
        self.view.render_annotations(self.annot_data)
        self.view.show()
        self.curr_img: Dict[str, str] = None
        # TODO: write to file only once, store annotations in dict

        self.annotation_dict: Dict[str, (List[str], List[str])] = {}

    def start_annotating(self, num_images: int):
        """
        Change annotation view to annotating mode and open a .csv file to write to.

        Parameters
        ----------
        num_images : int
            The total number of images to be annotated.
        """

        self.view.set_num_images(num_images)
        self.view.set_mode(mode=AnnotatorViewMode.ANNOTATE)
        self.view.make_annots_editable()

    def set_curr_img(self, curr_img: Dict[str, str]):
        """
        Set the current image and changes next button if annotating the last image.

        Parameters
        ----------
        curr_img : Dict[str, str]
            The current image file path, name, fms info, and row.
        """
        self.curr_img = curr_img
        path = curr_img["File Path"]
        if path not in self.annotation_dict.keys():
            self.annotation_dict.update(
                {path: [curr_img["File Name"], curr_img["FMS"]]})
            self.view.render_default_values()
        else:
            self.view.render_values(self.annotation_dict[path][2::])
        self.view.set_curr_index(curr_img["Row"])
        if int(curr_img["Row"]) == self.view.num_images - 1:
            self.view.next_btn.setText("Save and Export")

    def record_annotations(self, prev_img: Dict[str, str]):
        # filename, filepath, fms, annots
        lst = self.view.get_curr_annots()
        self.annotation_dict[prev_img['File Path']].extend(lst)

    def write_to_csv(self):
        file = open('test.csv', 'w')
        writer = csv.writer(file)
        header: List[str] = ["File Name", "File Path", "FMS"]
        for name in self.view.annots_order:
            header.append(name)
        writer.writerow(header)
        for key, val in self.annotation_dict.items():
            line: List[str] = [key] + val
            writer.writerow(line)
        file.close()
