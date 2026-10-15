# VHS source for docs/assets/demo.gif (reproducible terminal demo).
# Render: vhs docs/assets/demo.tape   (requires charmbracelet/vhs + ffmpeg)
# CI fallback: python docs/assets/generate_assets.py (PIL loop, no binaries needed)
Output docs/assets/demo.gif
Set Width 900
Set Height 420
Set FontSize 22
Set Framerate 30
Set TypingSpeed 40ms
Type "python benchmarks/run_all.py"
Enter
Sleep 2s
Type "cat benchmarks/results/summary.json"
Enter
Sleep 2s
