================
Block Device EFI
================

This provides a block-device configuration for the ``vm`` element to
get a single-partition disk suitable for EFI booting.

Based on upstream DIB element block-device-efi, the only modification
being the root fs type from hardcoded 'ext4' to relying on FS_TYPE.

Note on x86 this provides the extra `BIOS boot partition
<https://en.wikipedia.org/wiki/BIOS_boot_partition>`__ and a EFI boot
partition for maximum compatability.

