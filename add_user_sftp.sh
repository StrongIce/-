#!/bin/bash
user="$1"
echo "Пароль для  $user: " && read pass
useradd -M  -g sftp-group $user
echo -e "$pass\n$pass\n" | passwd  $user
mkdir -p /opt/sftp/$user
chmod 755 /opt/sftp/$user
echo "Match User $user" >> /etc/ssh/sshd_config
echo "  ForceCommand internal-sftp" >> /etc/ssh/sshd_config
echo "  PasswordAuthentication yes" >> /etc/ssh/sshd_config
echo "  ChrootDirectory /opt/sftp/$user" >> /etc/ssh/sshd_config
echo "  PermitTunnel no" >> /etc/ssh/sshd_config
echo "  AllowAgentForwarding no" >>/etc/ssh/sshd_config
echo "  AllowTcpForwarding no" >>/etc/ssh/sshd_config
echo "  X11Forwarding no" >> /etc/ssh/sshd_config
echo -e "Пользователь: $user\nПароль: $pass"
echo -e "Пользователь: $user\nПароль: $pass" >> users.txt
echo "____________________________" >> users.txt
service ssh restart

# ls | grep .sh | cut -d. -f -1  >> file.txt

   
