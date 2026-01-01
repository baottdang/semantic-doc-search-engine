import pikepdf
from resources.strings.string_resource import app_name, version
import os

def get_metadata(path):
    if os.path.isfile(path):
        pdf = pikepdf.open(path)
        docinfo = pdf.docinfo
        docinfo_dict = {str(k): str(v) for k, v in docinfo.items()}
        return docinfo_dict
    else:
        return dict()
    # with pdf.open_metadata() as meta:
    #     meta["xmp : CreatorTool"] = f"{app_name} version {version}"
    #     meta["pdf : Producer"] = "pikepdf"
    #     meta["custom : Insight"] = '{"foo": "bar", "baz": 123}'
