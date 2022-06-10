# 3. Automate adding new capabilities
In this chapter we explore how we can automatically push a ThousandEyes Enterprise Agent to a Catalyst 9300 switch, through two different examples which are presented in the two different sections below. 

Cisco ThousandEyes provides a 360-degree view of your hybrid digital ecosystem -- across cloud, SaaS and the Internet -- by combining Internet and WAN visibility, browser synthetics, end-user monitoring and Internet Insights. It helps troubleshoot application delivery and maps Internet performance, all from a SaaS-based platform. This is made possible by global vantage points from which you can run different tests that simulates user and application traffic. There are three types of vantage points: Cloud Agents, Enterprise Agents and Endpoint Agents. In this example we focus on the Enterprise Agent. 

## Section 1: Deploying a ThousandEyes Enterprise Agent by using cat9kthousandeyesctl
cat9kthousandeyesctl is a tool, developed by Cisco Systems Engineer Robert Csapo, which can be used to deploy Cisco ThousandEyes agent on Cisco Catalyst 9000. 

### Documentation
- [cat9kthousandeyesctl](https://github.com/robertcsapo/cat9kthousandeyesctl) GitHub page, where you find detailed documentation about the tool. 
- The [ThousandEyes Documentation](https://docs.thousandeyes.com/) page is where you can get an understand about the platform and how to further work with the solution. 
- Get a free ThousandEyes trial account [here](https://www.thousandeyes.com/signup/)
- 

### Requirements
- Network connectivity
  - Internet
  - DNS
  - DHCP
- Cisco ThousandEyes Account
  - ThousandEyes Token which you get from the ThousandEyes Dashboard
- One of the following Cisco Catalyst 9000 platforms
  - C9300
  - C9400
- Cisco IOS-XE Software
  - 17.3.3+
- netconf-yang enabled
- Python 3 (Version: 3.7+)
- Installation of cat9kthousandeyesctl in your environment (see [cat9kthousandeyesctl GitHub](https://github.com/robertcsapo/cat9kthousandeyesctl) for detailed steps)
- Edit the settings in the config.yaml file

### Deploy
```bash
cat9kthousandeyesctl deploy --config config.yaml
```

### Status
```bash
cat9kthousandeyesctl status --status config.yaml
```

### Undeploy
```bash
cat9kthousandeyesctl status --undeploy config.yaml
```

## Section 2: Deploying a ThousandEyes Enterprise Agent by using Cisco DNA Center
Please see the Cisco Live session [LINK](LINK)
