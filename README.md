# SublimeMSBuild
[Sublime Text](http://www.sublimetext.com/) package for editing and executing MSBuild scripts.

## Overview
[Sublime Text](http://www.sublimetext.com/) is a highly-customizable text editor that allows you to add functionality through use of "packages." This package adds the following functionality for MSBuild:

* **MSBuild file extension handling**:
	* .proj
	* .targets
	* .msbuild
	* .csproj
	* .vbproj
	* .fsproj
	* .vcxproj
* **Build system**: Execute the currently loaded MSBuild script and capture the results in the output pane. [Includes variants for 'Parallel,' 'Debug,' and 'Release' configurations.](https://github.com/tillig/SublimeMSBuild/wiki/Build-Variants)
* **Syntax highlighting**:
	* MSBuild keywords and flow-control elements
	* Standard MSBuild tasks
	* C#/VB special project item elements
	* Well-known item metadata and functions
	* Reserved properties
	* Variables
	* Conditional operators
	* Framework support functions
	* Comment blocks
* **Snippets**:
	* New MSBuild Script
	* Comment blocks [trigger = `c` + tab]
	* Self-closing/simple tags [trigger = `>` + tab]
	* Content/end-tag tags [trigger = `<` + tab]
* **Autocompletion**:
	* Standard/default tasks (e.g., `CallTarget`, `CombinePath`, `MakeDir`)
	* Project file entities (e.g., `Target`, `Choose`, `Import`)
	* Common item definitions (e.g., `Compile`, `Reference`, `EmbeddedResource`)
	* Well-known item metadata references (e.g., `%(Item.FullPath)`)
	* Reserved properties (e.g., `$(MSBuildProjectDirectory)`)
	* [MSBuild Community Tasks](https://github.com/loresoft/msbuildtasks) (if the `MSBuild.Community.Tasks.Targets` file is imported)
	* C#/VB special project item elements (e.g., `Reference`, `Compile`)
	* Supported framework method calls (e.g., `$([System.DateTime]::Now)`)

## Installation

**Install the package through [Sublime Package Control](http://wbond.net/sublime_packages/package_control).** Sublime Package Control is a package manager for Sublime Text. If you don't have it, you can [install it](http://wbond.net/sublime_packages/package_control/installation) and then install the `MSBuild` package by going to the command palette (Ctrl + Shift + P), selecting "Package Control: Install Package," and then selecting the MSBuild package from the list.

## License
[MIT License](https://github.com/tillig/SublimeMSBuild/blob/master/LICENSE.md)

## Build System MSBuild.exe Fallback
Most Sublime Text build systems assume you have the build executable (`MSBuild.exe`) in your path. The system included here dynamically looks for `MSBuild.exe` in the .NET framework folders in the event you don't already have it in your path. The fallback order is `v4.0.30319 -> v3.5 -> v2.0.50727`. If you want to modify that fallback order, edit the `MSBuild.sublime-build` file in your `Data\Packages\MSBuild` folder.

## Package Developers
If you want to modify the syntax highlighter or otherwise work on enhancing the package to suit your needs, it's recommended you get the [AAAPackageDev](https://github.com/SublimeText/AAAPackageDev) package for Sublime Text. This allows you to edit syntax files in `.JSON-tmLanguage` format and compile them into PList rather than manually editing PList directly. It also has several helpers/templates for adding functionality to Sublime Text packages.

Additional helpful links:

* [TextMate Language Grammars](http://manual.macromates.com/en/language_grammars) - Sublime Text uses a TextMate-compatible syntax highlighting mechanism including the naming for various scopes.
* [Syntax Definition Reference](http://docs.sublimetext.info/en/latest/reference/syntaxdefs.html)
* [Snippet Reference](http://docs.sublimetext.info/en/latest/reference/snippets.html)
* [Build System Reference](http://docs.sublimetext.info/en/latest/reference/build_systems.html)
* [Completion Reference](http://docs.sublimetext.info/en/latest/reference/completions.html)