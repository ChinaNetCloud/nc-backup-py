# Load Configuration File
[XML]$Setting = Get-Content D:\Dev\Backup_Powershell\WinConfig.xml

# Global Parameters
$files = @($Setting.Configuration.Fileset.FilesetInclude.Parameter.value)
$filesxlu = @($Setting.Configuration.Fileset.FilesetExclude.Parameter.value)
$Obj = $Setting.Configuration.Compression.Objective
$Dest = $Setting.Configuration.Compression.Destination

# 7-Zip
$7zadd = '7z a -tzip'
$7zparam = '-mx0 -r0'
$7zxlu = '-x!'

$BakDate = (Get-Date).ToString("yyMMddhhmmss")
$zipfile = $Obj + '\Files' + $BakDate + '.zip'
$zipcmd = $7zadd + " " + $zipfile + " "

Function Bak2Zip
{
    # Fileset include
    for($i=0; $i -lt $files.Count; $i++)
    {
        $inclucmd = $inclucmd + $files[$i] + " "
    }

    # Fileset exclude
    for($j=0; $j -lt $filesxlu.Count; $j++)
    {
        $xlucmd = $xlucmd + $7zxlu + $filesxlu[$j] + " "
    }
    
    # Generate bakcup command
    $zipcmd = $zipcmd + $inclucmd + $7zparam + " " + $xlucmd
    $zipcmd

    Invoke-Expression $zipcmd | Out-Null
}

Bak2Zip