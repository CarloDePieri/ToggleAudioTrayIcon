hostname = win-ToggleAudioTrayIcon


shell:
	vagrant ssh

ssh_config:
	vagrant ssh-config > ssh_config

mount: ssh_config
	mkdir -p mounted && \
		sshfs -v -F `realpath ssh_config` $(hostname):/C:/ToggleAudioTrayIcon mounted

umount:
	umount mounted & rm -rf mounted

sync: ssh_config
	rsync -ah -progress -e 'ssh -F ssh_config' --exclude-from=.rsyncignore ../ $(hostname):../../ToggleAudioTrayIcon && \
		vagrant winrm -c 'icacls C:\ToggleAudioTrayIcon\*.bat /grant vagrant:RX'


# uhm

check: ssh_config
	rsync -avun -e 'ssh -F ssh_config' --exclude-from=.rsyncignore ../ $(hostname):../../ToggleAudioTrayIcon


uhm: ssh_config
	rsync -avun --stats -e 'ssh -F ssh_config' --exclude-from=.rsyncignore ../ $(hostname):../../ToggleAudioTrayIcon | grep 'Number of regular files transferred' | awk -F ": " '{print $$2}'
