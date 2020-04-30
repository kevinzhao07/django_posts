## Wolverine-DM Change Logs

#### Release Beta 1.1 (Released 04-30-2020 1455 EST)
Primarily Bug/Design Fixes.
1. fixed bug where new messages sent wouldn't have their respective colors and only showed up with `default-blue`. 
2. updated background from `fixed` to `repeat`, leaving wolverine static, might think of both scrolling backgrounds?
3. DateTime model entries will now be shown in EST (UTC-5:00) instead of UTC (may convert back)
4. home page has a welcome message for users. It's now easier to see who you're logged in as, and statistics are offerred for users. 
5. files (such as static .css, .js, images, and profile pictures) are now stored within aws system, so it fixes a bug with them being deleted every time heroku stopped running (every 15-30 minutes)

#### Release Beta 1.0 (Released 04-25-2020 2230 EST)
First Release of 1.0 of **Wolverteen De-UM**! Might think about changing the name to Wolverine-DM but for now, I'm leaving it like this. There's a lot of bugs but hopefully the beta testers will figure them out.
