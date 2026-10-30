# UX Research Report: JetBrains Settings Prototype

## Objective

The study evaluated an updated JetBrains IDE settings interface. Participants were asked to enable "Use contrast scrollbars", save the change, and return to the code editor.

The aim of my analysis was to identify interaction patterns using click heatmaps and look for possible usability issues.

## Methodology

I analyzed the JSON export containing 76 respondent records and 851 valid click events.

I extracted the click coordinates, grouped them by screen ID, and generated heatmaps over the seven original screenshots using Gaussian smoothing.

I also examined the recorded task outcomes and navigation paths to better understand the interactions.

## Findings

**1. Participants interacted with the main settings controls.**

The Main Window heatmap shows a strong concentration around the top-right Settings icon. In the Context Menu, interactions concentrate around both Settings and Theme.

On the Default Settings screen, clicks appear around the requested "Use contrast scrollbars" checkbox, but also around the settings navigation.

The Changed Settings screen has a clear hotspot over Save Changes.

These patterns show interaction with the expected controls, although they do not prove that the interface was easy to use.

**2. Task completion was low, even though many participants reached the saved state.**

Only 19 out of 76 participants (25%) were marked as completing the task. The other 57 (75%) were marked as having given up.

However, 44 of the 57 unsuccessful participants visited the Saved Settings screen.

This suggests that the low recorded completion rate cannot be explained simply by participants failing to reach the saving stage.

**3. The final navigation step may have affected the recorded results.**

All 19 completed sessions ended on the Code Prototype screen.

Among the unsuccessful sessions, 34 ended on Main Window and 18 ended on Saved Settings.

Nineteen unsuccessful participants followed this sequence:

Main Window → Context Menu → Default Settings → Changed Settings → Saved Settings → Main Window.

Since Main Window also displays the code editor, participants may have interpreted returning there as completing the task.

This raises the possibility that the prototype's success criteria did not recognize every reasonable way of returning to code.

## Recommendations

I would examine whether the Settings tab and the return-to-editor interaction are sufficiently clear after saving a change.

Finally, I would investigate the clicks on Theme and other settings categories to understand whether they represent useful exploration or navigation difficulties.

## Limitations

The heatmaps show click locations, not eye movements or visual attention. High click density can reflect successful interactions, repeated attempts, or exploration.

The colors are normalized separately for each screen.

Screen visits do not independently confirm that the requested setting was changed correctly.

There is no comparison group for the previous settings design, so this analysis cannot determine whether the updated interface performs better or worse.

## Conclusion

The interaction data shows that participants often reached and used the expected settings controls, while the recorded task completion rate remained low.

The navigation paths suggest that the final return-to-editor step and the prototype's completion criteria deserve further investigation before attributing the results to usability problems in the redesigned settings interface.