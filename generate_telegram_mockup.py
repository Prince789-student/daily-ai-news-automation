import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure(figsize=(11, 9), dpi=160, facecolor='#0E1621')
ax = fig.add_subplot(111)
ax.set_facecolor('#0E1621')
ax.axis('off')

# Outer Telegram App Window
window = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle='round,pad=0.015,rounding_size=0.02',
                               edgecolor='#242F3D', facecolor='#17212B', linewidth=2)
ax.add_patch(window)

# Top Bar (Header)
top_bar = patches.Rectangle((0.02, 0.88), 0.96, 0.1, facecolor='#242F3D', edgecolor='none')
ax.add_patch(top_bar)

# Avatar
circle = patches.Circle((0.08, 0.93), 0.035, facecolor='#2AABEE')
ax.add_patch(circle)
ax.text(0.08, 0.93, 'BF', color='white', fontsize=12, fontweight='bold', ha='center', va='center')

# BotFather Title + Verified Badge
ax.text(0.13, 0.94, 'BotFather', color='#FFFFFF', fontsize=15, fontweight='bold')
ax.text(0.24, 0.94, '✓', color='#2AABEE', fontsize=13, fontweight='bold')
ax.text(0.13, 0.905, 'bot  •  official helper bot', color='#708499', fontsize=10)

# Chat Area background
chat_bg = patches.Rectangle((0.02, 0.02), 0.96, 0.86, facecolor='#0E1621', edgecolor='none')
ax.add_patch(chat_bg)

# Message 1: User -> /newbot
m1_bg = patches.FancyBboxPatch((0.68, 0.77), 0.28, 0.06, boxstyle='round,pad=0.01,rounding_size=0.015',
                              edgecolor='#2B5278', facecolor='#2B5278')
ax.add_patch(m1_bg)
ax.text(0.70, 0.795, '/newbot', color='#FFFFFF', fontsize=12, fontweight='bold', fontfamily='monospace')
ax.text(0.93, 0.775, '12:45', color='#6C8CAE', fontsize=8)

# Message 2: BotFather Reply 1
m2_bg = patches.FancyBboxPatch((0.05, 0.67), 0.65, 0.075, boxstyle='round,pad=0.01,rounding_size=0.015',
                              edgecolor='#182533', facecolor='#182533')
ax.add_patch(m2_bg)
ax.text(0.07, 0.715, 'Alright, a new bot. How are we going to call it?', color='#FFFFFF', fontsize=10.5)
ax.text(0.07, 0.685, 'Please choose a name for your bot.', color='#708499', fontsize=10)

# Message 3: User -> Prince Daily News
m3_bg = patches.FancyBboxPatch((0.58, 0.585), 0.38, 0.06, boxstyle='round,pad=0.01,rounding_size=0.015',
                              edgecolor='#2B5278', facecolor='#2B5278')
ax.add_patch(m3_bg)
ax.text(0.60, 0.61, 'Prince Daily News', color='#FFFFFF', fontsize=12, fontweight='bold')
ax.text(0.93, 0.59, '12:46', color='#6C8CAE', fontsize=8)

# Message 4: BotFather Reply 2
m4_bg = patches.FancyBboxPatch((0.05, 0.48), 0.72, 0.08, boxstyle='round,pad=0.01,rounding_size=0.015',
                              edgecolor='#182533', facecolor='#182533')
ax.add_patch(m4_bg)
ax.text(0.07, 0.525, "Good. Now let's choose a username for your bot.", color='#FFFFFF', fontsize=10.5)
ax.text(0.07, 0.495, "It must end in 'bot'. Like: prince_ai_bot", color='#708499', fontsize=10)

# Message 5: User -> prince_daily_ai_bot
m5_bg = patches.FancyBboxPatch((0.55, 0.395), 0.41, 0.06, boxstyle='round,pad=0.01,rounding_size=0.015',
                              edgecolor='#2B5278', facecolor='#2B5278')
ax.add_patch(m5_bg)
ax.text(0.57, 0.42, 'prince_daily_ai_bot', color='#FFFFFF', fontsize=12, fontweight='bold', fontfamily='monospace')
ax.text(0.93, 0.40, '12:46', color='#6C8CAE', fontsize=8)

# Message 6: BotFather Final Token Message
m6_bg = patches.FancyBboxPatch((0.05, 0.12), 0.88, 0.25, boxstyle='round,pad=0.015,rounding_size=0.02',
                              edgecolor='#284460', facecolor='#182533')
ax.add_patch(m6_bg)

msg6_text = (
    "Done! Congratulations on your new bot.\n\n"
    "Use this token to access the HTTP API:\n"
    "👉 7894561230:AAH_J4kLmNoPqRsTuVwXyZ123456789abc\n\n"
    "Keep your token secure and store it safely, it can be used\n"
    "by anyone to control your bot."
)
ax.text(0.07, 0.20, msg6_text, color='#E2E8F0', fontsize=10, fontfamily='sans-serif', linespacing=1.35)

# Highlighting Box around the TOKEN
tok_box = patches.FancyBboxPatch((0.065, 0.215), 0.85, 0.045, boxstyle='round,pad=0.005,rounding_size=0.01',
                                edgecolor='#EF4444', facecolor='#EF4444', alpha=0.2, linewidth=2, linestyle='--')
ax.add_patch(tok_box)

# Callout banner at bottom
bot_banner = patches.Rectangle((0.02, 0.02), 0.96, 0.08, facecolor='#059669', edgecolor='none')
ax.add_patch(bot_banner)
ax.text(0.5, 0.06, '⬆️ BotFather jo ye Token dega, use Copy karke bas yahan chat me bhej dijiye!',
        color='#FFFFFF', fontsize=12, fontweight='bold', ha='center', va='center')

plt.tight_layout()
out_file = r'C:\Users\princ\.gemini\antigravity\brain\369a09af-533e-4e40-b6cd-a77b1b612725\telegram_botfather_guide.png'
plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
print('SUCCESS_SAVED:', out_file)
