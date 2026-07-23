from ui.main_area.gallery_controller.gallery_controller_signal import get_gallery_controller_signal_instance
from ui.property.custom_metadata_panel.custom_metadata_utils import get_metadata_for_display

class CustomMetadataController():
    def __init__(self):
        # Signal
        self.gallery_controller_signal_instance = get_gallery_controller_signal_instance()
        self.gallery_controller_signal_instance.changed_page_signal.connect(get_metadata_for_display)