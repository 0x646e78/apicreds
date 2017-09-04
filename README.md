apicreds
========

A more secure than plaintext API credential management system.  Credentials are stored in an AES encrypted filestore.

This is presently tailored for AWS, the idea is to make this more generic.

You can use it to load creds into your environment at the start of your work session, or just print them once if you prefer.


Install
-------

1) Clone this repository

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) I suggest adding the repo location to $PATH

```bash
cd apicreds && printf "\n# ApiCreds\nPATH=$PATH:$(pwd)" >> ~/.bashrc
```

Use
----

By default your keys will be stored in an AES encrypted file at `~/.apicreds.aes`

You can change this location with the switch `-f`

Upon your first use, you will be prompted to choose a passphrase.

### Storing a credential set

```
$ apicreds -i
Enter your passphrase>

Enter the name of your new AWS environment: prod
Enter a brief desciption of the environment: AWS prod environment
Enter your AWS Access Key ID: <ACCESS-KEY-ID>
Enter your AWS Secret Key: <SECRET-ACCESS-KEY>
Enter the default region for this environment (blank for none):
```

### Exporting variables into your current shell

```
. apicreds -e <env>
```

### List all stored credential sets

```
apicreds -l
```

TODO
-----

Refer to the project Wiki for further ideas of expansion:

*https://github.com/auraltension/apicreds/wiki/TODO*
