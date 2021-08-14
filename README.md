# Bushel
Bushel is a bare-bones, self-contained digital gardening system. A digital garden is kind of like a wiki; a space for one to write small interlinked documents without the rigid structure of a blog.

### Why bushel?
Because there didn't appear to be a small, lightweight wiki/digital garden system where I could update content from the browser. And I know I'm lazy enough I would never update it if I couldn't do it from my phone. So I made many bad decisions and ended up with bushel!

### The Site
It's a pretty rudimentary flask application that uses GitHub's markdown api to create static html snippets. It's by no means the best solution, but it works and it's fairly fast.

You'll probably notice the similarities to Microsoft's docs site, both in styling and the fact that it too bases it's content off md files. This is for two reasons: one being that I really like md syntax, and two being that I really like Microsoft's docs site.

### What's coming
I'll probably be fixing and tweaking this site for a while, but for more immediate things you can check out the [roadmap](https://bushel-app.com/root/introduction/bushels-roadmap).

# Running
Active the python3 venv then set `FLASK_DEBUG=1` and `FLASK_APP=bushelapp` (I have this set in my venv activate). Then you can just run `flask run` and browse to `http://localhost:5000`.