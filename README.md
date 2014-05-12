apicreds
========

A secure API credential management system.  Credentials are stored in an AES encrypted filestore.

Presently tailored for AWS, work in progress to make this more generic.

Load at the start of your work session.  

Credentials stay in your shell environment for the remainder of your session.


Install
-------

1) Clone this repository

2) Install dependencies:

```
sudo pip install simple-crypt
```

Use
----

By default your keys will be stored in an AES encrypted file at ~/.apicreds.aes

You can change this location with the switch -f

I suggest adding the repo location to $PATH
```
cd apicreds && printf "\n# ApiCreds\nPATH=$PATH:$(pwd)" >> ~/.bashrc
```
Upon your first use, you will be prompted to choose a passphrase. Make it a good one.

### Store a credential set
```
$ apicreds -i
Enter your passphrase>

Enter the name of your new AWS environment: prod
Enter a brief desciption of the environment: AWS prod environment
Enter your AWS Access Key ID: <ACCESS-KEY-ID>
Enter your AWS Secret Key: <SECRET-ACCESS-KEY>
Enter the default region for this environment (blank for none):
```

### Export variables into your current shell
```
. apicreds -e <env>
```

### List all stored credential sets

```
apicreds -l
```

Tested On
---------

* Debian 7 with GNU Bash, version 4.2.37

TODO
-----

Refer to the project Wiki for further ideas of expansion:

*https://github.com/auraltension/apicreds/wiki/TODO*
