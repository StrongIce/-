$ExportFile = "C:\admins.csv"
$SearchBase = "DC=corp,DC=ru"
$AdminList = @{}
$ToCSV = ""
 
function Get-LocalAdmin { 
    param ($strcomputer)
    try {
       $users = Gwmi win32_groupuser –computer $strcomputer -ErrorAction Stop
    } catch {
        Write-Host $strcomputer
    }
    if ($users) {
        $admins = $users |? { ($_.groupcomponent –match 'Администраторы') -or ($_.groupcomponent –match 'Administrators') }
        $return = $admins |% { 
            $_.partcomponent –match “.+Domain\=(.+)\,Name\=(.+)$” > $nul 
            $matches[1].trim('"') + “\” + $matches[2].trim('"') 
        }
        return $return
    }
}
 
$ServersList = Get-ADComputer -SearchBase $SearchBase -Filter * -Properties OperatingSystem | Where { $_.OperatingSystem -match "Windows" }
$ServersList | Select-Object Name | ForEach-Object {
    $UserList = Get-LocalAdmin $_.Name
    if ($UserList) {
        $AdminList[$_.Name] = $UserList
    }
}
 
$AdminList.Keys | % {
    $ServerName = $_
    $AdminUsers = $AdminList[$ServerName]
    $ToCSV += "$ServerName;$AdminUsers`r`n"
}
 
if (Test-Path $ExportFile) {
    Remove-Item $ExportFile
}
 
$ToCSV >> $ExportFile