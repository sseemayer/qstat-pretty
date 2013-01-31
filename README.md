# qstat-pretty

qstat-pretty is a parser and pretty-printer for the output of the Grid Engine `qstat` program. It will parse the XML output produced by `qstat -xml` and display it in a table.

Some nice features:

  * No fixed-length cutoff for job names!
  * Pretty tables with borders and coloring
  * Tables automatically grow with terminal width
  * Can query local and remote grid status using SSH

## Getting started

qstat-pretty requires Python 2.7 or later (Python 3 supported!) and no additional modules.

  1. Check out qstat-pretty somewhere
  2. Run `python setup.py build` as non-root
  3. Run `python setup.py install` as root
  4. You can now use the `pstat` command.

qstat-pretty is still in very early development, so give me a message if you have problems getting things to run.

## Basic Usage

    $ pstat

## Advanced Usage

pstat supports getting job data from three sources: 

  * The local system (by running a `qstat` command) (default!)
  * Another host (by running `qstat` via `ssh`) (use the `-S [hostname]` option)
  * An XML file (use the `-X [xmlfile]` option)

All other parameters passed to pstat will be passed on to the qstat command. Examples:

  * Show my job status on the current system:

        $ pstat

  * Show my job status on the cluster head node reachable by `ssh clustmaster`:

        $ pstat -S clustmaster

  * Show job status for all users on clustmaster:

        $ pstat -S clustmaster -u "*"

  * Show job status on clustmaster for user jdoe:

        $ pstat -S clustmaster -u jdoe
