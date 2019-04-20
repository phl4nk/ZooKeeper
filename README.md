# ZooKeeper

Continuously monitor a file to watch for any (potentially malicious) URIs. Attempt to download them before they expire.

### Usage

`zookeeper.py <log_file> <zoo_folder>`

#### Example
```sh
$ ./zookeeper.py /var/log/apache2/access.log ~/Zoo/
[+] Starting to watch Log file: /var/log/apache2/access.log
[!] Duplicate link, not re-downloading
[+] Attempting to download: https://attacker.net/xxx/xzy/0day.zip
[+] Saving resource 
```

### TODO

- demonize
- proxy support
- network error handleing
- ignore local ip requests
- ignore baiting links
- automatic folder creation
