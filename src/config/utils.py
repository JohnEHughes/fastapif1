



# def combine_metadata():
#     """This is essentially my hack to prevent having
#     to do a bunch of imports across lots of files
#     to register the models."""
#     from sqlalchemy import MetaData

#     from src.models import SUPPORTED_MODELS

#     m = MetaData()
#     for model in SUPPORTED_MODELS:
#         for t in model.metadata.tables.values():
#             t.tometadata(m)
#     return m