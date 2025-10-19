#!/bin/bash

# Build array of NTFS entries
mapfile -t NTFS_ENTRIES < <(lsblk -o NAME,LABEL,FSTYPE,SIZE -nr | awk '$3 == "ntfs" {
    label = ($2 == "" ? "NoLabel" : $2)
    printf "/dev/%s - %s (%s)\n", $1, label, $4
}')

# If no NTFS drives found
if [ ${#NTFS_ENTRIES[@]} -eq 0 ]; then
    zenity --error --text="No NTFS partitions found."
    exit 1
fi

# Use zenity with proper array syntax
SELECTED=$(zenity --list \
  --title="Select NTFS Partition to Fix" \
  --column="NTFS Partitions" \
  "${NTFS_ENTRIES[@]}" \
  --height=400 \
  --width=500)

# If user cancels
[[ -z "$SELECTED" ]] && exit 1

# Extract device (e.g., /dev/sda2)
DEVICE=$(echo "$SELECTED" | awk '{print $1}')

# Confirm
zenity --question --text="Are you sure you want to run ntfsfix on:\n\n$SELECTED?"

[[ $? -ne 0 ]] && exit 1

NTFSFIX=$(command -v ntfsfix)
gnome-terminal -- bash -c "sudo $NTFSFIX $DEVICE; echo; echo 'Done. Press any key to close...'; read -n 1"


