import sublime, sublime_plugin
import re

# Enable autocomplete to be fired when $( is typed
# This is required because of the balanced-parentheses key binding
class CompleteOnPropertyListener(sublime_plugin.EventListener):
    def on_selection_modified(self,view):
        sel = view.sel()[0]
        if not view.match_selector(sel.a, "source.msbuild"):
            return
        ch = view.substr(sublime.Region(sel.a-2, sel.a))
        if ch == '$(':
            view.run_command('auto_complete')

# Provide completions that match just after typing a $() property reference
class ReservedPropertyCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild if it's a property
        if not view.match_selector(locations[0],
                "source.msbuild"):
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
            ("MSBuildProjectDefaultTargets", "MSBuildProjectDefaultTargets"),
            ("MSBuildProjectDirectory", "MSBuildProjectDirectory"),
            ("MSBuildProjectExtension", "MSBuildProjectExtension"),
            ("MSBuildProjectFile", "MSBuildProjectFile"),
            ("MSBuildProjectFullPath", "MSBuildProjectFullPath"),
            ("MSBuildProjectName", "MSBuildProjectName"),
            ("MSBuildStartupDirectory", "MSBuildStartupDirectory")
        ], sublime.INHIBIT_WORD_COMPLETIONS)

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
            ("ItemGroup", "ItemGroup>\n\t$1\n</ItemGroup>"),
            ("PropertyGroup", "PropertyGroup>\n\t$1\n</PropertyGroup>"),
            ("UsingTask", "UsingTask TaskName=\"$1\" AssemblyName=\"$2\" />"),
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
            ("Exec [Full]", "Exec\n\tCommand=\"$1\"\n\tCustomErrorRegularExpression=\"$2\"\n\tCustomWarningRegularExpression=\"$3\"\n\tIgnoreExitCode=\"${4:False}\"\n\tIgnoreStandardErrorWanringFormat=\"${5:False}\"\n\tStdErrEncoding=\"$6\"\n\tStdOutEncoding=\"$7\"\n\tWorkingDirectory=\"$8\">\n\t<Output TaskParameter=\"ExitCode\" PropertyName=\"$9\" />\n\t<Output TaskParameter=\"Outputs\" ItemName=\"$10\" />\n</Exec>"),
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
        if msbimport is None:
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
            ("AssemblyInfo [MSBCT]", "AssemblyInfo></AssemblyInfo>"),
            ("Attrib [MSBCT]", "Attrib></Attrib>"),
            ("Beep [MSBCT]", "Beep></Beep>"),
            ("BuildAssembler [MSBCT]", "BuildAssembler></BuildAssembler>"),
            ("ChmBuilder [MSBCT]", "ChmBuilder></ChmBuilder>"),
            ("ChmCompiler [MSBCT]", "ChmCompiler></ChmCompiler>"),
            ("Computer [MSBCT]", "Computer></Computer>"),
            ("DBCSFix [MSBCT]", "DBCSFix></DBCSFix>"),
            ("Divide [MSBCT]", "Divide Numbers=\"$1\" TruncateResult=\"${2:False}\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$3\" />\n</Divide>"),
            ("ExecuteDDL [MSBCT]", "ExecuteDDL></ExecuteDDL>"),
            ("FileUpdate [MSBCT]", "FileUpdate></FileUpdate>"),
            ("FtpCreateRemoteDirectory [MSBCT]", "FtpCreateRemoteDirectory></FtpCreateRemoteDirectory>"),
            ("FtpDirectoryExists [MSBCT]", "FtpDirectoryExists></FtpDirectoryExists>"),
            ("FtpUpload [MSBCT]", "FtpUpload></FtpUpload>"),
            ("FtpUploadDirectoryContent [MSBCT]", "FtpUploadDirectoryContent></FtpUploadDirectoryContent>"),
            ("FxCop [MSBCT]", "FxCop></FxCop>"),
            ("GacUtil [MSBCT]", "GacUtil></GacUtil>"),
            ("GetSolutionProjects [MSBCT]", "GetSolutionProjects></GetSolutionProjects>"),
            ("HxCompiler [MSBCT]", "HxCompiler></HxCompiler>"),
            ("ILMerge [MSBCT]", "ILMerge></ILMerge>"),
            ("InstallAspNet [MSBCT]", "InstallAspNet></InstallAspNet>"),
            ("InstallAssembly [MSBCT]", "InstallAssembly></InstallAssembly>"),
            ("JSCompress [MSBCT]", "JSCompress></JSCompress>"),
            ("Mail [MSBCT]", "Mail></Mail>"),
            ("Merge [MSBCT]", "Merge></Merge>"),
            ("Modulo [MSBCT]", "Modulo Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Modulo>"),
            ("Move [MSBCT]", "Move></Move>"),
            ("MRefBuilder [MSBCT]", "MRefBuilder></MRefBuilder>"),
            ("Multiple [MSBCT]", "Multiple Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Multiple>"),
            ("NDoc [MSBCT]", "NDoc></NDoc>"),
            ("NUnit [MSBCT]", "NUnit></NUnit>"),
            ("Prompt [MSBCT]", "Prompt></Prompt>"),
            ("RegexMatch [MSBCT]", "RegexMatch></RegexMatch>"),
            ("RegexReplace [MSBCT]", "RegexReplace></RegexReplace>"),
            ("RegistryRead [MSBCT]", "RegistryRead></RegistryRead>"),
            ("RegistryWrite [MSBCT]", "RegistryWrite></RegistryWrite>"),
            ("RoboCopy [MSBCT]", "RoboCopy></RoboCopy>"),
            ("Sandcastle [MSBCT]", "Sandcastle></Sandcastle>"),
            ("Script [MSBCT]", "Script></Script>"),
            ("ServiceController [MSBCT]", "ServiceController></ServiceController>"),
            ("ServiceQuery [MSBCT]", "ServiceQuery></ServiceQuery>"),
            ("Sleep [MSBCT]", "Sleep></Sleep>"),
            ("Sound [MSBCT]", "Sound></Sound>"),
            ("SqlExecute [MSBCT]", "SqlExecute></SqlExecute>"),
            ("SqlPubWiz [MSBCT]", "SqlPubWiz></SqlPubWiz>"),
            ("Subtract [MSBCT]", "Subtract Numbers=\"$1\">\n\t<Output TaskParameter=\"Result\" PropertyName=\"$2\" />\n</Subtract>"),
            ("SvnCheckout [MSBCT]", "SvnCheckout></SvnCheckout>"),
            ("SvnClient [MSBCT]", "SvnClient></SvnClient>"),
            ("SvnCommit [MSBCT]", "SvnCommit></SvnCommit>"),
            ("SvnCopy [MSBCT]", "SvnCopy></SvnCopy>"),
            ("SvnExport [MSBCT]", "SvnExport></SvnExport>"),
            ("SvnInfo [MSBCT]", "SvnInfo></SvnInfo>"),
            ("SvnUpdate [MSBCT]", "SvnUpdate></SvnUpdate>"),
            ("SvnVersion [MSBCT]", "SvnVersion></SvnVersion>"),
            ("TaskSchema [MSBCT]", "TaskSchema></TaskSchema>"),
            ("TemplateFile [MSBCT]", "TemplateFile></TemplateFile>"),
            ("TfsVersion [MSBCT]", "TfsVersion></TfsVersion>"),
            ("Time [MSBCT]", "Time></Time>"),
            ("UninstallAssembly [MSBCT]", "UninstallAssembly></UninstallAssembly>"),
            ("Unzip [MSBCT]", "Unzip></Unzip>"),
            ("User [MSBCT]", "User></User>"),
            ("Version [MSBCT]", "Version></Version>"),
            ("VssAdd [MSBCT]", "VssAdd></VssAdd>"),
            ("VssCheckin [MSBCT]", "VssCheckin></VssCheckin>"),
            ("VssCheckout [MSBCT]", "VssCheckout></VssCheckout>"),
            ("VssClean [MSBCT]", "VssClean></VssClean>"),
            ("VssDiff [MSBCT]", "VssDiff></VssDiff>"),
            ("VssGet [MSBCT]", "VssGet></VssGet>"),
            ("VssHistory [MSBCT]", "VssHistory></VssHistory>"),
            ("VssLabel [MSBCT]", "VssLabel></VssLabel>"),
            ("VssUndoCheckout [MSBCT]", "VssUndoCheckout></VssUndoCheckout>"),
            ("WebDirectoryCreate [MSBCT Simple]", "WebDirectoryCreate VirtualDirectoryName=\"$1\" VirtualDirectoryPhysicalPath=\"$2\" />"),
            ("WebDirectoryCreate [MSBCT Full]", "WebDirectoryCreate\n\tVirtualDirectoryName=\"$1\"\n\tVirtualDirectoryPhysicalPath=\"$2\"\n\tAccessExecute=\"${3:False}\"\n\tAccessNoRemoteExecute=\"${4:False}\"\n\tAccessNoRemoteRead=\"${5:False}\"\n\tAccessNoRemoteScript=\"${6:False}\"\n\tAccessNoRemoteWrite=\"${7:False}\"\n\tAccessRead=\"${8:True}\"\n\tAccessScript=\"${9:True}\"\n\tAccessSource=\"${10:False}\"\n\tAccessSsl=\"${11:False}\"\n\tAccessSsl128=\"${12:False}\"\n\tAccessSslMapCert=\"${13:False}\"\n\tAccessSslNegotiateCert=\"${14:False}\"\n\tAccessSslRequireCert=\"${15:False}\"\n\tAccessWrite=\"${16:False}\"\n\tAnonymousPasswordSync=\"${17:True}\"\n\tAppAllowClientDebug=\"${18:False}\"\n\tAppAllowDebugging=\"${19:False}\"\n\tAspAllowSessionState=\"${20:True}\"\n\tAspBufferingOn=\"${21:True}\"\n\tAspEnableApplicationRestart=\"${22:True}\"\n\tAspEnableAspHtmlFallback=\"${23:False}\"\n\tAspEnableChunkedEncoding=\"${24:False}\"\n\tAspEnableParentPaths=\"${25:True}\"\n\tAspEnableTypelibCache=\"${26:True}\"\n\tAspErrorsToNTLog=\"${27:False}\"\n\tAspExceptionCatchEnable=\"${28:True}\"\n\tAspLogErrorRequests=\"${29:True}\"\n\tAspScriptErrorMessage=\"${30:An error occurred on the server when processing the URL.  Please contact the system administrator.}\"\n\tAspScriptErrorSentToBrowser=\"${31:True}\"\n\tAspTrackThreadingModel=\"${32:False}\"\n\tAuthAnonymous=\"${33:True}\"\n\tAuthBasic=\"${34:False}\"\n\tAuthNtlm=\"${35:False}\"\n\tAuthPersistSingleRequest=\"${36:False}\"\n\tAuthPersistSingleRequestAlwaysIfProxy=\"${37:False}\"\n\tAuthPersistSingleRequestIfProxy=\"${38:True}\"\n\tCacheControlNoCache=\"${39:False}\"\n\tCacheIsapi=\"${40:True}\"\n\tContentIndexed=\"${41:True}\"\n\tCpuAppEnabled=\"${42:True}\"\n\tCpuCgiEnabled=\"${43:True}\"\n\tCreateCgiWithNewConsole=\"${44:False}\"\n\tCreateProcessAsUser=\"${45:True}\"\n\tDefaultDoc=\"${46:Default.htm, Default.asp, index.htm, iisstart.asp, Default.aspx}\"\n\tDirBrowseShowDate=\"${47:True}\"\n\tDirBrowseShowExtension=\"${48:True}\"\n\tDirBrowseShowLongDate=\"${49:True}\"\n\tDirBrowseShowSize=\"${50:True}\"\n\tDirBrowseShowTime=\"${51:True}\"\n\tDontLog=\"${52:False}\"\n\tEnableDefaultDoc=\"${53:True}\"\n\tEnableDirBrowsing=\"${54:False}\"\n\tEnableDocFooter=\"${55:False}\"\n\tEnableReverseDns=\"${56:False}\"\n\tSsiExecDisable=\"${57:False}\"\n\tUncAuthenticationPassthrough=\"${58:False}\"\n\tHostHeaderName=\"$59\"\n\tPassword=\"$60\"\n\tServerName=\"${61:localhost}\"\n\tServerPort=\"${62:80}\"\n\tUsername=\"$63\" />"),
            ("WebDirectoryDelete [MSBCT Simple]", "WebDirectoryDelete VirtualDirectoryName=\"$1\" />"),
            ("WebDirectoryDelete [MSBCT Full]", "WebDirectoryDelete\n\tVirtualDirectoryName=\"$1\"\n\tHostHeaderName=\"$2\"\n\tPassword=\"$3\"\n\tServerName=\"${4:localhost}\"\n\tServerPort=\"${5:80}\"\n\tUsername=\"$6\" />"),
            ("WebDirectoryScriptMap [MSBCT Simple]", "WebDirectoryScriptMap\n\tEnableScriptEngine=\"${1:False}\"\n\tExecutablePath=\"$2\"\n\tExtension=\"$3\"\n\tMapToAspNet=\"${4:False}\"\n\tVerbs=\"$5\"\n\tVerifyFileExists=\"${6:False}\"\n\tVirtualDirectoryName=\"$7\" />"),
            ("WebDirectoryScriptMap [MSBCT Full]", "WebDirectoryScriptMap\n\tEnableScriptEngine=\"${1:False}\"\n\tExecutablePath=\"$2\"\n\tExtension=\"$3\"\n\tMapToAspNet=\"${4:False}\"\n\tVerbs=\"$5\"\n\tVerifyFileExists=\"${6:False}\"\n\tVirtualDirectoryName=\"$7\"\n\tHostHeaderName=\"$8\"\n\tPassword=\"$9\"\n\tServerName=\"${10:localhost}\"\n\tServerPort=\"${11:80}\"\n\tUsername=\"$12\" />"),
            ("WebDirectorySetting [MSBCT Get]", "WebDirectorySetting VirtualDirectoryName=\"$1\" SettingName=\"$2\">\n\t<Output TaskParameter=\"SettingValue\" PropertyName=\"$3\" />\n</WebDirectorySetting>"),
            ("WebDirectorySetting [MSBCT Set]", "WebDirectorySetting\n\tVirtualDirectoryName=\"$1\"\n\tSettingName=\"$2\"\n\tSettingValue=\"$3\" />"),
            ("WebDirectorySetting [MSBCT Full]", "WebDirectorySetting\n\tVirtualDirectoryName=\"$1\"\n\tSettingName=\"$2\"\n\tSettingValue=\"$3\"\n\tHostHeaderName=\"$4\"\n\tPassword=\"$5\"\n\tServerName=\"${6:localhost}\"\n\tServerPort=\"${7:80}\"\n\tUsername=\"$8\">\n\t<Output TaskParameter=\"SettingValue\" PropertyName=\"$9\" />\n</WebDirectorySetting>"),
            ("WebDownload [MSBCT]", "WebDownload></WebDownload>"),
            ("XmlMassUpdate [MSBCT]", "XmlMassUpdate></XmlMassUpdate>"),
            ("XmlQuery [MSBCT]", "XmlQuery></XmlQuery>"),
            ("XmlRead [MSBCT]", "XmlRead></XmlRead>"),
            ("XmlUpdate [MSBCT]", "XmlUpdate></XmlUpdate>"),
            ("Xslt [MSBCT]", "Xslt></Xslt>"),
            ("XslTransform [MSBCT]", "XslTransform></XslTransform>"),
            ("Zip [MSBCT Simple]", "Zip\n\tFiles=\"${1:@(Files)}\"\n\tFlatten=\"${2:False}\"\n\tWorkingDirectory=\"$3\"\n\tZipFileName=\"$4\" />"),
            ("Zip [MSBCT Full]", "Zip\n\tComment=\"$1\"\n\tFiles=\"${2:@(Files)}\"\n\tEncryption=\"${3:None}\"\n\tFlatten=\"${4:False}\"\n\tPassword=\"$5\"\n\tWorkingDirectory=\"$6\"\n\tZipFileName=\"$7\"\n\tZipLevel=\"${8:6}\" />")
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
