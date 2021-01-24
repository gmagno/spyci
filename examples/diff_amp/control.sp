* Note that inside control block the commands order is relevant

.control
* set variables
set noaskquit
set filetype=ascii ; rawspice.raw (see `write` command) in ascii format
set nobreak ; output.log won't page break data
set noacct

options NOINIT NOMOD

* DC transfer characteristic:
*   - vary input voltage from -1V to 1V in steps of 0.1V
dc v1 -1 1 0.1

run ; run the actual simulation

* raw file path can be specified with -r flag: ngspice -r data.raw
* it defaults to ./rawspice.raw if a path is not specified with -r.
write
quit
.endc
