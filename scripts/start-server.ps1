Param(
    [string]$Action = 'start',
    [string]$ServerHost = '127.0.0.1',
    [int]$Port = 8080
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$root = Split-Path -Parent $scriptDir
$pidFile = Join-Path $root 'server.pid'
$outLog = Join-Path $root 'flask_stdout.log'
$errLog = Join-Path $root 'flask_stderr.log'

function Stop-Existing {
    if (Test-Path $pidFile) {
        try {
            $oldPid = Get-Content $pidFile | Select-Object -First 1
            if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
                Write-Output "Stopping existing server PID=$oldPid"
                Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
            }
        } catch {
            Write-Output "Failed stopping existing PID: $_"
        }
        Remove-Item $pidFile -ErrorAction SilentlyContinue
    }
}

if ($Action -eq 'stop') {
    Stop-Existing
    Write-Output 'Stopped.'
    exit 0
}

# start
Stop-Existing

if (Test-Path $outLog) { Remove-Item $outLog -Force }
if (Test-Path $errLog) { Remove-Item $errLog -Force }

$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) { $python = 'python' }

$args = "C:/Users/owner/OneDrive/Desktop/ai_robot_project/serve.py"

 $p = Start-Process -FilePath $python -ArgumentList $args -RedirectStandardOutput $outLog -RedirectStandardError $errLog -WorkingDirectory $root -PassThru
Start-Sleep -Seconds 1
if ($p -and (Get-Process -Id $p.Id -ErrorAction SilentlyContinue)) {
    $p.Id | Out-File -FilePath $pidFile -Encoding ascii
    Write-Output "Started server PID=$($p.Id), logs: $outLog / $errLog"
} else {
    Write-Output 'Failed to start server.'
}
