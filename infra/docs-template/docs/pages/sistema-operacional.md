# Sistema Operacional

De acordo com alguns apontamentos do TCE, entende-se que o melhor ambiente de desenvolvimento é distro Linux _Debian-based_.

<br>

---

## WSL

Considerando que o MPSP usa majoritariamente _Windows_, é possível contornar usando _Windows Subsystem for Linux (WSL)_. Fiz isso para desenvolver no Ubuntu.

Abaixo alguns comandos que podem auxiliar a usar o _WSL_.

```shell
# Habilita Recurso Windows Subsystem for Linux
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

# Habilita Recurso Virtual Machine Platform
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform

# Lista Distribuições Instaladas
wsl --list

# Instala Ubuntu
wsl --install -d Ubuntu-24.04

# Termina
wsl --terminate Ubuntu-24.04
```

<br>

É possível também usar _vagrant_ ou, ainda, _devcontainers_.
