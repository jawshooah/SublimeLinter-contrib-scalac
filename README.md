SublimeLinter-contrib-scalac
================================

[![Build Status][travis-badge]][travis]
[![Codacy Badge][codacy-badge]][codacy]

This linter plugin for [SublimeLinter][docs] provides an interface to
[scalac][scalac]. It will be used with files that have the “scala” syntax.

##### IMPORTANT!
Please note that because `scalac` requires a complete directory context in
order to work, this linter plugin currently will only lint a file **when it has
been saved**. As soon as you modify the file, all linter marks will be cleared.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter
3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that `scalac` is installed on your
system. `scalac` is part of the `scala` developer SDK, which can be downloaded
[here][scala-download].

**Note:** This plugin requires Scala 2.9.1 or later.

### Linter configuration
In order for `scalac` to be executed by SublimeLinter, you must ensure that its
path is available to SublimeLinter. Before going any further, please read and
follow the steps in [“Finding a linter executable”][finding-executable] through
“Validating your PATH” in the documentation.

Once you have installed and configured `scalac`, you can proceed to install the
SublimeLinter-contrib-scalac plugin if it is not yet installed.

### Plugin installation
Please use [Package Control][pc] to install the linter plugin. This will ensure
that the plugin will be updated when new versions are available. If you want to
install from source so you can modify the source code, you probably know what
you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`.
   Among the commands you should see `Package Control: Install Package`. If
   that command is not highlighted, use the keyboard or mouse to select it.
   There will be a pause of a few seconds while Package Control fetches the
   list of available plugins.

1. When the plugin list appears, type `scalac`. Among the entries you should
   see `SublimeLinter-contrib-scalac`. If that entry is not highlighted, use
   the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see
[Settings][settings]. For information on generic linter settings, please see
[Linter Settings][linter-settings].

In addition to the standard SublimeLinter settings,
SublimeLinter-contrib-scalac provides its own settings. Those marked as
“Inline Setting” or “Inline Override” may also be
[used inline][inline-settings].

|Setting           |Type         |Description                                       |Inline Setting|Inline Override|
|:-----------------|:------------|:-------------------------------------------------|:------------:|:-------------:|
|lint              |`str`\|`list`|A comma-delimited list of rules to apply.         |              |&#10003;       |
|classpath         |`str`\|`list`|A colon-delimited list of classpath entries.      |&#10003;      |               |
|classpath_filename|`str`        |Name of file containing colon-delimited classpath.|&#10003;      |               |

### `lint`

Valid rules for the `lint` option depend on the version of Scala you have
installed. Options with a check in the Default column are enabled by default:

|Rule                     |Description                                                                         |Scala Version|Default    |
|:------------------------|:-----------------------------------------------------------------------------------|:-----------:|:---------:|
|check-null               |Warn upon selection of nullable reference.                                          |2.9.1-2.10.4 |           |
|dead-code                |Warn when dead code is identified.                                                  |>= 2.9.1     |2.9.1-2.9.3|
|value-discard            |Warn when non-Unit expression results are unused.                                   |>= 2.9.1     |           |
|numeric-widen            |Warn when numerics are widened.                                                     |>= 2.9.1     |           |
|nullary-unit             |Warn when nullary methods return Unit.                                              |>= 2.9.1     |&#10003;   |
|inaccessible             |Warn about inaccessible types in method signatures.                                 |>= 2.9.1     |&#10003;   |
|nullary-override         |Warn when non-nullary `def f()` overrides nullary `def f`.                          |>= 2.9.1     |&#10003;   |
|adapted-args             |Warn if an argument list is modified to match the receiver.                         |>= 2.10.0    |&#10003;   |
|infer-any                |Warn when a type argument is inferred to be `Any`.                                  |>= 2.11.0    |&#10003;   |
|unused                   |Warn when local and private vals, vars, defs, and types are unused.                 |>= 2.11.0    |           |
|unused-import            |Warn when imports are unused.                                                       |>= 2.11.0    |           |
|missing-interpolator     |A string literal appears to be missing an interpolator id.                          |>= 2.11.2    |&#10003;   |
|doc-detached             |A ScalaDoc comment appears to be detached from its element.                         |>= 2.11.2    |&#10003;   |
|private-shadow           |A private field (or class parameter) shadows a superclass field.                    |>= 2.11.2    |&#10003;   |
|poly-implicit-overload   |Parameterized overloaded implicit methods are not visible as view bounds.           |>= 2.11.2    |&#10003;   |
|option-implicit          |Option.apply used implicit view.                                                    |>= 2.11.2    |&#10003;   |
|delayedinit-select       |Selecting member of DelayedInit.                                                    |>= 2.11.2    |&#10003;   |
|by-name-right-associative|By-name parameter of right associative operator.                                    |>= 2.11.2    |&#10003;   |
|package-object-classes   |Class or object defined in package object.                                          |>= 2.11.2    |&#10003;   |
|unsound-match            |Pattern match may not be typesafe.                                                  |>= 2.11.2    |&#10003;   |
|deprecation              |Emit warning and location for usages of deprecated APIs.                            |>= 2.9.1     |           |
|unchecked                |Enable additional warnings where generated code depends on assumptions.             |>= 2.9.1     |           |
|fatal-warnings           |Fail the compilation if there are any warnings.                                     |>= 2.9.1     |           |
|nowarn                   |Generate no warnings.                                                               |>= 2.9.1     |           |
|feature                  |Emit warning and location for usages of features that should be imported explicitly.|>= 2.10.0    |           |

For example, to enable `numeric-widen` and `deprecation`, you would add this to
the linter settings:

```json
"scalac": {
    "lint": "numeric-widen,deprecation"
}
```

Or as a list:

```json
"scalac": {
    "lint": [
        "numeric-widen",
        "deprecation"
    ]
}
```

To enable `feature` and disable `doc-detached` but keep the rest of the
settings, you would put this comment on the first or second line of the
file:

```scala
// [SublimeLinter scalac-lint:+feature,+-doc-detached]
```

### `classpath`

If you specify `classpath`, the linter plugin will use the given entries as
input to `scalac -classpath`.

With an [`sbt`][sbt] project, you can get your full classpath by running

```bash
sbt 'export fullClasspath'
```

You may specify `classpath` as a string:

```json
"scalac": {
    "classpath": "$PROJECT_PATH/target/scala-2.11/classes:$PROJECT_PATH/lib/lib.jar"
}
```

Or as a list:

```json
"scalac": {
    "classpath": [
        "$PROJECT_PATH/target/scala-2.11/classes",
        "$PROJECT_PATH/lib/lib.jar"
    ]
}
```

### `classpath_filename`

If you specify `classpath_filename`, the linter plugin will search for
a file with that name in the project directory and its parents. If found, it
will use the contents of that file with `scalac -classpath` for linting.

If both `classpath` and `classpath_filename` are specified, their values will
be merged.

The contents of the file must be a colon-delimited list of paths for the JVM to
search during compilation. For example:

```
/path/to/project/classes:/path/to/project/libs/lib.jar
```

You can also add whitespace between classpath entries for better readability:

```
:/path/to/project/classes
:/path/to/project/libs/lib.jar
```

### `target_directory`

This setting tells `scalac` where to put generated class files. If unset, class
files will be put in the same directory as their source files.

For example:

```json
"scalac": {
    "target_directory": "$PROJECT_PATH/target/scala-2.11/classes"
}
```

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `develop`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbrevations unless they are very
  well known.

##### IMPORTANT!
Also note that this repository uses [overcommit][overcommit] as a validation
tool. Before making any changes, please
[install overcommit][overcommit-install] in your local repository.

Thank you for helping out!

[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[codacy]: https://www.codacy.com/public/haginsjosh/SublimeLinter-contrib-scalac
[codacy-badge]: https://www.codacy.com/project/badge/1b0457e1263c4408a1e903a4be3733d9
[docs]: http://sublimelinter.readthedocs.org
[finding-executable]: http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[overcommit]: https://github.com/causes/overcommit
[overcommit-install]: https://github.com/causes/overcommit#installation
[pc]: https://sublime.wbond.net/installation
[sbt]: http://www.scala-sbt.org/
[scalac]: http://www.scala-lang.org/old/sites/default/files/linuxsoft_archives/docu/files/tools/scalac.html
[scala-download]: http://www.scala-lang.org/download/
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[travis]: https://travis-ci.org/jawshooah/SublimeLinter-contrib-scalac
[travis-badge]: https://travis-ci.org/jawshooah/SublimeLinter-contrib-scalac.svg?branch=develop
