The LOFAR calculator LUCI is deployed on ASTRON's webserver dop385 and is managed using [supervisord](http://supervisord.org/). Whenever you want to make a public release,

+ On your development node, create a new tag with ```git tag -m <message> <version id>``` and ```git push --follow-tags```.
+ Log on to dop385 and go to the appropriate directory with ```cd /data/LUCI/LOFAR-calculator```. 
+ Update the repository with ```git pull```. If you do not have write access to this directory, contact Reinoud Bokhorst.
+ Restart supervisord with ```supervisorctl restart luci```.
+ Check <https://support.astron.nl/luci/> if everything is fine. 
