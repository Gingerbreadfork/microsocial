# Microsocial
When social media first became popular, computers were a lot different to what they are today. It's quite possible that the phone you have in your pocket is more powerful that the computer you first used to sign up to Facebook or Twitter. With this in mind, perhaps this extreme growth in technology has begun to open up other ways to approach how we connect and enage with each other online. Is it a necessity to rely on a third-party to hoard our data en masse to then turn around and blanket us with agressive advertising in return or is there other alternatives?

What if everyone operated their own sort of "micro stack" and leveraged either our own hardware or opted to take advantage of the incredible infrastructure provided by Deta. What if you could take how you interacted online and tuned that to truly fit your perferences while others did the same, yet still retained more contol of what you choose to put out into the world. Microsocial takes these concepts and explores them and hopefully helps us to think about things a little differently.

## 😀 What is Microsocial?
Microsocial is an experimental approach for taking social media a new direction, one that explores the potential for a peer-to-peer (P2P) approach to something that traditionally has been much the opposite. While some other great alternative projects are creating their own vision of what this should look like, maybe it's time to take it a different direction, one that can be shaped by you, hosted by you, and built by you. Perhaps the answer to a more free form of social media is not just in looking at who controls intermediary servers, but instead trying to remove them from the structure of these networks.

## 🔥 What Can Microsocial Do?
* Enable you to connect with others running their own Microsocial deployments
* Contribute to a live feed that is populated with posts from connected friends
* Send messages privately between friends with the ability to clear the chat from either side
* Allow you to customize your experience while still engaging with others that may or may not do the same
* Provide you more control over your data and the content that you generate
* Deploy your own Microsocial instance for free on a Deta Micro or Deta Space (Coming soon)

## ✨ Deta Micro Installation
```
git clone https://github.com/Gingerbreadfork/microsocial
cd microsocial/client
npm i
npm run build
cd ..
deta new
```

## 📝 Notes
* If you modify the frontend or the API just give ```deploy.sh``` a run, it will rebuild the frontend and redeploy both in a few seconds.
* Multiple test micros can be deployed just use different folders and be sure to change the variable ```dbname``` in the file ```config.py```
* The frontend client is a Svelte app, and the backend is a FastAPI app that also serves the frontend.
* Currently deployments to Deta Micros won't be locked down and all routes are open (password protection for deployments to be added soon most likely)

## 🤔 FAQ
Q: Why does it not have *insert random feature*?  
A: Microsocial is still early, experimental and finding it's footing. It should work fairly reliably, but there's still so much more to do.

Q: How does Microsocial avoid using intermediary servers?  
A: It depends on the feature, for example the friend system sends a connection request directly to another deployment, if they accept they send one back and the cycle comples. Another example, when creating a post in the live feed your friends will be notified directly that you've "done something" and their deployment will then check with you for the new content and update the feed.

Q: Is it encrypted?  
A: There is some early stages of experimenting with this, it's nowhere near where it could be and the implimentation where it has been added is incredibly basic.

Q: Why Python and Svelte?  
A: Python is amazingly intuitive and it makes the backend portion of the platform much more approachable, there's minimal classing and the code should be fairly easy to dig around in. On the other side of things, Svelte apps compile to be incredibly light weight and are fantastic for a "micro stack" like this and is fantasticly friendly to use, something that is important to make this project more approachable.

Q: How is the frontend styled?  
A: Tailwind CSS, because manually writing CSS is something that feels a lot like unnecessary suffering and for fast prototyping like this project, it's great!

Q: How can I show support?
A: Drop a star on this repository, share it with your friends or even share it on those OTHER types of social platforms we all still use, at least for now.

## 🤗 Want to Contribute?  
Anyone is welcome to contribute to Microsocial. It doesn't matter how proficient you are at development, if you have a good idea you should explore that and your contributions, suggestions, feedback, and anything else you want to throw this way are more than welcome. Microsocial is far from perfect and there are a lot of areas that could be improved, expanded, and refactored so there is always opportunities to find something to put into a PR and leave your mark on this repository and whatever Microsocial may become in the future.

Microsocial is a project that attempts to explore things in new ways so has inherited some chaotic code in the process, feel free to help reign that in if you find it interesting. If you do want to add a larger feature or something that requires additional packages, please try and keep these new dependencies to a minimum to keep things light and easy to deploy.

## 💡 Future Goals
* Expand the codebase to allow for fully decentralized deployments for those wanting to take things even further
* Optimize how deployments communicate in terms of speed
* Minimize the number of requests deployments use
* Explore other forms of communication and collaboration (audio/video/etc)
* Develop alternative clients (e.g terminal based client, pure html, other frameworks)
* Standardize a base protocol so alternatives APIs could be created and mingle easily with existing deployments
* Lock down some core functionality in terms of the API to help with backwards compatability over time
* Encrypt all messages and posts to a decent standard

## 🙏 Thanks
Thanks to the Deta team for supporting this obscure vision and encouraging me to build out this concept, and for always offering their help and support along the way. If you're wanting to turn an idea into something more check out their various offerings (Deta Micros/Drive/Base/Space with more likely on the way) and support them as they continue to offer completey free services for those of us wanting to try things our own way, without having to worry about the resources we may need to get started on a new journey. If you haven't yet, go check it out at https://deta.dev/
