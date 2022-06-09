# 4. Get started today!

The most important part when starting to learn programmability is to start coding as soon as possible and trying things out. Hands-on is the best teacher! Even better - start working on your own Minimum Viable Product (MVP) around a use case relevant to you. This will both set the focus for you (there are so many tools available that it is otherwise hard to choose what to use!) and give a meaning and purpose to your learning. Read forward to find useful links and tips to complete your MVP.

## LEARN
Before you can start programming, you naturally need to study a bit. The good news is that just by watching this Cisco Live session and accessing these materials in GitHub, you have already started this step! 

- DevNet resources: [developer.cisco.com](https://developer.cisco.com) offers plenty of material to learn about programmability. If you are a beginner, a good place to start would be to select a couple of learning tracks to cover in [Devnet learning labs](https://developer.cisco.com/learning/). These are available for anyone with DevNet account, and if you don't have one yet, you can create one for free. Recommendations to get your learning started:
    - [Coding & APIs track](https://developer.cisco.com/learning/tracks/Coding-APIs-v0/) to get you started on Python and understanding and using REST APIs.
    - [Cisco DNA track](https://developer.cisco.com/learning/tracks/programming-dna/) to practice Cisco DNA Center REST APIs and IOS XE model driven programmability. This track also offers material to learn Ansible
- Training with instructors: If you want to get a fast start for your automation journey - either as an individual or as a team with your colleagues - check the [Cisco Training Bootcamp](https://www.cisco.com/c/en/us/training-events/training-certifications/training/bootcamps.html) offering. In these trainings you get to learn automation with the help and support of Cisco developer advocates.
- Solution documentation: To learn what is possible with the solution you are working on, the programmability and API documentations are good resources to have in you favourites.
    - [IOS XE 17.6.x Programmability Configuration guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/176/b_176_programmability_cg.html), or refer to the Programmability Configuration guide of your IOS XE version in the [general list of configuration guides](https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe-17/products-installation-and-configuration-guides-list.html)
    - [DevNet documentation on Cisco DNA Center platform](https://developer.cisco.com/docs/dna-center/#!cisco-dna-center-platform-overview), refer also to the documentation inbuilt in your own Cisco DNA Center

## PLAN
Before you start coding your MVP, take a moment to make a plan. This is important, as it will both make it easier for you to focus on the key areas when coding, and at the same time make sure that while you are learning, you are creating something that itself will bring you value. Planning what features you want to have now and what you want to have in the long run helps you make educated decisions when creating your script - you don't want to spend hours creating something that would not support your long term goals.

Questions to ask yourself:
### What is the use case?
Everything starts from a use case - there is no need for you to learn programming if there is nothing to solve with it. If you have hard time deciding what it is that you would like to automate, sit down with your team to brainstorm: What in your daily work is painfully manual? What is error prone and causes problems? What is something you would want to do in the network but there is never time as it would be so time consuming? What is some information that you would like the network to tell you?

### What manual steps does it include?
You cannot automate something you don't know the logic of before the automation. It is good to map for example what stake holders are involved to make sure they are taken into account in your automation process. At the same time, it is good to acknowledge that even if something needs to be done in certain ways when doing it manually, doesn't mean all those steps need to be included in automation as well. Recognise which steps become unnecessary when applying automation - what do you actually really need to reach a certain end goal?

### What automation tool to use?
In the session we have focused heavily on Python using NETCONF, REST APIs and pyATS. There are many other tools available, and there is no one correct answer to which you should choose. Think of the following when choosing the tool to work with:
- What fits best for the use case you have in mind? For example, if you want to test network state, you might want to choose pyATS as it already has inbuilt many useful features for you to use. There might already be sample scripts close to your use case available in certain language, and utilizing existing code snippets might speed up your development significantly.
- What is the experience in your team? It is the easiest to get your team working together and supporting each other on programmability if you focus on a tool that is most familiar to your team. If your team is fluent in Python but has never used Ansible, Python is most likely a better option for your MVP, even if some other team in another company would use Ansible for it instead.
- Is there some common tool already in use in your company? When choosing a tool that your company might already be utilizing, you will have people with experience that you can ask help for when stuck with some automation task or an error. Additionally, it will allow easier integration and collaboration between different tasks when utilizing the same, standardized tools inside your company.

### What features would you need?
One important thing about programmability is that even if you are just starting, you can already create something meaningful and usable, as long as you don't try to complete too big task in one go. In general, everytime you have a use case defined, it would be adviced to list down what the features are that you need in your final solution for the use case. Then you can prioritise these features, and easily separate the bigger task into small, more easily achievable tasks.

By defining the big picture before starting to code, you make sure that even when creating a small feature first, you have the big picture in mind. That guides your development: maybe, when getting certain information from a device, if you get it with certain API, it will be usable also in other feature in your use case.

## CREATE

When your plan is ready, it is time to start creating! Here are some tips to help you on the way:

### Copy with pride
Do not feel like you need to reinvent the wheel - if someone has already shared code samples of the use case you are solving, utilize it!

When utilizing code from GitHub, pay attention to when that code was last updated. If the code is old, it might be that some of it won't work on your device or Python versions. It is also possible that there has come out a better way of achieving the same end result since that code was updated.

Good places to find sample code:
- [DevNet Code Exchange](https://developer.cisco.com/codeexchange/) - Discover curated GitHub projects to jumpstart your work
- [DevNet Automation Exchange](https://developer.cisco.com/network-automation/) - shared code repositories from the DevNet community
- [GitHub repository for pyATS example scripts](https://github.com/CiscoTestAutomation/examples)
- Robert Csapo and Oren Brigg's GitHub repository for [curated list of awesome Cisco DNA Center frameworks, libraries, sdk, sample codes and resources](https://github.com/robertcsapo/awesome-cisco-dnac)
- Jeremy Cohoe's repository for [IOS XE automation examples and scripts](https://github.com/jeremycohoe)

### Test your code in sandbox! 
You can reserve a sandbox or use an alwas on version from [DevNet](https://developer.cisco.com/site/sandbox/).

### Refactor and comment
When your code works, take a moment to refactor and comment it. You can utilize a linter to help you refactor your code to follow best practices and thus make it easier to read by others.
- `pylint` is a good linter for Python scripts, and can be downloaded with `pip install pylint`. Once installed, you can run it in your system with `pylint <name of the python file>` to lint a specific file. Note: sometimes the linter picks up things from libraries that you have imported to your code. Focus on the notes that `pylint` gives on the code that you yourself have written.
- [PEP 8 is the style guide for Python code](https://peps.python.org/pep-0008/). Refer to that when you get further in your programming experience to understand what style you would be encouraged to use. If using some other automation tool, refer to their style guides.

### Use version control
Git version control will both make sure you can revert back to an earlier, working version of your code, as well as allow efficient team work once you start collaborating with your colleagues. Main Git commands are easiest to learn when you use them regularly - hence taking them into your daily workflow when creating code, even if only working on it alone, will make them a habit that helps you when starting to collaborate on your code.
- [Git webpage](https://git-scm.com/): includes the documentation and the free online version of Pro Git book
- [DevNet lab "Brief introduction to Git"](https://developer.cisco.com/learning/labs/dne-git-basic-workflows/introduction/) - this lab is useful for getting started with Git, and is included in the Coding & APIs Learning track


## MINIMUM VIABLE PRODUCT (MVP)

Once you have your very first feature working, congratulations! You have made your Minimum Viable Product (MVP). The key part of MVP is that you create only the code that is absolutely necessary for the feature to work, which means that you can create it fast. Once it works, you can start working on the next feature, while already getting value of what you created so far. And the best of all, when focusing on creating an MVP, you can quickly achieve the great feeling of creating your first working prototype!