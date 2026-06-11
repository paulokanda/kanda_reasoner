"""

what is the name of the parte in wich an EEg file (edf,  bdf,  emsa, nihon etc)  stores the info, reference ,
 channel names , all the info that can be exported?

in EEG file formats like EDF, BDF, EMSA, Nihon Kohden, etc.,
the part of the file that contains metadata such as channel names,
sampling rate, reference scheme, physical units,
and sometimes recording reference, is typically referred to as the:
✅ Header or File Header

| Component        | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| **Header**       | The section of the file that stores metadata:              |
|                  | – Patient info                                             |
|                  | – Recording date/time                                      |
|                  | – Channel names (labels)                                   |
|                  | – Sampling frequency per channel                           |
|                  | – Physical dimensions (µV, mV)                             |
|                  | – Reference electrode used (optional, depending on format) |
|                  | – Number of samples per record                             |
| **Data section** | The actual EEG signal (usually stored as binary values)    |


💡 Format-specific notes:

    EDF/EDF+: has a fixed-size 256-byte header + per-channel header blocks (label, transducer type, units, etc.)

    BDF: similar to EDF but uses 24-bit resolution

    Nihon Kohden: proprietary format; metadata is stored in structured headers (not openly documented, but accessible via SDKs or tools like mne.io.read_raw_brainvision)

    EMSA (Mitsar): has an XML-like header block

    BrainVision: uses separate .vhdr (header), .vmrk (markers), .eeg (data)



🧬 Reference info

    In many EEG file types, the reference used during acquisition is:

        not explicitly saved in the header (especially in EDF/EDF+)

        sometimes embedded in the channel labels (e.g., "Fp1-A1")

        or saved in a field like "transducer type" (e.g., “linked-ears”)


🔍 In MNE

When you load an EEG file, the header info is usually parsed into:

raw.info  # A dictionary-like object

Where you'll find:

    raw.info['ch_names'] — list of channel names

    raw.info['sfreq'] — sampling frequency

    raw.info['chs'] — per-channel dictionaries with metadata

    raw.info['description'] — recording description

    raw.info['line_freq'] — power line frequency (e.g., 50/60 Hz)

The correct term is “header”,
and it contains all metadata about the recording and channels.
Depending on the format, it may or may not explicitly state the reference
— this often has to be inferred from labels or acquisition documentation.

"""

