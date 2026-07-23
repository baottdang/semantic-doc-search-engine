from services.threads.taskqueue import get_task_queue_instance
from ui.property.default_metadata_panel.default_metadata_signal import get_default_metadata_signal_instance
from services.metadata.metadata import get_metadata

def get_metadata_for_display(path):
    # Load metadata in background (Not necessary since the process is blazing fast but good practice)
    tq = get_task_queue_instance()
    future = tq.submit(lambda : get_metadata(path))
    future.add_done_callback(done_get_query)

def done_get_query(future):
    default_metadata_panel_signal_instance = get_default_metadata_signal_instance()
    try:
        metadata_dict = future.result()
        default_metadata_panel_signal_instance.metadata_returned_signal.emit(metadata_dict)
    except Exception as e:
        default_metadata_panel_signal_instance.metadata_returned_signal.emit(dict())
