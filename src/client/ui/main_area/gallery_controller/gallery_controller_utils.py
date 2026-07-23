from resources.strings.string_resource import SUPPORTED_IMAGE_FORMATS
from services.image_handler.image_handler import pdf2QImage, image2QImage

def render_file(path, viewport_height, viewport_width, task_id, page=1, dpi=72):
    """
    Offloader function to render a file into QImage in workers, supports elimination of stale tasks through task's id.
    Viewport size is provided to render the file at an appropriate size, saving resources.

    :param viewport_height: Height of viewport
    :param viewport_width: Width of viewport
    :param task_id: Task's ID
    :param page: Page to render
    :param dpi: DPI
    """
    qimage = None
    if path.lower().endswith(SUPPORTED_IMAGE_FORMATS):
        qimage = image2QImage(path, viewport_height, viewport_width)
    elif path.lower().endswith(".pdf"):
        qimage = pdf2QImage(path, page, viewport_height, viewport_width, dpi)
    return (qimage, task_id)
    