## Treetracker Admin Dev Setup

You can find the Project Repos
  - [Admin](https://github.com/Greenstand/treetracker-admin)
  - [Admin API](https://github.com/Greenstand/treetracker-admin-api)

## Project Structure
Treetracker web interface is composed of 3 tiers

1. Front End - (HTML,JS,CSS)
2. Middleware - (Node.js)
3. Back End - (PostGreSQL)

Tier 1 is `treetracker-web-clustering`. To serve this front-end you can use something like NGINX

Tier 2 is `treetracker-map-api-master`, and this uses node.js

Tier 3 is `PostGreSQL` backend.


## Setup
To set up all 3 tiers in same machine.

#### Server
So if you are using something like `Ubuntu 16.07 LTS`:

First do this:
```sh
sudo apt-get update
```

Then

Install nginx
```sh
sudo apt-get install nginx
```

After installation Nginx:

Edit `/etc.nginx/sites-availale/default`

Starting from where it says root `/var/www/html` use this:

`root /var/www/html;`

```sh
# Add index.php to the list if you are using PHP
index index.html index.htm index.nginx-debian.html index.php;

      set $httpc  "http://";
      set $ip "127.0.0.1";
      set $lc "127.0.0.1";
      server_name "${ip}";

      resolver 84.200.69.80;



      #for nodejs api we woudl like /ap/*whatever* to rouse to the api
      location ^~ /api {
          #although URL will start with /api,

      #first rewrite so that it looks like /api isn't there anymore from perspective of node.js
              rewrite ^/api/(.*)$ /$1 break;
      #proxy_pass means we send the request over to our local node.js server on port 3000
              proxy_pass "${httpc}${lc}:3000${uri}";

      #the following line is not used
      #try_files $uri $uri/ =404;
      }

  #this is if you want to install phppgadmin, a UI to administer your PostGreSQL visually
      location ~ \.php$ {


          fastcgi_pass unix:/run/php/php7.1-fpm.sock;
          include snippets/fastcgi-php.conf;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;


      }

  #this is to serve our front-end files (the actual visual map, etc.)
  location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;

  }
```

Now in `/var/www/html` place the contents of `treetracker-web-clustering`

Now you run `sudo service nginx restart`

(since you made nginx config changes)

now it should show the map if you load the page in your browser.
(P.S. if you use cloud hosting be sure you open up Port 80
Depending on provider you may have to do this in your hosting UI
For instance, Azure you need to add an Inbound Port Rule for Port 80)

In addition it is a good idea to use UFW (firewall for linux) if you can also.
(ufw may have a prerequisite)

You may possibly safely skip these steps though:
```sh
sudo ufw status

sudo ufw allow 'Nginx Full'
sudo ufw allow 22

sudo ufw delete allow 'Nginx HTTP'

sudo ufw enable

sudo ufw status
```
---------------------------------

You need to set up node api now.

in your home directory, create a new folder, e.g. "mapapi"

in this new directory, place the contents of `treetracker-map-api-master`.

Also in this new directory create `config.js` and in it put these lines:
```js
// exports.connectionString = "postgres://treetracker:tr33dev@localhost/treetracker";
// exports.connectionString = "postgres://treetracker:tr33dev@104.236.153.87/treetracker";
```

If you want to use `PostGreSQL` from upstream developers and not set up your own DB,
then you uncomment the 2nd line. If you do this, you're almost done!

But if you want to use PostGreSQL from same server and you DO want to set up your own DB,
then you uncomment the 1st line. If you do this, you'll need some more steps.

Next:

You need to install `nodejs`

```sh
sudo apt-get install nodejs
sudo apt-get install npm
```

Also you need to run:
```sh
npm install -g express
npm install -g body-parser
npm install -g pg
```
now `cd` to that directory `/home/yourusername/mapapi` and run `node index`

This starts the nodejs server in your current shell.
To exit, type `CTRL+C` or something like that to break the session.

NGINX by default persists upon restart or shutdown.
However, node.js does not. When you type node index that will hang your shell.

You'll need to open a 2nd shell to your server to perform any more operations

`recommended` - if you want the server persist across shutdown and restart(and be daemonized)

you should use something like this: [Key Metrics](http://pm2.keymetrics.io/)
Check PM2 module setup for nodejs (optional).
If this is fully in place you'd type something like `pm2 restart all` after changing anything from node.js
It could be even configured to auto-restart node.js when you change a certain js file
(but do this later if you like that sort of thing - get basics working first)

And remember for nginx you say `sudo service nginx restart`

You should try first with uncommenting the 2nd line from that config file before.

Like this:

```js
exports.connectionString = "postgres://treetracker:tr33dev@localhost/treetracker";
//exports.connectionString = "postgres://treetracker:tr33dev@104.236.153.87/treetracker";
```

If it works and you want your own `PostGreSQL`, follow these steps:


FIRST if you proceed, go back to that config.js line, comment the 2nd line,
uncomment the 1st line, and restart nodejs (or shut it down and leave it off)

Should look like this now

```js
exports.connectionString = "postgres://treetracker:tr33dev@localhost/treetracker";
//exports.connectionString = "postgres://treetracker:tr33dev@104.236.153.87/treetracker";
```
it's helpful to have `phppgadmin`. It's optional and you can use command line,
but it could be very helpful for you.

`recommended` - you install phppgadmin

First you need php-7.1-fm - notice it was referenced in the nginx config -
now you need this module to install:

```sh
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update

sudo apt-get install php7.1
sudo apt-get install php7.1 php7.1-cli php7.1-common php7.1-json php7.1-opcache php7.1-mysql php7.1-mbstring php7.1-mcrypt php7.1-zip php7.1-fpm

sudo systemctl restart php7.1-fpm.service

php --ini |grep Loaded

Loaded Configuration File: `/etc/php/7.1/cli/php.ini`

sudo nano /etc/php/7.1/cli/php.ini
```

now

Make the following changes:

`cgi.fix_pathinfo=0`

Then, restart the PHP-FPM service:

```sh
sudo systemctl restart php7.1-fpm.service
sudo apt-get -y install postgresql postgresql-contrib phppgadmin
```



(should not be necessary but just in case) Enable Nginx and PHP-FPM on system boot:
```sh
sudo systemctl enable nginx.service
sudo systemctl enable php7.1-fpm.service
```


### Database
You need to install `postgresql` and `phppgadmin` here's how to do it.

#### Step 1 - Installing PostgreSQL

Follow the right block of steps based on your ubuntu version:

For any Ubuntu version you need to can do this by the official PostgreSQL Apt Repository.

##### Ubuntu Zesty (17.04)

Version 9.6 comes with the distribution.

```sh
sudo apt-get install postgresql-9.6
```

##### Ubuntu Yakkety (16.10)

(It is not officialy supported but it works using the Xenial repository.)

```sh
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
```

##### Ubuntu Xenial (16.04)

```sh
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
```

##### Ubuntu Trusty (14.04)

```sh
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
```

##### Ubuntu Precise (12.04)

```sh
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-9.6
```

#### Step 2 - Configure PostgreSQL user

```sh
sudo -u postgres psql
```

in `psql` shell now type this

```sh
createuser --pwprompt
```

At the Enter name of role to add: prompt, type the user's name

`treetracker`

At the Enter password for new role: prompt, type a password for the user:

`tr33dev`

At the Enter it again: prompt, retype the password:

`tr33dev`

At the Shall the new role be a superuser? prompt, type y if you want to grant superuser access. Otherwise, type n.

`type y`

At the Shall the new role be allowed to create databases? prompt, type y if you want to allow the user to create new databases. Otherwise, type n.

`type y`

At the Shall the new role be allowed to create more new roles? prompt, type y if you want to allow the user to create new users. Otherwise, type n.

`type y`

`PostgreSQL` creates the user with the settings you specified.

Alternatively instead of the above series of steps you could try just issuing
this single command in `psql` shell:

```sh
CREATE USER treetracker WITH LOGIN PASSWORD 'tr33dev' CREATEUSER;
```

also you should do one more command - create the treetracker database

```sh
CREATE DATABASE treetracker
```

now quit `psql` shell `(type \q)`

#### Step 3 - Configure phpPgAdmin

This is `optional` if you logged in as `treetracker` in `phppgmyadmin` - Not Recommended

Edit the file /etc/phppgadmin/config.inc.php by typing:
```sh
cd /etc/phppgadmin/
nano config.inc.php

Find the line $conf['extra_login_security'] = true; and change the value to false so you can login to phpPgAdmin with user postgres.
```

Ok so you need `PostGIS` with this code set or the points won't show up.

```note
PostGIS
postGIS does spatial related things like clustering of points
```

To install `postgis` do this:
```sh
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install postgis
```

Now you should do this to get phppgadmin working

in `/var/www/html` create symbolic link called `phppgadmin` pointing to `/usr/share/phppgadmin`

now go to `http://yourserverip/phppgadmin`

you should see phppgadmin 9.6 UI

Now go to login by clicking `PostgreSQL` on the left side

```note
username: treetracker
password: tr33dev
```
click `login`

Now click `:treetracker` on the left.

Drop any schemas if any, including the public schemas (click "drop" then check CASCADE and click "Drop" button)

click `SQL` in the right screen to the right of `schemas`

Now click `choose file`

Navigate to `treetracker-withusers-anon-1-22-2018.pgsql` (on your desktop)

Click `EXECUTE`

NOW go to `http://yourserverip`
You should see points on map just like `http://dev.treetracker.org`

Now you should have environment set up!

### References

Here are commands to restart `php7.1`, `nginx`, and `postgresql`:

```sh
sudo systemctl restart php7.1-fpm.service
sudo systemctl reload nginx
sudo systemctl restart postgresql
```
