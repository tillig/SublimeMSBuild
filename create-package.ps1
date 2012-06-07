# This script assumes use of the PowerShell Community Extensions Module
# http://pscx.codeplex.com/
Import-Module Pscx
Get-ChildItem -Exclude .git*,*.ps1 | Write-Zip -Level 9 -OutputPath MSBuild.sublime-package