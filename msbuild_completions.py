import sublime, sublime_plugin
import re

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
        # Only trigger within item references
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
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)

# Provide completions that match just after typing an opening angle bracket
class TagCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within MSBuild
        if not view.match_selector(locations[0],
                "source.msbuild"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        return ([
            ("Target", "Target Name=\"$1\" DependsOnTargets=\"$2\">\n\t$3\n</Target>"),
            ("  OnError", "OnError ExecuteTargets=\"$1\" />"),
            
            ("ItemGroup", "ItemGroup>\n\t$1\n</ItemGroup>"),

            ("PropertyGroup", "PropertyGroup>\n\t$1\n</PropertyGroup>"),
            
            ("UsingTask", "UsingTask TaskName=\"$1\" AssemblyName=\"$2\" />"),

            ("ImportGroup", "ImportGroup Condition=\"$1\">\n\t<Import Project=\"$2\" />\n</ImportGroup>"),
            ("  Import", "Import Project=\"$1\" />"),

            ("Choose", "Choose>\n\t<When Condition=\"$1\">$2</When>\n\t<Otherwise>$3</Otherwise>\n</Choose>"),
            ("  When", "When Condition=\"$1\">$2</When>"),
            ("  Otherwise", "Otherwise>$1</Otherwise>"),

            ("Project", "Project DefaultTargets=\"$1\" InitialTargets=\"$2\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\" ToolsVersion=\"4.0\">\n\t$3\n</Project>"),

            ("AL", "AL\n\tAlgorithmID=\"${1:CALG_SHA1}\"\n\tBaseAddress=\"$2\"\n\tCompanyName=\"${3:MyCompany}\"\n\tConfiguration=\"$4\"\n\tCopyright=\"$5\"\n\tCulture=\"${6:en-US}\"\n\tDelaySign=\"${7:false}\"\n\tDescription=\"$8\"\n\tEmbedResources=\"${9:@(ResourceList)}\"\n\tEvidenceFile=\"${10:Security.Evidence}\"\n\tFileVersion=\"${11:1.0.0.0}\"\n\tFlags=\"${12:0x0000}\"\n\tGenerateFullPaths=\"${13:false}\"\n\tKeyContainer=\"${14:KeyPair}\"\n\tKeyFile=\"${15:StrongNameKey.snk}\"\n\tLinkResources=\"${16:@(ResourceList)}\"\n\tMainEntryPoint=\"${17:App.Main}\"\n\tPlatform=\"${18:anycpu}\"\n\tProductName=\"${19:MyProduct}\"\n\tProductVersion=\"${20:1.0.0.0}\"\n\tResponseFiles=\"${21:@(ResponseFiles)}\"\n\tSdkToolsPath=\"${22:Path\\To\\Sdk}\"\n\tSourceModules=\"${23:@(Modules)}\"\n\tTargetType=\"${24:library}\"\n\tTemplateFile=\"${25:Template.dll}\"\n\tTimeout=\"$26\"\n\tTitle=\"${27:AssemblyTitle}\"\n\tToolPath=\"${28:Path\\To\\Al\\Folder}\"\n\tTrademark=\"$29\"\n\tVersion=\"${30:1.0.0.0}\"\n\tWin32Icon=\"${31:icon.ico}\"\n\tWin32Resource=\"${32:resources.res}\">\n\t<Output TaskParameter=\"OutputAssembly\" ItemName=\"$33\" />\n\t<Output TaskParameter=\"ExitCode\" PropertyName=\"$34\" />\n</AL>"),
            ("AspNetCompiler", "AspNetCompiler\n\tAllowPartiallyTrustedCallers=\"${1:true}\"\n\tClean=\"${2:false}\"\n\tDebug=\"${3:false}\"\n\tDelaySign=\"${4:false}\"\n\tFixedNames=\"${5:false}\"\n\tForce=\"${6:false}\"\n\tKeyContainer=\"${7:KeyPair}\"\n\tKeyFile=\"${8:StrongNameKey.snk}\"\n\tMetabasePath=\"${9:LM/W3SVC/1/ROOT}\"\n\tPhysicalPath=\"${10:C:\\inetpub\\wwwroot}\"\n\tTargetFrameworkMoniker=\"${11:.NETFramework,Version=v4.0}\"\n\tTargetPath=\"${12:Destination\\Folder}\"\n\tUpdateable=\"${13:false}\"\n\tVirtualPath=\"${14:/Virtual/App/Path}\" />"),
            ("AssignCulture", "AssignCulture Files=\"${1:@(Files)}\">\n\t<Output TaskParameter=\"AssignedFiles\" ItemName=\"$2\" />\n\t<Output TaskParameter=\"AssignedFilesWithCulture\" ItemName=\"$3\" />\n\t<Output TaskParameter=\"AssignedFilesWithNoCulture\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"CultureNeutralAssignedFiles\" ItemName=\"$5\" />\n</AssignCulture>"),
            ("AssignProjectConfiguration", "AssignProjectConfiguration\n\tCurrentProjectConfiguration=\"$1\"\n\tCurrentProjectPlatform=\"$2\"\n\tDefaultToVcxPlatformMapping=\"$3\"\n\tOnlyReferenceAndBuildProjectsEnabledInSolutionConfiguration=\"$4\"\n\tOutputType=\"$5\"\n\tResolveConfigurationPlatformUsingMappings=\"$6\"\n\tShouldUnsetParentConfigurationAndPlatform=\"$7\"\n\tSolutionConfigurationContents=\"$8\"\n\tVcxToDefaultPlatformMapping=\"$9\">\n\t<Output TaskParameter=\"AssignedProjects\" ItemName=\"$10\" />\n\t<Output TaskParameter=\"UnassignedProjects\" ItemName=\"$11\" />\n</AssignProjectConfiguration>"),
            ("AssignTargetPath", "AssignTargetPath RootFolder=\"$1\" Files=\"${2:@(Files)}\">\n\t<Output TaskParameter=\"AssignedFiles\" ItemName=\"$3\" />\n</AssignTargetPath>"),
            ("CallTarget [Simple]", "CallTarget Targets=\"$1\" />"),
            ("CallTarget [Full]", "CallTarget Targets=\"$1\" RunEachTargetSeparately=\"${2:false}\" UseResultsCache=\"${3:false}\">\n\t<Output TaskParameter=\"TargetOutputs\" ItemName=\"$4\" />\n</CallTarget>"),
            ("CombinePath", "CombinePath BasePath=\"$1\" Paths=\"${2:@(Paths)}\">\n\t<Output TaskParameter=\"CombinedPaths\" ItemName=\"$3\" />\n</CombinePath>"),
            ("ConvertToAbsolutePath", "ConvertToAbsolutePath Paths=\"${1:@(Paths)}\">\n\t<Output TaskParameter=\"AbsolutePaths\" ItemName=\"$2\" />\n</ConvertToAbsolutePath>"),
            ("Copy [Simple]", "Copy SourceFiles=\"${1:@(Files)}\" DestinationFiles=\"${2:@(Files->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\" DestinationFolder=\"$3\" />"),
            ("Copy [Full]", "Copy\n\tDestinationFiles=\"${1:@(Files->'c:\\MyDestinationTree\\%(RecursiveDir)%(Filename)%(Extension)')}\"\n\tDestinationFolder=\"$2\"\n\tOverwriteReadOnlyFiles=\"${3:false}\"\n\tRetries=\"${4:0}\"\n\tRetryDelayMilliseconds=\"${5:1000}\"\n\tSkipUnchangedFiles=\"${6:false}\"\n\tSourceFiles=\"${7:@(Files)}\"\n\tUseHardlinksIfPossible=\"${8:false}\">\n\t<Output TaskParameter=\"CopiedFiles\" ItemName=\"$9\" />\n</Copy>"),
            ("CreateCSharpManifestResourceName", "CreateCSharpManifestResourceName ResourceFiles=\"$1\" RootNamespace=\"$2\" PrependCultureAsDirectory=\"${3:true}\">\n\t<Output TaskParameter=\"ManifestResourceNames\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"ResourceFilesWithManifestResourceNames\" ItemName=\"$5\" />\n</CreateCSharpManifestResourceName>"),
            ("CreateItem [Simple]", "CreateItem Include=\"$1\" Exclude=\"$2\">\n\t<Output TaskParameter=\"Include\" ItemName=\"$3\" />\n</CreateItem>"),
            ("CreateItem [Full]", "CreateItem Include=\"$1\"\n\tExclude=\"$2\"\n\tAdditionalMetadata=\"$3\"\n\tPreserveExistingMetadata=\"${4:true}\">\n\t<Output TaskParameter=\"Include\" ItemName=\"$5\" />\n</CreateItem>"),
            ("CreateProperty", "CreateProperty Value=\"$1\">\n\t<Output TaskParameter=\"Value\" PropertyName=\"$2\" />\n</CreateProperty>"),
            ("CreateVisualBasicManifestResourceName", "CreateVisualBasicManifestResourceName ResourceFiles=\"$1\" RootNamespace=\"$2\" PrependCultureAsDirectory=\"${3:true}\">\n\t<Output TaskParameter=\"ManifestResourceNames\" ItemName=\"$4\" />\n\t<Output TaskParameter=\"ResourceFilesWithManifestResourceNames\" ItemName=\"$5\" />\n</CreateVisualBasicManifestResourceName>"),
            ("Csc", "Csc\n\tAdditionalLibPaths=\"${1:@(LibPaths)}\"\n\tAddModules=\"$2\"\n\tAllowUnsafeBlocks=\"${3:false}\"\n\tApplicationConfiguration=\"${4:App.config}\"\n\tBaseAddress=\"$5\"\n\tCheckForOverflowUnderflow=\"${6:false}\"\n\tCodePage=\"$7\"\n\tDebugType=\"${8:full}\"\n\tDefineConstants=\"${9:CODE_ANALYSIS}\"\n\tDelaySign=\"${10:false}\"\n\tDisabledWarnings=\"$11\"\n\tDocumentationFile=\"${12:MyProject.xml}\"\n\tEmitDebugInformation=\"${13:true}\"\n\tErrorReport=\"${14:prompt}\"\n\tFileAlignment=\"$15\"\n\tGenerateFullPaths=\"${16:false}\"\n\tKeyContainer=\"${17:KeyPair}\"\n\tKeyFile=\"${18:StrongNameKey.snk}\"\n\tLangVersion=\"${19:default}\"\n\tLinkResources=\"${20:@(ResourceList)}\"\n\tMainEntryPoint=\"${21:App.Main}\"\n\tModuleAssemblyName=\"$22\"\n\tNoConfig=\"${23:false}\"\n\tNoLogo=\"${24:true}\"\n\tNoStandardLib=\"${25:false}\"\n\tNoWin32Manifest=\"${26:false}\"\n\tOptimize=\"${27:true}\"\n\tOutputAssembly=\"${28:MyProject.dll}\"\n\tPdbFile=\"${29:MyProject.pdb}\"\n\tPlatform=\"${30:anycpu}\"\n\tReferences=\"${31:@(ReferenceList)}\"\n\tResources=\"${32:@(ResourceList)}\"\n\tResponseFiles=\"$33\"\n\tSources=\"${34:@(SourceList)}\"\n\tTargetType=\"${35:library}\"\n\tTreatWarningsAsErrors=\"${36:false}\"\n\tUtf8Output=\"${37:false}\"\n\tWarningLevel=\"${38:4}\"\n\tWarningsAsErrors=\"$39\"\n\tWarningsNotAsErrors=\"$40\"\n\tWin32Icon=\"${41:icon.ico}\"\n\tWin32Manifest=\"${42:file.manifest}\"\n\tWin32Resource=\"${43:resources.res}\">\n\t<Output TaskParameter=\"OutputAssembly\" ItemName=\"$44\" />\n</Csc>"),
            ("Delete", "Delete></Delete>"),
            ("Error", "Error></Error>"),
            ("Exec", "Exec></Exec>"),
            ("FindAppConfigFile", "FindAppConfigFile></FindAppConfigFile>"),
            ("FindInList", "FindInList></FindInList>"),
            ("FindUnderPath", "FindUnderPath></FindUnderPath>"),
            ("FormatUrl", "FormatUrl></FormatUrl>"),
            ("FormatVersion", "FormatVersion></FormatVersion>"),
            ("GenerateApplicationManifest", "GenerateApplicationManifest></GenerateApplicationManifest>"),
            ("GenerateDeploymentManifest", "GenerateDeploymentManifest></GenerateDeploymentManifest>"),
            ("GenerateResource", "GenerateResource></GenerateResource>"),
            ("GenerateTrustInfo", "GenerateTrustInfo></GenerateTrustInfo>"),
            ("GetAssemblyIdentity", "GetAssemblyIdentity></GetAssemblyIdentity>"),
            ("GetFrameworkPath", "GetFrameworkPath></GetFrameworkPath>"),
            ("GetFrameworkSdkPath", "GetFrameworkSdkPath></GetFrameworkSdkPath>"),
            ("GetReferenceAssemblyPaths", "GetReferenceAssemblyPaths></GetReferenceAssemblyPaths>"),
            ("LC", "LC></LC>"),
            ("MakeDir", "MakeDir></MakeDir>"),
            ("Message", "Message></Message>"),
            ("Move", "Move></Move>"),
            ("MSBuild", "MSBuild></MSBuild>"),
            ("ReadLinesFromFile", "ReadLinesFromFile></ReadLinesFromFile>"),
            ("RegisterAssembly", "RegisterAssembly></RegisterAssembly>"),
            ("RemoveDir", "RemoveDir></RemoveDir>"),
            ("RemoveDuplicates", "RemoveDuplicates></RemoveDuplicates>"),
            ("RequiresFramework35SP1Assembly", "RequiresFramework35SP1Assembly></RequiresFramework35SP1Assembly>"),
            ("ResolveAssemblyReference", "ResolveAssemblyReference></ResolveAssemblyReference>"),
            ("ResolveComReference", "ResolveComReference></ResolveComReference>"),
            ("ResolveKeySource", "ResolveKeySource></ResolveKeySource>"),
            ("ResolveManifestFiles", "ResolveManifestFiles></ResolveManifestFiles>"),
            ("ResolveNativeReference", "ResolveNativeReference></ResolveNativeReference>"),
            ("REsolveNonMSBuildProjectOutput", "REsolveNonMSBuildProjectOutput></REsolveNonMSBuildProjectOutput>"),
            ("SGen", "SGen></SGen>"),
            ("SignFile", "SignFile></SignFile>"),
            ("Touch", "Touch></Touch>"),
            ("UnregisterAssembly", "UnregisterAssembly></UnregisterAssembly>"),
            ("UpdateManifest", "UpdateManifest></UpdateManifest>"),
            ("Vbc", "Vbc></Vbc>"),
            ("Warning", "Warning></Warning>"),
            ("WriteCodeFragment", "WriteCodeFragment></WriteCodeFragment>"),
            ("WriteLinesToFile", "WriteLinesToFile></WriteLinesToFile>"),
            ("XmlPeek", "XmlPeek></XmlPeek>"),
            ("XmlPoke", "XmlPoke></XmlPoke>"),
            ("XslTransformation", "XslTransformation></XslTransformation>")
        ], sublime.INHIBIT_WORD_COMPLETIONS)

# Provide completions that match just after typing a . inside a %() item reference
class WellKnownItemMetadataCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within item references
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
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
