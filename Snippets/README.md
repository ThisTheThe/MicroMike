* sDensePrompt
  * This modifies the prompt window (Ctrl+P) to be more dense; this allows it to display more results.
    * ![Obsidian_25-03-30_12PM-30-53_010|300](https://github.com/user-attachments/assets/8d5ed934-e676-4ac4-8fcd-bdd263edd94d)
* sDenseSettings
  * This makes the settings (both the sidebar and main section) more dense, allowing for more information to be displayed. 
  * Why? It can often be obnoxious navigating the normal Obsidian settings, which give an excess of spacing to the detriment of seeing the full picture.
    * <img src="https://github.com/user-attachments/assets/207a17b2-5a87-4f08-9815-f2e0242f940e" alt="Description" height="200">
* sLeftAlignReadable 
  * When using readable line length, this will make the text align against the left side rather than center itself. 
  * This can reduce necessary eye movement if you work heavily on the left side of the screen.
  * Style settings allows for disabling left alignment, and a general use function for configuring the line length.
    * <img src="https://github.com/user-attachments/assets/f503db08-0ff6-49e6-b8ac-51f29ed77400" alt="Description" height="200">
* sLeftAlignSettingsControls
  * This makes interactable elements in the settings menu left-aligned, pushing against the text. 
  * It makes it much clearer which interactable belongs to which setting, and elegantly sectionally divides the window.
    * <img src="https://github.com/user-attachments/assets/48ca72e3-125c-404c-85e3-abf409859d49" alt="Description" height="200">
    * <img src="https://github.com/user-attachments/assets/5fcfaba5-f5cc-41b2-9364-1c8a2798e025" alt="Description" height="200"> - With sDenseSettings
* sMiniMode
  * Turn Obsidian into a convenient little notepad - just by resizing it.
  * This snippet will cause the sidebars, title bar, and status bar to disappear when the window below a certain width.
  * You'll have to change the minimum width that the "mini mode" activates at to your preference manually - this can't be changed in Style Settings due to CSS limitations.
    * <img src="https://github.com/user-attachments/assets/1a2c8b9a-994e-439f-9367-2849a34ef72b" alt="Description" height="200">
* sNearerTotalNumbers
  * This modifies how the number in the search, tags, backlinks/outlinks, etc works.
  * It moves it to the left alongside the text, which makes it easier and less ambiguous which number belongs to which entry.
    * <img src="https://github.com/user-attachments/assets/fb48f996-3851-458d-afee-f7fb10b1309f" alt="Description" height="200">
* sNoAnimations
  * This snippet disables animations. It includes a feature to workaround a problem causing the sidebars to close more slowly.
  * This is borrowed from https://github.com/SMUsamaShah/Obsidian-Win98-Edition
    * <img src="https://github.com/user-attachments/assets/e607cc01-576e-4e43-912a-5df30bb76ffc" alt="Description" height="200">
* sPositionablePrompt
	* Intended with Style Settings
	* This allows for granular control of the size and position of the prompt (Ctrl+P) window.
	* Options: 
		* Which corner to anchor in, or centered
		* Height/width in percentages
		* X/Y offsets in pixels
		* Minimum width in pixels
  		* <img src="https://github.com/user-attachments/assets/87c6e15e-fee5-43f2-a7bd-0d94b5cc3e27" alt="Description" height="200">
* sPositionableSettings
	* Intended with Style Settings
	* This allows for granular control of the size and position of the settings window.
	* Options: 
		* Which corner to anchor in, or centered
		* Height/width in percentages
		* X/Y offsets in pixels
		* Minimum width in pixels
		* <img src="https://github.com/user-attachments/assets/1675c87f-a34d-4195-bbd9-b0e2a90c020e" alt="Description" height="200">
* sResizableResizeBars
	* This snippet allows for a configurable width on the "resize handles" that determine the width of the sidebars.
	* Why? It's very precise to click the handles normally. If you do that often, you might find it a useful quality-of-life improvement.
	* Width value can be configured with Style Settings.
		* <img src="https://github.com/user-attachments/assets/1e01d7ac-98c5-446f-8a88-f54be5547380" alt="Description" height="200">
* sResizableScrollbar
	* This snippet allows for you to configure the width of the scrollbar.
	* Why? It can be precise to click the scrollbar. If you use it often, you might find adding this makes your workflow more efficient.
	* Width value can be configured with Style Settings.
		* <img src="https://github.com/user-attachments/assets/1e1d2391-3806-473e-8f20-1e9d955ce0c8" alt="Description" height="200">
* sSimpleEditor
	* This snippet enforces a uniform line-height in the editor, no matter what.
	* I find this "pseudo notepad" environment preferable to the more chaotic, jerky formatting shifts that occur switching between modes otherwise.
	* Due to fundamental HTML layout differences, I have to enforce a particular "pretty" note formatting style for this consistency.
		* <img src="https://github.com/user-attachments/assets/922f3667-9517-4ff9-abea-ca81f0156a56" alt="Description" height="200">
* sSimpleTag
	* This simplifies the appearance of tags - they now are just text colored with the selected accent.
		 * ![Obsidian_25-03-30_01PM-18-01_931](https://github.com/user-attachments/assets/47c01010-020f-45a7-8a68-398599d597bd)
* sSquareUI
	* This modified UI focuses on ergonomics and space-usage.
	* Style Settings can be used to precisely control the size of elements.
	* Features:
		- No more padding dead-zones. Anywhere. 
		- Sidebar tabs, and the buttons on the sidebars, fill the full space given.
		- Right sidebar button functions as a fourth titlebar button. (Modifiable)
		- Left sidebar button always anchored to top-left. (Modifiable)
		- Much easier to interact with note title; and buttons there are also larger.
		- Optional "Stack Tabs" mode - this literally stacks the tabs vertically on the window.
			- This can be desirable for users with lots of tabs - you move your eyes less, and the tabs' titles won't be compressed by their density.
		* <img src="https://github.com/user-attachments/assets/c9cd2eee-f286-4b0f-8aec-ff6c14e8771b" alt="Description" width="300" height="200"> 
 * sTopBacklinks
	* Toplinks (I.E. LYT/Ideaverse) are obnoxious to manually maintain. This snippet turns the backlinks's panel at the bottom into an automatic "Toplinks" section.
	* To adjust the characters before/after toplinks, go to the bottom.
		* <img src="https://github.com/user-attachments/assets/32a1fb97-ab5c-4a5f-921b-3627c0d36764" alt="Description" width="300" height="200">
