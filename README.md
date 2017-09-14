# README #

BOA License Manager is a license generator that can create a dual symmetric/asymmetric 
license file.

# INSTALLER #

The complete installation places these commands on the execution path:

* pyinstaller is the main command to build a bundled application. See Using PyInstaller.
* pyi-makespec is used to create a spec file. See Using Spec Files.
* pyi-archive_viewer is used to inspect a bundled application. See Inspecting Archives.
* pyi-bindepend is used to display dependencies of an executable. See Inspecting Executables.
* pyi-grab_version is used to extract a version resource from a Windows executable. See Capturing Windows Version Data.

:note:
The output of PyInstaller is specific to the active operating system and the active version of Python.  

1. a different OS
2. a different version of Python
3. a 32-bit or 64-bit OS

Build Process
-------------

* Writes '*.spec' in the same folder as the script
* Creates a folder build in the same folder as the script if it does not exist
* Writes some log files and working files in the build folder.
* Creates a folder 'dist' in the same folder as the script if it does not exist.
* Writes the 'myscript' executable folder in the 'dist' folder.

Modify the spec file
--------------------

There are four cases where it is useful to modify the spec file:

* When you want to bundle data files with the app.
* When you want to include run-time libraries (.dll or .so files) that PyInstaller does not know about from any other source.
* When you want to add Python run-time options to the executable.
* When you want to create a multiprogram bundle with merged common modules.

You create a spec file using this command:

    pyi-makespec [options name] *.py [other scripts ...]
    
The command creates the name .spec file but does not go on to build the executable.

After you have created a spec file and modified it as necessary, you build the application
by passing the spec file to the pyinstaller command:

    pyinstaller [option name] *.spec
    
When you create a spec file, most command options are encoded in the spec file.  When you
build from a spec file, those options cannot be changed.  If they are given on the command line
they are ignored and replaced by the options in the spec file.

Only the following are valid with spec file:

1. -upx.dir= 
2. -distpath= 
3. -workpath=
4. -noconfirm
5. -ascii
    
