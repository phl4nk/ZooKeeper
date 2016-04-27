# ZooKeeper

Continuously monitor a file to watch for any (potentially malicious) URIs. Attempt to download them before they expire.

### Usage
`ZooKeeper.pl <log_file> <zoo_folder>`

```sh
$ ZookKeeper.pl /var/log/apache2/access.log ~/Zoo/
[+] Zookeeper initiated
[+] Resource found: https://attacker.net/xxx/xzy/0day.zip
[+] File download returned with: 200
```

### TODO

- demonize
- proxy support
- network error handleing
- ignore local ip requests
- ignore baiting links
- automatic folder creation
