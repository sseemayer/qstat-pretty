# qstat-pretty

qstat-pretty is a parser and pretty-printer for the output of the Grid Engine or Torque Resource Manager `qstat` programs or the Platform LSF `bjobs` program. It will parse the output produced by `qstat` / `bjobs` and display it in a table.


![pstat screenshot](http://i.imgur.com/WkYaAyt.png)

Some nice features:

  * Table automatically grows with the size of the columns (up to the terminal width)
  * Different table styles to choose from
  * Can query local and remote grid status using SSH
  * Support for Torque Resource Manager, GridEngine, Platform LSF
 
## Getting started

qstat-pretty requires Python 2.6 or later (Python 3 supported!) and no additional modules.

To use locally:
  1. Check out qstat-pretty somewhere
  2. Copy qstat-pretty.conf.example to one of these locations - and edit to customize:
       * `/etc/qstat-pretty/qstat-pretty.conf`
       * `~/.config/qstat-pretty/qstat-pretty.conf`

  3. Link the pstat executable somewhere that can be found in `$PATH`
  4. You can now use the `pstat` command.

qstat-pretty is still in very early development, so give me a message if you have problems getting things to run.

## Basic Usage

    $ pstat

## Advanced Usage

pstat supports getting job data from three sources. This can be configured using the `qstat-pretty.conf` file or via the command line: 

  * The local system (by running the status command) (default!)
  * Another host (by running a command via `ssh`) (use the `--source-ssh [hostname]` option)
  * A file (use the `--source-file [path]` option)

All other parameters passed to pstat will be passed on to the actual status command. Examples:

  * Show my job status on the current system:

        $ pstat

  * Show my job status on the cluster head node reachable by `ssh clustmaster`:

        $ pstat --source-ssh clustmaster

  * Show job status for all users on clustmaster (for Platform LSF, use `-u all`):

        $ pstat --source-ssh clustmaster -u "*"

  * Show job status on clustmaster for user jdoe:

        $ pstat --source-ssh clustmaster -u jdoe

## License
GPLv2 or later
