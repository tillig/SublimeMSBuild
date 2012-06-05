import sublime, sublime_plugin
import re

def match(rex, str):
    m = rex.match(str)
    if m:
        return m.group(0)
    else:
        return None

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

            ("AL", "AL\n\tAlgorithmID=\"$1\"\n\tBaseAddress=\"$2\"\n\tCompanyName=\"$3\"\n\tConfiguration=\"$4\"\n\tCopyright=\"$5\"\n\tCulture=\"$6\"\n\tDelaySign=\"$7\"\n\tDescription=\"$8\"\n\tEmbedResources=\"$9\"\n\tEvidenceFile=\"$10\"\n\tExitCode=\"$11\"\n\tFileVersion=\"$12\"\n\tFlags=\"$13\"\n\tGenerateFullPaths=\"$14\"\n\tKeyContainer=\"$15\"\n\tKeyFile=\"$16\"\n\tLinkResources=\"$17\"\n\tMainEntryPoint=\"$18\"\n\tOutputAssembly=\"$19\"\n\tPlatform=\"$20\"\n\tProductName=\"$21\"\n\tProductVersion=\"$22\"\n\tResponseFiles=\"$23\"\n\tSdkToolsPath=\"$24\"\n\tSourceModules=\"$25\"\n\tTargetType=\"$26\"\n\tTemplateFile=\"$27\"\n\tTimeout=\"$28\"\n\tTitle=\"$29\"\n\tToolPath=\"$30\"\n\tTrademark=\"$31\"\n\tVersion=\"$32\"\n\tWin32Icon=\"$33\"\n\tWin32Resource=\"$34\">\n\t<Output TaskParameter=\"OutputAssembly\" ItemName=\"\" />\n</AL>"),
            ("AspNetCompiler", "AspNetCompiler></AspNetCompiler>"),
            ("AssignCulture", "AssignCulture></AssignCulture>"),
            ("AssignProjectConfiguration", "AssignProjectConfiguration></AssignProjectConfiguration>"),
            ("AssignTargetPath", "AssignTargetPath></AssignTargetPath>"),
            ("CallTarget", "CallTarget></CallTarget>"),
            ("CombinePath", "CombinePath></CombinePath>"),
            ("ConvertToAbsolutePath", "ConvertToAbsolutePath></ConvertToAbsolutePath>"),
            ("Copy", "Copy></Copy>"),
            ("CreateCSharpManifestResourceName", "CreateCSharpManifestResourceName></CreateCSharpManifestResourceName>"),
            ("CreateItem", "CreateItem></CreateItem>"),
            ("CreateProperty", "CreateProperty></CreateProperty>"),
            ("CreateVisualBasicManifestResourceName", "CreateVisualBasicManifestResourceName></CreateVisualBasicManifestResourceName>"),
            ("Csc", "Csc></Csc>"),
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
            (".RootDir", ".RootDir"),
        ], sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)
