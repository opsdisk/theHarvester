##### Introduction
One of the most popular tools to collect email addresses and other target information during a pen test is [theHarvester](http://www.edge-security.com/theharvester.php), written by Christian Martorella [@laramies](http://twitter.com/laramies) of the [Edge-Security Group](http://www.edge-security.com/).  The source code can be found here: [https://github.com/laramies/theHarvester](https://github.com/laramies/theHarvester), but it comes with Kali by default.  Motivated by the rewrite of [metagoofil](https://github.com/opsdisk/metagoofil), I decided to rewrite theHarvester, and update the email collection portion. The DNS portion is not included for now.

##### tl;dr
New code is here, take it for a spin: https://github.com/opsdisk/theHarvester

##### theHarvester
Just like the rewrite of metagoofil, the python `google` package is utilized.  The `google` package can be installed using pip

    pip install google

The script searches Google for pages utilizing both the `site:example.com` and `example.com -site:example.com` search criteria.  This allows the script to find emails on sites, like forums, that are not necessarily affiliated with the target domain. The Python `google` package will handle all the logic and heavy lifting of accurately searching Google, instead of relying on custom-written search code. I cover more of this information in the [metagoofil](http://blog.opsdisk.com/metagoofil/) blog post.

The remaining updates deal with the switches.  The same switches were kept as in the original metagoofil to avoid confusion, with new ones also added.

The `-b` switch specifies the data source and currently only supports Google, PGP from [https://pgp.mit.edu/](https://pgp.mit.edu/), and 'all', which is just both of them.  

The `-f` switch writes all the links to a domain + date-time stamped .txt file (e.g., example.com\_20151201_175822) instead of an HTML file.  This allows for quick copy/paste or as an input file for other tools.

The addition of the `-e` delay switch allows you to specify the time delay in seconds between searches.  If you request searches too quickly, Google will think you are a script or bot and will block your IP address for a while.  Experiment to see what works best for you.

Lastly, the `-t` switch specifies the amount of time to wait before trying to access a stale/defunct site.

##### Extracting Emails

The original theHarvester had a custom parser/module.  To simplify the code, the line below was used for email regex.

```python
emails = re.findall(r"[a-z0-9\.\-+_]+@[a-zA-Z0-9.-]*" + self.domain, response.read(), re.I)
```
##### Time Performance
The script runs a little slower than the original theHarvester, but is more comprehensive in it's searching, sorting, and data presentation. 

##### Future Work
Not sure if I'll add the other functionality that the original theHarvester has, since most of it requires an API key, there are other tools (dnsenum, dnsrecon), and during a social engineering campaign, I really only care about email addresses, not people.  

##### Conclusion
All of the code can be found on the Opsdisk Github repository here: https://github.com/opsdisk/theHarvester.  Comments, suggestions, and improvements are always welcome.  Be sure to follow [@opsdisk](https://twitter.com/opsdisk) on Twitter for the latest updates. 
 