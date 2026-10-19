param(
    [string]$Programmer = 'C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe'
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Programmer)) { throw 'Install STM32CubeProgrammer or specify -Programmer.' }
# First installation only: removes existing firmware and saved motor/app settings.
# Wire SWDIO, SWCLK, NRST, GND and target voltage reference before running.
& $Programmer -c port=SWD mode=UR reset=HWrst freq=1000 -e all
if ($LASTEXITCODE -ne 0) { throw 'Erase failed; no firmware was written.' }
& $Programmer -c port=SWD mode=UR reset=HWrst freq=1000 -d "$PSScriptRoot\drv8302_b02_factory.hex" -v -rst
if ($LASTEXITCODE -ne 0) { throw 'Programming or verification failed.' }
Write-Host 'Programming and read-back verification completed.'
