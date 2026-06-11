# -------------------------------------------------------
# Step 1 — Main function to check CUDA availability and print device information.
# -------------------------------------------------------
"""
This module, `check_cuda.py`, provides functionality to determine whether CUDA is available on the system. If CUDA is present, it retrieves and prints detailed information about the available CUDA devices. This is particularly useful for developers working with GPU-accelerated applications to ensure compatibility and to understand the capabilities of the hardware.
"""
import torch



def check_cuda():
    """
    Check if CUDA is available on the system and print device information if it is.
    """

    if torch.cuda.is_available():
        # --- 1  Evaluate conditional branch
        print(" CUDA is available!")
        # --- 2  Execute function call to print
        print("GPU Name:", torch.cuda.get_device_name(0))
        # --- 3  Execute function call to print
        print("Device count:", torch.cuda.device_count())
        print("Capability:", torch.cuda.get_device_capability(0))
    else:
        print(" CUDA is NOT available.")


check_cuda()
