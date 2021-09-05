# Microsocial
When social media first became popular, computers were a lot different from what they are today. The phone you have in your pocket may be more powerful than the computer you first used to sign up to Facebook or Twitter. With this in mind, perhaps this extreme technology growth has opened up other ways to approach how we connect and engage with each other online. For example, is it necessary to rely on a third party to hoard our data en masse to turn around and blanket us with aggressive advertising in return, or are there alternatives?

What if everyone operated their own sort of "micro stack" and leveraged either our own hardware or opted to take advantage of the excellent infrastructure provided by Deta. What if you could change how you interacted online to ensure you could retain control of what you choose to put out into the world. Microsocial takes these concepts, explores them, and hopefully helps us think about things differently.

## 😀 What is Microsocial?
Microsocial is an experimental approach for taking social media in a new direction, one that explores the potential for a peer-to-peer (P2P) approach to something that traditionally has been much the opposite. While some other excellent alternative projects are creating their vision of what this should look like, maybe it's time to take it in a different direction, one that can be shaped by you, hosted by you, and built by you. Perhaps the answer to a more free form of social media is not just looking at who controls intermediary servers but instead trying to remove them from the structure of these networks.

## 🔥 What Can Microsocial Do?
* Enable you to connect with others running Microsocial deployments
* Grow a live feed populated with posts from connected friends
* Send messages privately between friends and clear the chat any time
* Customize your experience with full access to the source code
* Keep control of your data and the content that you generate
* Deploy Microsocial for free on a Deta Micro or Deta Space

## ✨ Deta Micro Installation
To deploy Microsocial to a Deta Micro from a Linux command line:
```
git clone https://github.com/Gingerbreadfork/microsocial
cd microsocial/client
npm i
npm run build
cd ..
deta new
```

* If you modify the frontend or the API, give `deploy.sh` a run; it will rebuild the frontend and redeploy both in seconds.
* Multiple test micros can be deployed; use different folders and be sure to change the variable `dbname` in the file `config.py`
* The frontend client is a Svelte app and the backend is a Python FastAPI app that also serves the frontend.
* To disable basic auth for local dev or other testing change the variable `localdev`  in `config.py` to `True`

Deployments to Deta Micros rely on HTTP Basic Authentication to provide a simple way to secure them for now, by default the login details are below. You can change these default credentials on the settings tab once you have your deployment up and running. A better onboarding flow is coming soon!

**Username:** admin  
**Password:** password  

## 🤔 FAQ
**Why does it not have *insert random feature*?**  
Microsocial is still early, experimental, and finding its footing. It should work pretty reliably, but there's still so much more to do.

**How does Microsocial avoid using intermediary servers?**  
It depends on the feature; for example, the friend system sends a connection request directly to another deployment. If they accept, they send one back, and the cycle completes. Another example is when creating a post in the live feed; your friends will be "notified" directly that you've "done something," and their deployment will check with you for the new content and update the feed.

**Is it encrypted?**  
There are some early stages of experimenting with this, it's nowhere near where it could be, and the implementation where it has been added is incredibly basic. Assume that you aren't protected by encryption for now and act accordingly.

**Why Python and Svelte?**  
Python is amazingly intuitive, and it makes the backend portion of the platform much more approachable. There's minimal use of classes, and the code should be pretty easy to dig around in. On the other side of things, Svelte apps compile to be incredibly lightweight and are fantastic for a "micro stack" like this. Svelte is also very friendly to use, something that is important to make this project more approachable by anyone wanting to contribute.

**How is the frontend styled?**  
Tailwind CSS because manually writing CSS feels a lot like unnecessary suffering, and for fast prototyping something like this project, it's excellent!

**How can I show support?**  
Drop a star on this repository, tell your friends about it, or even share it on those OTHER types of social platforms we all still use, at least for now.

## 🤗 Want to Contribute?  
Anyone is welcome to contribute to Microsocial. It doesn't matter how proficient you are at development if you have a good idea. So your contributions, suggestions, feedback, and anything else you want to throw this way are more than welcome. Microsocial is far from perfect, and many areas could be improved, expanded, and refactored, so there are always opportunities to find something to put into a PR and leave your mark on this repository and whatever Microsocial may become in the future.

Microsocial is a project that attempts to explore things in new ways, so it has inherited some chaotic code in the process. Feel free to help reign that in if you find it interesting. If you want to add a more extensive feature or something that requires additional packages, please keep these new dependencies to a minimum to keep things light and easy to deploy.

## 💡 Future Goals
* Expand the codebase to allow for pure local self-hosting
* Optimize how deployments communicate in terms of speed
* Minimize the number of requests deployments use
* Explore other forms of communication and collaboration (audio/video/etc.)
* Develop alternative clients (e.g., terminal-based client, pure HTML, other frameworks)
* Standardize a base protocol so alternatives APIs could be created and mingle easily with existing deployments
* Lockdown some core functionality in the API to help with backward compatibility over time
* Encrypt all messages and posts to a decent standard
* Replace all use of browser dialogs with custom modals

## 🙏 Thanks
Thanks to the [Deta](https://deta.sh) team for supporting this obscure vision and encouraging me to build out this concept, and for always offering their help and support along the way. If you want to turn an idea into something more, check out their various offerings (Deta Micros/Drive/Base/Space with more likely on the way) and support them as they continue to offer completely free services for those of us wanting to try things our own way, without having to worry about the resources we may need to get started on a new journey. If you haven't yet, go check them out!
