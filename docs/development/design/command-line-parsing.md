# Command line parsing

An input from command line is important to specify important runtime environment variables other than simulation parameters (which are read using the input file).

## Command line input plays a different role from input file

Command line input and the input files both provide runtime information for the program. Input files specify all the simulation related contents, while the command line input specifies the parameters needed only for how the software runs. That is to say, **no matter how the command line input changes, if the input files stay the same, we could always consider them as the "same simulations"**. Due to this difference, the two different sources of input could contain the following information.

### Command line input
- Where to find the input files, and where the output should go
- Methods of informational output (log level, log file, verbosity, ...)
- Fixed random seed if applicable
- Parallelization methods (number of cores, mpi, ...)
- Auto restart configuration (e.g. start with restart is a restart file is available)

### Input files
- Simulation duration, algorithms used and algorithm parameters
- Name of additional input files
- Simulation output categories *(currently useless)*
- Geometric, mechanochemical parameters
- Simulation initialization parameters

## Command line input information storage

As the command line input provides different information from the input files, the structure that holds the information from command line input could also be separated from the system parameters. They could be stored as global variables in a certain namespace or as members of a class.

We should limit the ability to change these global variables everywhere. To achieve that without adding `get`/`set` functions for every variable, we can put the global variables in a struct, and use this struct as a private static member of another class. The class could provide two accessors, one for const access and one for non-const access. The code might look like the follows.

```C++
struct RuntimeGlobalVariableContainer {
    int some_integer;
    std::string some_string;
    // ...
};

class Global {
private:
    static RuntimeGlobalVariableContainer _runtime; // Definition elsewhere

public:
    static const RuntimeGlobalVariableContainer& runtime() {
        return _runtime;
    }
    static RuntimeGlobalVariableContainer& runtimeMutable() {
        return _runtime;
    }
};
```

Then, when trying to access a global variable without modification, one can use something like `Global::runtime().some_integer` to access the variable. For the functions like the parser that actually writes to the global variables, one has to use `Global::runtimeMutable().some_integer` to access the variables in a non-const manner.

One could also provide only the const accessor, and mark certain functions as `friend` to the class `Global`, so that they can access the non-const members using `Global::_runtime.some_integer`. This method is similar to current implementation of `SysParams` class in MEDYAN. But in this way, one class can only implement one set of accessibility control.

## Command line parsing specs for MEDYAN

No standard exists for command line parsing, and implementations vary a lot in popular programs. But there are some common conventions and other command line parsing libraries that we could follow.

Currently, MEDYAN is using `getopt` as the command line parser, but `getopt` offers limited functionality and is not portable (GNU project). Therefore, it is natural to write our very own parser that suits our needs.

The following specifies the MEDYAN command line syntax and parser.

### General

For simplicity, the lexing, parsing, data writing and simple data validation should be combined to a one-pass process. More validations can be applied after parsing is complete, such as option mutual exclusivity, option requiredness and number range check.

We do not explicitly support groups (optional or mutual exclusive) during parsing such as `MEDYAN [-a (-b | -c -d)] [-e | -f -g]`, though they could be checked in the validation process after parsing. In the help message, groups will not be hinted.

The command line syntax looks like this
```
cmd <required-options> [<options>] [--] <positional-arguments>
cmd <sub-command>
```

where `<>` encloses the name of an object and `[]` means optional.

### Positional argument

A command can specify 0 or more positional arguments.

To avoid recursive parsing, only one set of positional argument specification is allowed for a command, i.e. when reading a positional argument, the parser must know what this positional argument mean, and the type of this argument. And hence the following specifications.

A positional argument can be required or optional. In a command, an optional positional argument must appear later than the last required positional argument. Therefore, the following is a correct usage of positional arguments
```
cmd <file> [<path>] [<id>]
```
and the following is illegal
```
cmd [<file>] <path>
```

A positional argument could also be a positional argument list, denoted as `<argument-list>...`. At most one positional argument list is allowed in one command, and must be after all the other positional arguments.

A required positional argument list takes 1 or more arguments, and an optional positional argument list takes 0 or more arguments. If there exists at least one optional positional argument in a command that is not a list, then the positional argument list must be optional. Therefore, the following cases are the correct usages
```
cmd <arg1> <arg2> <arg-list>...
cmd <arg1> [<arg2>] [<arg-list>...]
```
while the following are incorrect usages
```
cmd <arg-list>... <arg1>
cmd <arg1> <arg-list1>... <arg-list2>...
cmd [<arg1>] <arg-list>...
```

For illegal cases in specification, an error should be generated before parsing.

During parsing, the parser will always fill the positional arguments from the first to the last, regardless of requiredness. For example, if the program specifies this
```
cmd1 <arg1> [<arg2>] [<arg3>] [<arg-list>...]
cmd2 <arg1> [<arg-list>...]
```
and runs with the following
```
cmd1 100 200
cmd2 100 200
```
then in `cmd1`, `200` will always bind with `arg2`, and in `cmd2`, `200` is the first and only element in `arg-list`. If the number of positional arguments supplied is more than the maximum number of positional argument and there is no argument list specified, an error should be generated. If the number of positional arguments supplied is less than the number of required positional argument, the parsing could finish successfully, but should fail the validation process after parsing, which generates an error.

### Option

A command can specify 0 or more options.

Unlike positional arguments, options can appear anywhere *after* the command, *before* the positional argument delimiter `--` (see next section).

An option starts with an option marker, and can take 0 or 1 variable *right after* the option marker. The option marker could be a short option marker or a long option marker.

A short option marker is 2 characters. The first character is `-`, and the second character is anything but `-`. During parsing, if the option takes 1 variable, then (1) if the argument is longer than 2 characters, the rest of the argument will be considered as the variable (2) otherwise the next argument will be considered as the argument. In the 2nd case, if the next argument does not exist (end of argument list), an error should be generated. For example, if `-t` is an option that takes 1 variable, then `-t est` and `-test` both mean taking `"est"` as the variable of `-t` option, and an error should be generated for `-t` without further arguments. If the option takes 0 variable and the argument has more than 2 characters, then append `-` before the rest, and parse it accordingly. For example, if `-t` does not take variable, then `-test` will be treated as the option `-t` showing up, and the parser will try to parse `-est` next.

As a more complicated example, assume `-s` and `-e` are options that take 1 variable, and `-t` is an option that takes no variable, then `-test` is parsed as `-t -e st` where `-t` shows up, `-e` shows up and gets a variable `"st"` and `-s` does not show up.

A long option marker has more than 2 characters and starts with `--`, and should not contain the character `=`. During parsing, the longest starting part in an argument that satisfies the criteria will be considered the long option marker. If the option takes no variable and `=` shows up, an error should be generated. If the option takes 1 variable, then (1) if at least one `=` shows up, everything after the first `=` will be considered the variable (2) otherwise, the next argument will be considered the variable. In the 2nd case, if the next argument does not exist (end of argument list), an error should be generated. For example, if `--test` is an option that takes one variable, then `--test=yes` and `--test yes` both mean taking "yes" as the variable of the `--test` option, and an error should be generated for `--test` without further arguments. Specifically, using `=` allows specifying empty string variable for options using long option markers. For example, if `--test` takes one variable, then `--test=` means giving empty string to `--test` as the variable.

During parsing, if an argument can be considered as an option, but the option does not exist, then an error is generated. If one really wants a positional argument that looks like an option, consider using the positional argument delimiter `--`.

Like positional arguments, an option can be required or optional. That an option is required means that the option must show up at least once. However, the requiredness should not have effect during parsing, as it can only be checked when parsing is finished. Nevertheless, the requiredness should be hinted in the help message.

### Positional argument delimiter `--`

During parsing, the positional argument delimiter is an argument that is exactly `--`. In a command, anything after `--` is considered positional arguments of that command, even if they look like options, subcommands or even the delimiter.

For example, if the specified syntax looks like this
```
cmd [-a] [-b] -c [--] <arg1> [<arg2>] [<arg-list>...]
cmd subcmd1
cmd subcmd2
```
Then running
```
cmd -b -c -- -a subcmd1 -- subcmd2
```
means that `-b` and `-c` show up, `-a` does not show up, `arg1 = "-a"`, `arg2 = "subcmd1"` and `arg-list = ["--", "subcmd2"]`. Notice that everything after the first `--` is considered the positional argument.

### Subcommand

A command can specify 0 or more subcommands.

During parsing, the first argument that is not an option will be matched against the list of subcommands. If it matches a subcommand, the subcommand will take over and parse all the remaining arguments. The control will not return to the parent command, which implies that running multiple subcommands in the same nested level is not possible. For example, with specification
```
cmd [--] [<arg1>]
cmd subcmd1
```
then running with `cmd subcmd1` will run subcommand `subcmd1` and leave `arg1` uninitialized (probably default value), but running with `cmd subcmd2` will set `arg1` to be `subcmd2`, since there is no subcommand with name `subcmd2`. If one really needs the positional argument that has the name of a subcommand, consider using the positional argument delimiter `--`.

A subcommand works like a command, and can specify its own positional arguments, options and subcommands. During parsing, when control moves to a subcommand, the subcommands and positional arguments of the parent command will no longer have effect. The options of the parent command, however, will be inherited to the subcommand, but subcommand options can overwrite the parent options with the same name. When parsing a subcommand, the parser should try to look for the option of an option-like argument from the most nested subcommand, all the way to the options of the main command, and if no option can be found, an error should be generated.

### Help message

Help message displays the basic usage of a command. A typical help message might look like this:
```
Usage: cmd <required-options> [<options>] [--] <arg1> [<arg2>] [<arg-list>...]

Subcommands:
    subcmd-name         Description
    subcmd-name-2       Description 2

Options:
    -o, --option        [Required] Description
    -2, --option-2      Description 2
    --option-3=<val>    Description 3
```

The parser should provide an auxiliary function that generates the formatted help message with the given specification. By convention, `-h` and `--help` options should be added to every command and subcommand to generate the help message and exit the program. Also the help message should be printed on parsing errors of the associated subcommand.

The subcommand help message should contain the chain of all parent command names. For example,
```
$ cmd run install --help
Usage: cmd run install [<options>] [--] <arg1> <arg-list>...

Options:
    -f, --file=<path>   File location
```

### Procedure and error handling

The program should hard code the specification for all commands and subcommands.

Before parsing, the specification will be checked against some rules, and if an violation happens, an exception should be thrown without handling, so that it aborts the parsing and the rest of the program, so no help message should be printed, as this is an internal error.

During parsing, the arguments of the main function `int argc, char *argv[]` will be fed to the parser. The parsing process follows the rules mentioned in the previous sections. If an error occurs, an exception should be thrown, which should be handled outside the parser. The simple data writing and validation should happen along with the parsing process. The parser should decide whether the simple data writing and validation is successful, and if it is not, an exception should be thrown which should be handled outside the parser. The handler should print the error, print the help message generated by the parser, and abort the program.

After parsing is complete, further validation and other initialization could kick in. The validation may decide to print the help message as needed. Specifically, an unprovided required option or unprovided required positional argument should result in the failure of the validation process, causing it to print the help message and abort the program.

