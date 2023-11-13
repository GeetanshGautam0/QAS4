from . import qa_file_std
from . import qa_theme_file as ThemeFile


# Create a global IO history manager. Assign it to a new file IO manager.
#   This FileIOManager will be passed onto each "standard" file format.
#   This ensures that the same IOHistory is shared between all file types.
global_io_history_manager = qa_file_std.IOHistory()
file_io_manager = qa_file_std.FileIO(global_io_history_manager)

# Set the same instance of FileIOManager as each individual script's FIOM.
ThemeFile.file_io_manager = file_io_manager
