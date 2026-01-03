from services.threads.taskqueue import get_task_queue_instance
from services.metadata.metadata import get_custom_xmp_metadata
from ui.property.custom_metadata_panel.custom_metadata_signal import get_custom_metadata_signal_instance
import json

def get_metadata_for_display(path):
    tq = get_task_queue_instance()
    future = tq.submit(lambda : get_custom_xmp_metadata(path))
    future.add_done_callback(done_get_xmp_metadata)

def done_get_xmp_metadata(future):
    custom_metadata_signal_instance = get_custom_metadata_signal_instance()
    try:
        metadata = json.loads(future.result()) # Returns a dict
        custom_metadata_signal_instance.done_get_xmp_metadata_signal.emit(metadata)
    except Exception as e:
        import traceback
        traceback.print_exc()
        custom_metadata_signal_instance.done_get_xmp_metadata_signal.emit(dict())
        

