muSICA
======

This is a lightweight toolbox for side-channel analysis projects.

The design goals are:
 * stand-alone commandline applications for signal processing and trace acquisition
 * lightweight, easy to understand code base

Tools
-----

### `cpa_aes`
Schoolbook implementation of Correlation Power Analysis on the Advanced Encryption Standard.

### `drag_curves`
Allows dragging a curve segment over a larger curve to inspect visually how well they align.

### `convert_dpabook`
Converts the traces (WS1/WS2) from the book [Power Analysis Attacks](https://www.dpabook.org) by Stefan Mangard et al.
to the internally used *processing format*.

### `sliding_corr`
Slides a trace segment over a larger curve and computes the Pearson correlation for each offset.

### `merge_traces`
Merge traces from the *acquisition format* to the *processing format*.

File Formats
------------

Due to different requirements for trace acquisition and trace processing (e.g. CPA), two different file formats are used.

### Acquisition Format
The following requirements have turned out useful for trace acquisition:
 1. The acquisition process shall be stoppable and resumable, such that the traces can later be used together for processing, if the setup has not changed
   (i.e. the trigger configuration, acquisition parameters, DUT firmware, etc must not be changed).
   *This turned out to be useful if the acquisition aborts due to an error, or if the speed of the acquisition is optimized during a long-running attack.*
 2. Only one trace shall be kept in RAM at a time.

Out of requirement 1., it seems reasonable to keep all data belonging to one trace (i.e. plaintext/ciphertext, actual samples, other metadata) in one single file such that confusing the different data parts at a later stage is avoided.
Also, it seems useful to annotate the type of data, e.g. by using variable names.
MATLAB files allow storing different variables with their names into a single file, and therefore, `.mat` files are used as the acquisition format.
Requirement 2. suggests that one file shall be used per trace, instead of accumulating multiple traces in one file.


### Processing Format
During processing (e.g. CPA), the following requirements seem reasonable:
 1. Loading a complete set of traces shall be fast.
 2. The processing format shall be compatible to other side-channel frameworks.
    *This helps to benefit from advantages of different tools and not be limited to muSICA.*

Loading a large number of smaller files is typically slower than loading a small number of large files.
Consequently, requirement 1. implies to accumulate traces into few files (ideally one).
The requirement from the acquisition format to only keep one trace in RAM at a time does not apply here, as processing typically requires all traces (or segments thereof) to be in RAM anyway.
Two well-known SCA frameworks are
 * [Inspector SCA](https://www.riscure.com/security-tools/inspector-sca/), a commercial package for side-channel analysis, consisting of different hard- and aoftware components.
   It uses a proprietary `.trs` format that is also available as an open source implementation as part of the [Jlsca](https://github.com/Riscure/Jlsca) SCA framework written in Julia.
 * [ChipWhisperer](https://www.newae.com/chipwhisperer) is a "semi"-commercial SCA framework by NewAE consisting of different hardware and software components.
   The [processing software](https://github.com/newaetech/chipwhisperer), and some of their hardware designs, are published on the [NewAE GitHub site](https://github.com/newaetech). 

Due to the open source nature and large community behind ChipWhisperer, muSICA uses numpy for traces and inputs/outputs in the same way as the [ChipWhisperer file format documentation](https://wiki.newae.com/File_Formats) suggests.
For now, the `.cfg` files containing metadata are not used.
