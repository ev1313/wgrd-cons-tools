## Sound Modding

### Sound files in Eugen Games

There are three file types for sounds:

 - ess -> these are essentially eugens custom audio container format, comparable to wav/ogg files
 - mpk -> these are just edat files with custom name, you can unpack them with wgrd\_cons\_parsers.edat
 - sformat -> these files contain extra information for the sound file. Often they contain only the same info as the ess header, but sometimes there is (probably) an [amplitude envelope](https://en.wikipedia.org/wiki/Envelope\_(waves)) in there.

### Tools

For this we will need the following tools:

 - edat Parser / Build from wgrd\_cons\_parsers
 - encode\_ess from wgrd\_cons\_tools
 - generate\_sformat from wgrd\_cons\_tools


### Unpack files
So first we unpack the NDF\_Win.dat in the 72352 folder in GameData and the ZZ\_1.dat in the 58710 folder. The 58710 file contains a mpk file, we also want to unpack.

``` bash
edat.exe <Path to WGRD Game Data>/68335/72352/ZZ\_1.dat -o out/
edat.exe <Path to WGRD Game Data>/49964/ZZ\_1.dat -o out\_58710/
edat.exe out\_58710/allplatforms/sound/pack/mainsound.mpk -o out/allplatforms/sound/pack/
```

Now you will find in the out folder the unpack dat file and a xml file containing something like the following:

``` xml
<EDat sectorSize="8192">
  <File path="pc\ndf\nonpatchable\clusterbootstrapgame.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusterbootstrapgameimpl.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusterbootstraplaunchallmap.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusterinitialisationnonpatchable.ndfbin" />
  <File path="pc\ndf\nonpatchable\clustermaingamerun.ndfbin" />
  <File path="pc\ndf\nonpatchable\clustermainlaunchallmap.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusteroptions.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusterrunallgamemaploop\_step2.ndfbin" />
  <File path="pc\ndf\nonpatchable\clusterversionoptions.ndfbin" />
	...
```

This references every file in the edat file - if you add a line it will add the binary file referenced by this to the edat file. We will do this later.

### create new files

First we take our wav file and run:

``` bash
encode\_ess.exe <Path to wav file> -o out/allplatforms/sound/assets/sons/outgame/badge.ess
```

Afterwards we need to create the sformat file:

``` bash
generate\_sformat.exe out/allplatforms/sound/assets/sons/outgame/badge.ess -o out/allplatforms/sound/pack/allplatforms/sound/assets/sons/outgame/badge.sformat
```

This will replace the existing sformat file.

**WARNO Note:** The generate\_sformat script does use the wgrd 0x06 magic byte in the header by default. If you want to use this on WARNO (untested!), you probably have to check what values WARNOs sformat files use and change them?

As we now changed the sformat file inside the mpk file, we have to rebuild the mpk file:

``` bash
edat.exe -p out/allplatforms/sound/pack/mainsound.mpk.xml -o out/allplatforms/sound/pack
```

**Note:**
Obviously you can edit multiple sformat files first and then repack the mpk file afterwards on bulk.

### update file list in edat

Now we add the new files to the edat file:

``` xml
...
  <File path="allplatforms\sound\pack\mainsound.mpk" />
  <File path="allplatforms\sound\assets\sons\outgame\badge.ess" />
</EDat>
```

Afterwards we can rebuild the NDF\_Win.dat file:

```bash
edat.exe -p out/ZZ\_1.dat.xml -o out/
```

This can now be loaded into the game (copy it into the/68335/72352/ZZ\_1.dat) and the badge sound effect (click on your rank badge) should be replaced.

**Note:**
Only because you reference a new file here, the game will not automatically load it, in the cluster*.ndfbin files there is a list of loaded files.
This is only necessary for **new** files though, in this case we replace existing files, which get referenced in the cluster of the main game.

### Loops

Some files use loops, especially weapon sounds. These can be set using Audacity the encode\_ess tool.

To mark an area as a loop, open your sound file in Audacity and create [a label track](https://manual.audacityteam.org/man/label_tracks.html).

Add a label from Selection and call this label "loop".

You can export the Labels in Audacity in File -> Export -> Export Labels. This will produce a txt file, for example "labels.txt".

Now when using encode\_ess, you can use the -l parameter for supplying the labels.txt:

``` bash
encode_ess.exe test.wav -l labels.txt -o test.ess
```

The generate\_sformat tool will also understand this.

### Limitations

There are a few unknowns in the sformat file:

 - unk4 This has the possible values (in the existing ingame files):
 	- 2, 4, 44, 112, 176, 736, 4096
 - the tool just assumes unk4 = 2

- data:
	- This is probably the amplitude envelope?

If you know what these are used for, please write me.

The current method only replaces existing sounds - if you want to add new sounds you probably have to edit some ndfbin files, so they get loaded properly / used properly, if anybody tries this out, also, please write me.
