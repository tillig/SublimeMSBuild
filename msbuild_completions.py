import sublime, sublime_plugin
import re

# Enable autocomplete to be fired when $( is typed
# This is required because of the balanced-parentheses key binding
class CompleteOnPropertyListener(sublime_plugin.EventListener):
    def on_modified(self,view):
        sel = view.sel()[0]
        if not view.match_selector(sel.a, "source.msbuild"):
            return

        ch = view.substr(sublime.Region(sel.a-3, sel.a))

        # Handle variables - $(...)
        # Handle static property methods - $([...]::...)
        if ch[-2:] == '$(' or  ch[-2:] == '::' or ch == '$([':
            view.run_command('auto_complete')


# Provide completions that match just after typing a $() property reference
class ReservedPropertyCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild if it's a property
        if not view.match_selector(locations[0],
                "variable.parameter.property.source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 2
        ch = view.substr(sublime.Region(pt, pt + 2))
        if ch != '$(':
            return []

        return ([
            ("MSBuildBinPath", "MSBuildBinPath"),
            ("MSBuildExtensionsPath", "MSBuildExtensionsPath"),
            ("MSBuildExtensionsPath32", "MSBuildExtensionsPath32"),
            ("MSBuildExtensionsPath64", "MSBuildExtensionsPath64"),
            ("MSBuildLastTaskResult", "MSBuildLastTaskResult"),
            ("MSBuildNodeCount", "MSBuildNodeCount"),
            ("MSBuildProgramFiles32", "MSBuildProgramFiles32"),
            ("MSBuildProjectDefaultTargets", "MSBuildProjectDefaultTargets"),
            ("MSBuildProjectDirectory", "MSBuildProjectDirectory"),
            ("MSBuildProjectDirectoryNoRoot", "MSBuildProjectDirectoryNoRoot"),
            ("MSBuildProjectExtension", "MSBuildProjectExtension"),
            ("MSBuildProjectFile", "MSBuildProjectFile"),
            ("MSBuildProjectFullPath", "MSBuildProjectFullPath"),
            ("MSBuildProjectName", "MSBuildProjectName"),
            ("MSBuildStartupDirectory", "MSBuildStartupDirectory"),
            ("MSBuildThisFile", "MSBuildThisFile"),
            ("MSBuildThisFileDirectory", "MSBuildThisFileDirectory"),
            ("MSBuildThisFileDirectoryNoRoot", "MSBuildThisFileDirectoryNoRoot"),
            ("MSBuildThisFileExtension", "MSBuildThisFileExtension"),
            ("MSBuildThisFileFullPath", "MSBuildThisFileFullPath"),
            ("MSBuildThisFileName", "MSBuildThisFileName"),
            ("MSBuildToolsPath", "MSBuildToolsPath"),
            ("MSBuildToolsVersion", "MSBuildToolsVersion")
        ], sublime.INHIBIT_WORD_COMPLETIONS)


# Provide completions that match just after typing a $([]) static method type reference
class StaticFunctionTypes(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild if it's a property
        if not view.match_selector(locations[0],
                "variable.parameter.property.source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 3
        ch = view.substr(sublime.Region(pt, pt + 3))
        if ch != '$([':
            return []

        return ([
            ("Byte (Functions)", "System.Byte"),
            ("Char (Functions)", "System.Char"),
            ("Convert (Functions)", "System.Convert"),
            ("DateTime (Functions)", "System.DateTime"),
            ("Decimal (Functions)", "System.Decimal"),
            ("Directory (Functions)", "System.IO.Directory"),
            ("Double (Functions)", "System.Double"),
            ("Enum (Functions)", "System.Enum"),
            ("Environment (Functions)", "System.Environment"),
            ("File (Functions)", "System.IO.File"),
            ("Guid (Functions)", "System.Guid"),
            ("Int16 (Functions)", "System.Int16"),
            ("Int32 (Functions)", "System.Int32"),
            ("Int64 (Functions)", "System.Int64"),
            ("Math (Functions)", "System.Math"),
            ("MSBuild (Functions)", "MSBuild"),
            ("Path (Functions)", "System.IO.Path"),
            ("Regex (Functions)", "System.Text.RegularExpressions.Regex"),
            ("SByte (Functions)", "System.SByte"),
            ("Single (Functions)", "System.Single"),
            ("String (Functions)", "System.String"),
            ("StringComparer (Functions)", "System.StringComparer"),
            ("TimeSpan (Functions)", "System.TimeSpan"),
            ("ToolLocationHelper (Functions)", "Microsoft.Build.Utilities.ToolLocationHelper"),
            ("UInt16 (Functions)", "System.UInt16"),
            ("UInt32 (Functions)", "System.UInt32"),
            ("UInt64 (Functions)", "System.UInt64")
        ], sublime.INHIBIT_WORD_COMPLETIONS)


# Provide completions that match just after typing a $([]) static method type reference
class StaticFunctions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild if it's a property
        if not view.match_selector(locations[0],
                "variable.parameter.property.source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 2
        ch = view.substr(sublime.Region(pt, pt + 2))
        if ch != '::':
            return []

        line = view.line(pt)
        partialLine = view.substr(sublime.Region(line.begin(), pt))
        staticTypeMatch = re.search(".*\\$\\(\\[([\\w\\.]+)\\]", partialLine)
        if staticTypeMatch is None:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)

        staticType = staticTypeMatch.group(1)
        if staticType == "Microsoft.Build.Utilities.ToolLocationHelper":
            return ([
                ("GetDotNetFrameworkRootRegistryKey", "GetDotNetFrameworkRootRegistryKey(version)"),
                ("GetDotNetFrameworkSdkInstallKeyValue", "GetDotNetFrameworkSdkInstallKeyValue(version)"),
                ("GetDotNetFrameworkVersionFolderPrefix", "GetDotNetFrameworkVersionFolderPrefix(version)"),
                ("GetPathToDotNetFramework", "GetPathToDotNetFramework(version)"),
                ("GetPathToDotNetFrameworkFile", "GetPathToDotNetFrameworkFile(fileName, version)"),
                ("GetPathToDotNetFrameworkSdk", "GetPathToDotNetFrameworkSdk(version)"),
                ("GetPathToDotNetFrameworkSdkFile", "GetPathToDotNetFrameworkSdkFile(fileName, version)"),
                ("GetPathToSystemFile", "GetPathToSystemFile(fileName)"),
                ("PathToSystem", "PathToSystem"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "MSBuild":
            return ([
                ("Add", "Add(a, b)"),
                ("BitwiseAnd", "BitwiseAnd(first, second)"),
                ("BitwiseNot", "BitwiseNot(first)"),
                ("BitwiseOr", "BitwiseOr(first, second)"),
                ("BitwiseXor", "BitwiseXor(first, second)"),
                ("Divide", "Divide(a, b)"),
                ("Escape", "Escape(unescaped)"),
                ("GetDirectoryNameOfFileAbove", "GetDirectoryNameOfFileAbove(path, file)"),
                ("GetRegistryValue", "GetRegistryValue(keyName, valueName)"),
                ("GetRegistryValueFromView", "GetRegistryValueFromView(keyName, valueName, defaultValue, views)"),
                ("Modulo", "Modulo(a, b)"),
                ("Multiply", "Multiply(a, b)"),
                ("Subtract", "Subtract(a, b)"),
                ("Unescape", "Unescape(escaped)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Byte":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Char":
            return ([
                ("ConvertFromUtf32", "ConvertFromUtf32(utf32)"),
                ("ConvertToUtf32", "ConvertToUtf32(s, index)"),
                ("GetNumericValue", "GetNumericValue(c)"),
                ("GetUnicodeCategory", "GetUnicodeCategory(c)"),
                ("IsControl", "IsControl(c)"),
                ("IsDigit", "IsDigit(c)"),
                ("IsHighSurrogate", "IsHighSurrogate(c)"),
                ("IsLetter", "IsLetter(c)"),
                ("IsLetterOrDigit", "IsLetterOrDigit(c)"),
                ("IsLower", "IsLower(c)"),
                ("IsLowSurrogate", "IsLowSurrogate(c)"),
                ("IsNumber", "IsNumber(c)"),
                ("IsPunctuation", "IsPunctuation(c)"),
                ("IsSeparator", "IsSeparator(c)"),
                ("IsSurrogate", "IsSurrogate(c)"),
                ("IsSurrogatePair", "IsSurrogatePair(s, index)"),
                ("IsSymbol", "IsSymbol(c)"),
                ("IsUpper", "IsUpper(c)"),
                ("IsWhiteSpace", "IsWhiteSpace(c)"),
                ("Parse", "Parse(s)"),
                ("ToLower", "ToLower(c)"),
                ("ToLowerInvariant", "ToLowerInvariant(c)"),
                ("ToString", "ToString(c)"),
                ("ToUpper", "ToUpper(c)"),
                ("ToUpperInvariant", "ToUpperInvariant(c)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Convert":
            return ([
                ("ChangeType", "ChangeType(value, conversionType)"),
                ("FromBase64CharArray", "FromBase64CharArray(inArray, offset, length)"),
                ("FromBase64String", "FromBase64String(s)"),
                ("GetTypeCode", "GetTypeCode(value)"),
                ("IsDBNull", "IsDBNull(value)"),
                ("ToBase64CharArray", "ToBase64CharArray(inArray, offsetIn, length, outArray, offsetOut)"),
                ("ToBase64String", "ToBase64String(inArray)"),
                ("ToBoolean", "ToBoolean(value)"),
                ("ToByte", "ToByte(value)"),
                ("ToChar", "ToChar(value)"),
                ("ToDateTime", "ToDateTime(value)"),
                ("ToDecimal", "ToDecimal(value)"),
                ("ToDouble", "ToDouble(value)"),
                ("ToInt16", "ToInt16(value)"),
                ("ToInt32", "ToInt32(value)"),
                ("ToInt64", "ToInt64(value)"),
                ("ToSByte", "ToSByte(value)"),
                ("ToSingle", "ToSingle(value)"),
                ("ToString", "ToString(value)"),
                ("ToUInt16", "ToUInt16(value)"),
                ("ToUInt32", "ToUInt32(value)"),
                ("ToUInt64", "ToUInt64(value)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.DateTime":
            return ([
                ("Compare", "Compare(t1, t2)"),
                ("DaysInMonth", "DaysInMonth(year, month)"),
                ("Equals", "Equals(t1, t2)"),
                ("FromBinary", "FromBinary(dateData)"),
                ("FromFileTime", "FromFileTime(fileTime)"),
                ("FromFileTimeUtc", "FromFileTimeUtc(fileTime)"),
                ("FromOADate", "FromOADate(d)"),
                ("IsLeapYear", "IsLeapYear(year)"),
                ("Now", "Now"),
                ("Parse", "Parse(s)"),
                ("Today", "Today"),
                ("UtcNow", "UtcNow"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Decimal":
            return ([
                ("Add", "Add(d1, d2)"),
                ("Ceiling", "Ceiling(d)"),
                ("Compare", "Compare(d1, d2)"),
                ("Divide", "Divide(d1, d2)"),
                ("Equals", "Equals(d1, d2)"),
                ("Floor", "Floor(d)"),
                ("FromOACurrency", "FromOACurrency(cy)"),
                ("GetBits", "GetBits(d)"),
                ("Multiply", "Multiply(d1, d2)"),
                ("Negate", "Negate(d)"),
                ("Parse", "Parse(s)"),
                ("Remainder", "Remainder(d1, d2)"),
                ("Round", "Round(d, decimals)"),
                ("Subtract", "Subtract(d1, d2)"),
                ("ToByte", "ToByte(value)"),
                ("ToDouble", "ToDouble(d)"),
                ("ToInt16", "ToInt16(value)"),
                ("ToInt32", "ToInt32(d)"),
                ("ToInt64", "ToInt64(d)"),
                ("ToOACurrency", "ToOACurrency(value)"),
                ("ToSByte", "ToSByte(value)"),
                ("ToSingle", "ToSingle(d)"),
                ("ToUInt16", "ToUInt16(value)"),
                ("ToUInt32", "ToUInt32(d)"),
                ("ToUInt64", "ToUInt64(d)"),
                ("Truncate", "Truncate(d)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Double":
            return ([
                ("IsInfinity", "IsInfinity(d)"),
                ("IsNaN", "IsNaN(d)"),
                ("IsNegativeInfinity", "IsNegativeInfinity(d)"),
                ("IsPositiveInfinity", "IsPositiveInfinity(d)"),
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Enum":
            return ([
                ("Format", "Format(enumType, value, format)"),
                ("GetName", "GetName(enumType, value)"),
                ("GetNames", "GetNames(enumType)"),
                ("GetUnderlyingType", "GetUnderlyingType(enumType)"),
                ("GetValues", "GetValues(enumType)"),
                ("IsDefined", "IsDefined(enumType, value)"),
                ("Parse", "Parse(enumType, value)"),
                ("Parse", "Parse(enumType, value, ignoreCase)"),
                ("ToObject", "ToObject(enumType, value)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Environment":
            return ([
                ("CommandLine", "CommandLine"),
                ("ExpandEnvironmentVariables", "ExpandEnvironmentVariables(name)"),
                ("GetEnvironmentVariable", "GetEnvironmentVariable(variable)"),
                ("GetEnvironmentVariable", "GetEnvironmentVariable(variable, target)"),
                ("GetEnvironmentVariables", "GetEnvironmentVariables"),
                ("GetEnvironmentVariables", "GetEnvironmentVariables(target)"),
                ("GetFolderPath", "GetFolderPath(folder)"),
                ("GetLogicalDrives", "GetLogicalDrives"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Guid":
            return ([
                ("NewGuid", "NewGuid"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Int16":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Int32":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Int64":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.IO.Directory":
            return ([
                ("GetDirectories", "GetDirectories(path, searchPattern)"),
                ("GetFiles", "GetFiles(path, searchPattern)"),
                ("GetLastAccessTime", "GetLastAccessTime(path)"),
                ("GetLastWriteTime", "GetLastWriteTime(path)"),
                ("GetParent", "GetParent(path)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.IO.File":
            return ([
                ("Exists", "Exists(path)"),
                ("GetAttributes", "GetAttributes(path)"),
                ("GetCreationTime", "GetCreationTime(path)"),
                ("GetLastAccessTime", "GetLastAccessTime(path)"),
                ("GetLastWriteTime", "GetLastWriteTime(path)"),
                ("ReadAllText", "ReadAllText(path)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.IO.Path":
            return ([
                ("ChangeExtension", "ChangeExtension(path, extension)"),
                ("Combine", "Combine(path1, path2)"),
                ("GetDirectoryName", "GetDirectoryName(path)"),
                ("GetExtension", "GetExtension(path)"),
                ("GetFileName", "GetFileName(path)"),
                ("GetFileNameWithoutExtension", "GetFileNameWithoutExtension(path)"),
                ("GetFullPath", "GetFullPath(path)"),
                ("GetInvalidFileNameChars", "GetInvalidFileNameChars"),
                ("GetInvalidPathChars", "GetInvalidPathChars"),
                ("GetPathRoot", "GetPathRoot(path)"),
                ("GetRandomFileName", "GetRandomFileName"),
                ("GetTempFileName", "GetTempFileName"),
                ("GetTempPath", "GetTempPath"),
                ("HasExtension", "HasExtension(path)"),
                ("IsPathRooted", "IsPathRooted(path)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Math":
            return ([
                ("Abs", "Abs(value)"),
                ("Acos", "Acos(d)"),
                ("Asin", "Asin(d)"),
                ("Atan", "Atan(d)"),
                ("Atan2", "Atan2(y, x)"),
                ("BigMul", "BigMul(a, b)"),
                ("Ceiling", "Ceiling(d)"),
                ("Cos", "Cos(d)"),
                ("Cosh", "Cosh(value)"),
                ("Exp", "Exp(d)"),
                ("Floor", "Floor(d)"),
                ("IEEERemainder", "IEEERemainder(x, y)"),
                ("Log", "Log(d)"),
                ("Log10", "Log10(d)"),
                ("Max", "Max(val1, val2)"),
                ("Min", "Min(val1, val2)"),
                ("Pow", "Pow(x, y)"),
                ("Round", "Round(value, digits)"),
                ("Sign", "Sign(value)"),
                ("Sin", "Sin(a)"),
                ("Sinh", "Sinh(value)"),
                ("Sqrt", "Sqrt(d)"),
                ("Tan", "Tan(a)"),
                ("Tanh", "Tanh(value)"),
                ("Truncate", "Truncate(d)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.SByte":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Single":
            return ([
                ("IsInfinity", "IsInfinity(f)"),
                ("IsNaN", "IsNaN(f)"),
                ("IsNegativeInfinity", "IsNegativeInfinity(f)"),
                ("IsPositiveInfinity", "IsPositiveInfinity(f)"),
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.String":
            return ([
                ("Compare", "Compare(strA, strB, ignoreCase)"),
                ("CompareOrdinal", "CompareOrdinal(strA, strB)"),
                ("Concat", "Concat(values)"),
                ("Copy", "Copy(str)"),
                ("Equals", "Equals(a, b)"),
                ("Format", "Format(format, args)"),
                ("Intern", "Intern(str)"),
                ("IsInterned", "IsInterned(str)"),
                ("IsNullOrEmpty", "IsNullOrEmpty(value)"),
                ("Join", "Join(separator, value)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.StringComparer":
            return ([
                ("Create", "Create(culture, ignoreCase)"),
                ("CurrentCulture", "CurrentCulture"),
                ("CurrentCultureIgnoreCase", "CurrentCultureIgnoreCase"),
                ("InvariantCulture", "InvariantCulture"),
                ("InvariantCultureIgnoreCase", "InvariantCultureIgnoreCase"),
                ("Ordinal", "Ordinal"),
                ("OrdinalIgnoreCase", "OrdinalIgnoreCase"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.Text.RegularExpressions.Regex":
            return ([
                ("CacheSize", "CacheSize"),
                ("CompileToAssembly", "CompileToAssembly(regexinfos, assemblyname)"),
                ("Escape", "Escape(str)"),
                ("IsMatch", "IsMatch(input, pattern)"),
                ("Match", "Match(input, pattern)"),
                ("Matches", "Matches(input, pattern)"),
                ("Replace", "Replace(input, pattern, replacement)"),
                ("Split", "Split(input, pattern)"),
                ("Unescape", "Unescape(str)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.TimeSpan":
            return ([
                ("Compare", "Compare(t1, t2)"),
                ("Equals", "Equals(t1, t2)"),
                ("FromDays", "FromDays(value)"),
                ("FromHours", "FromHours(value)"),
                ("FromMilliseconds", "FromMilliseconds(value)"),
                ("FromMinutes", "FromMinutes(value)"),
                ("FromSeconds", "FromSeconds(value)"),
                ("FromTicks", "FromTicks(value)"),
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.UInt16":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.UInt32":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        elif staticType == "System.UInt64":
            return ([
                ("Parse", "Parse(s)"),
            ], sublime.INHIBIT_WORD_COMPLETIONS)
        else:
            return ([], sublime.INHIBIT_WORD_COMPLETIONS)


# Provide completions that match just after typing an opening angle bracket
class TagCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild on tag start
        if not view.match_selector(locations[0],
                "source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        # completions initially contains only MSBuild standard tasks/items
        completions = [
            # MSBuild Project Schema: http://msdn.microsoft.com/en-us/library/5dy88c2e
            ("Target", "Target Name=\"$1\" DependsOnTargets=\"$2\">\n\t$3\n</Target>"),
            ("OnError", "OnError ExecuteTargets=\"$1\" />"),
            ("ItemGroup [Empty]", "ItemGroup>\n\t$1\n</ItemGroup>"),
            ("ItemGroup [Full]", "ItemGroup>\n\t<${1:ItemName}\n\t\tInclude=\"$2\"\n\t\tExclude=\"$3\"\n\t\tKeepMetadata=\"$4\"\n\t\tRemoveMetadata=\"$5\"\n\t\tKeepDuplicates=\"${6:False}\" />\n</ItemGroup>"),
            ("PropertyGroup", "PropertyGroup>\n\t$1\n</PropertyGroup>"),
            ("UsingTask", "UsingTask TaskName=\"$1\" AssemblyFile=\"$2\" />"),
            ("ImportGroup", "ImportGroup Condition=\"$1\">\n\t<Import Project=\"$2\" />\n</ImportGroup>"),
            ("Import", "Import Project=\"$1\" />"),
            ("Choose", "Choose>\n\t<When Condition=\"$1\">$2</When>\n\t<Otherwise>$3</Otherwise>\n</Choose>"),
            ("When", "When Condition=\"$1\">$2</When>"),
            ("Otherwise", "Otherwise>$1</Otherwise>"),
            ("Project", "Project DefaultTargets=\"$1\" InitialTargets=\"$2\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\" ToolsVersion=\"4.0\">\n\t$3\n</Project>"),

            # Common MSBuild Project Items: http://msdn.microsoft.com/en-us/library/bb629388
            ("Reference [Item]", "Reference Include=\"${1:MyAssembly, Version=0.0.0.0, Culture=neutral, PublicKeyToken=0000000000000000, processorArchitecture=MSIL}\">\n\t<HintPath>$2</HintPath>\n\t<Name>$3</Name>\n\t<FusionName>$4</FusionName>\n\t<SpecificVersion>${5:False}</SpecificVersion>\n\t<Aliases>$6</Aliases>\n\t<Private>${7:False}</Private>\n</Reference>"),
            ("COMReference [Item]", "COMReference Include=\"$1\">\n\t<Name>$2</Name>\n\t<Guid>$3</Guid>\n\t<VersionMajor>$4</VersionMajor>\n\t<VersionMinor>$5</VersionMinor>\n\t<LCID>$6</LCID>\n\t<WrapperTool>${7:TLBImp}</WrapperTool>\n\t<Isolated>$8</Isolated>\n<COMReference>"),
            ("COMFileReference [Item]", "COMFileReference Include=\"$1\">\n\t<WrapperTool>${2:TLBImp}</WrapperTool>\n<COMFileReference>"),
            ("NativeReference [Item]", "NativeReference Include=\"$1\">\n\t<HintPath>$2</HintPath>\n\t<Name>$3</Name>\n</NativeReference>"),
            ("ProjectReference [Item]", "ProjectReference Include=\"$1\">\n\t<Name>$2</Name>\n\t<Project>$3</Project>\n\t<Package>$4</Package>\n</ProjectReference>"),
            ("Compile [Item]", "Compile Include=\"$1\">\n\t<DependentUpon>$2</DependentUpon>\n\t<AutoGen>${3:False}</AutoGen>\n\t<Link>$4</Link>\n\t<Visible>${5:True}</Visible>\n\t<CopyToOutputDirectory>${6:False}</CopyToOutputDirectory>\n</Compile>"),
            ("EmbeddedResource [Item]", "EmbeddedResource Include=\"$1\">\n\t<DependentUpon>$2</DependentUpon>\n\t<Generator>$3</Generator>\n\t<LastGenOutput>$4</LastGenOutput>\n\t<CustomToolNamespace>$5</CustomToolNamespace>\n\t<Link>$6</Link>\n\t<Visible>${7:True}</Visible>\n\t<CopyToOutputDirectory>${8:False}</CopyToOutputDirectory>\n\t<LogicalName>$9</LogicalName>\n</EmbeddedResource>"),
            ("Content [Item]", "Content Include=\"$1\">\n\t<DependentUpon>$2</DependentUpon>\n\t<Generator>$3</Generator>\n\t<LastGenOutput>$4</LastGenOutput>\n\t<CustomToolNamespace>$5</CustomToolNamespace>\n\t<Link>$6</Link>\n\t<PublishState>${7:Default}</PublishState>\n\t<IsAssembly>$8</IsAssembly>\n\t<Visible>${9:True}</Visible>\n\t<CopyToOutputDirectory>${10:False}</CopyToOutputDirectory>\n</Content>"),
            ("None [Item]", "None Include=\"$1\">\n\t<DependentUpon>$2</DependentUpon>\n\t<Generator>$3</Generator>\n\t<LastGenOutput>$4</LastGenOutput>\n\t<CustomToolNamespace>$5</CustomToolNamespace>\n\t<Link>$6</Link>\n\t<Visible>${7:True}</Visible>\n\t<CopyToOutputDirectory>${8:False}</CopyToOutputDirectory>\n</None>"),

            # Task-Specific Project Items
            # BootstrapperItem is used by GenerateBootstrapper
            ("BootstrapperItem [Item]", "BootstrapperItem Include=\"$1\" Exclude=\"$2\">\n\t<ProductName>$3</ProductName>\n</BootstrapperItem>"),
            # TypeLibNames and TypeLibFiles are used by ResolveComReference
            ("TypeLibName [Item]", "TypeLibName Include=\"$1\">\n\t<GUID>$2</GUID>\n\t<VersionMajor>$3</VersionMajor>\n\t<VersionMinor>$4</VersionMinor>\n\t<LocaleIdentifier>$5</LocaleIdentifier>\n\t<WrapperTool>${6:TLBImp}</WrapperTool>\n</TypeLibName>"),
            ("TypeLibFile [Item]", "TypeLibFile Include=\"$1\" Exclude=\"$2\">\n\t<WrapperTool>${3:TLBImp}</WrapperTool>\n</TypeLibFile>"),
            # ApplicationManifestItem is used by GenerateApplicationManifest
            ("ApplicationManifestItem [Item]", "ApplicationManifestItem Include=\"$1\">\n\t<DependencyType>${2:Install}</DependencyType>\n\t<AssemblyType>${3:Unspecified}</AssemblyType>\n\t<Group>$4</Group>\n\t<TargetPath>$5</TargetPath>\n\t<IsDataFile>${6:False}</IsDataFile>\n</ApplicationManifestItem>"),

            # MSBuild Tasks: http://msdn.microsoft.com/en-us/library/7z253716
            ("AL", "AL\n\tAlgorithmID=\"${1:CALG_SHA1}\"\n\tBaseAddress=\"$2\"\n\tCompanyName=\"${3:MyCompany}\"\n\tConfiguration=\"$4\"\n\tCopyright=\"$5\"\n\tCulture=\"${6:en-US}\"\n\tDelaySign=\"${7:False}\"\n\tDescription=\"$8\"\n\tEmbedResources=\"${9:@(EmbeddedResource)}\"\n\tEvidenceFile=\"${10:Security.Evidence}\"\n\tFileVersion=\"${11:1.0.0.0}\"\n\tFlags=\"${12:0x0000}\"\n\tGenerateFullPaths=\"${13:False}\"\n\tKeyContainer=\"${14:KeyPair}\"\n\tKeyFile=\"${15:StrongNameKey.snk}\"\n\tLinkResources=\"${16:@(ResFile)}\"\n\tMainEntryPoint=\"${17:App.Main}\"\n\tPlatform=\"${18:anycpu}\"\n\tProductName=\"${19:MyProduct}\"\n\tProductVersion=\"${20:1.0.0.0}\"\n\tResponseFiles=\"${21:@(ResponseFile)}\"\n\tSdkToolsPath=\"$22\"\n\tSourceModules=\"${23:@(SourceModule)}\"\n\tTargetType=\"${24:library}\"\n\tTemplateFile=\"${25:Template.dll}\"\n\tTimeout=\"$26\"\n\tTitle=\"${27:AssemblyTitle}\"\n\tToolPath=\"${28:Path\\To\\Al\\Folder}\"\n\tTrademark=\"$29\"\n\tVersion=\"${30:1.0.0.0}\"\n\tWin32Icon=\"${31:icon.ico}\"\n\tWin32Resource=\"${32:resources.res}\">\n\t<Output TaskParameter=\"OutputAssembly\" ItemName=\"$33\" />\n\t<Output TaskParameter=\"ExitCode\" PropertyName=\"$34\" />\n</AL>"),
            ("AspNetCompiler", "AspNetCompiler\n\tAllowPartiallyTrustedCallers=\"${1:True}\"\n\tClean=\"${2:False}\"\n\tDebug=\"${3:False}\"\n\tDelaySign=\"${4:False}\"\n\tFixedNames=\"${5:False}\"\n\tForce=\"${6:False}\"\n\tKeyContainer=\"${7:KeyPair}\"\n\tKeyFile=\"${8:StrongNameKey.snk}\"\n\tMetabasePath=\"${9:LM/W3SVC/1/ROOT}\"\n\tPhysicalPath=\"${10:C:\\inetpub\\wwwroot}\"\n\tTargetFrameworkMoniker=\"${11:.NETFramework,Version=v4.0}\"\n\tTargetPath=\"${12:Destination\\Folder}\"\n\tUpdateable=\"${13:False}\"\n\tVirtualPath=\"${14:/Virtual/App/Path}\" />"),
            ("AssignCulture", "AssignCulture Files=\"${1:@(InputFile)}\">\n\t<Output TaskParameter=\"AssignedFiles\" ItemName=\"$2\" />\n\t<Output TaskParameter=\"AssignedFilesWithCulture\" ItemName=\"$3\" />\n\t<Output TaskParameter=\"AssignedFilesWithNoCulture\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"CultureNeutralAssignedFiles\" ItemName=\"$5\" />\n</AssignCulture>"),
            ("AssignProjectConfiguration", "AssignProjectConfiguration\n\tCurrentProjectConfiguration=\"$1\"\n\tCurrentProjectPlatform=\"$2\"\n\tDefaultToVcxPlatformMapping=\"$3\"\n\tOnlyReferenceAndBuildProjectsEnabledInSolutionConfiguration=\"$4\"\n\tOutputType=\"$5\"\n\tResolveConfigurationPlatformUsingMappings=\"$6\"\n\tShouldUnsetParentConfigurationAndPlatform=\"$7\"\n\tSolutionConfigurationContents=\"$8\"\n\tVcxToDefaultPlatformMapping=\"$9\">\n\t<Output TaskParameter=\"AssignedProjects\" ItemName=\"$10\" />\n\t<Output TaskParameter=\"UnassignedProjects\" ItemName=\"$11\" />\n</AssignProjectConfiguration>"),
            ("AssignTargetPath", "AssignTargetPath RootFolder=\"$1\" Files=\"${2:@(InputFile)}\">\n\t<Output TaskParameter=\"AssignedFiles\" ItemName=\"$3\" />\n</AssignTargetPath>"),
            ("CallTarget [Simple]", "CallTarget Targets=\"$1\" />"),
            ("CallTarget [Full]", "CallTarget Targets=\"$1\" RunEachTargetSeparately=\"${2:False}\" UseResultsCache=\"${3:False}\">\n\t<Output TaskParameter=\"TargetOutputs\" ItemName=\"$4\" />\n</CallTarget>"),
            ("CombinePath", "CombinePath BasePath=\"$1\" Paths=\"${2:@(Path)}\">\n\t<Output TaskParameter=\"CombinedPaths\" ItemName=\"$3\" />\n</CombinePath>"),
            ("ConvertToAbsolutePath", "ConvertToAbsolutePath Paths=\"${1:@(Path)}\">\n\t<Output TaskParameter=\"AbsolutePaths\" ItemName=\"$2\" />\n</ConvertToAbsolutePath>"),
            ("Copy [Simple]", "Copy SourceFiles=\"${1:@(SourceFile)}\" DestinationFiles=\"${2:@(SourceFile->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\" DestinationFolder=\"$3\" />"),
            ("Copy [Full]", "Copy\n\tDestinationFiles=\"${1:@(SourceFile->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\"\n\tDestinationFolder=\"$2\"\n\tOverwriteReadOnlyFiles=\"${3:False}\"\n\tRetries=\"${4:0}\"\n\tRetryDelayMilliseconds=\"${5:1000}\"\n\tSkipUnchangedFiles=\"${6:False}\"\n\tSourceFiles=\"${7:@(SourceFile)}\"\n\tUseHardlinksIfPossible=\"${8:False}\">\n\t<Output TaskParameter=\"CopiedFiles\" ItemName=\"$9\" />\n</Copy>"),
            ("CreateCSharpManifestResourceName", "CreateCSharpManifestResourceName ResourceFiles=\"$1\" RootNamespace=\"$2\" PrependCultureAsDirectory=\"${3:True}\">\n\t<Output TaskParameter=\"ManifestResourceNames\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"ResourceFilesWithManifestResourceNames\" ItemName=\"$5\" />\n</CreateCSharpManifestResourceName>"),
            ("CreateItem [Simple]", "CreateItem Include=\"$1\" Exclude=\"$2\">\n\t<Output TaskParameter=\"Include\" ItemName=\"$3\" />\n</CreateItem>"),
            ("CreateItem [Full]", "CreateItem Include=\"$1\"\n\tExclude=\"$2\"\n\tAdditionalMetadata=\"$3\"\n\tPreserveExistingMetadata=\"${4:True}\">\n\t<Output TaskParameter=\"Include\" ItemName=\"$5\" />\n</CreateItem>"),
            ("CreateProperty", "CreateProperty Value=\"$1\">\n\t<Output TaskParameter=\"Value\" PropertyName=\"$2\" />\n</CreateProperty>"),
            ("CreateVisualBasicManifestResourceName", "CreateVisualBasicManifestResourceName ResourceFiles=\"$1\" RootNamespace=\"$2\" PrependCultureAsDirectory=\"${3:True}\">\n\t<Output TaskParameter=\"ManifestResourceNames\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"ResourceFilesWithManifestResourceNames\" ItemName=\"$5\" />\n</CreateVisualBasicManifestResourceName>"),
            ("Csc", "Csc\n\tAdditionalLibPaths=\"${1:@(LibPath)}\"\n\tAddModules=\"$2\"\n\tAllowUnsafeBlocks=\"${3:False}\"\n\tApplicationConfiguration=\"${4:App.config}\"\n\tBaseAddress=\"$5\"\n\tCheckForOverflowUnderflow=\"${6:False}\"\n\tCodePage=\"$7\"\n\tDebugType=\"${8:full}\"\n\tDefineConstants=\"${9:CODE_ANALYSIS}\"\n\tDelaySign=\"${10:False}\"\n\tDisabledWarnings=\"$11\"\n\tDocumentationFile=\"${12:MyProject.xml}\"\n\tEmitDebugInformation=\"${13:True}\"\n\tErrorReport=\"${14:prompt}\"\n\tFileAlignment=\"$15\"\n\tGenerateFullPaths=\"${16:False}\"\n\tKeyContainer=\"${17:KeyPair}\"\n\tKeyFile=\"${18:StrongNameKey.snk}\"\n\tLangVersion=\"${19:default}\"\n\tLinkResources=\"${20:@(ResFile)}\"\n\tMainEntryPoint=\"${21:App.Main}\"\n\tModuleAssemblyName=\"$22\"\n\tNoConfig=\"${23:False}\"\n\tNoLogo=\"${24:True}\"\n\tNoStandardLib=\"${25:False}\"\n\tNoWin32Manifest=\"${26:False}\"\n\tOptimize=\"${27:True}\"\n\tOutputAssembly=\"${28:MyProject.dll}\"\n\tPdbFile=\"${29:MyProject.pdb}\"\n\tPlatform=\"${30:anycpu}\"\n\tReferences=\"${31:@(Reference)}\"\n\tResources=\"${32:@(EmbeddedResource)}\"\n\tResponseFiles=\"$33\"\n\tSources=\"${34:@(Compile)}\"\n\tTargetType=\"${35:library}\"\n\tTreatWarningsAsErrors=\"${36:False}\"\n\tUtf8Output=\"${37:False}\"\n\tWarningLevel=\"${38:4}\"\n\tWarningsAsErrors=\"$39\"\n\tWarningsNotAsErrors=\"$40\"\n\tWin32Icon=\"${41:icon.ico}\"\n\tWin32Manifest=\"${42:file.manifest}\"\n\tWin32Resource=\"${43:resources.res}\" />"),
            ("Delete [Simple]", "Delete Files=\"${1:@(File)}\" />"),
            ("Delete [Full]", "Delete Files=\"${1:@(File)}\" TreatErrorsAsWarnings=\"${2:False}\">\n\t<Output TaskParameter=\"DeletedFiles\" ItemName=\"$3\" />\n</Delete>"),
            ("Error [Simple]", "Error Text=\"$1\" />"),
            ("Error [Full]", "Error Code=\"${1:1}\" File=\"$2\" HelpKeyword=\"$3\" Text=\"$4\" />"),
            ("Exec [Simple]", "Exec Command=\"$1\" WorkingDirectory=\"$2\" />"),
            ("Exec [Full]", "Exec\n\tCommand=\"$1\"\n\tCustomErrorRegularExpression=\"$2\"\n\tCustomWarningRegularExpression=\"$3\"\n\tIgnoreExitCode=\"${4:False}\"\n\tIgnoreStandardErrorWarningFormat=\"${5:False}\"\n\tStdErrEncoding=\"$6\"\n\tStdOutEncoding=\"$7\"\n\tWorkingDirectory=\"$8\">\n\t<Output TaskParameter=\"ExitCode\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"Outputs\" ItemName=\"$10\" />\n</Exec>"),
            ("FindAppConfigFile", "FindAppConfigFile\n\tPrimaryList=\"${1:@(Primary)}\"\n\tSecondaryList=\"${2:@(Secondary)}\"\n\tTargetPath=\"$3\">\n\t<Output TaskParameter=\"AppConfigFile\" ItemName=\"$4\" />\n</FindAppConfigFile>"),
            ("FindInList", "FindInList\n\tCaseSensitive=\"${1:True}\"\n\tFindLastMatch=\"${2:False}\"\n\tItemSpecToFind=\"$3\"\n\tList=\"${4:@(InputFile)}\"\n\tMatchFileNameOnly=\"${5:True}\">\n\t<Output TaskParameter=\"ItemFound\" ItemName=\"$6\" />\n</FindInList>"),
            ("FindUnderPath", "FindUnderPath Files=\"${1:@(InputFile)}\" Path=\"$2\" UpdateToAbsolutePaths=\"${3:False}\">\n\t<Output TaskParameter=\"InPath\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"OutOfPath\" ItemName=\"$5\" />\n</FindUnderPath>"),
            ("FormatUrl", "FormatUrl InputUrl=\"$1\">\n\t<Output TaskParameter=\"OutputUrl\" PropertyName=\"$2\" />\n</FormatUrl>"),
            ("FormatVersion", "FormatVersion FormatType=\"${1:Version}\" Version=\"$2\" Revision=\"$3\">\n\t<Output TaskParameter=\"OutputVersion\" PropertyName=\"$4\" />\n</FormatVersion>"),
            ("GenerateApplicationManifest", "GenerateApplicationManifest\n\tAssemblyName=\"$1\"\n\tAssemblyVersion=\"${2:1.0.0.0}\"\n\tClrVersion=\"$3\"\n\tConfigFile=\"${4:App.config}\"\n\tDependencies=\"${5:@(ApplicationManifestDependency)}\"\n\tDescription=\"$6\"\n\tEntryPoint=\"$7\"\n\tErrorReportUrl=\"${8:http://}\"\n\tFileAssociations=\"${9:@(FileType)}\"\n\tFiles=\"${10:@(InputFile)}\"\n\tHostInBrowser=\"${11:False}\"\n\tIconFile=\"${12:icon.ico}\"\n\tInputManifest=\"$13\"\n\tIsolatedComReferences=\"${14:@(ComReference)}\"\n\tManifestType=\"${15:ClickOnce}\"\n\tMaxTargetPath=\"${16:0}\"\n\tOSVersion=\"${17:6.1.0.0}\"\n\tPlatform=\"${18:AnyCPU}\"\n\tProduct=\"$19\"\n\tPublisher=\"$20\"\n\tRequiresMinimumFramework35SP1=\"${21:True}\"\n\tTargetCulture=\"$22\"\n\tTargetFrameworkMoniker=\"${23:.NETFramework,Version=v4.0}\"\n\tTargetFrameworkProfile=\"$24\"\n\tTargetFrameworkSubset=\"$25\"\n\tTargetFrameworkVersion=\"${26:4.0.30319}\"\n\tTrustInfoFile=\"$27\"\n\tUseApplicationTrust=\"${28:True}\">\n\t<Output TaskParameter=\"OutputManifest\" ItemName=\"$29\" />\n</GenerateApplicationManifest>"),
            ("GenerateBootstrapper", "GenerateBootstrapper\n\tApplicationFile=\"${1:MyApplication.application}\"\n\tApplicationName=\"${2:MyApplication}\"\n\tApplicationRequiresElevation=\"${3:True}\"\n\tApplicationUrl=\"${4:http://}\"\n\tBootstrapperItems=\"${5:@(BootstrapperItem)}\"\n\tBootstrapperKeyFile=\"${6:setup.exe}\"\n\tComponentsLocation=\"${7:HomeSite}\"\n\tComponentsUrl=\"${8:http://}\"\n\tCopyComponents=\"${9:True}\"\n\tCulture=\"$10\"\n\tFallbackCulture=\"$11\"\n\tOutputPath=\"${12:Path\\To\\Output}\"\n\tPath=\"${13:Path\\To\\Prerequisites}\"\n\tSupportUrl=\"${14:http://}\"\n\tValidate=\"${15:False}\">\n\t<Output TaskParameter=\"BootstrapperComponentFiles\" PropertyName=\"$16\" />\n</GenerateBootstrapper>"),
            ("GenerateDeploymentManifest", "GenerateDeploymentManifest\n\tAssemblyName=\"$1\"\n\tAssemblyVersion=\"${2:1.0.0.0}\"\n\tCreateDesktopShortcut=\"${3:False}\"\n\tDeploymentUrl=\"${4:http://}\"\n\tDescription=\"$5\"\n\tDisallowUrlActivation=\"${6:False}\"\n\tEntryPoint=\"${7:@(EntryPoint)}\"\n\tErrorReportUrl=\"${8:http://}\"\n\tInputManifest=\"$9\"\n\tInstall=\"${10:True}\"\n\tMapFileExtensions=\"${11:False}\"\n\tMaxTargetPath=\"${12:0}\"\n\tMinimumRequiredVersion=\"${13:1.0.0.0}\"\n\tPlatform=\"${14:AnyCPU}\"\n\tProduct=\"$15\"\n\tPublisher=\"$16\"\n\tSuiteName=\"${17:My Start Menu Folder}\"\n\tSupportUrl=\"${18:http://}\"\n\tTargetCulture=\"$19\"\n\tTrustUrlParameters=\"${20:False}\"\n\tUpdateEnabled=\"${21:False}\"\n\tUpdateInterval=\"${22:0}\"\n\tUpdateMode=\"${23:Background}\"\n\tUpdateUnit=\"${24:Hours}\">\n\t<Output TaskParameter=\"OutputManifest\" ItemName=\"$25\" />\n</GenerateDeploymentManifest>"),
            ("GenerateResource", "GenerateResource\n\tAdditionalInputs=\"${1:@(AdditionalInput)}\"\n\tEnvironmentVariables=\"$2\"\n\tExcludedInputPaths=\"${3:@(ExcludedPath)}\"\n\tExecuteAsTool=\"${4:True}\"\n\tMinimalRebuildFromTracking=\"${5:True}\"\n\tNeverLockTypeAssemblies=\"${6:False}\"\n\tPublicClass=\"${7:False}\"\n\tReferences=\"${8:@(Reference)}\"\n\tSdkToolsPath=\"$9\"\n\tSources=\"${10:@(SourceResx)}\"\n\tStateFile=\"$11\"\n\tStronglyTypedClassName=\"$12\"\n\tStronglyTypedFilename=\"$13\"\n\tStronglyTypedLanguage=\"${14:C#}\"\n\tStronglyTypedManifestPrefix=\"$15\"\n\tStronglyTypedNamespace=\"$16\"\n\tToolArchitecture=\"${17:ManagedIL}\"\n\tTrackerFrameworkPath=\"$18\"\n\tTrackerLogDirectory=\"$19\"\n\tTrackerSdkPath=\"$20\"\n\tTrackFileAccess=\"${21:True}\"\n\tUseSourcePath=\"${22:False}\">\n\t<Output TaskParameter=\"FilesWritten\" ItemName=\"$23\" />\n\t<Output TaskParameter=\"OutputResources\" ItemName=\"$24\" />\n</GenerateResource>"),
            ("GenerateTrustInfo", "GenerateTrustInfo\n\tApplicationDependencies=\"${1:@(Dependncy)}\"\n\tBaseManifest=\"$2\"\n\tExcludedPermissions=\"$3\"\n\tTargetZone=\"${4:Internet}\">\n\t<Output TaskParameter=\"TrustInfoFile\" ItemName=\"$5\" />\n</GenerateTrustInfo>"),
            ("GetAssemblyIdentity", "GetAssemblyIdentity AssemblyFiles=\"${1:@(InputAssembly)}\">\n\t<Output TaskParameter=\"Assemblies\" ItemName=\"$2\" />\n</GetAssemblyIdentity>"),
            ("GetFrameworkPath", "GetFrameworkPath>\n\t<Output TaskParameter=\"FrameworkVersion11Path\" PropertyName=\"$1\" />\n\t<Output TaskParameter=\"FrameworkVersion20Path\" PropertyName=\"$2\" />\n\t<Output TaskParameter=\"FrameworkVersion30Path\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"FrameworkVersion35Path\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"FrameworkVersion40Path\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"Path\" PropertyName=\"$6\" />\n</GetFrameworkPath>"),
            ("GetFrameworkSdkPath", "GetFrameworkSdkPath>\n\t<Output TaskParameter=\"FrameworkVersion20Path\" PropertyName=\"$1\" />\n\t<Output TaskParameter=\"FrameworkVersion35Path\" PropertyName=\"$2\" />\n\t<Output TaskParameter=\"FrameworkVersion40Path\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"Path\" PropertyName=\"$4\" />\n</GetFrameworkSdkPath>"),
            ("GetReferenceAssemblyPaths", "GetReferenceAssemblyPaths\n\tTargetFrameworkMoniker=\"${1:.NETFramework,Version=v4.0}\"\n\tRootPath=\"$2\"\n\tBypassFrameworkInstallChecks=\"${3:False}\">\n\t<Output TaskParameter=\"ReferenceAssemblyPaths\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"FullFrameworkReferenceAssemblyPaths\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"TargetFrameworkMonikerDisplayName\" PropertyName=\"$6\" />\n</GetReferenceAssemblyPaths>"),
            ("LC", "LC\n\tLicenseTarget=\"${1:MyApp.exe}\"\n\tNoLogo=\"${2:True}\"\n\tOutputDirectory=\"$3\"\n\tReferencedAssemblies=\"${4:@(Reference)}\"\n\tSdkToolsPath=\"$5\"\n\tSources=\"${6:@(LicensedComponent)}\">\n\t<Output TaskParameter=\"OutputLicense\" ItemName=\"$7\" />\n</LC>"),
            ("MakeDir [Simple]", "MakeDir Directories=\"$1\" />"),
            ("MakeDir [Full]", "MakeDir Directories=\"$1\">\n\t<Output TaskParameter=\"DirectoriesCreated\" ItemName=\"$2\" />\n</MakeDir>"),
            ("Message [Simple]", "Message Text=\"$1\" />"),
            ("Message [Full]", "Message Text=\"$1\" Importance=\"${2:normal}\" />"),
            ("Move [Simple]", "Move SourceFiles=\"${1:@(SourceFile)}\" DestinationFiles=\"${2:@(SourceFile->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\" DestinationFolder=\"$3\" />"),
            ("Move [Full]", "Move\n\tDestinationFiles=\"${1:@(SourceFile->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\"\n\tDestinationFolder=\"$2\"\n\tOverwriteReadOnlyFiles=\"${3:False}\"\n\tSourceFiles=\"${4:@(SourceFile)}\">\n\t<Output TaskParameter=\"MovedFiles\" ItemName=\"$5\" />\n</Move>"),
            ("MSBuild [Simple]", "MSBuild Projects=\"${1:@(InputProject)}\" Targets=\"$2\" Properties=\"$3\" />"),
            ("MSBuild [Full]", "MSBuild\n\tBuildInParallel=\"${1:False}\"\n\tProjects=\"${2:@(InputProject)}\"\n\tProperties=\"$3\"\n\tRebaseOutputs=\"${4:False}\"\n\tRemoveProperties=\"$5\"\n\tRunEachTargetSeparately=\"${6:True}\"\n\tSkipNonexistentProjects=\"${7:False}\"\n\tStopOnFirstFailure=\"${8:False}\"\n\tTargetAndPropertyListSeparators=\"$9\"\n\tTargets=\"$10\"\n\tToolsVersion=\"${11:4.0}\"\n\tUnloadProjectsOnCompletion=\"${12:False}\"\n\tUseResultsCache=\"${13:True}\">\n\t<Output TaskParameter=\"TargetOutputs\" ItemName=\"$14\" />\n</MSBuild>"),
            ("ReadLinesFromFile", "ReadLinesFromFile File=\"$1\">\n\t<Output TaskParameter=\"Lines\" ItemName=\"$2\" />\n</ReadLinesFromFile>"),
            ("RegisterAssembly", "RegisterAssembly\n\tAssemblies=\"${1:@(InputAssembly)}\"\n\tAssemblyListFile=\"$2\"\n\tCreateCodeBase=\"${3:False}\">\n\t<Output TaskParameter=\"TypeLibFiles\" ItemName=\"$4\" />\n</RegisterAssembly>"),
            ("RemoveDir [Simple]", "RemoveDir Directories=\"$1\" />"),
            ("RemoveDir [Full]", "RemoveDir Directories=\"$1\">\n\t<Output TaskParameter=\"RemovedDirectories\" ItemName=\"$2\" />\n</RemoveDir>"),
            ("RemoveDuplicates", "RemoveDuplicates Inputs=\"${1:@(InputItem)}\">\n\t<Output TaskParameter=\"Filtered\" ItemName=\"$2\" />\n</RemoveDuplicates>"),
            ("RequiresFramework35SP1Assembly", "RequiresFramework35SP1Assembly\n\tAssemblies=\"${1:@(InputAssembly)}\"\n\tCreateDesktopShortcut=\"${2:False}\"\n\tDeploymentManifestEntryPoint=\"${3:app.manifest}\"\n\tEntryPoint=\"${4:App.exe}\"\n\tErrorReportUrl=\"${5:http://}\"\n\tFiles=\"${6:@(DeployedFile)}\"\n\tReferencedAssemblies=\"${7:@(Reference)}\"\n\tSuiteName=\"${8:My Start Menu Folder}\"\n\tTargetFrameworkVersion=\"${9:4.0}\">\n\t<Output TaskParameter=\"RequiresMinimumFramework35SP1\" PropertyName=\"$10\" /> \n\t<Output TaskParameter=\"SigningManifests\" PropertyName=\"$11\" />\n</RequiresFramework35SP1Assembly>"),
            ("ResolveAssemblyReference", "ResolveAssemblyReference\n\tAllowedAssemblyExtensions=\"$1\"\n\tAllowedRelatedFileExtensions=\"$2\"\n\tAppConfigFile=\"$3\"\n\tAssemblies=\"${4:@(Reference)}\"\n\tAssemblyFiles=\"${5:@(AssemblyFile)}\"\n\tAutoUnify=\"${6:False}\"\n\tCandidateAssemblyFiles=\"$7\"\n\tCopyLocalDependenciesWhenParentReferenceInGac=\"${8:True}\"\n\tFindDependencies=\"${9:True}\"\n\tFindRelatedFiles=\"${10:True}\"\n\tFindSatellites=\"${11:True}\"\n\tFindSerializationAssemblies=\"${12:True}\"\n\tFullFrameworkAssemblyTables=\"$13\"\n\tFullFrameworkFolders=\"$14\"\n\tFullTargetFrameworkSubsetNames=\"$15\"\n\tIgnoreDefaultInstalledAssemblyTables=\"${16:False}\"\n\tIgnoreDefaultInstalledAssemblySubsetTables=\"${17:False}\"\n\tInstalledAssemblySubsetTables=\"${18:@(SubsetTable)}\"\n\tInstalledAssemblyTables=\"${19:@(AssemblyTable)}\"\n\tLatestTargetFrameworkDirectories=\"$20\"\n\tProfileName=\"$21\"\n\tSearchPaths=\"$22\"\n\tSilent=\"${23:False}\"\n\tStateFile=\"$24\"\n\tTargetedRuntimeVersion=\"${25:4.0.30319}\"\n\tTargetFrameworkDirectories=\"$26\"\n\tTargetFrameworkMoniker=\"${27:.NETFramework,Version=v4.0}\"\n\tTargetFrameworkMonikerDisplayName=\"${28:.NET 4.0}\"\n\tTargetFrameworkSubsets=\"$29\"\n\tTargetFrameworkVersion=\"${30:4.0.30319}\"\n\tTargetProcessorArchitecture=\"$31\">\n\t<Output TaskParameter=\"CopyLocalFiles\" ItemName=\"$32\" />\n\t<Output TaskParameter=\"FilesWritten\" ItemName=\"$33\" />\n\t<Output TaskParameter=\"RelatedFiles\" ItemName=\"$34\" />\n\t<Output TaskParameter=\"ResolvedDependencyFiles\" ItemName=\"$35\" />\n\t<Output TaskParameter=\"ResolvedFiles\" ItemName=\"$36\" />\n\t<Output TaskParameter=\"SatelliteFiles\" ItemName=\"$37\" />\n\t<Output TaskParameter=\"ScatterFiles\" ItemName=\"$38\" />\n\t<Output TaskParameter=\"SerializationAssemblyFiles\" ItemName=\"$39\" />\n\t<Output TaskParameter=\"SuggestedRedirects\" ItemName=\"$40\" />\n</ResolveAssemblyReference>"),
            ("ResolveComReference", "ResolveComReference\n\tDelaySign=\"${1:False}\"\n\tEnvironmentVariables=\"$2\"\n\tExecuteAsTool=\"${3:True}\"\n\tIncludeVersionInInteropName=\"${4:False}\"\n\tKeyContainer=\"${5:KeyPair}\"\n\tKeyFile=\"${6:StrongNameKey.snk}\"\n\tNoClassMembers=\"${7:False}\"\n\tSdkToolsPath=\"$8\"\n\tStateFile=\"$9\"\n\tTargetFrameworkVersion=\"$10\"\n\tTargetProcessorArchitecture=\"${11:MSIL}\"\n\tTypeLibFiles=\"${12:@(TypeLibFile)}\"\n\tTypeLibNames=\"${13:@(TypeLibName)}\"\n\tWrapperOutputDirectory=\"$14\">\n\t<Output TaskParameter=\"ResolvedAssemblyReferences\" ItemName=\"$15\" />\n\t<Output TaskParameter=\"ResolvedFiles\" ItemName=\"$16\" />\n\t<Output TaskParameter=\"ResolvedModules\" ItemName=\"$17\" />\n</ResolveComReference>"),
            ("ResolveKeySource", "ResolveKeySource\n\tAutoClosePasswordPromptShow=\"${1:15}\"\n\tAutoClosePasswordPromptTimeout=\"${2:20}\"\n\tCertificateFile=\"$3\"\n\tCertificateThumbprint=\"$4\"\n\tKeyFile=\"$5\"\n\tShowImportDialogDespitePreviousFailures=\"${6:False}\"\n\tSuppressAutoClosePasswordPrompt=\"${7:False}\">\n\t<Output TaskParameter=\"ResolvedKeyContainer\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"ResolvedKeyFile\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"ResolvedThumbprint\" PropertyName=\"$10\" />\n</ResolveKeySource>"),
            ("ResolveManifestFiles", "ResolveManifestFiles\n\tDeploymentManifestEntryPoint=\"${1:App.manifest}\"\n\tEntryPoint=\"$2\"\n\tExtraFiles=\"${3:@(ExtraFile)}\"\n\tManagedAssemblies=\"${4:@(ManagedAssembly)}\"\n\tNativeAssemblies=\"${5:@(NativeAssembly)}\"\n\tPublishFiles=\"${6:@(PublishFile)}\"\n\tSatelliteAssemblies=\"${7:@(SatelliteAssembly)}\"\n\tSigningManifests=\"${8:False}\"\n\tTargetCulture=\"$9\"\n\tTargetFrameworkVersion=\"${10:v4.0}\">\n\t<Output TaskParameter=\"OutputAssemblies\" ItemName=\"$11\" />\n\t<Output TaskParameter=\"OutputDeploymentManifestEntryPoint\" ItemName=\"$12\" />\n\t<Output TaskParameter=\"OutputEntryPoint\" ItemName=\"$13\" />\n\t<Output TaskParameter=\"OutputFiles\" ItemName=\"$14\" />\n</ResolveManifestFiles>"),
            ("ResolveNativeReference", "ResolveNativeReference\n\tAdditionalSearchPaths=\"$1\"\n\tNativeReferences=\"${2:@(NativeReference)}\">\n\t<Output TaskParameter=\"ContainedComComponents\" ItemName=\"$3\" />\n\t<Output TaskParameter=\"ContainedLooseEtcFiles\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"ContainedLooseTlbFiles\" ItemName=\"$5\" />\n\t<Output TaskParameter=\"ContainedPrerequisiteAssemblies\" ItemName=\"$6\" />\n\t<Output TaskParameter=\"ContainedTypeLibraries\" ItemName=\"$7\" />\n\t<Output TaskParameter=\"ContainingReferenceFiles\" ItemName=\"$8\" />\n</ResolveNativeReference>"),
            ("ResolveNonMSBuildProjectOutput", "ResolveNonMSBuildProjectOutput PreresolvedProjectOutputs=\"$1\">\n\t<Output TaskParameter=\"ProjectReferences\" ItemName=\"$2\" />\n\t<Output TaskParameter=\"ResolvedOutputPaths\" ItemName=\"$3\" />\n\t<Output TaskParameter=\"UnresolvedProjectReferences\" ItemName=\"$4\" />\n</ResolveNonMSBuildProjectOutput>"),
            ("SGen", "SGen\n\tBuildAssemblyName=\"$1\"\n\tBuildAssemblyPath=\"$2\"\n\tDelaySign=\"${3:False}\"\n\tKeyContainer=\"${4:KeyPair}\"\n\tKeyFile=\"${5:StrongNameKey.snk}\"\n\tPlatform=\"${6:anycpu}\"\n\tReferences=\"${7:@(Reference)}\"\n\tSdkToolsPath=\"$8\"\n\tSerializationAssemblyName=\"$9\"\n\tShouldGenerateSerializer=\"${10:False}\"\n\tTimeout=\"$11\"\n\tToolPath=\"$12\"\n\tTypes=\"$13\"\n\tUseProxyTypes=\"${14:False}\">\n\t<Output TaskParameter=\"SerializationAssembly\" ItemName=\"$15\" />\n</SGen>"),
            ("SignFile", "SignFile\n\tCertificateThumbprint=\"$1\"\n\tSigningTarget=\"$2\"\n\tTimestampUrl=\"$3\" />"),
            ("Touch [Simple]", "Touch Files=\"${1:@(InputFile)}\" />"),
            ("Touch [Full]", "Touch\n\tAlwaysCreate=\"${1:False}\"\n\tFiles=\"${2:@(InputFile)}\"\n\tForceTouch=\"${3:False}\"\n\tTime=\"$4\">\n\t<Output TaskParameter=\"TouchedFiles\" ItemName=\"$5\" />\n</Touch>"),
            ("UnregisterAssembly", "UnregisterAssembly\n\tAssemblies=\"${1:@(InputAssembly)}\"\n\tAssemblyListFile=\"$2\">\n\t<Output TaskParameter=\"TypeLibFiles\" ItemName=\"$3\" />\n</UnregisterAssembly>"),
            ("UpdateManifest", "UpdateManifest\n\tApplicationManifest=\"$1\"\n\tApplicationPath=\"$2\"\n\tInputManifest=\"$3\">\n\t<Output TaskParameter=\"OutputManifest\" ItemName=\"$4\" />\n</UpdateManifest>"),
            ("Vbc", "Vbc\n\tAdditionalLibPaths=\"${1:@(LibPath)}\"\n\tAddModules=\"$2\"\n\tBaseAddress=\"$3\"\n\tCodePage=\"$4\"\n\tDebugType=\"${5:full}\"\n\tDefineConstants=\"${6:CODE_ANALYSIS}\"\n\tDelaySign=\"${7:False}\"\n\tDisabledWarnings=\"$8\"\n\tDocumentationFile=\"${9:MyProject.xml}\"\n\tEmitDebugInformation=\"${10:True}\"\n\tErrorReport=\"${11:none}\"\n\tFileAlignment=\"$12\"\n\tGenerateDocumentation=\"${13:False}\"\n\tImports=\"${14:@(ImportNamespace)}\"\n\tKeyContainer=\"${15:KeyPair}\"\n\tKeyFile=\"${16:StrongNameKey.snk}\"\n\tLangVersion=\"${17:10}\"\n\tLinkResources=\"${18:@(ResFile)}\"\n\tMainEntryPoint=\"${19:App.Main}\"\n\tModuleAssemblyName=\"$20\"\n\tNoConfig=\"${21:False}\"\n\tNoLogo=\"${22:True}\"\n\tNoStandardLib=\"${23:False}\"\n\tNoVBRuntimeReference=\"${24:False}\"\n\tNoWarnings=\"${25:False}\"\n\tOptimize=\"${26:True}\"\n\tOptionCompare=\"${27:binary}\"\n\tOptionExplicit=\"${28:True}\"\n\tOptionInfer=\"${29:False}\"\n\tOptionStrict=\"${30:False}\"\n\tOptionStrictType=\"${31:custom}\"\n\tOutputAssembly=\"${32:MyProject.dll}\"\n\tPlatform=\"${33:anycpu}\"\n\tReferences=\"${34:@(Reference)}\"\n\tRemoveIntegerChecks=\"${35:False}\"\n\tResources=\"${36:@(EmbeddedResource)}\"\n\tResponseFiles=\"$37\"\n\tRootNamespace=\"$38\"\n\tSdkPath=\"$39\"\n\tSources=\"${40:@(Compile)}\"\n\tTargetCompactFramework=\"${41:False}\"\n\tTargetType=\"${42:library}\"\n\tTimeout=\"$43\"\n\tToolPath=\"$44\"\n\tTreatWarningsAsErrors=\"${45:False}\"\n\tUtf8Output=\"${46:False}\"\n\tVerbosity=\"${47:Normal}\"\n\tWarningsAsErrors=\"$48\"\n\tWarningsNotAsErrors=\"$49\"\n\tWin32Icon=\"${50:icon.ico}\"\n\tWin32Resource=\"${51:resources.res}\" />"),
            ("Warning [Simple]", "Warning Text=\"$1\" />"),
            ("Warning [Full]", "Warning Code=\"${1:1}\" File=\"$2\" HelpKeyword=\"$3\" Text=\"$4\" />"),
            ("WriteCodeFragment", "WriteCodeFragment\n\tAssemblyAttributes=\"${1:@(Attribute)}\"\n\tLanguage=\"${2:C#}\"\n\tOutputDirectory=\"$3\">\n\t<Output TaskParameter=\"OutputFile\" ItemName=\"$4\" />\n</WriteCodeFragment>"),
            ("WriteLinesToFile [Simple]", "WriteLinesToFile File=\"$1\" Lines=\"${2:@(Line)}\" />"),
            ("WriteLinesToFile [Full]", "WriteLinesToFile\n\tFile=\"$1\"\n\tLines=\"${2:@(Line)}\"\n\tOverwrite=\"${3:False}\"\n\tEncoding=\"${4:UTF-8}\" />"),
            ("XmlPeek", "XmlPeek\n\tNamespaces=\"${1:&lt;Namespace Prefix='tmp' Uri='http://tempuri.org' /&gt;}\"\n\tQuery=\"${2:/tmp:Node1/tmp:Node2/text()}\"\n\tXmlContent=\"$3\"\n\tXmlInputPath=\"${4:input.xml}\">\n\t<Output TaskParameter=\"Result\" ItemName=\"$5\" />\n</XmlPeek>"),
            ("XmlPoke", "XmlPoke\n\tNamespaces=\"${1:&lt;Namespace Prefix='tmp' Uri='http://tempuri.org' /&gt;}\"\n\tQuery=\"${2:/tmp:Node1/tmp:Node2/@attrib}\"\n\tValue=\"$3\"\n\tXmlInputPath=\"${4:input.xml}\" />"),
            ("XslTransformation", "XslTransformation\n\tOutputPaths=\"${1:@(OutputPath)}\"\n\tParameters=\"$2\"\n\tXmlContent=\"$3\"\n\tXmlInputPaths=\"${4:@(InputXmlFile)}\"\n\tXslCompiledDllPath=\"${5:CompiledXslt.dll}\"\n\tXslContent=\"$6\"\n\tXslInputPath=\"${7:input.xslt}\" />")
        ]

        # If MSBuild Community Tasks isn't imported, we're done.
        msbimport = view.find("((?i)<import\\s+project\\s*=\\s*\"([^\"]*msbuild.community.tasks.targets)\"[^>]*>)", 1)
        if msbimport is None or msbimport.empty():
            completions = sorted(completions, key=lambda completion: completion[0])
            return (completions, sublime.INHIBIT_WORD_COMPLETIONS)

        # MSBuild Community Tasks IS imported, so add those completions, too.
        # https://github.com/loresoft/msbuildtasks
        completions.extend([
            ("Add [MSBCT]", "Add Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Add>"),
            ("AddTnsName [MSBCT]", "AddTnsName\n\tAllowUpdates=\"${1:False}\"\n\tEntryName=\"$2\"\n\tEntryText=\"$3\"\n\tTnsNamesFile=\"$4\">\n\t<Output TaskParameter=\"ModifiedFile\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"ModifiedFileText\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"OriginalFileText\" PropertyName=\"$7\" />\n</AddTnsName>"),
            ("AppPoolController [MSBCT Simple]", "AppPoolController Action=\"${1:Recycle}\" ApplicationPoolName=\"$2\" />"),
            ("AppPoolController [MSBCT Full]", "AppPoolController\n\tAction=\"${1:Recycle}\"\n\tApplicationPoolName=\"$2\"\n\tHostHeaderName=\"$3\"\n\tPassword=\"$4\"\n\tServerName=\"${5:localhost}\"\n\tServerPort=\"${6:80}\"\n\tUsername=\"$7\" />"),
            ("AppPoolCreate [MSBCT]", "AppPoolCreate\n\tApplicationPoolName=\"$1\"\n\tAppPoolAutoStart=\"${2:True}\"\n\tAppPoolIdentityType=\"${3:2}\"\n\tAppPoolQueueLength=\"${4:1000}\"\n\tAutoShutdownAppPoolExe=\"$5\"\n\tAutoShutdownAppPoolParams=\"$6\"\n\tCPUAction=\"${7:-1}\"\n\tCPULimit=\"$8\"\n\tCPUResetInterval=\"${9:5}\"\n\tDisallowOverlappingRotation=\"${10:False}\"\n\tDisallowRotationOnConfigChange=\"${11:False}\"\n\tIdleTimeout=\"${12:20}\"\n\tLoadBalancerCapabilities=\"${13:2}\"\n\tLogEventOnRecycle=\"${14:0}\"\n\tLogonMethod=\"${15:-1}\"\n\tMaxProcesses=\"${16:1}\"\n\tOrphanActionExe=\"$17\"\n\tOrphanActionParams=\"$18\"\n\tOrphanWorkerProcess=\"${19:False}\"\n\tPeriodicRestartMemory=\"${20:0}\"\n\tPeriodicRestartPrivateMemory=\"${21:0}\"\n\tPeriodicRestartRequests=\"${22:0}\"\n\tPeriodicRestartSchedule=\"$23\"\n\tPeriodicRestartTime=\"${24:1740}\"\n\tPingingEnabled=\"${25:False}\"\n\tPingInterval=\"${26:30}\"\n\tPingResponseTime=\"${27:90}\"\n\tRapidFailProtection=\"${28:True}\"\n\tRapidFailProtectionInterval=\"${29:5}\"\n\tRapidFailProtectionMaxCrashes=\"${30:5}\"\n\tShutdownTimeLimit=\"${31:90}\"\n\tSMPAffinitized=\"${32:False}\"\n\tSMPProcessorAffinityMask=\"${33:4294967295}\"\n\tStartupTimeLimit=\"${34:90}\"\n\tWAMUserName=\"$35\"\n\tWAMUserPass=\"$36\"\n\tHostHeaderName=\"$37\"\n\tPassword=\"$38\"\n\tServerName=\"${39:localhost}\"\n\tServerPort=\"${40:80}\"\n\tUsername=\"$41\" />"),
            ("AppPoolDelete [MSBCT Simple]", "AppPoolDelete ApplicationPoolName=\"$1\" />"),
            ("AppPoolDelete [MSBCT Full]", "AppPoolDelete\n\tApplicationPoolName=\"$1\"\n\tHostHeaderName=\"$2\"\n\tPassword=\"$3\"\n\tServerName=\"${4:localhost}\"\n\tServerPort=\"${5:80}\"\n\tUsername=\"$6\" />"),
            ("AssemblyInfo [MSBCT]", "AssemblyInfo\n\tAllowPartiallyTrustedCallers=\"${1:False}\"\n\tAssemblyCompany=\"$2\"\n\tAssemblyConfiguration=\"$3\"\n\tAssemblyCopyright=\"$4\"\n\tAssemblyCulture=\"$5\"\n\tAssemblyDelaySign=\"${6:False}\"\n\tAssemblyDescription=\"$7\"\n\tAssemblyFileVersion=\"$8\"\n\tAssemblyInformationalVersion=\"$9\"\n\tAssemblyKeyFile=\"$10\"\n\tAssemblyKeyName=\"$11\"\n\tAssemblyProduct=\"$12\"\n\tAssemblyTitle=\"$13\"\n\tAssemblyTrademark=\"$14\"\n\tAssemblyVersion=\"$15\"\n\tCLSCompliant=\"${16:False}\"\n\tCodeLanguage=\"${17:CS}\"\n\tComVisible=\"${18:False}\"\n\tGenerateClass=\"${19:False}\"\n\tGuid=\"$20\"\n\tInternalsVisibleTo=\"$21\"\n\tNeutralResourcesLanguage=\"$22\"\n\tOutputFile=\"${23:AssemblyInfo.cs}\"\n\tSkipVerification=\"${24:False}\"\n\tUnmanagedCode=\"${25:False}\">\n\t<Output TaskParameter=\"OutputFile\" PropertyName=\"$26\" />\n</AssemblyInfo>"),
            ("Attrib [MSBCT]", "Attrib\n\tArchive=\"${1:False}\"\n\tCompressed=\"${2:False}\"\n\tDirectories=\"${3:@(Directory)}\"\n\tEncrypted=\"${4:False}\"\n\tFiles=\"${5:@(File)}\"\n\tHidden=\"${6:False}\"\n\tNormal=\"${7:False}\"\n\tReadOnly=\"${8:False}\"\n\tSystem=\"${9:False}\" />"),
            ("Beep [MSBCT]", "Beep Duration=\"${1:200}\" Frequency=\"${2:800}\" />"),
            ("BuildAssembler [MSBCT]", "BuildAssembler\n\tConfigFile=\"$1\"\n\tManifestFile=\"$2\"\n\tNoInfoMessages=\"${3:False}\"\n\tNoWarnMessages=\"${4:False}\"\n\tSandcastleRoot=\"$5\" />"),
            ("ChmCompiler [MSBCT]", "ChmCompiler ProjectFile=\"$1\" />"),
            ("ChmBuilder [MSBCT]", "ChmBuilder\n\tHtmlDirectory=\"$1\"\n\tLanguageId=\"$2\"\n\tMetadata=\"$3\"\n\tOutputDirectory=\"$4\"\n\tProjectName=\"$5\"\n\tTocFile=\"$6\"\n\tNoInfoMessages=\"${7:False}\"\n\tNoWarnMessages=\"${8:False}\"\n\tSandcastleRoot=\"$9\" />"),
            ("Computer [MSBCT]", "Computer>\n\t<Output TaskParameter=\"Name\" PropertyName=\"$1\" />\n\t<Output TaskParameter=\"IPAddress\" PropertyName=\"$2\" />\n\t<Output TaskParameter=\"OSPlatform\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"OSVersion\" PropertyName=\"$4\" />\n</Computer>"),
            ("DBCSFix [MSBCT]", "DBCSFix\n\tChmDirectory=\"$1\"\n\tLanguageId=\"$2\"\n\tNoInfoMessages=\"${3:False}\"\n\tNoWarnMessages=\"${4:False}\"\n\tSandcastleRoot=\"$5\" />"),
            ("Divide [MSBCT]", "Divide Numbers=\"$1\" TruncateResult=\"${2:False}\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$3\" />\n</Divide>"),
            ("ExecuteDDL [MSBCT]", "ExecuteDDL\n\tBatchSeparator=\"${1:GO}\"\n\tConnectionString=\"$2\"\n\tFiles=\"${3:@(File)}\"\n\tStatementTimeout=\"${4:30}\">\n\t<Output TaskParameter=\"Results\" PropertyName=\"$5\" />\n</ExecuteDDL>"),
            ("FileUpdate [MSBCT]", "FileUpdate\n\tEncoding=\"${1:UTF-8}\"\n\tFiles=\"${2:@(File)}\"\n\tIgnoreCase=\"${3:False}\"\n\tMultiline=\"${4:False}\"\n\tRegex=\"$5\"\n\tReplacementCount=\"${6:-1}\"\n\tReplacementText=\"${7:}\"\n\tSingleline=\"${8:False}\"\n\tWarnOnNoUpdate=\"${9:False}\" />"),
            ("FtpCreateRemoteDirectory [MSBCT]", "FtpCreateRemoteDirectory\n\tRemoteDirectory=\"$1\"\n\tBufferSize=\"${2:8196}\"\n\tPassword=\"$3\"\n\tPort=\"${4:21}\"\n\tServerHost=\"${5:localhost}\"\n\tUsername=\"$6\" />"),
            ("FtpDirectoryExists [MSBCT]", "FtpDirectoryExists\n\tRemoteDirectory=\"$1\"\n\tBufferSize=\"${2:8196}\"\n\tPassword=\"$3\"\n\tPort=\"${4:21}\"\n\tServerHost=\"${5:localhost}\"\n\tUsername=\"$6\">\n\t<Output TaskParameter=\"Exists\" PropertyName=\"$7\" />\n</FtpDirectoryExists>"),
            ("FtpUpload [MSBCT]", "FtpUpload\n\tLocalFiles=\"${1:@(LocalFile)}\"\n\tPassword=\"$2\"\n\tRemoteFiles=\"${3:@(RemoteFile)}\"\n\tRemoteUri=\"$4\"\n\tUsePassive=\"${5:False}\"\n\tUsername=\"${6:anonymous}\" />"),
            ("FtpUploadDirectoryContent [MSBCT]", "FtpUploadDirectoryContent\n\tLocalDirectory=\"$1\"\n\tRemoteDirectory=\"$2\"\n\tRecursive=\"${3:False}\"\n\tBufferSize=\"${4:8196}\"\n\tPassword=\"$5\"\n\tPort=\"${6:21}\"\n\tServerHost=\"${7:localhost}\"\n\tUsername=\"$8\" />"),
            ("FxCop [MSBCT]", "FxCop\n\tAnalysisReportFileName=\"$1\"\n\tApplyOutXsl=\"${2:False}\"\n\tConsoleXslFileName=\"$3\"\n\tDependencyDirectories=\"${4:@(DependencyDirectory)}\"\n\tDirectOutputToConsole=\"${5:False}\"\n\tFailOnError=\"${6:True}\"\n\tImportFiles=\"${7:@(ImportFile)}\"\n\tIncludeSummaryReport=\"${8:False}\"\n\tOuptutXslFileName=\"$9\"\n\tPlatformDirectory=\"$10\"\n\tProjectFile=\"$11\"\n\tRuleLibraries=\"${12:@(RuleLibrary)}\"\n\tRules=\"${13:@(Rule)}\"\n\tSaveResults=\"${14:False}\"\n\tSearchGac=\"${15:False}\"\n\tTargetAssemblies=\"${16:@(Assembly)}\"\n\tTypeList=\"$17\"\n\tVerbose=\"${18:False}\"\n\tWorkingDirectory=\"$19\" />"),
            ("GacUtil [MSBCT]", "GacUtil\n\tAssemblies=\"${1:@(Assembly)}\"\n\tCommand=\"${2:Install}\"\n\tForce=\"${3:False}\"\n\tIncludeRelatedFiles=\"${4:False}\"\n\tQuiet=\"${5:False}\"\n\tRelatedFileExtensions=\"${6:.pdb;.xml}\">\n\t<Output TaskParameter=\"Failed\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"InstalledNames\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"InstalledPaths\" ItemName=\"$9\" />\n\t<Output TaskParameter=\"Skipped\" PropertyName=\"$10\" />\n\t<Output TaskParameter=\"Successful\" PropertyName=\"$11\" />\n</GacUtil>"),
            ("GetSolutionProjects [MSBCT]", "GetSolutionProjects Solution=\"$1\">\n\t<Output TaskParameter=\"Output\" ItemName=\"$2\" />\n</GetSolutionProjects>"),
            ("HxCompiler [MSBCT]", "HxCompiler\n\tLogFile=\"$1\"\n\tNoErrorMessages=\"${2:False}\"\n\tNoInfoMessages=\"${3:False}\"\n\tNoWarningMessages=\"${4:False}\"\n\tOutputFile=\"$5\"\n\tProjectFile=\"$6\"\n\tProjectRoot=\"$7\"\n\tQuiteMode=\"${8:False}\"\n\tUncompileDirectory=\"$9\"\n\tUncompileFile=\"$10\" />"),
            ("ILMerge [MSBCT]", "ILMerge\n\tAllowDuplicateTypes=\"${1:@(DuplicatePublicType)}\"\n\tAllowZeroPeKind=\"${2:False}\"\n\tAttributeFile=\"$3\"\n\tClosed=\"${4:False}\"\n\tCopyAttributes=\"${5:False}\"\n\tDebugInfo=\"${6:True}\"\n\tDelaySign=\"${7:False}\"\n\tExcludeFile=\"$8\"\n\tInputAssemblies=\"${9:@(InputAssembly)}\"\n\tInternalize=\"${10:False}\"\n\tKeyFile=\"${11:StrongNameKey.snk}\"\n\tLogFile=\"$12\"\n\tOuptutFile=\"$13\"\n\tPublicKeyTokens=\"${14:False}\"\n\tTargetKind=\"${15:dll}\"\n\tTargetPlatformDirectory=\"${16:\$(ProgramFiles)\\Reference Assemblies\\Microsoft\\Framework\\.NETFramework\\v4.0}\"\n\tTargetPlatformVersion=\"${17:v4}\"\n\tVersion=\"${18:1.0.0.0}\"\n\tXmlDocumentation=\"${19:False}\" />"),
            ("InstallAspNet [MSBCT FullInstall]", "InstallAspNet\n\tApplyScriptMaps=\"${1:UnlessNewerExist}\"\n\tPath=\"${2:W3SVC/1/Root}\"\n\tRecursive=\"${3:True}\"\n\tVersion=\"${4:VersionLatest}\" />"),
            ("InstallAspNet [MSBCT ClientOnly]", "InstallAspNet ClientScriptsOnly=\"${1:True}\" Recursive=\"${2:True}\" Version=\"${3:VersionLatest}\" />"),
            ("InstallAssembly [MSBCT]", "InstallAssembly\n\tAssemblyNames=\"${1:@(Assembly)}\"\n\tAssemblyFiles=\"${2:@(AssemblyFile)}\"\n\tLogFile=\"$3\"\n\tShowCallStack=\"${4:False}\" />"),
            ("JSCompress [MSBCT]", "JSCompress Files=\"${1:@(ScriptFile)}\" Encoding=\"${2:UTF-8}\">\n\t<Output TaskParameter=\"CompressedFiles\" ItemName=\"$3\" />\n</JSCompress>"),
            ("Mail [MSBCT Simple]", "Mail\n\tSmtpServer=\"${1:localhost}\"\n\tTo=\"${2:to@email.com}\"\n\tFrom=\"${3:from@email.com}\"\n\tSubject=\"$4\"\n\tBody=\"$5\" />"),
            ("Mail [MSBCT Full]", "Mail\n\tSmtpServer=\"${1:localhost}\"\n\tTo=\"${2:to@email.com}\"\n\tFrom=\"${3:from@email.com}\"\n\tSubject=\"$4\"\n\tBody=\"$5\"\n\tAttachments=\"${6:@(Attachment)}\"\n\tBcc=\"${7:@(Bcc)}\"\n\tCC=\"${8:@(CC)}\"\n\tEnableSsl=\"${9:False}\"\n\tIsBodyHtml=\"${10:False}\"\n\tPassword=\"$11\"\n\tPriority=\"${12:Normal}\"\n\tUsername=\"$13\" />"),
            ("Merge [MSBCT]", "Merge\n\tDestinationFile=\"$1\"\n\tMode=\"${2:TextLine}\"\n\tSourceFiles=\"${3:@(MergeSource)}\" />"),
            ("Modulo [MSBCT]", "Modulo Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Modulo>"),
            ("MRefBuilder [MSBCT]", "MRefBuilder\n\tAssemblies=\"${1:@(Assembly)}\"\n\tConfigFile=\"$2\"\n\tIncludeInternal=\"$3\"\n\tOutputFile=\"$4\"\n\tReferences=\"${5:@(Reference)}\"\n\tNoInfoMessages=\"${6:False}\"\n\tNoWarnMessages=\"${7:False}\"\n\tSandcastleRoot=\"$8\" />"),
            ("Multiple [MSBCT]", "Multiple Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Multiple>"),
            ("NDoc [MSBCT]", "NDoc\n\tDocumenter=\"${1:MSDN}\"\n\tProjectFilePath=\"${2:Project.ndoc}\"\n\tVerbose=\"${3:False}\"\n\tWorkingDirectory=\"$4\" />"),
            ("NUnit [MSBCT Full]", "NUnit\n\tAssemblies=\"${1:@(TestAssembly)}\"\n\tDisableShadowCopy=\"${2:False}\"\n\tErrorOutputFile=\"$3\"\n\tExcludeCategory=\"$4\"\n\tFixture=\"$5\"\n\tForce32Bit=\"${6:False}\"\n\tIncludeCategory=\"$7\"\n\tOutputXmlFile=\"$8\"\n\tProjectConfiguration=\"$9\"\n\tTestInNewThread=\"${10:False}\"\n\tWorkingDirectory=\"$11\"\n\tXsltTransformFile=\"$12\" />"),
            ("NUnit [MSBCT Simple]", "NUnit Assemblies=\"${1:@(TestAssembly)}\" OutputXmlFile=\"$2\" />"),
            ("Prompt [MSBCT]", "Prompt Text=\"$1\">\n\t<Ouptut TaskParameter=\"UserInput\" PropertyName=\"$2\" />\n</Prompt>"),
            ("RegexMatch [MSBCT]", "RegexMatch\n\tExpression=\"$1\"\n\tInput=\"$2\"\n\tOptions=\"${3:None}\">\n\t<Output TaskParameter=\"Output\" ItemName=\"$4\" />\n</RegexMatch>"),
            ("RegexReplace [MSBCT]", "RegexReplace\n\tExpression=\"$1\"\n\tInput=\"$2\"\n\tOptions=\"${3:None}\"\n\tCount=\"$4\"\n\tReplacement=\"$5\"\n\tStartAt=\"$6\">\n\t<Output TaskParameter=\"Output\" ItemName=\"$7\" />\n</RegexReplace>"),
            ("RegistryRead [MSBCT]", "RegistryRead\n\tKeyName=\"$1\"\n\tValueName=\"$2\"\n\tDefaultValue=\"$3\">\n\t<Output TaskParameter=\"Value\" PropertyName=\"$4\" />\n</RegistryRead>"),
            ("RegistryWrite [MSBCT]", "RegistryWrite\n\tKeyName=\"$1\"\n\tValueName=\"$2\"\n\tValue=\"$3\" />"),
            ("RoboCopy [MSBCT]", "RoboCopy\n\tAllSubdirectories=\"${1:False}\"\n\tAppendLogFile=\"$2\"\n\tBackupMode=\"${3:False}\"\n\tCopyAll=\"${4:False}\"\n\tCopyFlags=\"$5\"\n\tCreate=\"${6:False}\"\n\tDestinationFolder=\"$7\"\n\tExcludeFiles=\"$8\"\n\tExcludeFolders=\"$9\"\n\tExcludeJunctions=\"${10:False}\"\n\tExcluedAttributes=\"$11\"\n\tFatFileNames=\"${12:False}\"\n\tFatFileTimes=\"${13:False}\"\n\tIncludeArchive=\"${14:False}\"\n\tIncludeArchiveClear=\"${15:False}\"\n\tIncludeAttributes=\"$16\"\n\tLogFile=\"$17\"\n\tMirror=\"${18:False}\"\n\tMove=\"${19:False}\"\n\tMoveFiles=\"${20:False}\"\n\tNoCopy=\"${21:False}\"\n\tNoFileLogging=\"${22:False}\"\n\tNoFolderLogging=\"${23:False}\"\n\tNoJobHeader=\"${24:False}\"\n\tNoJobSummary=\"${25:False}\"\n\tNoProgress=\"${26:True}\"\n\tOptions=\"$27\"\n\tPurge=\"${28:False}\"\n\tRestartableMode=\"${29:False}\"\n\tSecurity=\"${30:False}\"\n\tSourceFiles=\"$31\"\n\tSourceFolder=\"$32\"\n\tSubdirectories=\"${33:False}\"\n\tVerbose=\"${34:False}\" />"),
            ("Sandcastle [MSBCT]", "Sandcastle\n\tAssemblies=\"${1:@(AssemblyToDocument)}\"\n\tChmName=\"$2\"\n\tClean=\"${3:False}\"\n\tComments=\"${4:@(XmlCommentFile)}\"\n\tHxName=\"$5\"\n\tLanguageId=\"${6:1033}\"\n\tNoInfoMessages=\"${7:True}\"\n\tNoWarnMessages=\"${8:False}\"\n\tReferences=\"${9:@(Reference)}\"\n\tSandcastleConfig=\"$10\"\n\tSandcastleRoot=\"$11\"\n\tTopicStyle=\"${12:vs2005}\"\n\tWorkingDirectory=\"$13\" />"),
            ("Script [MSBCT]", "Script\n\tCode=\"$1\"\n\tImports=\"${2:@(Namespace)}\"\n\tLanguage=\"${3:C#}\"\n\tMainClass=\"$4\"\n\tReferences=\"${5:@(Reference)}\">\n\t<Output TaskParameter=\"ReturnValue\" PropertyName=\"$6\" />\n</Script>"),
            ("ServiceController [MSBCT]", "ServiceController\n\tServiceName=\"$1\"\n\tMachineName=\"$2\"\n\tAction=\"${3:Restart}\"\n\tTimeout=\"${4:60000}\">\n\t<Output TaskParameter=\"Status\" PropertyName=\"$5\" />\n</ServiceController>"),
            ("ServiceQuery [MSBCT]", "ServiceQuery ServiceName=\"$1\" MachineName=\"$2\">\n\t<Output TaskParameter=\"CanPauseAndContinue\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"CanShutdown\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"CanStop\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"DisplayName\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"Exists\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"Status\" PropertyName=\"$8\" />\n</ServiceQuery>"),
            ("Sleep [MSBCT]", "Sleep Minutes=\"$1\" Seconds=\"$2\" Milliseconds=\"$3\" />"),
            ("Sound [MSBCT]", "Sound\n\tMyMusicFile=\"$1\"\n\tSystemSoundFile=\"$2\"\n\tSoundLocation=\"$3\"\n\tSynchron=\"${4:True}\"\n\tLoadTimeout=\"${5:10000}\" />"),
            ("SqlExecute [MSBCT]", "SqlExecute\n\tCommand=\"$1\"\n\tConnectionString=\"$2\"\n\tCommandTimeout=\"${3:30}\"\n\tOutputFile=\"$4\"\n\tSelectMode=\"${5:Scalar}\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$6\" />\n</SqlExecute>"),
            ("SqlPubWiz [MSBCT]", "SqlPubWiz\n\tCommand=\"$1\"\n\tConnectionString=\"$2\"\n\tDatabase=\"$3\"\n\tDataOnly=\"${4:False}\"\n\tHosterName=\"$5\"\n\tNoDropExisting=\"${6:False}\"\n\tNoSchemaQualify=\"${7:False}\"\n\tNoTransaction=\"${8:False}\"\n\tOutput=\"$9\"\n\tPassword=\"$10\"\n\tQuiet=\"${11:False}\"\n\tSchemaOnly=\"${12:False}\"\n\tServer=\"$13\"\n\tServiceDatabase=\"$14\"\n\tServiceDatabaseServer=\"$15\"\n\tServicePassword=\"$16\"\n\tServiceUsername=\"$17\"\n\tTargetServer=\"$18\"\n\tUsername=\"$19\"\n\tWebServiceAddress=\"$20\" />"),
            ("Subtract [MSBCT]", "Subtract Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Subtract>"),
            ("SvnCheckout [MSBCT]", "SvnCheckout\n\tLocalPath=\"$1\"\n\tRepositoryPath=\"$2\"\n\tRevision=\"$3\"\n\tNoAuthCache=\"${4:True}\"\n\tNonInteractive=\"${5:True}\"\n\tUsername=\"$6\"\n\tPassword=\"$7\"\n\tTrustServerCert=\"${8:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$10\" />\n</SvnCheckout>"),
            ("SvnClient [MSBCT]", "SvnClient\n\tArguments=\"$1\"\n\tCommand=\"$2\"\n\tForce=\"${3:False}\"\n\tLocalPath=\"$4\"\n\tMessage=\"$5\"\n\tMessageFile=\"$6\"\n\tRevision=\"$7\"\n\tTargetFile=\"$8\"\n\tTargets=\"$9\"\n\tVerbose=\"${10:False}\"\n\tXml=\"${11:False}\"\n\tNoAuthCache=\"${12:True}\"\n\tNonInteractive=\"${13:True}\"\n\tUsername=\"$14\"\n\tPassword=\"$15\"\n\tTrustServerCert=\"${16:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$17\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$18\" />\n</SvnClient>"),
            ("SvnCommit [MSBCT]", "SvnCommit\n\tTargets=\"$1\"\n\tMessage=\"$2\"\n\tMessageFile=\"$3\"\n\tNoAuthCache=\"${4:True}\"\n\tNonInteractive=\"${5:True}\"\n\tUsername=\"$6\"\n\tPassword=\"$7\"\n\tTrustServerCert=\"${8:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$10\" />\n</SvnCommit>"),
            ("SvnCopy [MSBCT]", "SvnCopy\n\tSourcePath=\"$1\"\n\tDestinationPath=\"$2\"\n\tRevision=\"$3\"\n\tNoAuthCache=\"${4:True}\"\n\tNonInteractive=\"${5:True}\"\n\tUsername=\"$6\"\n\tPassword=\"$7\"\n\tTrustServerCert=\"${8:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$10\" />\n</SvnCopy>"),
            ("SvnExport [MSBCT]", "SvnExport\n\tRepositoryPath=\"$1\"\n\tRevision=\"$2\"\n\tForce=\"${3:False}\"\n\tNoAuthCache=\"${4:True}\"\n\tNonInteractive=\"${5:True}\"\n\tUsername=\"$6\"\n\tPassword=\"$7\"\n\tTrustServerCert=\"${8:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$10\" />\n</SvnExport>"),
            ("SvnInfo [MSBCT]", "SvnInfo\n\tLocalPath=\"$1\"\n\tRepositoryPath=\"$2\"\n\tRevision=\"$3\">\n\t<Output TaskParameter=\"LastChangedAuthor\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"LastChangedDate\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"LastChangedRevision\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"NodeKind\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"RepositoryPath\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"RepositoryRoot\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"RepositoryUuid\" PropertyName=\"$10\" />\n\t<Output TaskParameter=\"Revision\" PropertyName=\"$11\" />\n\t<Output TaskParameter=\"Schedule\" PropertyName=\"$12\" />\n</SvnInfo>"),
            ("SvnStatus [MSBCT]", "SvnStatus LocalPath=\"$1\">\n\t<Output TaskParameter=\"Entries\" ItemName=\"$2\" />\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$4\" />\n</SvnStatus>"),
            ("SvnUpdate [MSBCT]", "SvnUpdate\n\tLocalPath=\"$1\"\n\tRevision=\"$2\"\n\tForce=\"${3:False}\"\n\tNoAuthCache=\"${4:True}\"\n\tNonInteractive=\"${5:True}\"\n\tUsername=\"$6\"\n\tPassword=\"$7\"\n\tTrustServerCert=\"${8:False}\">\n\t<Output TaskParameter=\"StandardError\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"StandardOutput\" PropertyName=\"$10\" />\n</SvnUpdate>"),
            ("SvnVersion [MSBCT]", "SvnVersion LocalPath=\"$1\" UseLastCommittedRevision=\"${2:False}\">\n\t<Output TaskParameter=\"Exported\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"HighRevision\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"LowRevision\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"Modifications\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"Revision\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"Switched\" PropertyName=\"$8\" />\n</SvnVersion>"),
            ("TaskSchema [MSBCT]", "TaskSchema\n\tAssemblies=\"${1:@(Assembly)}\"\n\tCreateTaskList=\"${2:True}\"\n\tIgnoreDocumentation=\"${3:False}\"\n\tIgnoreMsBuildSchema=\"${4:False}\"\n\tIncludes=\"${5:@(Include)}\"\n\tOutputPath=\"$6\"\n\tTaskListAssemblyFormat=\"${7:AssemblyFileName}\">\n\t<Output TaskParameter=\"Schemas\" ItemName=\"$8\" />\n\t<Output TaskParameter=\"TaskLists\" ItemName=\"$9\" />\n</TaskSchema>"),
            ("TemplateFile [MSBCT]", "TemplateFile\n\tOutputFilename=\"$1\"\n\tTemplate=\"$2\"\n\tTokens=\"${3:@(Token)}\">\n\t<Output TaskParameter=\"OutputFile\" ItemName=\"$4\" />\n</TemplateFile>"),
            ("TfsVersion [MSBCT]", "TfsVersion\n\tLocalPath=\"$1\"\n\tTfsLibraryLocation=\"$2\"\n\tDomain=\"$3\"\n\tUsername=\"$4\"\n\tPassword=\"$5\">\n\t<Output TaskParameter=\"Changeset\" PropertyName=\"$6\" />\n</TfsVersion>"),
            ("Time [MSBCT]", "Time Format=\"${1:R}\">\n\t<Output TaskParameter=\"Day\" PropertyName=\"$2\" />\n\t<Output TaskParameter=\"DayOfWeek\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"DayOfYear\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"FormattedTime\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"Hour\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"Kind\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"LongDate\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"LongTime\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"Millisecond\" PropertyName=\"$10\" />\n\t<Output TaskParameter=\"Minute\" PropertyName=\"$11\" />\n\t<Output TaskParameter=\"Month\" PropertyName=\"$12\" />\n\t<Output TaskParameter=\"Second\" PropertyName=\"$13\" />\n\t<Output TaskParameter=\"ShortDate\" PropertyName=\"$14\" />\n\t<Output TaskParameter=\"ShortTime\" PropertyName=\"$15\" />\n\t<Output TaskParameter=\"Ticks\" PropertyName=\"$16\" />\n\t<Output TaskParameter=\"TimeOfDay\" PropertyName=\"$17\" />\n\t<Output TaskParameter=\"Year\" PropertyName=\"$18\" />\n</Time>"),
            ("Token [MSBCT Item]", "Token Include=\"$1\">\n\t<ReplacementValue>$2</ReplacementValue>\n</Token>"),
            ("UninstallAssembly [MSBCT]", "UninstallAssembly\n\tAssemblyNames=\"${1:@(Assembly)}\"\n\tAssemblyFiles=\"${2:@(AssemblyFile)}\"\n\tLogFile=\"$3\"\n\tShowCallStack=\"${4:False}\" />"),
            ("Unzip [MSBCT]", "Unzip\n\tZipFileName=\"$1\"\n\tTargetDirectory=\"$2\"\n\tOverwrite=\"${3:True}\">\n\t<Output TaskParameter=\"ExtractedFiles\" ItemName=\"$4\" />\n</Unzip>"),
            ("User [MSBCT]", "User>\n\t<Output TaskParameter=\"DomainName\" PropertyName=\"$1\" />\n\t<Output TaskParameter=\"Email\" PropertyName=\"$2\" />\n\t<Output TaskParameter=\"FirstName\" PropertyName=\"$3\" />\n\t<Output TaskParameter=\"FullName\" PropertyName=\"$4\" />\n\t<Output TaskParameter=\"LastName\" PropertyName=\"$5\" />\n\t<Output TaskParameter=\"MiddleInitial\" PropertyName=\"$6\" />\n\t<Output TaskParameter=\"Phone\" PropertyName=\"$7\" />\n\t<Output TaskParameter=\"UserName\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"UserNameWithDomain\" PropertyName=\"$9\" />\n</User>"),
            ("Version [MSBCT]", "Version\n\tMajor=\"${1:1}\"\n\tMajorType=\"${2:None}\"\n\tMinor=\"${3:0}\"\n\tMinorType=\"${4:None}\"\n\tBuild=\"${5:0}\"\n\tBuildType=\"${6:None}\"\n\tRevision=\"${7:0}\"\n\tRevisionType=\"${8:Automatic}\"\n\tStartDate=\"$9\"\n\tVersionFile=\"$10\">\n\t<Output TaskParameter=\"Major\" PropertyName=\"$11\" />\n\t<Output TaskParameter=\"Minor\" PropertyName=\"$12\" />\n\t<Output TaskParameter=\"Build\" PropertyName=\"$13\" />\n\t<Output TaskParameter=\"Revision\" PropertyName=\"$14\" />\n</Version>"),
            ("VssAdd [MSBCT]", "VssAdd\n\tComment=\"$1\"\n\tFiles=\"${2:@(File)}\"\n\tDatabasePath=\"$3\"\n\tPath=\"$4\"\n\tVersion=\"$5\"\n\tUserName=\"$6\"\n\tPassword=\"$7\" />"),
            ("VssCheckin [MSBCT]", "VssCheckin\n\tComment=\"$1\"\n\tLocalPath=\"$2\"\n\tWritable=\"${3:False}\"\n\tRecursive=\"${4:True}\"\n\tDatabasePath=\"$5\"\n\tPath=\"$6\"\n\tVersion=\"$7\"\n\tUserName=\"$8\"\n\tPassword=\"$9\" />"),
            ("VssCheckout [MSBCT]", "VssCheckout\n\tLocalPath=\"$1\"\n\tWritable=\"${2:False}\"\n\tRecursive=\"${3:True}\"\n\tDatabasePath=\"$4\"\n\tPath=\"$5\"\n\tVersion=\"$6\"\n\tUserName=\"$7\"\n\tPassword=\"$8\" />"),
            ("VssDiff [MSBCT]", "VssDiff\n\tLabel=\"$1\"\n\tOutputFile=\"$2\"\n\tDatabasePath=\"$3\"\n\tPath=\"$4\"\n\tVersion=\"$5\"\n\tUserName=\"$6\"\n\tPassword=\"$7\" />"),
            ("VssGet [MSBCT]", "VssGet\n\tLocalPath=\"$1\"\n\tReplace=\"${2:False}\"\n\tWritable=\"${3:False}\"\n\tRecursive=\"${4:True}\"\n\tDatabasePath=\"$5\"\n\tPath=\"$6\"\n\tVersion=\"$7\"\n\tUserName=\"$8\"\n\tPassword=\"$9\" />"),
            ("VssHistory [MSBCT]", "VssHistory\n\tFromDate=\"$1\"\n\tFromLabel=\"$2\"\n\tOutputFile=\"$3\"\n\tToDate=\"$4\"\n\tToLabel=\"$5\"\n\tUser=\"$6\"\n\tRecursive=\"${7:True}\"\n\tDatabasePath=\"$8\"\n\tPath=\"$9\"\n\tVersion=\"$10\"\n\tUserName=\"$11\"\n\tPassword=\"$12\" />"),
            ("VssLabel [MSBCT]", "VssLabel\n\tComment=\"$1\"\n\tLabel=\"$2\"\n\tRecursive=\"${3:True}\"\n\tDatabasePath=\"$4\"\n\tPath=\"$5\"\n\tVersion=\"$6\"\n\tUserName=\"$7\"\n\tPassword=\"$8\" />"),
            ("VssUndoCheckout [MSBCT]", "VssUndoCheckout\n\tLocalPath=\"$1\"\n\tRecursive=\"${2:True}\"\n\tDatabasePath=\"$3\"\n\tPath=\"$4\"\n\tVersion=\"$5\"\n\tUserName=\"$6\"\n\tPassword=\"$7\" />"),
            ("WebDirectoryCreate [MSBCT Simple]", "WebDirectoryCreate VirtualDirectoryName=\"$1\" VirtualDirectoryPhysicalPath=\"$2\" />"),
            ("WebDirectoryCreate [MSBCT Full]", "WebDirectoryCreate\n\tVirtualDirectoryName=\"$1\"\n\tVirtualDirectoryPhysicalPath=\"$2\"\n\tAccessExecute=\"${3:False}\"\n\tAccessNoRemoteExecute=\"${4:False}\"\n\tAccessNoRemoteRead=\"${5:False}\"\n\tAccessNoRemoteScript=\"${6:False}\"\n\tAccessNoRemoteWrite=\"${7:False}\"\n\tAccessRead=\"${8:True}\"\n\tAccessScript=\"${9:True}\"\n\tAccessSource=\"${10:False}\"\n\tAccessSsl=\"${11:False}\"\n\tAccessSsl128=\"${12:False}\"\n\tAccessSslMapCert=\"${13:False}\"\n\tAccessSslNegotiateCert=\"${14:False}\"\n\tAccessSslRequireCert=\"${15:False}\"\n\tAccessWrite=\"${16:False}\"\n\tAnonymousPasswordSync=\"${17:True}\"\n\tAppAllowClientDebug=\"${18:False}\"\n\tAppAllowDebugging=\"${19:False}\"\n\tAspAllowSessionState=\"${20:True}\"\n\tAspBufferingOn=\"${21:True}\"\n\tAspEnableApplicationRestart=\"${22:True}\"\n\tAspEnableAspHtmlFallback=\"${23:False}\"\n\tAspEnableChunkedEncoding=\"${24:False}\"\n\tAspEnableParentPaths=\"${25:True}\"\n\tAspEnableTypelibCache=\"${26:True}\"\n\tAspErrorsToNTLog=\"${27:False}\"\n\tAspExceptionCatchEnable=\"${28:True}\"\n\tAspLogErrorRequests=\"${29:True}\"\n\tAspScriptErrorMessage=\"${30:An error occurred on the server when processing the URL.  Please contact the system administrator.}\"\n\tAspScriptErrorSentToBrowser=\"${31:True}\"\n\tAspTrackThreadingModel=\"${32:False}\"\n\tAuthAnonymous=\"${33:True}\"\n\tAuthBasic=\"${34:False}\"\n\tAuthNtlm=\"${35:False}\"\n\tAuthPersistSingleRequest=\"${36:False}\"\n\tAuthPersistSingleRequestAlwaysIfProxy=\"${37:False}\"\n\tAuthPersistSingleRequestIfProxy=\"${38:True}\"\n\tCacheControlNoCache=\"${39:False}\"\n\tCacheIsapi=\"${40:True}\"\n\tContentIndexed=\"${41:True}\"\n\tCpuAppEnabled=\"${42:True}\"\n\tCpuCgiEnabled=\"${43:True}\"\n\tCreateCgiWithNewConsole=\"${44:False}\"\n\tCreateProcessAsUser=\"${45:True}\"\n\tDefaultDoc=\"${46:Default.htm, Default.asp, index.htm, iisstart.asp, Default.aspx}\"\n\tDirBrowseShowDate=\"${47:True}\"\n\tDirBrowseShowExtension=\"${48:True}\"\n\tDirBrowseShowLongDate=\"${49:True}\"\n\tDirBrowseShowSize=\"${50:True}\"\n\tDirBrowseShowTime=\"${51:True}\"\n\tDontLog=\"${52:False}\"\n\tEnableDefaultDoc=\"${53:True}\"\n\tEnableDirBrowsing=\"${54:False}\"\n\tEnableDocFooter=\"${55:False}\"\n\tEnableReverseDns=\"${56:False}\"\n\tSsiExecDisable=\"${57:False}\"\n\tUncAuthenticationPassthrough=\"${58:False}\"\n\tHostHeaderName=\"$59\"\n\tPassword=\"$60\"\n\tServerName=\"${61:localhost}\"\n\tServerPort=\"${62:80}\"\n\tUsername=\"$63\" />"),
            ("WebDirectoryDelete [MSBCT Simple]", "WebDirectoryDelete VirtualDirectoryName=\"$1\" />"),
            ("WebDirectoryDelete [MSBCT Full]", "WebDirectoryDelete\n\tVirtualDirectoryName=\"$1\"\n\tHostHeaderName=\"$2\"\n\tPassword=\"$3\"\n\tServerName=\"${4:localhost}\"\n\tServerPort=\"${5:80}\"\n\tUsername=\"$6\" />"),
            ("WebDirectoryScriptMap [MSBCT Simple]", "WebDirectoryScriptMap\n\tEnableScriptEngine=\"${1:False}\"\n\tExecutablePath=\"$2\"\n\tExtension=\"$3\"\n\tMapToAspNet=\"${4:False}\"\n\tVerbs=\"$5\"\n\tVerifyFileExists=\"${6:False}\"\n\tVirtualDirectoryName=\"$7\" />"),
            ("WebDirectoryScriptMap [MSBCT Full]", "WebDirectoryScriptMap\n\tEnableScriptEngine=\"${1:False}\"\n\tExecutablePath=\"$2\"\n\tExtension=\"$3\"\n\tMapToAspNet=\"${4:False}\"\n\tVerbs=\"$5\"\n\tVerifyFileExists=\"${6:False}\"\n\tVirtualDirectoryName=\"$7\"\n\tHostHeaderName=\"$8\"\n\tPassword=\"$9\"\n\tServerName=\"${10:localhost}\"\n\tServerPort=\"${11:80}\"\n\tUsername=\"$12\" />"),
            ("WebDirectorySetting [MSBCT Get]", "WebDirectorySetting VirtualDirectoryName=\"$1\" SettingName=\"$2\">\n\t<Output TaskParameter=\"SettingValue\" PropertyName=\"$3\" />\n</WebDirectorySetting>"),
            ("WebDirectorySetting [MSBCT Set]", "WebDirectorySetting\n\tVirtualDirectoryName=\"$1\"\n\tSettingName=\"$2\"\n\tSettingValue=\"$3\" />"),
            ("WebDirectorySetting [MSBCT Full]", "WebDirectorySetting\n\tVirtualDirectoryName=\"$1\"\n\tSettingName=\"$2\"\n\tSettingValue=\"$3\"\n\tHostHeaderName=\"$4\"\n\tPassword=\"$5\"\n\tServerName=\"${6:localhost}\"\n\tServerPort=\"${7:80}\"\n\tUsername=\"$8\">\n\t<Output TaskParameter=\"SettingValue\" PropertyName=\"$9\" />\n</WebDirectorySetting>"),
            ("WebDownload [MSBCT]", "WebDownload\n\tFileName=\"$1\"\n\tFileUri=\"$2\"\n\tUseDefaultCredentials=\"${3:False}\"\n\tDomain=\"$4\"\n\tUsername=\"$5\"\n\tPassword=\"$6\" />"),
            ("XmlMassUpdate [MSBCT]", "XmlMassUpdate\n\tContentFile=\"$1\"\n\tContentRoot=\"$2\"\n\tMergedFile=\"$3\"\n\tNamespaceDefinitions=\"${4:@(XmlNamespace)}\"\n\tSubstitutionsFile=\"$5\"\n\tSubstitutionsRoot=\"$6\"\n\tUpdateControlNamespace=\"$7\">\n\t<Output TaskParameter=\"ContentPathUsedByTask\" PropertyName=\"$8\" />\n\t<Output TaskParameter=\"MergedPathUsedByTask\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"SubstitutionsPathUsedByTask\" PropertyName=\"$10\" />\n</XmlMassUpdate>"),
            ("XmlUpdate [MSBCT]", "XmlUpdate\n\tXmlFileName=\"$1\"\n\tXPath=\"$2\"\n\tDelete=\"${3:False}\"\n\tNamespace=\"$4\"\n\tPrefix=\"$5\"\n\tValue=\"$6\" />"),
            ("XslTransform [MSBCT]", "XslTransform\n\tArguments=\"$1\"\n\tOutputFile=\"$2\"\n\tXmlFile=\"$3\"\n\tXsltFiles=\"${4:@(XsltFile)}\"\n\tNoInfoMessages=\"${5:False}\"\n\tNoWarnMessages=\"${6:False}\"\n\tSandcastleRoot=\"$7\" />"),
            ("Zip [MSBCT Simple]", "Zip\n\tFiles=\"${1:@(File)}\"\n\tFlatten=\"${2:False}\"\n\tWorkingDirectory=\"$3\"\n\tZipFileName=\"$4\" />"),
            ("Zip [MSBCT Full]", "Zip\n\tComment=\"$1\"\n\tFiles=\"${2:@(File)}\"\n\tEncryption=\"${3:None}\"\n\tFlatten=\"${4:False}\"\n\tPassword=\"$5\"\n\tWorkingDirectory=\"$6\"\n\tZipFileName=\"$7\"\n\tZipLevel=\"${8:6}\" />")
        ])
        completions = sorted(completions, key=lambda completion: completion[0])
        return (completions, sublime.INHIBIT_WORD_COMPLETIONS)


# Provide completions that match just after typing a . inside a %() item reference
class WellKnownItemMetadataCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild item references
        if not view.match_selector(locations[0],
                "variable.parameter.item.source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '.':
            return []

        return ([
            (".AccessedTime", ".AccessedTime"),
            (".CreatedTime", ".CreatedTime"),
            (".Directory", ".Directory"),
            (".Extension", ".Extension"),
            (".Filename", ".Filename"),
            (".FullPath", ".FullPath"),
            (".Identity", ".Identity"),
            (".ModifiedTime", ".ModifiedTime"),
            (".RecursiveDir", ".RecursiveDir"),
            (".RelativeDir", ".RelativeDir"),
            (".RootDir", ".RootDir")
        ], sublime.INHIBIT_WORD_COMPLETIONS)
