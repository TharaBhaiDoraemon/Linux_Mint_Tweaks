# Fix NTFS Partition Nemo Action

This Nemo action allows you to run `ntfsfix` on an NTFS partition directly from the Nemo file manager.

## Installation

1.  Copy the `fix-ntfs.nemo_action` file to `~/.local/share/nemo/actions/`.
2.  Restart Nemo.

## Usage

1.  Open Nemo and navigate to the directory where your NTFS partition is mounted.
2.  Right-click on the directory.
3.  Select "Fix NTFS Partition" from the context menu.

This will execute the `fix_ntfs_gui.sh` script, which in turn runs `ntfsfix` on the selected partition.
