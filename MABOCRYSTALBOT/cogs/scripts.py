@commands.command()
async def getscript(self, ctx):
    try:
        # Check if user has premium role
        premium_role = discord.utils.get(ctx.guild.roles, id=1343002193321791558)
        if premium_role not in ctx.author.roles:
            await ctx.send("You need premium to use Crystal Hub!")
            return

        # Generate HWID for user
        hwid = hashlib.sha256(f"crystal_hub_{ctx.author.id}".encode()).hexdigest()[:32]
        
        # Get user's current game from presence
        member = ctx.author
        game_found = False
        
        for activity in member.activities:
            if isinstance(activity, discord.Activity):
                if activity.application_id:
                    game_id = str(activity.application_id)
                    game_found = True
                    
                    try:
                        # Connect to dashboard database
                        conn = sqlite3.connect('../dashboard/instance/crystal.db')
                        cursor = conn.cursor()
                        
                        # Get script for current game
                        cursor.execute('SELECT content FROM script WHERE game_id = ?', (game_id,))
                        result = cursor.fetchone()
                        
                        if result:
                            script = result[0]
                            # Insert HWID into script
                            final_script = f"_G.HWID = '{hwid}'\n{script}"
                            
                            # Update stats
                            cursor.execute('UPDATE stats SET total_executions = total_executions + 1')
                            cursor.execute('UPDATE stats SET active_users = active_users + 1')
                            conn.commit()
                            
                            # Send script via DM
                            try:
                                await ctx.author.send(f"```lua\n{final_script}\n```")
                                await ctx.send("✅ Script sent to your DMs!")
                            except:
                                await ctx.send("❌ Couldn't DM you. Please enable DMs from server members.")
                        else:
                            await ctx.send("❌ Crystal Hub doesn't support this game yet!")
                    
                    except sqlite3.Error as e:
                        await ctx.send("❌ Database error occurred. Please try again later.")
                        print(f"Database error: {e}")
                    finally:
                        if conn:
                            conn.close()
                    break
        
        if not game_found:
            await ctx.send("❌ Please join a Roblox game first!")
            
    except Exception as e:
        await ctx.send("❌ An error occurred. Please try again later.")
        print(f"Error in getscript: {e}")