# Treasure Boxes

Welcome to the Treasure Boxes!
Treasure Boxes offers a pre-built pieces of code for developing, optimizing, and analyzing your data!

* Analytic Box - Best-practice design patterns for various types of analysis
* Integration Box - Data Ingestions and exports for a third-party data source (e.g. Salesforce, Zendesk, AWS S3)
* Data Box - Techniques for specific types of data enrichments
* Machine Learning Box - Custom Machine Learning Catalogs you can figure out values from your data
* Tool Box - Tools better to utilize Treasure CDP

# How to Request a new Box

Submitting a Box request does not mean that Treasure Data will create the requested Box, but let's us know that our customers want it. All new Box requests will be logged and prioritized by the Treasure Boxes team. 

Link is https://boxes.treasuredata.com/hc/en-us/

# Contributing Guide

We love your input! If you have any own box that you can share, please follow this guide.

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same MIT License that covers the project. Feel free to contact the maintainers if that's a concern.

## Do not contain any private information in any contributions

Anyone can access this repository. Before you contribute to us, please verify whether your contribute doesn't contain any private information.

## Steps to send a new box or fix a existing box

### Fork the code

Firstly you need a local fork of the the project, so go ahead and press the “fork” button in GitHub. This will create a copy of the repository in your own GitHub account and you’ll see a note that it’s been forked underneath the project name.

### Download the code

Now you need a copy locally, so find the “Clone with HTTPS” in the right hand column and use that to clone locally using a terminal:

```
$ git clone https://github.com/treasure-data/treasure-boxes.git
```

### Create a new branch

Firest, change into the new project’s directory: 

```
$ cd treasure-boxes
```

Now create a branch using the git checkout command:

```
$ git checkout -b <add-your-new-branch-name>
```

The name of the branch does not need to have the word add in it, but it's a reasonable thing to include because the purpose of this branch is to add your name to a list.

### Make necessary changes and commit those changes

Now that you have the source code, get it working on your computer.
Choose a box you want to contribute, and make a new foloder under the box you choose.
The box is expected to contain at least README.md and one source code file you want to contribute as a Box.

### Add your change to the branch

If you go to the project directory and execute the command `git status`, you'll see there are changes.
Add those changes to the branch you just created using the git add command:

```
$ git add <FILE YOU ADDED>
```

Now commit those changes using the git commit command:

```
$ git commit -m "Add XXXX as a new Box"
```

### Push changes to GitHub

Push your changes using the command git push:

```
$ git push origin <add-your-branch-name>
```

### Submit your changes for review

If you go to your repository on GitHub, you'll see a Compare & pull request button. Click on that button.
Soon the Treasure Boxes team will be merging all your changes into the master branch of this project. You will get a notification email once the changes have been merged.

### Where to go from here?

Congrats! You just completed a contribution process.
