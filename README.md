#SublimeMSBuild
[Sublime Text 2](http://www.sublimetext.com/) package for editing and executing MSBuild scripts.

##Overview
[Sublime Text 2](http://www.sublimetext.com/) is a highly-customizable text editor that allows you to add functionality through use of "packages." This package adds the following functionality for MSBuild:

* **MSBuild file extension handling**: Recognizes the following extensions as MSBuild...
	* .proj
	* .targets
	* .msbuild
	* .csproj
	* .vbproj
* **Build system**: Execute the currently loaded MSBuild script and capture the results in the output pane.
* **Syntax highlighting**: Support for properly highlighting...
	* MSBuild keywords and flow-control elements
	* Standard MSBuild tasks
	* C#/VB special project item elements
	* Well-known item metadata
	* Reserved properties
	* Variables
	* Conditional operators
	* Framework support functions
	* Comment blocks
* **Snippets**:
	* Empty MSBuild Script

##Installation
Download MSBuild.sublime-package and install it [using the Sublime Text package installation instructions](http://sublimetext.info/docs/en/extensibility/packages.html#installation-of-packages).

Basically this means either double-clicking on the package file (if you have installed Sublime Text) or copying the package file into your `Data/Installed Packages` folder (if you're using a portable install of Sublime Text).

##License
[MIT License](https://github.com/tillig/SublimeMSBuild/blob/master/LICENSE.md)

##Additional Notes
**Build system MSBuild.exe fallback**: Most Sublime Text build systems assume you have the build executable (`MSBuild.exe`) in your path. The system included here dynamically looks for `MSBuild.exe` in the .NET framework folders in the event you don't already have it in your path. The fallback order is `v4.0.30319 -> v3.5 -> v2.0.50727`. If you want to modify that fallback order, edit the `MSBuild.sublime-build` file in your `Data\Packages\MSBuild` folder.