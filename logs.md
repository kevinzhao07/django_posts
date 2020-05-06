## Wolverine-DM Change Logs

#### Release Beta 1.3 (Release )


#### Release Beta 1.2 (Release 05-04-2020 2140 EST)

**As of 05-01-2020:**  
Working on implementing jQuery, AJAX, and JS into our project to stop automatic reloads on likes and pinning posts. As of now, 05-01-2020 21:00 EST, liking on the home page works.
- doesn't reload on every like, and updates the "like photo feed" dynamically. 
- doesn't update the statistics portion dynamically, but don't think it is necessary. 

New post page got a complete remodeling, and fits in with the entire theme of everything. The white was too contrasting with the darker blue and grey background, so now it has been blended in and looks like an actual post. The post has some placeholder text to indicate where to write. 

**As of 05-02-2020:**  
As of 05-02-2020 20:00 EST, pinning any post changes the textures, but doesn't pin post to the top until a refresh (this is intended). However, this allows users to pin unlimited post, this may change in the future. 
- thinking of adding a statistic of how many posts pinned?

Comments got an update as well, so the white form is all gone. The comment form is now displayed as if an actual comment. UI looks smoother and fits in with the theme.

Changed website logo! The site is officially known as "Wolverine-DM"!

**As of 05-04-2020:**
+New Post now doesn't take the user to a new page, but uses Javascript to display the new post form. The UX seems a bit better for users with slower internet.

#### Release Beta 1.1 (Released 04-30-2020 1455 EST)
Primarily Bug/Design Fixes.
1. fixed bug where new messages sent wouldn't have their respective colors and only showed up with `default-blue`. 
2. updated background from `fixed` to `repeat`, leaving wolverine static, might think of both scrolling backgrounds?
3. DateTime model entries will now be shown in EST (UTC-5:00) instead of UTC (may convert back)
4. home page has a welcome message for users. It's now easier to see who you're logged in as, and statistics are offerred for users. 
5. files (such as static .css, .js, images, and profile pictures) are now stored within aws system, so it fixes a bug with them being deleted every time heroku stopped running (every 15-30 minutes)

**Updates for the future**: 'likes' and 'pinning' all cause a refresh, which I don't like. Comments and messages also do this, which I haven't fixed yet but my main concern is fixing the front page for now to fix liking and pinning. 

#### Release Beta 1.0 (Released 04-25-2020 2230 EST)
First Release of 1.0 of **Wolverteen De-UM**! Might think about changing the name to Wolverine-DM but for now, I'm leaving it like this. There's a lot of bugs but hopefully the beta testers will figure them out.
