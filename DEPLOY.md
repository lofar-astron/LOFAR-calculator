# How to make a public release?

The LOFAR calculator LUCI is deployed on ASTRON's webserver dop385 and is managed using [supervisord](http://supervisord.org/). Whenever you want to make a public release,

+ On your development node, create a new tag with ```git tag -m <message> <version id>``` and ```git push --follow-tags```.
+ Log on to dop385 and go to the appropriate directory with ```cd /data/LUCI/LOFAR-calculator```. 
+ Update the repository with ```git pull```. If you do not have write access to this directory, contact Reinoud Bokhorst.
+ Restart supervisord with ```supervisorctl restart luci```.
+ Check <https://support.astron.nl/luci/> if everything is fine. 

# How to update the singularity image?

All the required dependencies for LUCI on dop385 is installed inside a singularity container. We do not have to update the container every time we make a public release. However, if you want to update the container, do the following:

+ The recipe for creating the container is supplied with the repository. See file ```singularity.recipe```. Make changes to the file as needed.
+ Build the container with ```sudo singularity build lofarcalc.simg singularity.recipte```. If the build is successful, you will see a new file called lofarcalc.simg. 
+ Copy ```lofarcalc.simg``` to ```dop385:/data/LUCI```. If you do not have write access to this directory, contact Reinoud Bokhorst.
+ Restart supervisord with ```supervisorctl restart luci```.
+ Check <https://support.astron.nl/luci/> if everything is fine. 
