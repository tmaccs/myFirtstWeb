#! /bin/bash
SITE_PATH='/html1/myFirtstWeb'
USER='www'
USERGROUP='www'

cd $SITE_PATH
git reset --hard origin/master
git clean -f
git pull
git checkout master
chown -R $USER:$USERGROUP $SITE_PATH