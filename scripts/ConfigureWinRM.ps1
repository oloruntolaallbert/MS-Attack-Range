param(
    [int]$Port = 5985,
    [switch]$EnableDefenderOnboarding,
    [string]$DefenderOnboardingScriptPath,
    [string[]]$DefenderOnboardingArguments
)

$ErrorActionPreference = 'Stop'

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force | Out-Null

Write-Host "[+] Configuring WinRM listener on port $Port" -ForegroundColor Cyan

function Ensure-ServiceRunning {
    param(
        [string]$Name
    )

    $service = Get-Service -Name $Name -ErrorAction Stop
    if ($service.StartType -ne 'Automatic') {
        Set-Service -Name $Name -StartupType Automatic
    }
    if ($service.Status -ne 'Running') {
        Start-Service -Name $Name
    }
}

function Invoke-DefenderOnboarding {
    param(
        [Parameter(Mandatory)]
        [string]$ScriptPath,
        [string[]]$Arguments
    )

    if (-not (Test-Path -Path $ScriptPath -PathType Leaf)) {
        throw "Microsoft Defender for Endpoint onboarding script not found at $ScriptPath"
    }

    Write-Host "[+] Running Microsoft Defender for Endpoint onboarding script" -ForegroundColor Cyan

    if ($Arguments) {
        $output = & $ScriptPath @Arguments 2>&1
    }
    else {
        $output = & $ScriptPath 2>&1
    }

    if (-not $?) {
        $message = "Microsoft Defender for Endpoint onboarding script failed"
        if ($output) {
            $message = "$message: $output"
        }
        throw $message
    }

    if ($output) {
        $output | ForEach-Object { Write-Host "    $_" }
    }

    Write-Host "[+] Microsoft Defender for Endpoint onboarding completed" -ForegroundColor Green
}

try {
    Enable-PSRemoting -Force -SkipNetworkProfileCheck | Out-Null

    Ensure-ServiceRunning -Name 'WinRM'

    $listener = Get-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet @{Address='*';Transport='HTTP'} -ErrorAction SilentlyContinue
    if (-not $listener) {
        Write-Host '[+] Creating WinRM HTTP listener' -ForegroundColor Cyan
        New-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet @{Address='*';Transport='HTTP'} -ValueSet @{Port=$Port} | Out-Null
    }
    else {
        if ($listener.Port -ne $Port) {
            Write-Host "[+] Updating WinRM HTTP listener to port $Port" -ForegroundColor Cyan
            Set-Item -Path 'WSMan:\localhost\Listener\Listener*\Port' -Value $Port
        }
    }

    Write-Host '[+] Enabling basic authentication and allowing unencrypted traffic' -ForegroundColor Cyan
    Set-Item -Path 'WSMan:\localhost\Service\AllowUnencrypted' -Value $true
    Set-Item -Path 'WSMan:\localhost\Service\Auth\Basic' -Value $true

    if (Get-Command -Name 'New-NetFirewallRule' -ErrorAction SilentlyContinue) {
        if (-not (Get-NetFirewallRule -DisplayName 'WinRM HTTP (5985)' -ErrorAction SilentlyContinue)) {
            Write-Host '[+] Creating firewall rule for WinRM HTTP' -ForegroundColor Cyan
            New-NetFirewallRule -DisplayName 'WinRM HTTP (5985)' -Direction Inbound -Protocol TCP -LocalPort $Port -Action Allow | Out-Null
        }
        else {
            Set-NetFirewallRule -DisplayName 'WinRM HTTP (5985)' -Enabled True | Out-Null
        }
    }
    else {
        Write-Warning 'Firewall cmdlets not available. Ensure TCP port is allowed manually.'
    }

    if ($EnableDefenderOnboarding) {
        if (-not $DefenderOnboardingScriptPath) {
            throw 'EnableDefenderOnboarding was specified, but no DefenderOnboardingScriptPath was provided.'
        }

        Invoke-DefenderOnboarding -ScriptPath $DefenderOnboardingScriptPath -Arguments $DefenderOnboardingArguments
    }
    elseif ($DefenderOnboardingScriptPath) {
        Write-Warning 'Defender onboarding script path provided without EnableDefenderOnboarding. Skipping execution.'
    }
    else {
        Write-Host '[+] Microsoft Defender for Endpoint onboarding not requested. Skipping.' -ForegroundColor Yellow
    }

    Write-Host '[+] WinRM configuration complete' -ForegroundColor Green
}
catch {
    Write-Error "[-] Failed to configure WinRM: $($_.Exception.Message)"
    exit 1
}
