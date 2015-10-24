# Robotcore
*This is the main FTC api responsible for API functions and abilities that pertain to the robot. This repository acts as a medium for maven hosting and tracking each version of the robotcore API. In the scope of the project maven is used to allow coding in a separate project without the dependency of the whole APK. In no way is this project associated with FTC or a part of the core FTC libraries. Additionally, the project is not claiming ownership of the files just providing another vehicle in accessing them.*

## Using Maven
Added the following repository to your maven list. The available versions are available based off the last time the github has been updated. Expect some delays between FTC updates and this Repo's updates.
```
<repository>
    <id>com.qualcomm.robotcore</id>
    <name>Robotcore</name>
    <url>https://raw.githubusercontent.com/dynapp/robot-core/master/repo/</url>
</repository>
```
Add this to your dependency list. When updating your code you must change the value in the tag so it can be properly downloaded from maven. This page will always have the latest version listed in the version tag. 
```
<dependency>
	<groupId>com.qualcomm</groupId>
	<artifactId>robotcore</artifactId>
	<version>{0}</version>
</dependency>
```

## Direct Download
If you would prefer to direct download the robotcore opposed from using maven you can goto this link:  [Here](https://github.com/dynapp/robot-core/raw/master/robotcore-latest.jar) It is not recommended you use this system because it is very easy to lose track of the current module version; however, if it suits your needs we have provided the option.

## Latest Version
{0}

## Licensee
MIT Licensee